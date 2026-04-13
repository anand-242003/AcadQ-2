import os
import re
import joblib
import numpy as np
import pandas as pd
from pathlib import Path

# ─── Model Loading ────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # project root
MODEL_DIR = BASE_DIR / "model"
DATA_DIR = BASE_DIR / "Data"

_models: dict = {}


def load_models() -> dict:
    global _models
    try:
        _models['classifier']        = joblib.load(MODEL_DIR / "classification_model.pkl")
        _models['regressor']         = joblib.load(MODEL_DIR / "regression_model.pkl")
        _models['kmeans']            = joblib.load(MODEL_DIR / "clustering_model.pkl")
        _models['scaler']            = joblib.load(MODEL_DIR / "scaler.pkl")
        _models['feature_columns']   = joblib.load(MODEL_DIR / "feature_columns.pkl")
        _models['cluster_label_map'] = joblib.load(MODEL_DIR / "cluster_label_map.pkl")
        _models['loaded']            = True

        # Precompute dataset column means for weakness computation
        dataset_path = DATA_DIR / "StudentDataset.csv"
        if dataset_path.exists():
            df = pd.read_csv(dataset_path)
            _models['dataset_means'] = df.select_dtypes(include=[np.number]).mean().to_dict()
        else:
            _models['dataset_means'] = {}

    except FileNotFoundError as e:
        _models['loaded'] = False
        _models['error']  = str(e)
    except Exception as e:
        _models['loaded'] = False
        _models['error']  = f"Unexpected error: {e}"

    return _models


def get_models() -> dict:
    if not _models:
        load_models()
    return _models


# ─── Preprocessing ────────────────────────────────────────────────────────────

def preprocess_input(raw: dict, models: dict):
    """Replicates Milestone 1 preprocessing pipeline exactly."""
    df = pd.DataFrame([raw])

    # Categorical encoding — must match training encoding
    df['gender']            = df['gender'].map({'Male': 1, 'Female': 0, 'Other': 2})
    df['academic_level']    = df['academic_level'].map({'High School': 0, 'Undergraduate': 1, 'Postgraduate': 1})
    df['internet_quality']  = df['internet_quality'].map({'Good': 1, 'Poor': 0})
    df['part_time_job']     = 1 if raw['part_time_job']     == 'Yes' else 0
    df['upcoming_deadline'] = 1 if raw['upcoming_deadline'] == 'Yes' else 0

    # Feature engineering — must match Milestone 1 derived features
    df['total_active_hours']      = df['study_hours'] + df['self_study_hours'] + df['online_classes_hours']
    df['total_distraction_hours'] = df['social_media_hours'] + df['gaming_hours']
    df['study_distraction_ratio'] = df['study_hours'] / df['total_distraction_hours'].replace(0, 0.1)
    df['healthy_sleep']           = df['sleep_hours'].apply(lambda x: 1 if 7 <= x <= 9 else 0)
    df['wellness_score']          = (df['mental_health_score'] * 0.4
                                     + df['sleep_hours'] * 0.3
                                     + (df['exercise_minutes'] / 60) * 0.3)
    df['stress_index']            = (df['burnout_level'] * 0.5
                                     + df['screen_time_hours'] * 0.3
                                     + (10 - df['sleep_hours']) * 0.2)

    # Align to training feature columns
    cols = models['feature_columns']
    for c in cols:
        if c not in df.columns:
            df[c] = 0
    df = df[cols]

    unscaled_df = df.copy()
    scaled = models['scaler'].transform(df)
    scaled_df = pd.DataFrame(scaled, columns=cols)

    return scaled_df, unscaled_df


# ─── Learner Type Resolution ──────────────────────────────────────────────────

def _resolve_learner_type(score: float, pass_prob: float, cluster_label: str) -> str:
    """Exact replication of Milestone 1 _resolve_learner_type logic."""
    if score >= 75 and pass_prob >= 70:
        return "High Achiever"
    if score >= 60 and pass_prob >= 50:
        return "Developing Learner"
    if score >= 40:
        return "Average Learner"
    if score >= 20:
        return "Struggling Learner"
    return "At Risk Learner"


# ─── Top Weaknesses ───────────────────────────────────────────────────────────

NUMERIC_FEATURES = [
    'study_hours', 'self_study_hours', 'online_classes_hours',
    'sleep_hours', 'exercise_minutes', 'mental_health_score',
    'focus_index', 'productivity_score', 'quiz_avg', 'assignment_avg',
    'midterm_score', 'topics_completed',
]

INVERTED_FEATURES = ['social_media_hours', 'gaming_hours', 'screen_time_hours',
                     'caffeine_intake_mg', 'burnout_level']


def compute_top_weaknesses(raw: dict, models: dict, k: int = 3) -> list:
    """
    Compare student values against dataset averages.
    Returns k WeaknessItem dicts sorted by delta ascending (most negative first).
    """
    dataset_means = models.get('dataset_means', {})
    candidates = []

    for feature in NUMERIC_FEATURES:
        if feature not in raw or feature not in dataset_means:
            continue
        student_val = float(raw[feature])
        dataset_avg = float(dataset_means[feature])
        delta = student_val - dataset_avg

        if delta < 0:
            candidates.append({
                "feature": feature,
                "student_value": round(student_val, 2),
                "dataset_average": round(dataset_avg, 2),
                "delta": round(delta, 2),
            })

    candidates.sort(key=lambda x: x['delta'])
    return candidates[:k]


# ─── Recommendations ─────────────────────────────────────────────────────────

def _strip_emoji(text: str) -> str:
    return re.sub(
        r'[\U00010000-\U0010ffff\u2600-\u26FF\u2700-\u27BF\U0001F300-\U0001F9FF]+\s*',
        '', text,
    ).strip()


def generate_recommendations(results: dict) -> list:
    """Replicates Milestone 1 generate_recommendations logic exactly."""
    tips = []
    score = results['pred_score']

    if score < 20:
        tips.append(("Critical alert",  "Predicted score is very low. Speak with your academic advisor as soon as possible."))
        tips.append(("Study approach",  "Review foundational concepts before attempting advanced material."))
    elif score < 40:
        tips.append(("At risk",         "You are at risk of failing. Increase daily study hours significantly."))
        tips.append(("Planning",        "Build a structured weekly timetable and commit to it every day."))
    elif score < 60:
        tips.append(("Room to improve", "You are passing but there is clear room for improvement."))
        tips.append(("Study strategy",  "Practice with past exam papers and focus on your weakest topics."))
    else:
        tips.append(("Performing well", "You are on track. Stay consistent and maintain your current habits."))
        tips.append(("Next level",      "Challenge yourself with harder material to push your score even higher."))

    if results['study_hours'] < 2:
        tips.append(("Study time", "Less than 2 hours of study per day. Aim for at least 4 to 5 hours for meaningful progress."))
    elif results['study_hours'] < 4:
        tips.append(("Study time", "Consider increasing to 5 to 6 study hours per day for better retention."))

    if results['sleep_hours'] < 6:
        tips.append(("Sleep", "Under 6 hours of sleep significantly impairs memory and focus. Target 7 to 8 hours per night."))
    elif results['sleep_hours'] > 9:
        tips.append(("Sleep", "Oversleeping can reduce motivation. 7 to 8 hours is the optimal range."))

    total_distraction = results['social_media_hours'] + results['gaming_hours']
    if total_distraction > 4:
        tips.append(("Distractions", "More than 4 hours on social media and gaming per day is reducing your study effectiveness."))
    elif total_distraction > 2:
        tips.append(("Distractions", "Aim to keep social media and gaming under 2 hours per day to free up study time."))

    if results['mental_health_score'] <= 3:
        tips.append(("Mental health", "Mental health score is low. Consider speaking with a counselor or a trusted person."))
    elif results['mental_health_score'] <= 6:
        tips.append(("Mental health", "Try the Pomodoro method — 25 minutes of focused study followed by a 5-minute break."))

    if results['burnout_level'] > 70:
        tips.append(("Burnout", "Burnout level is very high. Take a full rest day and avoid cramming sessions."))
    elif results['burnout_level'] > 50:
        tips.append(("Burnout", "Moderate burnout detected. Space out study sessions and include planned rest."))

    if results['exercise_minutes'] < 20:
        tips.append(("Exercise", "Less than 20 minutes of activity per day. A 30-minute walk improves focus and retention."))

    if results['internet_quality'] == 'Poor':
        tips.append(("Connectivity", "Poor internet detected. Download study materials in advance for offline access."))

    learner = _strip_emoji(results['pred_learner_type'])
    if 'At Risk' in learner:
        tips.append(("Learner profile", "Seek immediate academic support — a tutor, study group, or advisor can help you build a recovery plan."))
    elif 'Struggling' in learner:
        tips.append(("Learner profile", "Join a study group or work with a tutor. Peer learning significantly accelerates understanding."))
    elif 'Average' in learner:
        tips.append(("Learner profile", "Set small measurable daily goals and review your progress at the end of each week."))
    elif 'Developing' in learner:
        tips.append(("Learner profile", "You are on the right trajectory. Consistency is your biggest asset right now."))
    elif 'High Achiever' in learner:
        tips.append(("Learner profile", "Consider mentoring peers. Teaching material is one of the most effective ways to master it."))

    return tips


# ─── Grade Computation ────────────────────────────────────────────────────────

def get_grade(score: float) -> str:
    if score >= 75:
        return "A"
    if score >= 60:
        return "B"
    if score >= 45:
        return "C"
    if score >= 30:
        return "D"
    return "F"


# ─── Main Prediction Function ─────────────────────────────────────────────────

def run_predictions(raw: dict) -> dict:
    models = get_models()

    if not models.get('loaded'):
        raise RuntimeError(f"Model not loaded: {models.get('error', 'unknown error')}")

    scaled_df, unscaled_df = preprocess_input(raw, models)

    pred_class   = int(models['classifier'].predict(scaled_df)[0])
    proba        = models['classifier'].predict_proba(scaled_df)[0]
    pred_score   = round(float(np.clip(models['regressor'].predict(scaled_df)[0], 0, 100)), 2)
    pred_cluster = int(models['kmeans'].predict(scaled_df)[0])
    raw_ltype    = models['cluster_label_map'].get(pred_cluster, "Unknown")
    pass_prob    = round(float(proba[1]) * 100, 1)
    fail_prob    = round(float(proba[0]) * 100, 1)
    ltype        = _resolve_learner_type(pred_score, pass_prob, raw_ltype)
    grade        = get_grade(pred_score)

    # Build results dict for recommendations (matches Milestone 1 format)
    results_for_recs = {
        "pred_score"          : pred_score,
        "pred_learner_type"   : ltype,
        "study_hours"         : raw['study_hours'],
        "sleep_hours"         : raw['sleep_hours'],
        "social_media_hours"  : raw['social_media_hours'],
        "gaming_hours"        : raw['gaming_hours'],
        "mental_health_score" : raw['mental_health_score'],
        "burnout_level"       : raw['burnout_level'],
        "exercise_minutes"    : raw['exercise_minutes'],
        "internet_quality"    : raw['internet_quality'],
        "productivity_score"  : raw['productivity_score'],
        "screen_time_hours"   : raw['screen_time_hours'],
        "caffeine_intake_mg"  : raw['caffeine_intake_mg'],
        "focus_index"         : raw['focus_index'],
    }

    raw_tips = generate_recommendations(results_for_recs)
    recommendations = [{"category": cat, "message": msg} for cat, msg in raw_tips]

    top_weaknesses = compute_top_weaknesses(raw, models)

    return {
        "predicted_score"  : pred_score,
        "grade"            : grade,
        "pass_probability" : pass_prob,
        "fail_probability" : fail_prob,
        "classification"   : "Pass" if pred_class == 1 else "Fail",
        "learner_type"     : ltype,
        "cluster_id"       : pred_cluster,
        "top_weaknesses"   : top_weaknesses,
        "recommendations"  : recommendations,
    }

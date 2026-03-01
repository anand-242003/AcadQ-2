import re
import joblib
import numpy as np
import pandas as pd
import streamlit as st


@st.cache_resource
def load_all_models() -> dict:
    m = {}
    try:
        m['classifier']        = joblib.load("Notebook/student_ml_app/classification_model.pkl")
        m['regressor']         = joblib.load("Notebook/student_ml_app/regression_model.pkl")
        m['kmeans']            = joblib.load("Notebook/student_ml_app/clustering_model.pkl")
        m['scaler']            = joblib.load("Notebook/student_ml_app/scaler.pkl")
        m['feature_columns']   = joblib.load("Notebook/student_ml_app/feature_columns.pkl")
        m['cluster_label_map'] = joblib.load("Notebook/student_ml_app/cluster_label_map.pkl")
        m['loaded']            = True
    except FileNotFoundError as e:
        m['loaded'] = False
        m['error']  = str(e)
    except Exception as e:
        m['loaded'] = False
        m['error']  = f"Unexpected error: {e}"
    return m


def preprocess_input(raw: dict, models: dict):
    df = pd.DataFrame([raw])

    df['gender']            = df['gender'].map({'Male': 1, 'Female': 0, 'Other': 2})
    df['academic_level']    = df['academic_level'].map({'High School': 0, 'Undergraduate': 1})
    df['internet_quality']  = df['internet_quality'].map({'Good': 1, 'Poor': 0})
    df['part_time_job']     = 1 if raw['part_time_job']     == 'Yes' else 0
    df['upcoming_deadline'] = 1 if raw['upcoming_deadline'] == 'Yes' else 0

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

    cols = models['feature_columns']
    for c in cols:
        if c not in df.columns:
            df[c] = 0
    df = df[cols]

    scaled = models['scaler'].transform(df)
    return pd.DataFrame(scaled, columns=cols), df


def _resolve_learner_type(score: float, pass_prob: float, cluster_label: str) -> str:
    if score >= 75 and pass_prob >= 70:
        return "High Achiever"
    if score >= 60 and pass_prob >= 50:
        return "Developing Learner"
    if score >= 40:
        return "Average Learner"
    if score >= 20:
        return "Struggling Learner"
    return "At Risk Learner"


def run_predictions(raw: dict, models: dict) -> dict:
    scaled_df, _ = preprocess_input(raw, models)

    pred_class   = int(models['classifier'].predict(scaled_df)[0])
    proba        = models['classifier'].predict_proba(scaled_df)[0]
    pred_score   = round(float(np.clip(models['regressor'].predict(scaled_df)[0], 0, 100)), 2)
    pred_cluster = int(models['kmeans'].predict(scaled_df)[0])
    raw_ltype    = models['cluster_label_map'].get(pred_cluster, "Unknown")
    pass_prob    = round(float(proba[1]) * 100, 1)
    ltype        = _resolve_learner_type(pred_score, pass_prob, raw_ltype)

    return {
        "pred_score"             : pred_score,
        "pred_class"             : pred_class,
        "pass_probability"       : pass_prob,
        "fail_probability"       : round(float(proba[0]) * 100, 1),
        "pred_learner_type"      : ltype,
        "raw_cluster_label"      : raw_ltype,
        "pred_cluster"           : pred_cluster,
        "study_hours"            : raw['study_hours'],
        "sleep_hours"            : raw['sleep_hours'],
        "total_distraction_hours": raw['social_media_hours'] + raw['gaming_hours'],
        "mental_health_score"    : raw['mental_health_score'],
        "burnout_level"          : raw['burnout_level'],
        "exercise_minutes"       : raw['exercise_minutes'],
        "internet_quality"       : raw['internet_quality'],
        "productivity_score"     : raw['productivity_score'],
        "social_media_hours"     : raw['social_media_hours'],
        "gaming_hours"           : raw['gaming_hours'],
        "screen_time_hours"      : raw['screen_time_hours'],
        "caffeine_intake_mg"     : raw['caffeine_intake_mg'],
        "focus_index"            : raw['focus_index'],
    }


def generate_recommendations(results: dict) -> list:
    tips  = []
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

    if results['total_distraction_hours'] > 4:
        tips.append(("Distractions", "More than 4 hours on social media and gaming per day is reducing your study effectiveness."))
    elif results['total_distraction_hours'] > 2:
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

    learner = strip_emoji(results['pred_learner_type'])
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


def strip_emoji(text: str) -> str:
    return re.sub(
        r'[\U00010000-\U0010ffff\u2600-\u26FF\u2700-\u27BF\U0001F300-\U0001F9FF]+\s*',
        '', text,
    ).strip()

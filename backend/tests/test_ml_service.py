import pytest
import numpy as np
import pandas as pd
from unittest.mock import MagicMock, patch
from services.ml_service import (
    preprocess_input, _resolve_learner_type, compute_top_weaknesses,
    get_grade, generate_recommendations, NUMERIC_FEATURES
)

SAMPLE_RAW = {
    "age": 20, "gender": "Male", "academic_level": "Undergraduate",
    "study_hours": 4.0, "self_study_hours": 2.0, "online_classes_hours": 1.5,
    "social_media_hours": 2.0, "gaming_hours": 1.0, "sleep_hours": 7.0,
    "screen_time_hours": 5.0, "exercise_minutes": 30, "caffeine_intake_mg": 100,
    "part_time_job": "No", "upcoming_deadline": "No", "internet_quality": "Good",
    "mental_health_score": 7, "focus_index": 60.0, "burnout_level": 30.0,
    "productivity_score": 60.0, "quiz_avg": 65.0, "assignment_avg": 65.0,
    "midterm_score": 60.0, "topics_completed": 15,
}


def make_mock_models(feature_columns=None):
    if feature_columns is None:
        feature_columns = [
            "age", "gender", "academic_level", "study_hours", "self_study_hours",
            "online_classes_hours", "social_media_hours", "gaming_hours", "sleep_hours",
            "screen_time_hours", "exercise_minutes", "caffeine_intake_mg",
            "part_time_job", "upcoming_deadline", "internet_quality",
            "mental_health_score", "focus_index", "burnout_level", "productivity_score",
            "quiz_avg", "assignment_avg", "midterm_score", "topics_completed",
            "total_active_hours", "total_distraction_hours", "study_distraction_ratio",
            "healthy_sleep", "wellness_score", "stress_index",
        ]
    scaler = MagicMock()
    scaler.transform = lambda x: x.values
    return {
        "loaded": True,
        "feature_columns": feature_columns,
        "scaler": scaler,
        "dataset_means": {f: 5.0 for f in NUMERIC_FEATURES},
    }


class TestPreprocessInput:
    def test_categorical_encoding_gender(self):
        models = make_mock_models()
        scaled, unscaled = preprocess_input({**SAMPLE_RAW, "gender": "Male"}, models)
        assert "gender" in unscaled.columns

    def test_categorical_encoding_female(self):
        models = make_mock_models()
        scaled, unscaled = preprocess_input({**SAMPLE_RAW, "gender": "Female"}, models)
        assert "gender" in unscaled.columns

    def test_derived_features_present(self):
        models = make_mock_models()
        scaled, unscaled = preprocess_input(SAMPLE_RAW, models)
        for feat in ["total_active_hours", "total_distraction_hours", "study_distraction_ratio",
                     "healthy_sleep", "wellness_score", "stress_index"]:
            assert feat in unscaled.columns

    def test_total_active_hours_computation(self):
        models = make_mock_models()
        raw = {**SAMPLE_RAW, "study_hours": 3.0, "self_study_hours": 2.0, "online_classes_hours": 1.0}
        scaled, unscaled = preprocess_input(raw, models)
        assert abs(float(unscaled["total_active_hours"].iloc[0]) - 6.0) < 0.01

    def test_healthy_sleep_true(self):
        models = make_mock_models()
        raw = {**SAMPLE_RAW, "sleep_hours": 8.0}
        scaled, unscaled = preprocess_input(raw, models)
        assert int(unscaled["healthy_sleep"].iloc[0]) == 1

    def test_healthy_sleep_false(self):
        models = make_mock_models()
        raw = {**SAMPLE_RAW, "sleep_hours": 6.0}
        scaled, unscaled = preprocess_input(raw, models)
        assert int(unscaled["healthy_sleep"].iloc[0]) == 0

    def test_column_order_matches_feature_columns(self):
        models = make_mock_models()
        scaled, unscaled = preprocess_input(SAMPLE_RAW, models)
        assert list(unscaled.columns) == models["feature_columns"]

    def test_idempotency(self):
        models = make_mock_models()
        scaled1, _ = preprocess_input(SAMPLE_RAW, models)
        scaled2, _ = preprocess_input(SAMPLE_RAW, models)
        np.testing.assert_array_almost_equal(scaled1, scaled2)


class TestResolveLearnerType:
    def test_high_achiever(self):
        assert _resolve_learner_type(80, 75, "any") == "High Achiever"

    def test_developing_learner(self):
        assert _resolve_learner_type(65, 55, "any") == "Developing Learner"

    def test_average_learner(self):
        assert _resolve_learner_type(45, 40, "any") == "Average Learner"

    def test_struggling_learner(self):
        assert _resolve_learner_type(25, 30, "any") == "Struggling Learner"

    def test_at_risk_learner(self):
        assert _resolve_learner_type(10, 20, "any") == "At Risk Learner"

    def test_always_returns_valid_type(self):
        valid = {"High Achiever", "Developing Learner", "Average Learner", "Struggling Learner", "At Risk Learner"}
        for score in [0, 25, 45, 65, 85]:
            for prob in [0, 30, 55, 75]:
                result = _resolve_learner_type(score, prob, "any")
                assert result in valid


class TestComputeTopWeaknesses:
    def test_returns_at_most_k_items(self):
        models = make_mock_models()
        raw = {**SAMPLE_RAW, "study_hours": 1.0, "sleep_hours": 4.0, "focus_index": 10.0}
        result = compute_top_weaknesses(raw, models, k=3)
        assert len(result) <= 3

    def test_sorted_by_delta_ascending(self):
        models = make_mock_models()
        raw = {**SAMPLE_RAW, "study_hours": 1.0, "sleep_hours": 3.0, "focus_index": 5.0}
        result = compute_top_weaknesses(raw, models, k=3)
        deltas = [w["delta"] for w in result]
        assert deltas == sorted(deltas)

    def test_only_negative_deltas(self):
        models = make_mock_models()
        result = compute_top_weaknesses(SAMPLE_RAW, models)
        for w in result:
            assert w["delta"] < 0

    def test_weakness_item_has_required_keys(self):
        models = make_mock_models()
        raw = {**SAMPLE_RAW, "study_hours": 1.0}
        result = compute_top_weaknesses(raw, models, k=1)
        if result:
            assert all(k in result[0] for k in ["feature", "student_value", "dataset_average", "delta"])


class TestGetGrade:
    def test_grade_a(self):
        assert get_grade(80) == "A"

    def test_grade_b(self):
        assert get_grade(65) == "B"

    def test_grade_c(self):
        assert get_grade(50) == "C"

    def test_grade_d(self):
        assert get_grade(35) == "D"

    def test_grade_f(self):
        assert get_grade(20) == "F"



try:
    from hypothesis import given, settings, HealthCheck
    from hypothesis import strategies as st
    HYPOTHESIS_AVAILABLE = True
except ImportError:
    HYPOTHESIS_AVAILABLE = False

if HYPOTHESIS_AVAILABLE:
    VALID_LEARNER_TYPES = {
        "High Achiever", "Developing Learner", "Average Learner",
        "Struggling Learner", "At Risk Learner"
    }

    @given(
        score=st.floats(min_value=0, max_value=100, allow_nan=False),
        pass_prob=st.floats(min_value=0, max_value=100, allow_nan=False),
    )
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    def test_learner_type_always_valid(score, pass_prob):
        """Property 4: For any score/pass_prob, learner_type is always a valid value."""
        result = _resolve_learner_type(score, pass_prob, "any")
        assert result in VALID_LEARNER_TYPES

    @given(
        score=st.floats(min_value=0, max_value=100, allow_nan=False),
    )
    @settings(max_examples=50)
    def test_grade_always_valid(score):
        """Grade is always one of A/B/C/D/F."""
        grade = get_grade(score)
        assert grade in {"A", "B", "C", "D", "F"}

    @given(
        email=st.emails(),
    )
    @settings(max_examples=50)
    def test_token_round_trip(email):
        """Property 9: verify_token(create_access_token(email)) returns original email."""
        from routes.auth import create_access_token, SECRET_KEY, ALGORITHM
        from jose import jwt
        token = create_access_token(email)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload["sub"] == email

if HYPOTHESIS_AVAILABLE:

    @given(
        study_hours=st.floats(min_value=0, max_value=16, allow_nan=False),
        sleep_hours=st.floats(min_value=4, max_value=12, allow_nan=False),
        focus_index=st.floats(min_value=0, max_value=100, allow_nan=False),
        exercise_minutes=st.floats(min_value=0, max_value=180, allow_nan=False),
    )
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    def test_weaknesses_sorted_by_delta_ascending(study_hours, sleep_hours, focus_index, exercise_minutes):
        """Property 7: compute_top_weaknesses always returns items sorted by delta ascending."""
        models = make_mock_models()
        raw = {
            **SAMPLE_RAW,
            "study_hours": study_hours,
            "sleep_hours": sleep_hours,
            "focus_index": focus_index,
            "exercise_minutes": exercise_minutes,
        }
        result = compute_top_weaknesses(raw, models, k=5)
        deltas = [w["delta"] for w in result]
        assert deltas == sorted(deltas)


    @given(
        study_hours=st.floats(min_value=0, max_value=16, allow_nan=False),
        sleep_hours=st.floats(min_value=4, max_value=12, allow_nan=False),
        social_media_hours=st.floats(min_value=0, max_value=12, allow_nan=False),
        gaming_hours=st.floats(min_value=0, max_value=10, allow_nan=False),
    )
    @settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow])
    def test_preprocess_input_idempotent(study_hours, sleep_hours, social_media_hours, gaming_hours):
        """Property 5: preprocess_input called twice returns identical scaled output."""
        models = make_mock_models()
        raw = {
            **SAMPLE_RAW,
            "study_hours": study_hours,
            "sleep_hours": sleep_hours,
            "social_media_hours": social_media_hours,
            "gaming_hours": gaming_hours,
        }
        scaled1, _ = preprocess_input(raw, models)
        scaled2, _ = preprocess_input(raw, models)
        np.testing.assert_array_almost_equal(scaled1, scaled2)

if HYPOTHESIS_AVAILABLE:

    _VALID_GENDERS = ["Male", "Female", "Other"]
    _VALID_LEVELS = ["High School", "Undergraduate", "Postgraduate"]
    _VALID_QUALITY = ["Good", "Poor"]
    _VALID_YESNO = ["Yes", "No"]

    _student_input_strategy = st.fixed_dictionaries({
        "age": st.integers(min_value=16, max_value=40),
        "gender": st.sampled_from(_VALID_GENDERS),
        "academic_level": st.sampled_from(_VALID_LEVELS),
        "study_hours": st.floats(min_value=0, max_value=16, allow_nan=False),
        "self_study_hours": st.floats(min_value=0, max_value=10, allow_nan=False),
        "online_classes_hours": st.floats(min_value=0, max_value=10, allow_nan=False),
        "social_media_hours": st.floats(min_value=0, max_value=12, allow_nan=False),
        "gaming_hours": st.floats(min_value=0, max_value=10, allow_nan=False),
        "sleep_hours": st.floats(min_value=4, max_value=12, allow_nan=False),
        "screen_time_hours": st.floats(min_value=0, max_value=16, allow_nan=False),
        "exercise_minutes": st.integers(min_value=0, max_value=180),
        "caffeine_intake_mg": st.integers(min_value=0, max_value=600),
        "part_time_job": st.sampled_from(_VALID_YESNO),
        "upcoming_deadline": st.sampled_from(_VALID_YESNO),
        "internet_quality": st.sampled_from(_VALID_QUALITY),
        "mental_health_score": st.integers(min_value=1, max_value=10),
        "focus_index": st.floats(min_value=0, max_value=100, allow_nan=False),
        "burnout_level": st.floats(min_value=0, max_value=100, allow_nan=False),
        "productivity_score": st.floats(min_value=0, max_value=100, allow_nan=False),
        "quiz_avg": st.floats(min_value=0, max_value=100, allow_nan=False),
        "assignment_avg": st.floats(min_value=0, max_value=100, allow_nan=False),
        "midterm_score": st.floats(min_value=0, max_value=100, allow_nan=False),
        "topics_completed": st.integers(min_value=0, max_value=50),
    })

    @given(raw=_student_input_strategy)
    @settings(max_examples=30, suppress_health_check=[HealthCheck.too_slow], deadline=None)
    def test_run_predictions_score_in_range(raw):
        """Property 1: predicted_score is always in [0, 100]."""
        from services.ml_service import run_predictions
        result = run_predictions(raw)
        assert 0 <= result["predicted_score"] <= 100

    @given(raw=_student_input_strategy)
    @settings(max_examples=30, suppress_health_check=[HealthCheck.too_slow], deadline=None)
    def test_run_predictions_probabilities_sum_to_100(raw):
        """Property 2: pass_probability + fail_probability ≈ 100.0 ±0.01."""
        from services.ml_service import run_predictions
        result = run_predictions(raw)
        total = result["pass_probability"] + result["fail_probability"]
        assert abs(total - 100.0) <= 0.1

    @given(raw=_student_input_strategy)
    @settings(max_examples=30, suppress_health_check=[HealthCheck.too_slow], deadline=None)
    def test_run_predictions_classification_matches_probability(raw):
        """Property 3: classification == 'Pass' iff pass_probability > 50.0."""
        from services.ml_service import run_predictions
        result = run_predictions(raw)
        if result["pass_probability"] > 50.0:
            assert result["classification"] == "Pass"
        else:
            assert result["classification"] == "Fail"

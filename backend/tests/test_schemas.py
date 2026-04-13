import pytest
from pydantic import ValidationError
from models.schemas import StudentInput, RegisterRequest, LoginRequest


class TestStudentInputValidation:
    def test_valid_input_passes(self):
        data = {
            "age": 20, "gender": "Male", "academic_level": "Undergraduate",
            "study_hours": 4.0, "self_study_hours": 2.0, "online_classes_hours": 1.5,
            "social_media_hours": 2.0, "gaming_hours": 1.0, "sleep_hours": 7.0,
            "screen_time_hours": 5.0, "exercise_minutes": 30, "caffeine_intake_mg": 100,
            "part_time_job": "No", "upcoming_deadline": "No", "internet_quality": "Good",
            "mental_health_score": 7, "focus_index": 60.0, "burnout_level": 30.0,
            "productivity_score": 60.0, "quiz_avg": 65.0, "assignment_avg": 65.0,
            "midterm_score": 60.0, "topics_completed": 15,
        }
        student = StudentInput(**data)
        assert student.age == 20

    def test_age_below_minimum_fails(self):
        with pytest.raises(ValidationError):
            StudentInput(age=10, gender="Male", academic_level="Undergraduate",
                        study_hours=4, self_study_hours=2, online_classes_hours=1,
                        social_media_hours=2, gaming_hours=1, sleep_hours=7,
                        screen_time_hours=5, exercise_minutes=30, caffeine_intake_mg=100,
                        part_time_job="No", upcoming_deadline="No", internet_quality="Good",
                        mental_health_score=7, focus_index=60, burnout_level=30,
                        productivity_score=60)

    def test_invalid_gender_fails(self):
        with pytest.raises(ValidationError):
            StudentInput(age=20, gender="Unknown", academic_level="Undergraduate",
                        study_hours=4, self_study_hours=2, online_classes_hours=1,
                        social_media_hours=2, gaming_hours=1, sleep_hours=7,
                        screen_time_hours=5, exercise_minutes=30, caffeine_intake_mg=100,
                        part_time_job="No", upcoming_deadline="No", internet_quality="Good",
                        mental_health_score=7, focus_index=60, burnout_level=30,
                        productivity_score=60)

    def test_focus_index_above_max_fails(self):
        with pytest.raises(ValidationError):
            StudentInput(age=20, gender="Male", academic_level="Undergraduate",
                        study_hours=4, self_study_hours=2, online_classes_hours=1,
                        social_media_hours=2, gaming_hours=1, sleep_hours=7,
                        screen_time_hours=5, exercise_minutes=30, caffeine_intake_mg=100,
                        part_time_job="No", upcoming_deadline="No", internet_quality="Good",
                        mental_health_score=7, focus_index=150, burnout_level=30,
                        productivity_score=60)


class TestRegisterRequestValidation:
    def test_valid_register(self):
        req = RegisterRequest(name="John Doe", email="john@example.com", password="password123")
        assert req.name == "John Doe"

    def test_short_name_fails(self):
        with pytest.raises(ValidationError):
            RegisterRequest(name="J", email="j@example.com", password="password123")

    def test_short_password_fails(self):
        with pytest.raises(ValidationError):
            RegisterRequest(name="John", email="john@example.com", password="short")

    def test_invalid_email_fails(self):
        with pytest.raises(ValidationError):
            RegisterRequest(name="John", email="not-an-email", password="password123")

from pydantic import BaseModel, Field, EmailStr
from typing import Literal, Optional


# ─── Student Input ────────────────────────────────────────────────────────────

class StudentInput(BaseModel):
    age: int = Field(ge=16, le=40, default=20)
    gender: Literal["Male", "Female", "Other"]
    academic_level: Literal["High School", "Undergraduate", "Postgraduate"]
    study_hours: float = Field(ge=0, le=16, default=4.0)
    self_study_hours: float = Field(ge=0, le=10, default=2.0)
    online_classes_hours: float = Field(ge=0, le=10, default=1.5)
    social_media_hours: float = Field(ge=0, le=12, default=2.0)
    gaming_hours: float = Field(ge=0, le=10, default=1.0)
    sleep_hours: float = Field(ge=4, le=12, default=7.0)
    screen_time_hours: float = Field(ge=0, le=16, default=5.0)
    exercise_minutes: int = Field(ge=0, le=180, default=30)
    caffeine_intake_mg: int = Field(ge=0, le=600, default=100)
    part_time_job: Literal["Yes", "No"] = "No"
    upcoming_deadline: Literal["Yes", "No"] = "No"
    internet_quality: Literal["Good", "Poor", "Average", "Excellent"] = "Good"
    mental_health_score: int = Field(ge=1, le=10, default=7)
    focus_index: float = Field(ge=0, le=100, default=60.0)
    burnout_level: float = Field(ge=0, le=100, default=30.0)
    productivity_score: float = Field(ge=0, le=100, default=60.0)
    quiz_avg: float = Field(ge=0, le=100, default=65.0)
    assignment_avg: float = Field(ge=0, le=100, default=65.0)
    midterm_score: float = Field(ge=0, le=100, default=60.0)
    topics_completed: int = Field(ge=0, le=50, default=15)


# ─── Prediction Response ──────────────────────────────────────────────────────

class WeaknessItem(BaseModel):
    feature: str
    student_value: float
    dataset_average: float
    delta: float  # student_value - dataset_average (negative = below average)


class RecommendationItem(BaseModel):
    category: str
    message: str


class PredictionResponse(BaseModel):
    predicted_score: float
    grade: str
    pass_probability: float
    fail_probability: float
    classification: str
    learner_type: str
    cluster_id: int
    top_weaknesses: list[WeaknessItem]
    recommendations: list[RecommendationItem]


# ─── Report Schemas ───────────────────────────────────────────────────────────

class ReportItem(BaseModel):
    id: str  # MongoDB ObjectId as string
    user_email: str
    timestamp: str  # ISO format
    prediction: PredictionResponse
    input_data: StudentInput  # Store the input for reference


class ReportsHistoryResponse(BaseModel):
    reports: list[ReportItem]


# ─── Auth Schemas ─────────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    token: str
    name: str
    email: str


class UserResponse(BaseModel):
    name: str
    email: str


# ─── Coach Schemas ────────────────────────────────────────────────────────────

class StudentProfile(BaseModel):
    predicted_score: float
    classification: str
    pass_probability: float
    learner_type: str
    top_weaknesses: list[WeaknessItem]


class CoachChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    student_profile: StudentProfile


class CoachChatResponse(BaseModel):
    reply: str
    session_id: str


class ResourceItem(BaseModel):
    topic: str
    title: str
    url: str
    description: str


class StudyPlanRequest(BaseModel):
    student_profile: StudentProfile
    goals: Optional[str] = None


class StudyPlanResponse(BaseModel):
    plan: str
    weekly_goal: str
    resources: list[ResourceItem]


class DiagnoseRequest(BaseModel):
    student_profile: StudentProfile


class DiagnoseResponse(BaseModel):
    gaps: list[str]
    reasoning: str


class MessageResponse(BaseModel):
    message: str

# ─── Quiz Schemas ─────────────────────────────────────────────────────────────

class QuizGenerateRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=100)
    count: int = Field(ge=1, le=20, default=5)
    level: str = Field(default="High School")
    difficulty: str = Field(default="Average")
    distractor_count: int = Field(ge=1, le=5, default=3)
    include_answers: bool = Field(default=True)
    language: str = Field(default="English (USA)")

class QuizOption(BaseModel):
    label: str  # e.g., "A", "B", "C"
    text: str

class QuizQuestion(BaseModel):
    number: int
    question: str
    options: list[QuizOption]
    correct_option_label: str
    explanation: Optional[str] = None

class QuizGenerateResponse(BaseModel):
    title: str
    questions: list[QuizQuestion]

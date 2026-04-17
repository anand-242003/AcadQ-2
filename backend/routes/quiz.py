from fastapi import APIRouter, HTTPException, Depends
from models.schemas import QuizGenerateRequest, QuizGenerateResponse
from services.quiz_service import generate_quiz
from routes.auth import get_current_user

router = APIRouter()

@router.post("/generate", response_model=QuizGenerateResponse)
async def generate_quiz_endpoint(request: QuizGenerateRequest, current_user: str = Depends(get_current_user)):
    try:
        result = generate_quiz(
            topic=request.topic,
            count=request.count,
            level=request.level,
            diff=request.difficulty,
            distractors=request.distractor_count,
            lang=request.language
        )
        return QuizGenerateResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate quiz: {str(e)}")

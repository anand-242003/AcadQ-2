from fastapi import APIRouter, HTTPException, Depends

from models.schemas import StudentInput, PredictionResponse
from services import ml_service
from routes.auth import get_current_user

router = APIRouter()


@router.post("/", response_model=PredictionResponse)
async def predict(
    student_input: StudentInput,
    current_user: str = Depends(get_current_user),
):
    try:
        raw = student_input.model_dump()
        result = ml_service.run_predictions(raw)
        return PredictionResponse(**result)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

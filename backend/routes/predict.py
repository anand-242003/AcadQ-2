from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from models.schemas import StudentInput, PredictionResponse, ReportItem, ReportsHistoryResponse
from services import ml_service
from routes.auth import get_current_user
from database.mongo import insert_report, get_reports_by_user

router = APIRouter()


@router.post("/", response_model=PredictionResponse)
async def predict(
    student_input: StudentInput,
    current_user: str = Depends(get_current_user),
):
    try:
        raw = student_input.model_dump()
        result = ml_service.run_predictions(raw)
        response = PredictionResponse(**result)


        report = {
            "user_email": current_user,
            "timestamp": datetime.utcnow().isoformat(),
            "prediction": response.model_dump(),
            "input_data": raw
        }
        insert_report(report)

        return response
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@router.get("/history", response_model=ReportsHistoryResponse)
async def get_reports_history(current_user: str = Depends(get_current_user)):
    try:
        reports = get_reports_by_user(current_user)

        for report in reports:
            report["id"] = str(report["_id"])
            del report["_id"]
        return ReportsHistoryResponse(reports=reports)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve reports: {str(e)}")

from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from services.rag_service import PDF_RESOURCES_DIR

router = APIRouter()


@router.get("/files/{file_name}")
async def get_resource_file(file_name: str):
    """Serve PDF resources indexed by the RAG pipeline."""
    safe_name = Path(file_name).name
    if safe_name != file_name:
        raise HTTPException(status_code=400, detail="Invalid file path")
    if not safe_name.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    file_path = PDF_RESOURCES_DIR / safe_name
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Resource file not found")

    return FileResponse(
        path=str(file_path),
        media_type="application/pdf",
        filename=safe_name,
    )
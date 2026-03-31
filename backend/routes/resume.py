from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import fitz  # PyMuPDF

from database.db import get_db
from models.resume import Resume

router = APIRouter()

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):

    contents = await file.read()

    # Open PDF
    doc = fitz.open(stream=contents, filetype="pdf")

    text = ""
    for page in doc:
        text += page.get_text()

    new_resume = Resume(
        user_id=1,  # temporary (we’ll link JWT later)
        resume_text=text
    )

    db.add(new_resume)
    db.commit()

    return {
        "message": "Resume uploaded successfully",
        "text_preview": text[:200]
    }
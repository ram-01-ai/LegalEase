from fastapi import APIRouter
from pydantic import BaseModel

from ai_core.gemini_generator import generate_legal_document


router = APIRouter()


class LegalDocumentRequest(BaseModel):
    document_type: str
    parties: str
    terms: str
    effective_date: str


@router.post("/generate-document")
def generate_document(request: LegalDocumentRequest):

    document = generate_legal_document(
        document_type=request.document_type,
        parties=request.parties,
        terms=request.terms,
        effective_date=request.effective_date
    )

    return {
        "message": "Document generated successfully!",
        "document": document
    }


@router.get("/test")
def test_route():
    return {"message": "LegalEase route is working!"}
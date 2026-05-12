from fastapi import APIRouter, UploadFile, File, Header, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid

router = APIRouter()


class SessionResponse(BaseModel):
    session_id: str
    expires_in: int = 600   # 10 minutes


class VerificationResult(BaseModel):
    session_id: str
    status: str              # "verified" | "failed" | "pending_review"
    liveness_score: Optional[float] = None
    face_match_score: Optional[float] = None
    ocr_confidence: Optional[float] = None
    fraud_score: Optional[float] = None


@router.post("/session/start", response_model=SessionResponse)
async def start_session(x_api_key: str = Header(...)):
    # TODO: validate API key, create session in DB/Redis
    session_id = str(uuid.uuid4())
    return SessionResponse(session_id=session_id)


@router.post("/liveness")
async def check_liveness(
    session_id: str,
    selfie: UploadFile = File(...),
    x_api_key: str = Header(...),
):
    # TODO: run Silent-Face + MediaPipe liveness check via Celery
    return {"session_id": session_id, "liveness_score": 0.0, "status": "processing"}


@router.post("/document")
async def verify_document(
    session_id: str,
    cnic_front: UploadFile = File(...),
    cnic_back: UploadFile = File(...),
    x_api_key: str = Header(...),
):
    # TODO: run PaddleOCR + ELA tampering check via Celery
    return {"session_id": session_id, "ocr_confidence": 0.0, "status": "processing"}


@router.post("/face-match")
async def face_match(
    session_id: str,
    selfie: UploadFile = File(...),
    id_photo: UploadFile = File(...),
    x_api_key: str = Header(...),
):
    # TODO: InsightFace ArcFace embedding comparison
    return {"session_id": session_id, "match_score": 0.0, "status": "processing"}


@router.post("/complete", response_model=VerificationResult)
async def full_kyc(
    session_id: str,
    selfie: UploadFile = File(...),
    cnic_front: UploadFile = File(...),
    cnic_back: UploadFile = File(...),
    x_api_key: str = Header(...),
):
    # TODO: single-call full KYC — chains liveness + OCR + face-match
    return VerificationResult(
        session_id=session_id,
        status="processing",
    )


@router.get("/{session_id}", response_model=VerificationResult)
async def get_result(session_id: str, x_api_key: str = Header(...)):
    # TODO: fetch result from DB
    return VerificationResult(session_id=session_id, status="pending")

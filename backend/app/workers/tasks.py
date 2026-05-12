from app.workers.celery_app import celery_app


@celery_app.task(bind=True, max_retries=3)
def run_liveness_check(self, session_id: str, image_path: str):
    # TODO: load Silent-Face model, run inference, update DB
    return {"session_id": session_id, "liveness_score": 0.0}


@celery_app.task(bind=True, max_retries=3)
def run_ocr(self, session_id: str, front_path: str, back_path: str):
    # TODO: PaddleOCR on CNIC images, extract name/CNIC number/DOB
    return {"session_id": session_id, "extracted": {}}


@celery_app.task(bind=True, max_retries=3)
def run_face_match(self, session_id: str, selfie_path: str, id_photo_path: str):
    # TODO: InsightFace ArcFace embedding, cosine similarity
    return {"session_id": session_id, "match_score": 0.0}


@celery_app.task(bind=True, max_retries=3)
def run_full_kyc(self, session_id: str, selfie_path: str, front_path: str, back_path: str):
    # Chains liveness + OCR + face match, writes final result to DB
    return {"session_id": session_id, "status": "pending"}

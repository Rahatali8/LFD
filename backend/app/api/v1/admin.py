from fastapi import APIRouter, Header

router = APIRouter()


@router.get("/stats")
async def get_stats(x_api_key: str = Header(...)):
    # TODO: pull from DB — total verifications, pass/fail rate, today's count
    return {
        "total_verifications": 0,
        "today": 0,
        "pass_rate": 0.0,
        "pending_review": 0,
    }


@router.get("/pending-reviews")
async def pending_reviews(x_api_key: str = Header(...)):
    # TODO: fetch verifications flagged for manual review
    return {"items": [], "total": 0}


@router.post("/review/{verification_id}/approve")
async def approve_review(verification_id: str, x_api_key: str = Header(...)):
    # TODO: update verification status, trigger webhook
    return {"verification_id": verification_id, "status": "approved"}


@router.post("/review/{verification_id}/reject")
async def reject_review(verification_id: str, x_api_key: str = Header(...)):
    return {"verification_id": verification_id, "status": "rejected"}

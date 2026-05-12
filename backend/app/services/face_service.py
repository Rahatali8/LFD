import numpy as np
from pathlib import Path
from app.core.config import get_settings

settings = get_settings()

_face_analysis = None


def get_face_analysis():
    global _face_analysis
    if _face_analysis is None:
        import insightface
        _face_analysis = insightface.app.FaceAnalysis(
            name=settings.INSIGHTFACE_MODEL,
            root=str(Path(settings.MODELS_PATH) / "insightface"),
            providers=["CUDAExecutionProvider", "CPUExecutionProvider"],
        )
        _face_analysis.prepare(ctx_id=0, det_size=(640, 640))
    return _face_analysis


def detect_faces(img: np.ndarray) -> list:
    fa = get_face_analysis()
    return fa.get(img)


def get_embedding(img: np.ndarray) -> np.ndarray | None:
    faces = detect_faces(img)
    if not faces:
        return None
    largest = max(faces, key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]))
    return largest.normed_embedding


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b))


def face_match(embed_a: np.ndarray, embed_b: np.ndarray, threshold: float | None = None) -> dict:
    if threshold is None:
        threshold = settings.FACE_MATCH_THRESHOLD
    score = cosine_similarity(embed_a, embed_b)
    return {
        "score": round(score, 4),
        "match": score >= threshold,
        "threshold": threshold,
    }

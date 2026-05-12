import cv2
import numpy as np
from pathlib import Path
from app.core.config import get_settings

settings = get_settings()

_liveness_model = None
MODEL_PATH = Path(settings.MODELS_PATH) / "anti-spoof"


def get_liveness_model():
    global _liveness_model
    if _liveness_model is None:
        import onnxruntime as ort
        model_file = MODEL_PATH / "anti_spoof.onnx"
        if not model_file.exists():
            raise FileNotFoundError(f"Liveness model not found: {model_file}")
        _liveness_model = ort.InferenceSession(
            str(model_file),
            providers=["CUDAExecutionProvider", "CPUExecutionProvider"],
        )
    return _liveness_model


def preprocess_face(img: np.ndarray, size: tuple = (80, 80)) -> np.ndarray:
    face = cv2.resize(img, size)
    face = face.astype(np.float32) / 255.0
    face = (face - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
    return face.transpose(2, 0, 1)[np.newaxis, ...]


def check_liveness(img: np.ndarray, face_bbox: list) -> dict:
    x1, y1, x2, y2 = [int(v) for v in face_bbox]
    margin = 20
    h, w = img.shape[:2]
    x1 = max(0, x1 - margin)
    y1 = max(0, y1 - margin)
    x2 = min(w, x2 + margin)
    y2 = min(h, y2 + margin)

    face_crop = img[y1:y2, x1:x2]
    if face_crop.size == 0:
        return {"score": 0.0, "is_live": False, "error": "empty_crop"}

    model = get_liveness_model()
    input_data = preprocess_face(face_crop)
    input_name = model.get_inputs()[0].name
    outputs = model.run(None, {input_name: input_data})

    # output: [spoof_prob, live_prob]
    live_prob = float(outputs[0][0][1])
    threshold = settings.LIVENESS_SCORE_THRESHOLD

    return {
        "score": round(live_prob, 4),
        "is_live": live_prob >= threshold,
        "threshold": threshold,
    }

import cv2
import numpy as np
from pathlib import Path
from app.core.config import get_settings

settings = get_settings()

_ocr = None


def get_ocr():
    global _ocr
    if _ocr is None:
        from paddleocr import PaddleOCR
        _ocr = PaddleOCR(
            use_angle_cls=True,
            lang="en",
            show_log=False,
            det_model_dir=str(Path(settings.MODELS_PATH) / "paddleocr/det"),
            rec_model_dir=str(Path(settings.MODELS_PATH) / "paddleocr/rec"),
            cls_model_dir=str(Path(settings.MODELS_PATH) / "paddleocr/cls"),
        )
    return _ocr


def extract_cnic_text(img: np.ndarray) -> dict:
    ocr = get_ocr()
    result = ocr.ocr(img, cls=True)

    lines = []
    avg_confidence = 0.0

    if result and result[0]:
        confidences = []
        for line in result[0]:
            text, conf = line[1]
            lines.append(text.strip())
            confidences.append(conf)
        avg_confidence = float(np.mean(confidences)) if confidences else 0.0

    raw_text = "\n".join(lines)
    parsed = _parse_cnic_fields(lines)

    return {
        "raw_text": raw_text,
        "lines": lines,
        "confidence": round(avg_confidence, 4),
        "parsed": parsed,
    }


def _parse_cnic_fields(lines: list[str]) -> dict:
    import re
    result = {}
    cnic_pattern = re.compile(r"\d{5}-\d{7}-\d{1}")
    date_pattern = re.compile(r"\d{2}\.\d{2}\.\d{4}")

    for line in lines:
        cnic_match = cnic_pattern.search(line)
        if cnic_match:
            result["cnic_number"] = cnic_match.group()

        date_matches = date_pattern.findall(line)
        if date_matches:
            key = "issue_date" if "issue_date" not in result else "expiry_date"
            result[key] = date_matches[0]

        if "name" not in result and len(line) > 3 and line.replace(" ", "").isalpha():
            result["name"] = line

    return result

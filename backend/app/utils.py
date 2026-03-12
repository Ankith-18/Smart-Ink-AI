import base64
import re
from io import BytesIO

import cv2
import numpy as np
from PIL import Image


def decode_base64_image(image_base64: str) -> np.ndarray:
    encoded = image_base64.split(',')[-1]
    image_bytes = base64.b64decode(encoded)
    image = Image.open(BytesIO(image_bytes)).convert('L')
    return np.array(image)


def detect_shape(gray_image: np.ndarray) -> tuple[str | None, np.ndarray | None]:
    blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None, None

    contour = max(contours, key=cv2.contourArea)
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.04 * peri, True)

    if len(approx) >= 8:
        shape = 'diagram'
    elif len(approx) == 4:
        x, y, w, h = cv2.boundingRect(approx)
        ratio = w / float(h)
        shape = 'square' if 0.9 <= ratio <= 1.1 else 'rectangle'
    elif len(approx) > 5:
        shape = 'circle'
    else:
        shape = None

    return shape, approx


def normalize_expression(raw: str) -> str:
    return raw.replace('x', '*').replace('X', '*').replace('÷', '/').replace(' ', '')


def parse_expression(raw: str) -> tuple[bool, str | None, float | None]:
    expr = normalize_expression(raw)
    if not re.fullmatch(r'\d+[+\-*/]\d+', expr):
        return False, None, None
    a, op, b = re.match(r'(\d+)([+\-*/])(\d+)', expr).groups()
    a, b = float(a), float(b)
    if op == '+':
        result = a + b
    elif op == '-':
        result = a - b
    elif op == '*':
        result = a * b
    else:
        result = a / b if b != 0 else float('inf')
    return True, expr, result


def detect_phone(raw: str) -> str | None:
    digits = re.sub(r'\D', '', raw)
    return digits if len(digits) == 10 else None


def detect_email(raw: str) -> str | None:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return raw if re.fullmatch(pattern, raw.strip()) else None

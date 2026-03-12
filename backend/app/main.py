import os

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .schemas import InkRequest
from .utils import decode_base64_image, detect_email, detect_phone, detect_shape, parse_expression

ML_SERVICE_URL = os.getenv('ML_SERVICE_URL', 'http://ml-service:8001')

app = FastAPI(title='Smart Ink AI Backend')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/health')
async def health() -> dict:
    return {'status': 'ok'}


@app.post('/predict-digit')
async def predict_digit(payload: InkRequest) -> dict:
    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.post(f'{ML_SERVICE_URL}/infer-digit', json={'image_base64': payload.image_base64})
        response.raise_for_status()
        return response.json()


@app.post('/detect-expression')
async def detect_expression(payload: InkRequest) -> dict:
    candidate = payload.text_hint or ''
    is_expression, normalized, result = parse_expression(candidate)
    return {
        'is_expression': is_expression,
        'normalized': normalized,
        'result': result,
    }


@app.post('/detect-phone')
async def detect_phone_endpoint(payload: InkRequest) -> dict:
    value = detect_phone(payload.text_hint or '')
    return {
        'is_phone': bool(value),
        'value': value,
        'suggestions': ['Call number', 'Save contact'] if value else [],
    }


@app.post('/detect-email')
async def detect_email_endpoint(payload: InkRequest) -> dict:
    value = detect_email(payload.text_hint or '')
    return {
        'is_email': bool(value),
        'value': value,
        'suggestions': ['Send email'] if value else [],
    }


@app.post('/detect-shape')
async def detect_shape_endpoint(payload: InkRequest) -> dict:
    gray = decode_base64_image(payload.image_base64)
    shape, _ = detect_shape(gray)
    return {
        'shape': shape,
        'action': f'convert_to_perfect_{shape}' if shape else None,
    }

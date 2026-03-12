import base64
from io import BytesIO

import numpy as np
from fastapi import FastAPI
from PIL import Image, ImageOps

from .model import load_or_train_model

app = FastAPI(title='Smart Ink AI ML Service')
model = load_or_train_model()


def preprocess(image_base64: str) -> np.ndarray:
    encoded = image_base64.split(',')[-1]
    image_bytes = base64.b64decode(encoded)
    image = Image.open(BytesIO(image_bytes)).convert('L')
    image = ImageOps.invert(image)
    image = image.resize((28, 28))
    arr = np.array(image).astype('float32') / 255.0
    arr = np.expand_dims(arr, axis=(0, -1))
    return arr


@app.get('/health')
async def health() -> dict:
    return {'status': 'ok'}


@app.post('/infer-digit')
async def infer_digit(payload: dict) -> dict:
    arr = preprocess(payload['image_base64'])
    probs = model.predict(arr, verbose=0)[0]
    digit = int(np.argmax(probs))
    return {
        'digit': digit,
        'confidence': float(probs[digit]),
        'probabilities': probs.tolist(),
    }

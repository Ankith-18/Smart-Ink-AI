# SMART INK AI – Intelligent Handwriting Recognition Platform

Smart Ink AI is a full-stack handwriting recognition system inspired by Samsung S-Pen style intelligent inking.

## Features
- Handwritten digit recognition (MNIST CNN)
- Math expression detection and evaluation from text hints
- Phone number detection with smart actions
- Email detection with suggestion
- Shape detection (circle, square, rectangle) + diagram heuristic
- Smart suggestion panel in React UI
- Dockerized multi-service setup

## Project Structure
```
/frontend      # React + Tailwind canvas UI
/backend       # FastAPI orchestration API
/ml-model      # FastAPI CNN inference service
/docker        # Dockerfiles for services
```

## API Endpoints
Backend (`:8000`):
- `POST /predict-digit`
- `POST /detect-shape`
- `POST /detect-expression`
- `POST /detect-phone`
- `POST /detect-email`

ML Service (`:8001`):
- `POST /infer-digit`

## Run with Docker
```bash
docker compose up --build
```

Frontend: http://localhost:5173

## Local Development
### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### ML Service
```bash
cd ml-model
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

> Note: the ML service will auto-train and save a lightweight CNN on MNIST the first time if no model file exists.
> TensorFlow is pinned as `tensorflow-cpu>=2.20,<2.22` for broader compatibility on newer Python environments (including recent Windows installs).

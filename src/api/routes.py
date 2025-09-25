from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, Request, Form
from sqlalchemy.orm import Session
from src.utils.db import SessionLocal
from src.data.database import FeedbackUsers, Base, engine, time_metrics
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import sys
from pathlib import Path
import time
from datetime import datetime
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

Base.metadata.create_all(bind=engine)

# Ajouter le répertoire racine au path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))
BASE_DIR = ROOT_DIR / "src" / "data" / "images"


from .auth import verify_token
from src.models.predictor import CatDogPredictor
from src.monitoring.metrics import time_inference, log_inference_time

# Configuration des templates
TEMPLATES_DIR = ROOT_DIR / "src" / "web" / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

router = APIRouter()
auth_scheme = HTTPBearer()

# Initialisation de la session DB 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialisation du prédicteur
predictor = CatDogPredictor()

@router.get("/", response_class=HTMLResponse)
async def welcome(request: Request):
    """Page d'accueil avec interface web"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "model_loaded": predictor.is_loaded()
    })

@router.get("/info", response_class=HTMLResponse)
async def info_page(request: Request):
    """Page d'informations"""
    model_info = {
        "name": "Cats vs Dogs Classifier",
        "version": "1.0.0",
        "description": "Modèle CNN pour classification chats/chiens",
        "parameters": predictor.model.count_params() if predictor.is_loaded() else 0,
        "classes": ["Cat", "Dog"],
        "input_size": f"{predictor.image_size[0]}x{predictor.image_size[1]}",
        "model_loaded": predictor.is_loaded()
    }
    return templates.TemplateResponse("info.html", {
        "request": request, 
        "model_info": model_info
    })

@router.get("/inference", response_class=HTMLResponse)
async def inference_page(request: Request):
    """Page d'inférence"""
    return templates.TemplateResponse("inference.html", {
        "request": request,
        "model_loaded": predictor.is_loaded()
    })

@router.post("/api/predict")
async def predict_api(
    file: UploadFile = File(...),
    token: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    if not predictor.is_loaded():
        raise HTTPException(status_code=503, detail="Modèle non disponible")

    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Format d'image invalide")

    start_time = time.perf_counter()
    try:
        image_data = await file.read()
        result = predictor.predict(image_data)

        inference_time_ms = (time.perf_counter() - start_time) * 1000

        # Créer entrée time_metrics
        metric = time_metrics(
            inference_time_ms=inference_time_ms,
            success=True
        )
        db.add(metric)
        db.commit()
        db.refresh(metric)

        response_data = {
            "filename": file.filename,
            "prediction": result["prediction"],
            "confidence": f"{result['confidence']:.2%}",
            "probabilities": {
                "cat": f"{result['probabilities']['cat']:.2%}",
                "dog": f"{result['probabilities']['dog']:.2%}"
            },
            "time_metric_id": metric.id
        }

        return response_data

    except Exception as e:
        end_time = time.perf_counter()
        inference_time_ms = (end_time - start_time) * 1000

        log_inference_time(
            inference_time_ms=inference_time_ms,
            filename=file.filename if file else "unknown",
            success=False
        )

        raise HTTPException(status_code=500, detail=f"Erreur de prédiction: {str(e)}")

@router.post("/api/feedback")
async def feedback(
    file: UploadFile = File(...),
    feedback: int = Form(...),  # 1 = positif, 0 = négatif
    prediction: str = Form(...),  # "c" ou "d"
    proba: int = Form(...),  # pourcentage (ex: 90)
    time_metric_id: int = Form(...),
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    db: Session = Depends(get_db)
):
    # Vérification du token
    if token.credentials != "?C@TS&D0GS!":
        raise HTTPException(status_code=403, detail="Token invalide")

    # Définir dossier selon feedback et prédiction
    feedback_dir = "positif" if feedback == 1 else "negatif"
    pred_dir = "chat" if prediction == "c" else "chien"

    save_dir = BASE_DIR / feedback_dir / pred_dir
    save_dir.mkdir(parents=True, exist_ok=True)

    # Génération du nom du fichier
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{feedback}_{prediction}_{proba}.jpg"
    filepath = save_dir / filename
    path_str = str(filepath)

    # Sauvegarde du fichier sur le disque
    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())

    # Création de l'entrée Feedback en base (on stocke juste le chemin)
    feedback_entry = FeedbackUsers(
        image_path=path_str,      # <-- on change image_data en image_path
        feedback=feedback,
        prediction=prediction,
        time_metric_id=time_metric_id
    )

    db.add(feedback_entry)
    db.commit()
    db.refresh(feedback_entry)

    return {
        "detail": "Feedback reçu et image sauvegardée",
        "feedback": feedback,
        "prediction": prediction,
        "image_path": filepath
    }
@router.get("/api/info")
async def api_info():
    """Informations API JSON"""
    return {
        "model_loaded": predictor.is_loaded(),
        "model_path": str(predictor.model_path),
        "version": "1.0.0",
        "parameters": predictor.model.count_params() if predictor.is_loaded() else 0
    }

@router.get("/health")
async def health_check():
    """Vérification de l'état de l'API"""
    return {
        "status": "healthy",
        "model_loaded": predictor.is_loaded()
    }
import pytest
import requests
from config.settings import API_CONFIG
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.data.database import Base, time_metrics, SessionLocal
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL= os.getenv("DATABASE_URL")

# Configuration
BASE_URL = "http://localhost:8000"
TOKEN = API_CONFIG["token"]
DATA_DIR = Path(__file__).parent.parent / "data"

@pytest.fixture(scope="module")
def db_session():
    """Fixture pour gérer la session DB"""
    session = SessionLocal()
    yield session
    session.close()

@pytest.fixture(scope="module")
def test_image():
    cat_dir = DATA_DIR / "raw" / "PetImages" / "Cat"
    for file_path in cat_dir.iterdir():
        if file_path.suffix.lower() in [".jpg", ".jpeg", ".png"]:
            return file_path
    pytest.skip("Aucune image de test valide trouvée")

def test_api_predict_and_db(db_session, test_image):
    headers = {"Authorization": f"Bearer {TOKEN}"}

    with open(test_image, "rb") as f:
        files = {"file": (test_image.name, f, "image/jpeg")}
        response = requests.post(f"{BASE_URL}/api/predict", files=files, headers=headers)

    assert response.status_code == 200, f"Erreur API : {response.text}"
    data = response.json()

    metric_id = data.get("time_metric_id")
    assert metric_id is not None, "time_metric_id absent dans la réponse"

    metric = db_session.query(time_metrics).filter_by(id=metric_id).first()
    assert metric is not None, "Entrée non trouvée en DB"
    assert metric.success is True

    print(f"Entrée insérée en DB : ID = {metric.id}, temps = {metric.inference_time_ms:.2f} ms")

    db_session.delete(metric)
    db_session.commit()

    metric = db_session.query(time_metrics).filter_by(id=metric_id).first()
    assert metric is None, "L’entrée n’a pas été supprimée"

    print("Entrée supprimée correctement")

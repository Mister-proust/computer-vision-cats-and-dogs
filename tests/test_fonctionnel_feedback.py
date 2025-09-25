import pytest
import requests
from config.settings import API_CONFIG
from src.data.database import SessionLocal, time_metrics, FeedbackUsers
from pathlib import Path

BASE_URL = "http://localhost:8000"
TOKEN = API_CONFIG["token"]
DATA_DIR = Path(__file__).parent.parent / "data"

@pytest.fixture(scope="module")
def db_session():
    session = SessionLocal()
    yield session
    session.close()

@pytest.fixture(scope="module")
def test_image():
    cat_dir = DATA_DIR / "raw" / "PetImages" / "Cat"
    for file_path in cat_dir.iterdir():
        if file_path.suffix.lower() in [".jpg", ".jpeg", ".png"]:
            return file_path
    pytest.skip("Aucune image valide trouvée")

def test_feedback_integration(db_session, test_image):
    headers = {"Authorization": f"Bearer {TOKEN}"}

    # 1. Faire une prédiction
    with open(test_image, "rb") as f:
        files = {"file": (test_image.name, f, "image/jpeg")}
        response = requests.post(f"{BASE_URL}/api/predict", files=files, headers=headers)

    assert response.status_code == 200
    data = response.json()
    metric_id = data.get("time_metric_id")
    assert metric_id is not None

    # 2. Ajouter un feedback utilisateur (multipart/form-data)
    with open(test_image, "rb") as f:
        files = {"file": (test_image.name, f, "image/jpeg")}
        form_data = {
            "feedback": "1",              # ⚠️ en string car Form(...)
            "prediction": "c",            # ou "d"
            "proba": "90",                # toujours string
            "time_metric_id": str(metric_id)
        }
        fb_response = requests.post(
            f"{BASE_URL}/api/feedback",
            files=files,
            data=form_data,
            headers=headers
        )

    assert fb_response.status_code == 200

    fb_data = fb_response.json()
    # si ta route ne renvoie pas l'id, il faudra le chercher en base
    fb_entry = db_session.query(FeedbackUsers).filter_by(time_metric_id=metric_id).first()
    assert fb_entry is not None
    assert fb_entry.feedback == 1
    assert fb_entry.prediction in ["c", "d"]

    print(f"Feedback enregistré : ID={fb_entry.id}, prediction_id={metric_id}")

    db_session.delete(fb_entry)
    db_session.commit()
    fb_entry = db_session.query(FeedbackUsers).filter_by(id=fb_entry.id).first()
    assert fb_entry is None

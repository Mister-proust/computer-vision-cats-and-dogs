import time
import requests
from pathlib import Path
from config.settings import DATA_DIR, API_CONFIG

BASE_URL = "http://localhost:8000"
TOKEN = API_CONFIG["token"]

test_image = DATA_DIR / "raw" / "PetImages" / "Cat" / "6653.jpg"
test_image_chien =  DATA_DIR / "raw" / "PetImages" / "Dog" / "6.jpg"

def test_prediction_speed():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    start = time.time()
    with open(test_image, "rb") as f:
        files = {"file": (test_image.name, f, "image/jpeg")}
        response = requests.post(f"{BASE_URL}/api/predict", files=files, headers=headers)
    duration = time.time() - start
    assert duration < 2.0, f"Temps de prédiction trop long : {duration:.2f}s"


def test_prediction_cat():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    with open(test_image, "rb") as f:
        files = {"file": (test_image.name, f, "image/jpeg")}
        response = requests.post(f"{BASE_URL}/api/predict", files=files, headers=headers)

    assert response.status_code == 200, f"Erreur API: {response.text}"
    
    data = response.json()  
    prediction = data.get("prediction", "").lower()

    assert prediction == "cat", f"Prédiction incorrecte : {prediction}"

def test_prediction_dog():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    with open(test_image_chien, "rb") as f:
        files = {"file": (test_image_chien.name, f, "image/jpeg")}
        response = requests.post(f"{BASE_URL}/api/predict", files=files, headers=headers)

    assert response.status_code == 200, f"Erreur API: {response.text}"
    
    data = response.json()  
    prediction = data.get("prediction", "").lower()

    assert prediction == "dog", f"Prédiction incorrecte : {prediction}"

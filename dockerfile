# Choix de l'image Python
FROM python:3.10

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements/base.txt .
RUN pip install -r base.txt

COPY . .

# Exposer le port sur lequel tourne FastAPI
EXPOSE 8000

# Commande par défaut pour démarrer l'API
CMD ["python", "scripts/run_api.py"]

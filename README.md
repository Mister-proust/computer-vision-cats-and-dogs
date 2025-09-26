# Template Data IA MLOps

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![FAST Api](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-257bd6?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=for-the-badge)](CONTRIBUTING.md)

<div align="center">

<h3>Template de projet GitHub pour les projets data science, IA et MLOps.
<br>Structure simple et flexible qui s'adapte à tes besoins.</br></h3>

[Explore the docs](docs/)

</div>

---

## 🚀 Démarrage rapide

1. **Utilise ce template** en cliquant sur "Use this template" sur GitHub
2. **Clone ton nouveau repo** : `git clone <ton-repo>`
3. **Configure l'environnement** : `cp .env.example .env`
4. **Installe les dépendances** : `pip install -r requirements/base.txt`
5. **Lance les tests** : `pytest`

## 📁 Structure du projet

```txt
project-name/
├── .github/
│   ├── workflows/           # CI/CD pipelines
│   └── ISSUE_TEMPLATE/      # Templates d'issues
├── src/                     # Code source principal
│   ├── api/                 # APIs et services web
│   ├── data/                # Stockage des images récupérées
│   ├── models/              # Modèles ML/IA
│   ├── monitoring/          # Monitoring de l'API
│   ├── init/                # Schéma SQL
│   └── utils/               # Utilitaires partagés
├── data/
│   ├── raw/                 # Données brutes (gitignored)
│   ├── processed/           # Données traitées (gitignored)
│   └── external/            # Données externes/références
├── notebooks/               # Jupyter notebooks pour exploration
├── config/                  # Fichiers de configuration
├── docker/                  # Dockerfiles et compose
├── docs/                    # Documentation
├── tests/                   # Tests unitaires et d'intégration
├── scripts/                 # Scripts d'automatisation/déploiement
├── requirements/            # Dépendances par environnement
│   ├── base.txt
├── .gitignore
├── README.md
```

## 📊 Types de projets supportés

- **Data Science** : Analyse exploratoire, pipelines de données
- **Machine Learning** : Entraînement, évaluation, déploiement
- **APIs** : Services REST/GraphQL, microservices
- **MLOps** : CI/CD, monitoring, versioning des modèles

## 🤝 Contribution

1. Fork le projet
2. Crée ta branche (`git checkout -b feature/amelioration`)
3. Commit tes changes (`git commit -m 'Ajout fonctionnalité'`)
4. Push vers la branche (`git push origin feature/amelioration`)
5. Ouvre une Pull Request

## 📄 Licence
MIT - voir LICENSE pour plus de détails.

## RGPD 

Les images envoyées par les utilisateurs ne sont pas conservés sauf si l'utilisateur donne un feedback. A ce moment la, l'utilisateur consent à ce que son image soit enregistré afin d'être potentiellement réutilisée dans le cadre d'un réapprentissage du modèle. L'image ne sera pas utilisé pour autre chose que le réapprentissage du modèle et surtout, l'image ne sera pas vendue. Il est tout à fait possible de demander à supprimer les images en envoyant un mail. 

## Procédure de réentrainement

Les images stockées et récupérées par le feedback feront l'objet d'une analyse par un humain. Si ces images sont pertinentes, elles seront conservées afin de les utiliser pour réentrainer le modèle. 

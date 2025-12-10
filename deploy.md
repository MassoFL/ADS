# Guide de Déploiement

## 🚀 Options de Déploiement

### 1. Heroku
```bash
# Installer Heroku CLI puis :
heroku create votre-app-name
heroku config:set MISTRAL_API_KEY=votre_clé_api
heroku config:set FLASK_CONFIG=production
git push heroku main
```

### 2. Railway
```bash
# Connectez votre repo GitHub à Railway
# Ajoutez les variables d'environnement :
# MISTRAL_API_KEY=votre_clé_api
# FLASK_CONFIG=production
```

### 3. Render
```bash
# Connectez votre repo GitHub à Render
# Configurez :
# Build Command: pip install -r requirements.txt
# Start Command: gunicorn app:app
# Variables d'environnement :
# MISTRAL_API_KEY=votre_clé_api
# FLASK_CONFIG=production
```

### 4. Docker
```bash
docker build -t ads-generator .
docker run -p 8080:8080 -e MISTRAL_API_KEY=votre_clé_api ads-generator
```

## 🔧 Variables d'Environnement Requises

- `MISTRAL_API_KEY` : Votre clé API Mistral (obligatoire)
- `FLASK_CONFIG` : `production` pour le déploiement
- `PORT` : Port d'écoute (défaut: 8080)
- `SECRET_KEY` : Clé secrète Flask (optionnel, généré automatiquement)

## 📝 Notes

- Le fichier `.env` est exclu du repository pour la sécurité
- Configurez toujours les variables d'environnement sur votre plateforme de déploiement
- L'application utilise gunicorn en production pour de meilleures performances
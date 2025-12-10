# Générateur de Publicités IA

Application web qui analyse le contenu d'articles ou de fichiers PDF et génère des suggestions de publicités pertinentes grâce à Mistral AI.

## 🚀 Fonctionnalités

- **Analyse d'URLs** : Extrait et analyse le contenu de pages web
- **Analyse de PDFs** : Traite les fichiers PDF pour extraire le texte
- **IA Mistral** : Utilise Mistral AI pour générer des suggestions publicitaires contextuelles
- **Interface moderne** : Interface web responsive avec Bootstrap
- **API REST** : Endpoint API pour intégration dans d'autres applications

## 📋 Prérequis

- Python 3.8+
- Clé API Mistral AI ([obtenez-la ici](https://console.mistral.ai/))

## 🛠️ Installation

1. **Clonez le projet** (ou téléchargez les fichiers)

2. **Installez les dépendances** :
```bash
pip install -r requirements.txt
```

3. **Configurez votre clé API** :
```bash
# Copiez le fichier d'exemple
cp .env.example .env

# Éditez .env et ajoutez votre clé API Mistral
MISTRAL_API_KEY=votre_clé_api_mistral_ici
```

## 🚀 Démarrage

### Méthode simple
```bash
python run.py
```

### Méthode manuelle
```bash
export MISTRAL_API_KEY="votre_clé_api_mistral"
python app.py
```

L'application sera accessible sur : **http://localhost:5000**

## 💻 Utilisation

### Interface Web
1. Ouvrez http://localhost:5000 dans votre navigateur
2. Choisissez une option :
   - **URL** : Collez le lien d'un article à analyser
   - **PDF** : Téléchargez un fichier PDF (glisser-déposer supporté)
3. Cliquez sur "Générer les suggestions publicitaires"
4. Consultez les résultats et copiez-les si nécessaire

### API REST
```bash
# Analyser une URL
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://exemple.com/article"}'

# Analyser du texte directement
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Votre contenu à analyser..."}'
```

## 📁 Structure du Projet

```
.
├── app.py                 # Application Flask principale
├── run.py                 # Script de démarrage
├── modify_pdf.py          # Script utilitaire pour modifier les PDFs
├── requirements.txt       # Dépendances Python
├── .env.example          # Exemple de configuration
├── templates/            # Templates HTML
│   ├── base.html         # Template de base
│   ├── index.html        # Page d'accueil
│   └── results.html      # Page de résultats
└── uploads/              # Dossier temporaire pour les fichiers
```

## 🔧 Configuration

### Variables d'environnement
- `MISTRAL_API_KEY` : Clé API Mistral AI (obligatoire)
- `SECRET_KEY` : Clé secrète Flask (optionnel)
- `FLASK_ENV` : Environnement Flask (optionnel)

### Limites
- Taille max des PDFs : 16MB
- Formats supportés : PDF uniquement pour les fichiers
- Timeout des requêtes web : 10 secondes

## 🛠️ Script de Modification PDF (Legacy)

Le script `modify_pdf.py` permet d'ajouter une barre blanche sur les PDFs :

```bash
python modify_pdf.py input.pdf [output.pdf]
```

## 🤝 Contribution

1. Fork le projet
2. Créez une branche pour votre fonctionnalité
3. Committez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

## 📝 Licence

Ce projet est sous licence MIT.

## 🆘 Support

Si vous rencontrez des problèmes :
1. Vérifiez que votre clé API Mistral est correcte
2. Assurez-vous que toutes les dépendances sont installées
3. Consultez les logs de l'application pour plus de détails


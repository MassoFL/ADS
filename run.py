#!/usr/bin/env python3
"""
Script de démarrage pour l'application de génération de publicités IA.
"""

import os
import sys
from pathlib import Path

def load_env_file():
    """Charge les variables d'environnement depuis le fichier .env s'il existe."""
    env_file = Path('.env')
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

def check_requirements():
    """Vérifie que les dépendances sont installées."""
    try:
        import flask
        import mistralai
        import fitz
        import requests
        import bs4
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        print("📦 Installez les dépendances avec: pip install -r requirements.txt")
        sys.exit(1)

def main():
    """Fonction principale."""
    print("🚀 Démarrage de l'application de génération de publicités IA...")
    
    # Charger les variables d'environnement
    load_env_file()
    
    # Vérifier les dépendances
    check_requirements()
    
    # Vérifier la clé API Mistral
    if not os.environ.get('MISTRAL_API_KEY'):
        print("⚠️  ATTENTION: Variable d'environnement MISTRAL_API_KEY non définie!")
        print("   1. Copiez .env.example vers .env")
        print("   2. Ajoutez votre clé API Mistral dans le fichier .env")
        print("   3. Ou définissez-la avec: export MISTRAL_API_KEY='votre-clé-api'")
        print()
        response = input("Continuer sans clé API? (l'application ne fonctionnera pas) [y/N]: ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Importer et démarrer l'application
    from app import app
    
    print("✅ Application prête!")
    print("🌐 Accédez à l'application sur: http://localhost:8080")
    print("🛑 Appuyez sur Ctrl+C pour arrêter")
    print()
    
    app.run(debug=True, host='0.0.0.0', port=8080)

if __name__ == '__main__':
    main()
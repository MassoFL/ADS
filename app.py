#!/usr/bin/env python3
"""
Application web pour analyser le contenu d'articles/PDFs et générer des suggestions publicitaires
avec Mistral AI.
"""

import os
import tempfile
import requests
import uuid
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename
import fitz  # PyMuPDF
from mistralai import Mistral
from urllib.parse import urlparse
import re
from bs4 import BeautifulSoup

app = Flask(__name__)

# Configuration
ALLOWED_EXTENSIONS = {'pdf'}

# Load configuration
config_name = os.environ.get('FLASK_CONFIG', 'default')
if config_name == 'production':
    from config import ProductionConfig
    app.config.from_object(ProductionConfig)
    # Use system temp directory for serverless environments
    UPLOAD_FOLDER = tempfile.gettempdir()
else:
    from config import DevelopmentConfig
    app.config.from_object(DevelopmentConfig)
    UPLOAD_FOLDER = 'uploads'
    # Créer le dossier uploads s'il n'existe pas (seulement en dev)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Client Mistral AI
mistral_client = None
try:
    mistral_api_key = os.environ.get('MISTRAL_API_KEY')
    if mistral_api_key:
        mistral_client = Mistral(api_key=mistral_api_key)
except Exception as e:
    print(f"Erreur lors de l'initialisation du client Mistral: {e}")


def allowed_file(filename):
    """Vérifie si le fichier a une extension autorisée."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(pdf_path):
    """Extrait le texte d'un fichier PDF."""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page_num in range(len(doc)):
            page = doc[page_num]
            text += page.get_text()
        doc.close()
        return text.strip()
    except Exception as e:
        raise Exception(f"Erreur lors de l'extraction du PDF: {str(e)}")


def extract_text_from_url(url):
    """Extrait le texte d'une page web."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Supprimer les scripts et styles
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Extraire le texte principal
        text = soup.get_text()
        
        # Nettoyer le texte
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        raise Exception(f"Erreur lors de l'extraction de l'URL: {str(e)}")


def generate_ad_suggestions(content):
    """Génère des suggestions publicitaires avec Mistral AI."""
    if not mistral_client:
        raise Exception("Client Mistral AI non configuré. Veuillez définir MISTRAL_API_KEY.")
    
    # Limiter le contenu pour éviter les tokens excessifs
    content = content[:4000] if len(content) > 4000 else content
    
    prompt = f"""
Analyse le contenu suivant et génère 3 suggestions de publicités qui seraient pertinentes à placer dans cet article.

Pour chaque suggestion, fournis:
1. Le type de produit/service
2. Le public cible
3. Le message publicitaire (slogan/accroche)
4. Pourquoi cette publicité serait pertinente dans ce contexte

Contenu à analyser:
{content}

Réponds en français avec un format structuré.
"""

    try:
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        chat_response = mistral_client.chat.complete(
            model="mistral-large-latest",
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )
        
        return chat_response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Erreur lors de la génération avec Mistral: {str(e)}")


@app.route('/')
def index():
    """Page d'accueil."""
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyse le contenu et génère des suggestions publicitaires."""
    try:
        content = ""
        source_type = ""
        
        # Vérifier si c'est un fichier PDF
        if 'pdf_file' in request.files and request.files['pdf_file'].filename:
            file = request.files['pdf_file']
            if file and allowed_file(file.filename):
                # Créer un fichier temporaire unique
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    file.save(tmp_file.name)
                    content = extract_text_from_pdf(tmp_file.name)
                    source_type = "PDF"
                    # Nettoyer le fichier temporaire
                    os.unlink(tmp_file.name)
            else:
                flash('Fichier PDF invalide.')
                return redirect(url_for('index'))
        
        # Vérifier si c'est une URL
        elif 'url' in request.form and request.form['url'].strip():
            url = request.form['url'].strip()
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            content = extract_text_from_url(url)
            source_type = "URL"
        
        else:
            flash('Veuillez fournir soit un fichier PDF soit une URL.')
            return redirect(url_for('index'))
        
        if not content.strip():
            flash('Aucun contenu textuel trouvé.')
            return redirect(url_for('index'))
        
        # Générer les suggestions publicitaires
        ad_suggestions = generate_ad_suggestions(content)
        
        return render_template('results.html', 
                             suggestions=ad_suggestions,
                             source_type=source_type,
                             content_preview=content[:500] + "..." if len(content) > 500 else content)
    
    except Exception as e:
        flash(f'Erreur: {str(e)}')
        return redirect(url_for('index'))


@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint pour l'analyse."""
    try:
        data = request.get_json()
        
        if 'url' in data:
            content = extract_text_from_url(data['url'])
            source_type = "URL"
        elif 'text' in data:
            content = data['text']
            source_type = "TEXT"
        else:
            return jsonify({'error': 'URL ou texte requis'}), 400
        
        suggestions = generate_ad_suggestions(content)
        
        return jsonify({
            'success': True,
            'source_type': source_type,
            'suggestions': suggestions,
            'content_preview': content[:500] + "..." if len(content) > 500 else content
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    if not os.environ.get('MISTRAL_API_KEY'):
        print("⚠️  ATTENTION: Variable d'environnement MISTRAL_API_KEY non définie!")
        print("   Définissez-la avec: export MISTRAL_API_KEY='votre-clé-api'")
    
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=port)
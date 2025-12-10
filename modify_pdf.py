#!/usr/bin/env python3
"""
Script pour modifier un fichier PDF en ajoutant une barre blanche horizontale
sur toutes les pages à un endroit précis.
"""

import fitz  # PyMuPDF
import sys
import os
from pathlib import Path


def add_white_bar_to_pdf(input_path, output_path, x0, y0, x1, y1):
    """
    Ajoute une barre blanche horizontale sur toutes les pages d'un PDF.
    
    Args:
        input_path: Chemin vers le fichier PDF d'entrée
        output_path: Chemin vers le fichier PDF de sortie
        x0: Coordonnée X du début de la barre (en points)
        y0: Coordonnée Y du début de la barre (en points)
        x1: Coordonnée X de la fin de la barre (en points)
        y1: Coordonnée Y de la fin de la barre (en points)
    """
    # Ouvrir le document PDF
    doc = fitz.open(input_path)
    
    print(f"Traitement de {len(doc)} page(s)...")
    
    # Parcourir toutes les pages
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # Créer un rectangle pour la barre blanche
        rect = fitz.Rect(x0, y0, x1, y1)
        
        # Dessiner un rectangle blanc (la barre)
        page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1), width=0)
        
        print(f"  Barre ajoutée sur la page {page_num + 1}")
    
    # Sauvegarder le document modifié
    doc.save(output_path)
    doc.close()
    
    print(f"\nPDF modifié sauvegardé sous: {output_path}")


def main():
    """
    Fonction principale avec des paramètres configurables.
    """
    if len(sys.argv) < 2:
        print("Usage: python modify_pdf.py <fichier_pdf> [fichier_sortie]")
        print("\nOu utilisez les paramètres par défaut dans le script.")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.pdf', '_modified.pdf')
    
    # Vérifier que le fichier d'entrée existe
    if not os.path.exists(input_file):
        print(f"Erreur: Le fichier '{input_file}' n'existe pas.")
        sys.exit(1)
    
    # Configuration de la barre blanche
    # Vous pouvez ajuster ces valeurs selon vos besoins
    # Format: (x0, y0, x1, y1) en points (1 point = 1/72 pouce)
    
    # Exemple 1: Barre horizontale au milieu de la page (pour une page A4 = 595x842 points)
    # x0 = 0          # Début de la barre (bord gauche)
    # y0 = 400        # Position verticale du haut de la barre
    # x1 = 595        # Fin de la barre (bord droit)
    # y1 = 450        # Position verticale du bas de la barre (épaisseur de 50 points)
    
    # Exemple 2: Barre horizontale en haut de la page
    x0 = 0
    y0 = 0
    x1 = 595  # Largeur A4 en points
    y1 = 50   # Épaisseur de la barre
    
    # Exemple 3: Barre horizontale au milieu
    # x0 = 0
    # y0 = 400
    # x1 = 595
    # y1 = 450
    
    # Exemple 4: Barre horizontale en bas
    # x0 = 0
    # y0 = 792  # Pour une page A4 (842 - 50)
    # x1 = 595
    # y1 = 842
    
    # Vous pouvez aussi utiliser des pourcentages de la page
    # Pour cela, vous devez d'abord obtenir les dimensions de la page:
    doc_temp = fitz.open(input_file)
    first_page = doc_temp[0]
    page_width = first_page.rect.width
    page_height = first_page.rect.height
    doc_temp.close()
    
    # Exemple avec pourcentages (barre au milieu verticalement, 10% de la hauteur)
    # x0 = 0
    # y0 = page_height * 0.45  # 45% du haut
    # x1 = page_width
    # y1 = page_height * 0.55   # 55% du haut (barre de 10% d'épaisseur)
    
    # Configuration actuelle (barre en haut de 50 points)
    x0 = 0
    y0 = 0
    x1 = page_width
    y1 = 50
    
    print(f"Dimensions de la page: {page_width} x {page_height} points")
    print(f"Position de la barre: ({x0}, {y0}) à ({x1}, {y1})")
    print()
    
    # Appliquer les modifications
    add_white_bar_to_pdf(input_file, output_file, x0, y0, x1, y1)


if __name__ == "__main__":
    main()


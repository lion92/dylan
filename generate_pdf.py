#!/usr/bin/env python3
"""
Script pour générer un PDF à partir du CV HTML
"""
import os
import subprocess
import sys
from pathlib import Path

def generate_pdf():
    """Génère le PDF du CV à partir du fichier HTML"""
    current_dir = Path(__file__).parent
    html_file = current_dir / "cv-jeff-dylan.html"
    pdf_file = current_dir / "cv-jeff-dylan.pdf"

    if not html_file.exists():
        print(f"Erreur: {html_file} n'existe pas")
        return False

    try:
        # Essayer avec wkhtmltopdf si disponible
        cmd = [
            "wkhtmltopdf",
            "--page-size", "A4",
            "--margin-top", "10mm",
            "--margin-bottom", "10mm",
            "--margin-left", "10mm",
            "--margin-right", "10mm",
            "--disable-smart-shrinking",
            str(html_file),
            str(pdf_file)
        ]

        subprocess.run(cmd, check=True, capture_output=True)
        print(f"✅ PDF généré avec succès: {pdf_file}")
        return True

    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            # Essayer avec Chrome/Chromium
            chrome_commands = [
                "google-chrome",
                "chromium",
                "chromium-browser",
                "chrome"
            ]

            for chrome_cmd in chrome_commands:
                try:
                    cmd = [
                        chrome_cmd,
                        "--headless",
                        "--disable-gpu",
                        "--no-sandbox",
                        "--print-to-pdf=" + str(pdf_file),
                        "--print-to-pdf-no-header",
                        "file://" + str(html_file.absolute())
                    ]

                    subprocess.run(cmd, check=True, capture_output=True)
                    print(f"✅ PDF généré avec Chrome: {pdf_file}")
                    return True

                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue

            print("❌ Impossible de générer le PDF automatiquement")
            print("Veuillez ouvrir cv-jeff-dylan.html dans votre navigateur")
            print("et utiliser Ctrl+P pour enregistrer en PDF manuellement")
            return False

        except Exception as e:
            print(f"❌ Erreur lors de la génération du PDF: {e}")
            return False

if __name__ == "__main__":
    success = generate_pdf()
    sys.exit(0 if success else 1)
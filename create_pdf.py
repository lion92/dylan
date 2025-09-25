import subprocess
import sys
from pathlib import Path

def generate_pdf():
    current_dir = Path.cwd()
    html_file = current_dir / 'cv-jeff-dylan.html'
    pdf_file = current_dir / 'cv-jeff-dylan.pdf'

    print(f'Tentative de génération PDF...')
    print(f'HTML: {html_file}')
    print(f'PDF: {pdf_file}')

    if not html_file.exists():
        print(f'Erreur: Le fichier HTML n\'existe pas: {html_file}')
        return False

    # Essayer avec différents navigateurs Chrome
    chrome_paths = [
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
        'chrome',
        'google-chrome'
    ]

    for chrome_path in chrome_paths:
        try:
            # Convertir le chemin Windows en URL file://
            html_url = 'file:///' + str(html_file.absolute()).replace('\\', '/')

            cmd = [
                chrome_path,
                '--headless',
                '--disable-gpu',
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--print-to-pdf=' + str(pdf_file),
                '--print-to-pdf-no-header',
                html_url
            ]

            print(f'Essai avec: {chrome_path}')
            print(f'URL: {html_url}')

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if pdf_file.exists():
                file_size = pdf_file.stat().st_size
                print(f'✅ PDF généré avec succès!')
                print(f'Fichier: {pdf_file}')
                print(f'Taille: {file_size} bytes')
                return True
            else:
                print(f'❌ PDF non créé avec {chrome_path}')
                if result.stderr:
                    print(f'Erreur: {result.stderr}')

        except subprocess.TimeoutExpired:
            print(f'⏱️ Timeout avec {chrome_path}')
        except FileNotFoundError:
            print(f'❌ {chrome_path} non trouvé')
        except Exception as e:
            print(f'❌ Erreur avec {chrome_path}: {e}')
            continue

    print('❌ Impossible de générer le PDF automatiquement')
    print('Veuillez ouvrir cv-jeff-dylan.html et utiliser Ctrl+P pour créer le PDF manuellement')
    return False

if __name__ == '__main__':
    generate_pdf()
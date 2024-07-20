import os
import sys
import subprocess
import tempfile
import shutil
import zipfile
import urllib.request
from tkinter import Tk, filedialog, messagebox

def install_dependencies():
    print("Verifica e installazione delle dipendenze...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "pdf2image"])
        print("Dipendenze installate con successo.")
    except subprocess.CalledProcessError:
        print("Errore nell'installazione delle dipendenze.")
        sys.exit(1)

def download_and_extract_poppler():
    poppler_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "poppler")
    if os.path.exists(poppler_path):
        return poppler_path

    print("Download di Poppler...")
    url = "https://github.com/oschwartz10612/poppler-windows/releases/download/v23.08.0-0/Release-23.08.0-0.zip"
    zip_path = os.path.join(tempfile.gettempdir(), "poppler.zip")
    
    urllib.request.urlretrieve(url, zip_path)
    
    print("Estrazione di Poppler...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(poppler_path)
    
    os.remove(zip_path)
    return poppler_path

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

# Il resto delle funzioni (convert_pdf_to_image, convert_to_ico, convert_bat_to_exe, convert_file) rimane invariato

def main():
    if not is_admin():
        print("Riavvio con privilegi di amministratore...")
        run_as_admin()
        return

    install_dependencies()
    poppler_path = download_and_extract_poppler()
    os.environ["PATH"] += os.pathsep + os.path.join(poppler_path, "Library", "bin")

    if len(sys.argv) != 2:
        print("Uso: python convert_script.py <percorso_del_file>")
    else:
        convert_file(sys.argv[1])

if __name__ == "__main__":
    main()

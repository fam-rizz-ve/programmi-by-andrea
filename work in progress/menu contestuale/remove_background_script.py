import os
import sys
from PIL import Image
import numpy as np
from rembg import remove

def remove_background(input_path):
    # Ottieni il nome del file e l'estensione
    file_name, file_extension = os.path.splitext(input_path)
    
    # Crea il nome del file di output
    output_path = f"{file_name}_no_bg{file_extension}"
    
    try:
        # Apri l'immagine
        with Image.open(input_path) as img:
            # Rimuovi lo sfondo
            output = remove(img)
            
            # Salva l'immagine risultante
            output.save(output_path)
        
        print(f"Sfondo rimosso con successo. File salvato: {output_path}")
    except Exception as e:
        print(f"Errore durante la rimozione dello sfondo: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python remove_background_script.py <percorso_del_file>")
    else:
        remove_background(sys.argv[1])

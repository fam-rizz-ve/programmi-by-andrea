import os
import sys
import winreg
from PIL import Image
from rembg import remove
import tkinter as tk
from tkinter import filedialog, messagebox
import moviepy.editor as mp
import docx2pdf
import pypandoc
import subprocess
import shutil

def aggiungi_al_menu_contestuale():
    chiave_base = winreg.HKEY_CLASSES_ROOT
    percorso_chiave = r"*\shell\MenuPersonalizzato"
    
    try:
        chiave = winreg.CreateKey(chiave_base, percorso_chiave)
        winreg.SetValue(chiave, "", winreg.REG_SZ, "Menu Personalizzato")
        
        chiave_comando = winreg.CreateKey(chiave, "command")
        winreg.SetValue(chiave_comando, "", winreg.REG_SZ, f'"{sys.executable}" "{os.path.abspath(__file__)}" "%1"')
        
        print("Menu contestuale aggiunto con successo.")
    except Exception as e:
        print(f"Errore durante l'aggiunta del menu contestuale: {e}")

def converti_file(percorso_file):
    percorso_file = os.path.normpath(percorso_file)
    estensione = os.path.splitext(percorso_file)[1].lower()
    
    formati_immagine = [".jpg", ".png", ".bmp", ".gif", ".tiff", ".webp"]
    formati_video = [".mp4", ".avi", ".mov", ".mkv", ".webm"]
    formati_testo = [".txt", ".docx", ".pdf", ".md", ".html"]
    
    if estensione in formati_immagine:
        converti_immagine(percorso_file)
    elif estensione in formati_video:
        converti_video(percorso_file)
    elif estensione in formati_testo:
        converti_testo(percorso_file)
    elif estensione == '.mp3':
        converti_mp3(percorso_file)
    elif estensione == '.bat':
        converti_bat_to_exe(percorso_file)
    elif estensione == '.exe':
        converti_exe_to_bat(percorso_file)
    elif estensione == '.py':
        converti_py_to_exe(percorso_file)
    else:
        messagebox.showerror("Errore", "Formato file non supportato per la conversione.")

def converti_immagine(percorso_file):
    formati = [".jpg", ".png", ".bmp", ".gif", ".tiff", ".webp"]
    formato_scelto = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("Immagine", f"*{ext}") for ext in formati]
    )
    
    if formato_scelto:
        try:
            immagine = Image.open(percorso_file)
            immagine.save(formato_scelto)
            messagebox.showinfo("Successo", f"File convertito e salvato come {formato_scelto}")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante la conversione del file: {e}")
    else:
        messagebox.showinfo("Informazione", "Conversione annullata.")

def converti_video(percorso_file):
    formati = [".mp4", ".avi", ".mov", ".mkv", ".webm"]
    formato_scelto = filedialog.asksaveasfilename(
        defaultextension=".mp4",
        filetypes=[("Video", f"*{ext}") for ext in formati]
    )
    
    if formato_scelto:
        try:
            video = mp.VideoFileClip(percorso_file)
            video.write_videofile(formato_scelto)
            messagebox.showinfo("Successo", f"Video convertito e salvato come {formato_scelto}")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante la conversione del video: {e}")
    else:
        messagebox.showinfo("Informazione", "Conversione annullata.")

def converti_testo(percorso_file):
    formati = [".txt", ".docx", ".pdf", ".md", ".html"]
    formato_scelto = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("Documento", f"*{ext}") for ext in formati]
    )
    
    if formato_scelto:
        try:
            estensione_input = os.path.splitext(percorso_file)[1].lower()
            estensione_output = os.path.splitext(formato_scelto)[1].lower()
            
            if estensione_input == '.docx' and estensione_output == '.pdf':
                docx2pdf.convert(percorso_file, formato_scelto)
            else:
                pypandoc.convert_file(percorso_file, estensione_output[1:], outputfile=formato_scelto)
            
            messagebox.showinfo("Successo", f"File convertito e salvato come {formato_scelto}")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante la conversione del file: {e}")
    else:
        messagebox.showinfo("Informazione", "Conversione annullata.")

def converti_mp3(percorso_file):
    formati = [".wav", ".ogg", ".flac"]
    formato_scelto = filedialog.asksaveasfilename(
        defaultextension=".wav",
        filetypes=[("Audio", f"*{ext}") for ext in formati]
    )
    
    if formato_scelto:
        try:
            audio = mp.AudioFileClip(percorso_file)
            audio.write_audiofile(formato_scelto)
            messagebox.showinfo("Successo", f"Audio convertito e salvato come {formato_scelto}")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante la conversione dell'audio: {e}")
    else:
        messagebox.showinfo("Informazione", "Conversione annullata.")

def converti_bat_to_exe(percorso_file):
    try:
        nome_file = os.path.splitext(os.path.basename(percorso_file))[0]
        output_file = f"{nome_file}.exe"
        
        comando = f'bat2exe "{percorso_file}" "{output_file}"'
        subprocess.run(comando, shell=True, check=True)
        
        messagebox.showinfo("Successo", f"File BAT convertito in EXE: {output_file}")
    except Exception as e:
        messagebox.showerror("Errore", f"Errore durante la conversione BAT to EXE: {e}")

def converti_exe_to_bat(percorso_file):
    try:
        nome_file = os.path.splitext(os.path.basename(percorso_file))[0]
        output_file = f"{nome_file}.bat"
        
        shutil.copy(percorso_file, output_file)
        
        messagebox.showinfo("Successo", f"File EXE copiato come BAT: {output_file}")
        messagebox.showwarning("Attenzione", "La conversione da EXE a BAT è una copia semplice. Il file BAT potrebbe non funzionare come previsto.")
    except Exception as e:
        messagebox.showerror("Errore", f"Errore durante la conversione EXE to BAT: {e}")

def converti_py_to_exe(percorso_file):
    try:
        nome_file = os.path.splitext(os.path.basename(percorso_file))[0]
        output_file = f"{nome_file}.exe"
        
        comando = f'pyinstaller --onefile "{percorso_file}"'
        subprocess.run(comando, shell=True, check=True)
        
        # Sposta il file EXE dalla cartella dist alla directory corrente
        shutil.move(os.path.join("dist", output_file), output_file)
        
        # Rimuovi le cartelle create da PyInstaller
        shutil.rmtree("build", ignore_errors=True)
        shutil.rmtree("dist", ignore_errors=True)
        os.remove(f"{nome_file}.spec")
        
        messagebox.showinfo("Successo", f"File Python convertito in EXE: {output_file}")
    except Exception as e:
        messagebox.showerror("Errore", f"Errore durante la conversione Python to EXE: {e}")

def rimuovi_sfondo(percorso_immagine):
    try:
        input_image = Image.open(percorso_immagine)
        output_image = remove(input_image)
        
        nome_file, estensione = os.path.splitext(percorso_immagine)
        nuovo_percorso = f"{nome_file}_senza_sfondo{estensione}"
        
        output_image.save(nuovo_percorso)
        messagebox.showinfo("Successo", f"Sfondo rimosso. Immagine salvata come {nuovo_percorso}")
    except Exception as e:
        messagebox.showerror("Errore", f"Errore durante la rimozione dello sfondo: {e}")

def main():
    print(f"Argomenti ricevuti: {sys.argv}")
    if len(sys.argv) < 2:
        messagebox.showerror("Errore", "Nessun file selezionato.")
        return
    
    percorso_file = sys.argv[1]
    print(f"Percorso file: {percorso_file}")
    
    root = tk.Tk()
    root.withdraw()
    
    scelta = messagebox.askquestion("Scegli l'operazione", 
                                    "Vuoi convertire il file o rimuovere lo sfondo?",
                                    icon='question',
                                    type='yesnocancel')
    
    if scelta == 'yes':
        converti_file(percorso_file)
    elif scelta == 'no':
        rimuovi_sfondo(percorso_file)
    else:
        messagebox.showinfo("Informazione", "Operazione annullata.")

if __name__ == "__main__":
    print("Script avviato")
    if len(sys.argv) == 1:
        aggiungi_al_menu_contestuale()
        messagebox.showinfo("Successo", "Menu contestuale aggiunto con successo.")
    else:
        main()

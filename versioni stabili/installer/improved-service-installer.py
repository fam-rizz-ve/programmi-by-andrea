import tkinter as tk
from tkinter import messagebox, ttk
import requests
import zipfile
import os

def is_zip_file(file_content):
    return file_content.startswith(b'PK\x03\x04')

def download_and_extract(url, filename, service_folder):
    try:
        response = requests.get(url, allow_redirects=True)
        response.raise_for_status()

        if not is_zip_file(response.content):
            raise ValueError("Il contenuto scaricato non è un file ZIP valido")

        with open(filename, 'wb') as file:
            file.write(response.content)

        extracted_folder = os.path.splitext(filename)[0]
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall(extracted_folder)

        os.remove(filename)

        service_specific_folder = os.path.join(extracted_folder, service_folder)

        if not os.path.exists(service_specific_folder):
            raise FileNotFoundError(f"La cartella {service_folder} non è stata trovata")

        bat_files = [f for f in os.listdir(service_specific_folder) if f.endswith('.bat')]
        if not bat_files:
            raise FileNotFoundError(f"Nessun file .bat trovato nella cartella {service_folder}")

        main_bat = os.path.join(service_specific_folder, bat_files[0])

        return f"File estratti con successo. Il file .bat principale si trova in: {main_bat}"

    except requests.RequestException as e:
        raise Exception(f"Errore durante il download: {str(e)}")
    except (zipfile.BadZipFile, ValueError) as e:
        raise Exception(f"Errore con il file ZIP: {str(e)}")
    except FileNotFoundError as e:
        raise Exception(f"Errore nel trovare il file o la cartella: {str(e)}")

def extract_selected():
    service_info = {
        "cleaner": {
            "url": "https://github.com/fam-rizz-ve/cleaner/archive/refs/heads/main.zip",
            "folder": "cleaner-main"
        },
        "spegnimento": {
            "url": "https://github.com/fam-rizz-ve/spegnimento/archive/refs/heads/main.zip",
            "folder": "spegnimento-main"
        },
        "BIOS": {
            "url": "https://github.com/fam-rizz-ve/BIOS/archive/refs/heads/main.zip",
            "folder": "BIOS-main"
        }
    }

    selected = [service for service, var in services.items() if var.get()]
    
    if selected:
        progress_window = tk.Toplevel(root)
        progress_window.title("Progresso Estrazione")
        progress_window.geometry("300x150")
        
        progress_label = ttk.Label(progress_window, text="Estrazione in corso...")
        progress_label.pack(pady=10)
        
        progress_bar = ttk.Progressbar(progress_window, length=250, mode='determinate')
        progress_bar.pack(pady=10)
        
        for i, service in enumerate(selected):
            url = service_info[service]["url"]
            folder = service_info[service]["folder"]
            filename = f"{service.lower().replace(' ', '_')}.zip"
            try:
                progress_label.config(text=f"Estrazione di {service}...")
                progress_bar['value'] = (i / len(selected)) * 100
                progress_window.update()
                
                result = download_and_extract(url, filename, folder)
                messagebox.showinfo("Successo", f"{service}: {result}")
            except Exception as e:
                messagebox.showerror("Errore", f"Errore durante l'estrazione di {service}: {str(e)}")
            
            progress_bar['value'] = ((i + 1) / len(selected)) * 100
            progress_window.update()
        
        progress_window.destroy()
        messagebox.showinfo("Completato", "Estrazione dei servizi selezionati completata!")
        root.quit()  # Chiude l'applicazione
    else:
        messagebox.showwarning("Attenzione", "Nessun servizio selezionato!")

# Crea la finestra principale dell'applicazione
root = tk.Tk()
root.title("Estrazione Servizi")
root.geometry("400x350")  # Finestra più larga
root.configure(bg='#f0f0f0')  # Sfondo grigio chiaro

# Stile per i widget
style = ttk.Style()
style.theme_use('clam')
style.configure('TLabel', background='#f0f0f0', font=('Helvetica', 12))
style.configure('TButton', font=('Helvetica', 11, 'bold'))

# Personalizza lo stile delle checkbox
style.configure('Transparent.TCheckbutton', 
                background='#f0f0f0',  # Stesso colore dello sfondo
                foreground='black',
                font=('Helvetica', 11))
style.map('Transparent.TCheckbutton',
          background=[('active', '#f0f0f0')],  # Rimuove l'effetto hover
          highlightcolor=[('focus', '#f0f0f0')],  # Rimuove il riquadro di focus
          highlightbackground=[('focus', '#f0f0f0')])  # Rimuove il riquadro di focus

# Crea e posiziona l'etichetta principale
label = ttk.Label(root, text="Seleziona i servizi da estrarre:", style='TLabel')
label.pack(pady=20)

# Frame per contenere le checkbox
checkbox_frame = ttk.Frame(root, style='TFrame')
checkbox_frame.pack(fill='x', padx=30)

# Lista dei servizi disponibili
service_list = ["cleaner", "spegnimento", "BIOS"]

# Crea le checkbox per ogni servizio
services = {}
for service in service_list:
    var = tk.BooleanVar()
    cb = ttk.Checkbutton(checkbox_frame, text=service, variable=var, style='Transparent.TCheckbutton')
    cb.pack(anchor="w", pady=5)
    services[service] = var

# Crea e posiziona il pulsante per l'estrazione
extract_button = ttk.Button(root, text="Estrai i selezionati", command=extract_selected, style='TButton')
extract_button.pack(pady=30)

# Avvia il loop principale dell'interfaccia grafica
root.mainloop()

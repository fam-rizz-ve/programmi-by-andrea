import tkinter as tk
from tkinter import messagebox
import requests
import zipfile
import os
import subprocess

def download_and_run(url, filename):
    # Scarica il file dall'URL specificato
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)
    
    # Decomprime il file ZIP scaricato
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall('.')
    
    # Rimuove il file ZIP dopo l'estrazione
    os.remove(filename)
    
    # Avvia il file Python estratto (assumendo che abbia lo stesso nome del file ZIP)
    subprocess.run(['python', filename.replace('.zip', '.py')])

def install_selected():
    # Crea una lista dei servizi selezionati
    selected = [service for service, var in services.items() if var.get()]
    
    if selected:
        # Mostra un messaggio con i servizi selezionati
        messagebox.showinfo("Download", f"Scaricamento e installazione di: {', '.join(selected)}")
        
        # URL del repository GitHub da cui scaricare i file (da modificare con l'URL effettivo)
        url = "https://github.com/tuouser/tuorepository/archive/main.zip"
        
        # Avvia il processo di download e installazione
        download_and_run(url, "servizi.zip")
    else:
        # Avvisa l'utente se nessun servizio è stato selezionato
        messagebox.showwarning("Attenzione", "Nessun servizio selezionato!")

# Crea la finestra principale dell'applicazione
root = tk.Tk()
root.title("Selezione Servizi")

# Crea e posiziona l'etichetta principale
label = tk.Label(root, text="Quali dei nostri servizi vuole visualizzare?")
label.pack(pady=10)

# Lista dei servizi disponibili (modificabile secondo necessità)
service_list = ["Servizio 1", "Servizio 2", "Servizio 3", "Servizio 4"]

# Crea le checkbox per ogni servizio
services = {}
for service in service_list:
    var = tk.BooleanVar()
    cb = tk.Checkbutton(root, text=service, variable=var)
    cb.pack(anchor="w", padx=20)
    services[service] = var

# Crea e posiziona il pulsante per l'installazione
install_button = tk.Button(root, text="Installa i selezionati", command=install_selected)
install_button.pack(pady=20)

# Avvia il loop principale dell'interfaccia grafica
root.mainloop()

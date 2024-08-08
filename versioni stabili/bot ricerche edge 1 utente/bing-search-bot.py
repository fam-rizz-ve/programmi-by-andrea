import subprocess
import sys
import os
import traceback
import time

def install_dependencies():
    print("Installazione delle dipendenze...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium", "webdriver_manager"])
        print("Dipendenze installate con successo.")
    except subprocess.CalledProcessError:
        print("Errore durante l'installazione delle dipendenze.")
        sys.exit(1)

def get_edge_driver(attempts=3):
    from selenium import webdriver
    from selenium.webdriver.edge.service import Service
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    from selenium.common.exceptions import SessionNotCreatedException

    for attempt in range(attempts):
        try:
            service = Service(EdgeChromiumDriverManager().install())
            options = webdriver.EdgeOptions()
            
            # Usa il profilo principale di Edge
            user_data_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'Microsoft', 'Edge', 'User Data')
            options.add_argument(f"user-data-dir={user_data_dir}")
            
            # Aggiungi queste opzioni per migliorare la stabilità
            options.add_argument("--no-first-run")
            options.add_argument("--no-default-browser-check")
            options.add_argument("--start-maximized")
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            
            # Aggiungi questa opzione per evitare problemi di compatibilità
            options.add_argument("--ignore-certificate-errors")
            
            # Prova ad avviare Edge in modalità headless
            if attempt > 0:
                print(f"Tentativo {attempt + 1}: Avvio di Edge in modalità headless...")
                options.add_argument("--headless")

            driver = webdriver.Edge(service=service, options=options)
            print("Driver Edge inizializzato con successo.")
            return driver
        except SessionNotCreatedException as e:
            print(f"Errore durante l'inizializzazione del driver Edge (tentativo {attempt + 1}):")
            print(str(e))
            if attempt < attempts - 1:
                print("Riprovo tra 5 secondi...")
                time.sleep(5)
            else:
                print("Impossibile inizializzare il driver Edge dopo multipli tentativi.")
                print("Per favore, prova le seguenti soluzioni:")
                print("1. Chiudi tutte le istanze di Microsoft Edge e riprova.")
                print("2. Aggiorna Microsoft Edge all'ultima versione.")
                print("3. Verifica che non ci siano processi di Edge in esecuzione nel Task Manager.")
                print("4. Riavvia il computer e riprova.")
                print("Stack trace completo:")
                traceback.print_exc()
                sys.exit(1)
        except Exception as e:
            print(f"Errore imprevisto durante l'inizializzazione del driver Edge: {str(e)}")
            print("Stack trace completo:")
            traceback.print_exc()
            sys.exit(1)

def bing_search_bot():
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys
    import random
    import string

    driver = get_edge_driver()

    try:
        for i in range(30):  # Ripeti il processo 30 volte
            search_letter = random.choice(string.ascii_lowercase)
            driver.get("https://www.bing.com")
            
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            search_box.send_keys(search_letter)

            # Attendi che appaiano i suggerimenti
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ul.sa_drw li"))
            )

            # Ottieni tutti i suggerimenti
            suggestions = driver.find_elements(By.CSS_SELECTOR, "ul.sa_drw li")

            if suggestions:
                random_suggestion = random.choice(suggestions)
                print(f"Iterazione {i+1}:")
                print(f"Lettera cercata: {search_letter}")
                print(f"Suggerimento selezionato: {random_suggestion.text}")
                random_suggestion.click()
            else:
                print(f"Iterazione {i+1}:")
                print(f"Nessun suggerimento trovato per la lettera: {search_letter}")
                search_box.send_keys(Keys.RETURN)

            time.sleep(3)
            print(f"Titolo della pagina dei risultati: {driver.title}")
            print("-" * 50)

    except Exception as e:
        print(f"Si è verificato un errore durante l'esecuzione del bot: {str(e)}")
        print("Stack trace completo:")
        traceback.print_exc()
    finally:
        driver.quit()

if __name__ == "__main__":
    print("ATTENZIONE: Questo script utilizzerà il tuo profilo principale di Edge.")
    print("Ciò potrebbe influenzare le tue impostazioni personali e la cronologia di navigazione.")
    print("Lo script verrà eseguito automaticamente senza richiedere ulteriori conferme.")
    
    install_dependencies()
    bing_search_bot()

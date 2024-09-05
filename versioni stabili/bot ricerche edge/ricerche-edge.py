import subprocess
import sys
import os
import traceback
import time
import random
import string
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, WebDriverException

def install_dependencies():
    print("Installazione delle dipendenze...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium", "webdriver_manager"])
        print("Dipendenze installate con successo.")
    except subprocess.CalledProcessError:
        print("Errore durante l'installazione delle dipendenze.")
        sys.exit(1)

def get_edge_driver(attempts=3):
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
            options.add_argument("--ignore-certificate-errors")
            
            # Prova ad avviare Edge in modalità headless negli ultimi tentativi
            if attempt > 0:
                print(f"Tentativo {attempt + 1}: Avvio di Edge in modalità headless...")
                options.add_argument("--headless")

            driver = webdriver.Edge(service=service, options=options)
            print("Driver Edge inizializzato con successo.")
            return driver
        except Exception as e:
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

def wait_for_element(driver, by, value, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    except TimeoutException:
        return None

def bing_search_bot():
    driver = get_edge_driver()
    successful_searches = 0

    try:
        while successful_searches < 30:
            try:
                search_letter = random.choice(string.ascii_lowercase)
                driver.get("https://www.bing.com")
                
                search_box = wait_for_element(driver, By.NAME, "q")
                if not search_box:
                    print("Impossibile trovare la casella di ricerca. Riprovo.")
                    continue

                search_box.send_keys(search_letter)
                time.sleep(2)  # Attesa aggiuntiva per assicurarsi che i suggerimenti siano caricati

                # Attendi che appaiano i suggerimenti
                suggestions = wait_for_element(driver, By.CSS_SELECTOR, "ul.sa_drw li", timeout=5)

                if suggestions:
                    suggestions = driver.find_elements(By.CSS_SELECTOR, "ul.sa_drw li")
                    for suggestion in suggestions:
                        # Controlla se il suggerimento ha una descrizione sotto
                        if suggestion.find_elements(By.CSS_SELECTOR, "div.b_secondaryLabel"):
                            print(f"Ricerca {successful_searches + 1}:")
                            print(f"Lettera cercata: {search_letter}")
                            print(f"Suggerimento selezionato: {suggestion.text}")
                            suggestion.click()
                            break
                    else:
                        print(f"Ricerca {successful_searches + 1}: Nessun suggerimento con descrizione trovato per la lettera: {search_letter}")
                        search_box.send_keys(Keys.RETURN)
                else:
                    print(f"Ricerca {successful_searches + 1}: Nessun suggerimento trovato per la lettera: {search_letter}")
                    search_box.send_keys(Keys.RETURN)

                # Attendi il caricamento della pagina dei risultati
                wait_for_element(driver, By.ID, "b_results")
                
                print(f"Titolo della pagina dei risultati: {driver.title}")
                successful_searches += 1
            except WebDriverException as e:
                print(f"Errore WebDriver: {str(e)}")
                print("Riavvio il driver...")
                driver.quit()
                driver = get_edge_driver()
            except Exception as e:
                print(f"Errore imprevisto: {str(e)}")
                print("Stack trace:")
                traceback.print_exc()
            finally:
                print("Attendo 10 secondi prima della prossima ricerca...")
                print("-" * 50)
                time.sleep(10)

    except Exception as e:
        print(f"Si è verificato un errore durante l'esecuzione del bot: {str(e)}")
        print("Stack trace completo:")
        traceback.print_exc()
    finally:
        driver.quit()

if __name__ == "__main__":
    print("ATTENZIONE: Questo script utilizzerà il tuo profilo principale di Edge.")
    print("Ciò potrebbe influenzare le tue impostazioni personali e la cronologia di navigazione.")
    print("Lo script eseguirà esattamente 30 ricerche riuscite, attendendo 10 secondi tra ogni ricerca.")
    print("Lo script verrà eseguito automaticamente senza richiedere ulteriori conferme.")
    
    install_dependencies()
    bing_search_bot()
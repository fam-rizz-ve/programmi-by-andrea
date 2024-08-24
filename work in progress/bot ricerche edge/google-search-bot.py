import subprocess
import sys
import random
import string
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, ElementNotInteractableException

def install_dependencies():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium"])

def get_edge_driver():
    options = Options()
    options.use_chromium = True
    service = Service()
    return webdriver.Edge(service=service, options=options)

def bing_search_bot():
    driver = get_edge_driver()
    try:
        for i in range(30):  # Ripeti il processo 30 volte
            search_letter = random.choice(string.ascii_lowercase)
            driver.get("https://www.bing.com")
            
            try:
                search_box = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "sb_form_q"))
                )
                search_box.clear()
                search_box.send_keys(search_letter)
                
                suggestions = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.sa_sg"))
                )
                
                if suggestions:
                    for _ in range(3):  # Tenta fino a 3 volte
                        try:
                            random_suggestion = random.choice(suggestions)
                            print(f"Iterazione {i+1}:")
                            print(f"Lettera cercata: {search_letter}")
                            print(f"Suggerimento selezionato: {random_suggestion.text}")
                            random_suggestion.click()
                            break
                        except (ElementClickInterceptedException, ElementNotInteractableException):
                            print("Tentativo di click fallito, riprovo...")
                            time.sleep(1)
                    else:
                        print("Non è stato possibile cliccare sul suggerimento dopo 3 tentativi.")
                        continue
                else:
                    print(f"Iterazione {i+1}:")
                    print(f"Nessun suggerimento trovato per la lettera: {search_letter}")
                    search_box.submit()  # Invia la ricerca se non ci sono suggerimenti
                
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "b_results"))
                )
                print(f"Titolo della pagina dei risultati: {driver.title}")
                print("-" * 50)
            except TimeoutException:
                print(f"Timeout durante l'iterazione {i+1}. Passo alla successiva.")
            except Exception as e:
                print(f"Si è verificato un errore durante l'iterazione {i+1}: {str(e)}")
            
            time.sleep(20)
    except Exception as e:
        print(f"Si è verificato un errore generale: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    print("Installazione delle dipendenze...")
    install_dependencies()
    
    print("Avvio del bot di ricerca Bing...")
    bing_search_bot()

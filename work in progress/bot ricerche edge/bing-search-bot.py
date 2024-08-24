import os
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
import random
import string

# Lista degli account Microsoft
MICROSOFT_ACCOUNTS = [
    {"email": "igor_76@hotmail.it", "password": "dfpbvn01"},
    {"email": "fam.rizz.ve@gmail.com", "password": "dfpbvn01"},
    {"email": "techitplay@gmail.com", "password": "dfpbvn01"},
    # Aggiungi altri account secondo necessità
]

last_used_account_index = 0

def get_edge_driver():
    service = Service(EdgeChromiumDriverManager().install())
    options = webdriver.EdgeOptions()
    
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Usa un profilo temporaneo per ogni sessione
    temp_profile = os.path.join(os.getcwd(), f"edge_temp_profile_{random.randint(1000, 9999)}")
    options.add_argument(f"--user-data-dir={temp_profile}")

    driver = webdriver.Edge(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def wait_for_element(driver, by, value, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    except TimeoutException:
        return None

def is_logged_in(driver):
    driver.get("https://www.bing.com")
    time.sleep(random.uniform(3, 5))  # Attesa randomizzata
    try:
        # Cerca un elemento che indica che l'utente è loggato
        profile_element = driver.find_element(By.ID, "id_n")  # Modifica questo ID se necessario
        return True
    except NoSuchElementException:
        return False

def login_to_microsoft_account(driver, email, password):
    if is_logged_in(driver):
        print(f"Già loggato con un account. Tentativo di logout...")
        logout(driver)

    driver.get("https://login.live.com/")
    time.sleep(random.uniform(3, 5))  # Attesa randomizzata
    
    # Inserisci email
    email_input = wait_for_element(driver, By.NAME, "loginfmt")
    if email_input:
        email_input.clear()
        email_input.send_keys(email)
        email_input.send_keys(Keys.RETURN)
        time.sleep(random.uniform(2, 4))
    else:
        print("Elemento email non trovato. Verifica la pagina di login.")
        return False
    
    # Inserisci password
    password_input = wait_for_element(driver, By.NAME, "passwd")
    if password_input:
        password_input.clear()
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        time.sleep(random.uniform(2, 4))
    else:
        print("Elemento password non trovato. Possibile errore nel login.")
        return False
    
    # Gestisci eventuali richieste di "Resta connesso"
    stay_signed_in = wait_for_element(driver, By.ID, "idSIButton9")
    if stay_signed_in:
        stay_signed_in.click()
        time.sleep(random.uniform(2, 4))

    # Verifica se il login è avvenuto con successo
    if is_logged_in(driver):
        print("Login completato con successo.")
        return True
    else:
        print("Login non riuscito. Verifica le credenziali e lo stato della pagina.")
        return False

def logout(driver):
    driver.delete_all_cookies()
    driver.get("https://www.bing.com")
    time.sleep(random.uniform(3, 5))
    print("Cookies cancellati e pagina ricaricata.")

def bing_search_bot(account):
    driver = get_edge_driver()
    
    try:
        for attempt in range(3):  # Prova il login fino a 3 volte
            if login_to_microsoft_account(driver, account["email"], account["password"]):
                break
            else:
                print(f"Tentativo di login {attempt+1} fallito. Riprovo...")
                time.sleep(random.uniform(5, 10))
        else:
            print(f"Impossibile effettuare il login per l'account {account['email']} dopo 3 tentativi. Passaggio al successivo.")
            return

        successful_searches = 0
        while successful_searches < 30:
            try:
                search_letter = random.choice(string.ascii_lowercase)
                driver.get("https://www.bing.com")
                time.sleep(random.uniform(2, 4))
                
                search_box = wait_for_element(driver, By.NAME, "q")
                if not search_box:
                    continue

                search_box.send_keys(search_letter)
                time.sleep(random.uniform(1, 2))

                suggestions = wait_for_element(driver, By.CSS_SELECTOR, "ul.sa_drw li", timeout=5)

                if suggestions:
                    suggestions = driver.find_elements(By.CSS_SELECTOR, "ul.sa_drw li")
                    random_suggestion = random.choice(suggestions)
                    random_suggestion.click()
                else:
                    search_box.send_keys(Keys.RETURN)

                wait_for_element(driver, By.ID, "b_results")
                
                successful_searches += 1
                print(f"Account: {account['email']} - Ricerca completata: {successful_searches}/30")
            except WebDriverException as e:
                print(f"Errore WebDriver: {str(e)}")
                driver.quit()
                driver = get_edge_driver()
                if not login_to_microsoft_account(driver, account["email"], account["password"]):
                    print(f"Impossibile rieffettuare il login per l'account {account['email']}. Terminazione.")
                    return
            except Exception as e:
                print(f"Errore durante la ricerca: {str(e)}")
            finally:
                time.sleep(random.uniform(8, 12))

    except Exception as e:
        print(f"Errore generale per l'account {account['email']}: {str(e)}")
    finally:
        logout(driver)
        driver.quit()

if __name__ == "__main__":
    for i, account in enumerate(MICROSOFT_ACCOUNTS):
        print(f"Avvio delle ricerche per l'account: {account['email']}")
        bing_search_bot(account)
        print(f"Completate le ricerche per l'account: {account['email']}")
        time.sleep(random.uniform(25, 35))
        last_used_account_index = i

    print("Tutte le ricerche sono state completate per tutti gli account.")

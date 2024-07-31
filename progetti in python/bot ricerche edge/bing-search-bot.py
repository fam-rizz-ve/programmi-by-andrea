import os
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, WebDriverException
import random
import string

# Lista degli utenti predefiniti
PREDEFINED_USERS = [
    {"email": "igor_76@hotmail.it", "password": "dfpbvn01"},
    {"email": "fam.rizz.ve@gmail.com", "password": "dfpbvn01"},
    {"email": "techitplay@gmail.com", "password": "dfpbvn01"},
    # Aggiungi altri utenti secondo necessità
]

# Lista dei profili Edge
EDGE_PROFILES = ["igor", "fam.rizz", "techitplay"]  # Aggiungi o rimuovi profili secondo necessità

def get_edge_driver(profile):
    service = Service(EdgeChromiumDriverManager().install())
    options = webdriver.EdgeOptions()
    
    user_data_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'Microsoft', 'Edge', 'User Data', profile)
    options.add_argument(f"user-data-dir={user_data_dir}")
    
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("user-data-dir=" + user_data_dir)
    options.add_argument("--profile-directory=" + profile)

    driver = webdriver.Edge(service=service, options=options)
    return driver

def wait_for_element(driver, by, value, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    except TimeoutException:
        return None

def login_to_microsoft_account(driver, email, password):
    driver.get("https://login.live.com/")
    
    # Inserisci email
    email_input = wait_for_element(driver, By.NAME, "loginfmt")
    if email_input:
        email_input.send_keys(email)
        email_input.send_keys(Keys.RETURN)
        time.sleep(2)
    
    # Inserisci password
    password_input = wait_for_element(driver, By.NAME, "passwd")
    if password_input:
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        time.sleep(2)
    
    # Gestisci eventuali richieste di "Resta connesso"
    stay_signed_in = wait_for_element(driver, By.ID, "idSIButton9")
    if stay_signed_in:
        stay_signed_in.click()

def bing_search_bot(user, profile):
    driver = get_edge_driver(profile)
    
    try:
        login_to_microsoft_account(driver, user["email"], user["password"])
        
        successful_searches = 0
        while successful_searches < 30:
            try:
                search_letter = random.choice(string.ascii_lowercase)
                driver.get("https://www.bing.com")
                
                search_box = wait_for_element(driver, By.NAME, "q")
                if not search_box:
                    continue

                search_box.send_keys(search_letter)

                suggestions = wait_for_element(driver, By.CSS_SELECTOR, "ul.sa_drw li", timeout=5)

                if suggestions:
                    suggestions = driver.find_elements(By.CSS_SELECTOR, "ul.sa_drw li")
                    random_suggestion = random.choice(suggestions)
                    random_suggestion.click()
                else:
                    search_box.send_keys(Keys.RETURN)

                wait_for_element(driver, By.ID, "b_results")
                
                successful_searches += 1
            except WebDriverException:
                driver.quit()
                driver = get_edge_driver(profile)
                login_to_microsoft_account(driver, user["email"], user["password"])
            except Exception:
                pass
            finally:
                time.sleep(random.uniform(8, 12))

    except Exception:
        pass
    finally:
        driver.quit()

if __name__ == "__main__":
    for user, profile in zip(PREDEFINED_USERS, EDGE_PROFILES):
        print(f"Avvio delle ricerche per l'utente: {user['email']} con il profilo: {profile}")
        bing_search_bot(user, profile)
        time.sleep(random.uniform(25, 35))

    print("Tutte le ricerche sono state completate per tutti gli utenti predefiniti.")

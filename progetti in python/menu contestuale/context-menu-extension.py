import winreg
import os
import sys
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def add_context_menu_option(file_type, menu_name, batch_path):
    key_path = f"{file_type}\\shell\\{menu_name}"
    
    try:
        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_path)
        winreg.SetValue(key, "", winreg.REG_SZ, menu_name)
        
        command_key = winreg.CreateKey(key, "command")
        command = f'cmd /k "\"{batch_path}\" \"%1\""'
        winreg.SetValue(command_key, "", winreg.REG_SZ, command)
        
        print(f"Aggiunta l'opzione '{menu_name}' al menu contestuale per {file_type}")
        print(f"Comando registrato: {command}")
        return True
    except Exception as e:
        print(f"Errore nell'aggiunta dell'opzione al menu: {str(e)}")
        return False

def create_batch_file(script_name, batch_name, script_dir):
    batch_path = os.path.join(script_dir, batch_name)
    script_path = os.path.join(script_dir, script_name)
    
    if not os.path.exists(script_path):
        print(f"ERRORE: Il file {script_name} non esiste in {script_dir}")
        return None
    
    with open(batch_path, "w") as f:
        f.write('@echo on\n')
        f.write('setlocal enabledelayedexpansion\n')
        f.write(f'echo Esecuzione di {script_name}...\n')
        f.write('echo Directory corrente: %cd%\n')
        f.write(f'echo Percorso completo dello script: "%~dp0{script_name}"\n')
        f.write('echo File di input: "%~1"\n')
        f.write(f'python "%~dp0{script_name}" "%~1"\n')
        f.write('if %errorlevel% neq 0 (\n')
        f.write('    echo Si è verificato un errore durante l\'esecuzione dello script.\n')
        f.write('    pause\n')
        f.write('    exit /b %errorlevel%\n')
        f.write(')\n')
        f.write('echo Esecuzione completata con successo.\n')
        f.write('pause\n')
    
    print(f"File batch creato: {batch_path}")
    return batch_path

def remove_existing_keys():
    try:
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r"*\shell\Converti formato\command")
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r"*\shell\Converti formato")
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r"*\shell\Rimuovi sfondo\command")
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r"*\shell\Rimuovi sfondo")
        print("Chiavi del registro esistenti rimosse con successo.")
    except WindowsError:
        # Le chiavi potrebbero non esistere, quindi ignoriamo l'errore
        pass

def main():
    if not is_admin():
        print("Riavvio con privilegi di amministratore...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        return

    print("Esecuzione con privilegi di amministratore.")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Directory dello script: {script_dir}")
    
    remove_existing_keys()
    
    convert_batch = create_batch_file("convert_script.py", "run_convert.bat", script_dir)
    remove_bg_batch = create_batch_file("remove_background_script.py", "run_remove_bg.bat", script_dir)

    if convert_batch and remove_bg_batch:
        success_convert = add_context_menu_option("*", "Converti formato", convert_batch)
        success_remove_bg = add_context_menu_option("*", "Rimuovi sfondo", remove_bg_batch)
        
        if success_convert and success_remove_bg:
            print("Voci del menu contestuale create con successo.")
        else:
            print("Si sono verificati errori durante la creazione delle voci del menu contestuale.")
    else:
        print("Impossibile creare le voci del menu contestuale a causa di errori nei file script.")

    print("\nVerifica delle chiavi del registro create:")
    try:
        key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r"*\shell\Converti formato\command", 0, winreg.KEY_READ)
        value, _ = winreg.QueryValueEx(key, "")
        print(f"Comando 'Converti formato': {value}")
        winreg.CloseKey(key)

        key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r"*\shell\Rimuovi sfondo\command", 0, winreg.KEY_READ)
        value, _ = winreg.QueryValueEx(key, "")
        print(f"Comando 'Rimuovi sfondo': {value}")
        winreg.CloseKey(key)
    except WindowsError as e:
        print(f"Errore nella verifica delle chiavi del registro: {str(e)}")

    input("Premi Invio per chiudere...")

if __name__ == "__main__":
    main()

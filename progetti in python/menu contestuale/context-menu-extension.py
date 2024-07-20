import winreg
import os
import sys
import ctypes
import subprocess

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def install_dependencies():
    dependencies = ['Pillow', 'numpy', 'rembg']
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"{dep} è già installato.")
        except ImportError:
            print(f"Installazione di {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])

def add_context_menu_option(file_type, menu_name, command, icon_path=None):
    key_path = f"{file_type}\\shell\\{menu_name}"
    
    try:
        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_path)
        winreg.SetValue(key, "", winreg.REG_SZ, menu_name)
        
        if icon_path:
            winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, icon_path)
        
        command_key = winreg.CreateKey(key, "command")
        winreg.SetValue(command_key, "", winreg.REG_SZ, command)
        
        print(f"Aggiunta l'opzione '{menu_name}' al menu contestuale per {file_type}")
    except Exception as e:
        print(f"Errore nell'aggiunta dell'opzione al menu: {str(e)}")

def create_batch_file(script_name, batch_name, script_dir):
    batch_path = os.path.join(script_dir, batch_name)
    python_path = sys.executable

    with open(batch_path, "w", encoding="utf-8") as f:
        f.write('@echo off\n')
        f.write('cd /d "%~dp0"\n')
        f.write(f'echo Installazione delle dipendenze...\n')
        f.write(f'"{python_path}" -c "import sys; sys.path.append(r\'{script_dir}\'); from context_menu_extension import install_dependencies; install_dependencies()"\n')
        f.write(f'echo Esecuzione di {script_name}...\n')
        f.write(f'"{python_path}" "{script_name}" %*\n')
        f.write('if errorlevel 1 (\n')
        f.write('    echo Si è verificato un errore durante l\'esecuzione dello script.\n')
        f.write('    pause\n')
        f.write('    exit /b 1\n')
        f.write(')\n')
        f.write('echo Esecuzione completata con successo.\n')
        f.write('pause\n')
    
    return batch_path

def main():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        return

    print("Verifica e installazione delle dipendenze...")
    install_dependencies()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    context_menu_batch = create_batch_file("context-menu-extension.py", "run_context_menu_extension.bat", script_dir)
    remove_bg_batch = create_batch_file("remove_background_script.py", "run_remove_bg.bat", script_dir)

    if context_menu_batch and remove_bg_batch:
        context_menu_command = f'"{context_menu_batch}" "%1"'
        add_context_menu_option("*", "Aggiungi al menu contestuale", context_menu_command)
        
        remove_bg_command = f'"{remove_bg_batch}" "%1"'
        add_context_menu_option("*", "Rimuovi sfondo", remove_bg_command)
        
        print("Installazione completata con successo.")
        print("Le nuove opzioni sono state aggiunte al menu contestuale.")
    else:
        print("Impossibile creare le voci del menu contestuale a causa di errori nei file script.")

    input("Premi Invio per chiudere questa finestra...")

if __name__ == "__main__":
    main()

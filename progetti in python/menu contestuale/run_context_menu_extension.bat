@echo off
cd /d "%~dp0"
echo Installazione delle dipendenze...
"C:\Users\Andrea\scoop\apps\python\current\python.exe" -c "import sys; sys.path.append('C:\Users\Andrea\Documents\GitHub\programmi-by-andrea\progetti in python\menu contestuale'); from context_menu_extension import install_dependencies; install_dependencies()"
echo Esecuzione di context-menu-extension.py...
"C:\Users\Andrea\scoop\apps\python\current\python.exe" "context-menu-extension.py" %*
if errorlevel 1 (
    echo Si è verificato un errore durante l'esecuzione dello script.
    pause
    exit /b 1
)
echo Esecuzione completata con successo.
pause

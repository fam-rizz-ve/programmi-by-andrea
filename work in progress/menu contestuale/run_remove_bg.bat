@echo on
setlocal enabledelayedexpansion
echo Esecuzione di remove_background_script.py...
echo Directory corrente: %cd%
echo Percorso completo dello script: "%~dp0remove_background_script.py"
echo File di input: "%~1"
python "%~dp0remove_background_script.py" "%~1"
if %errorlevel% neq 0 (
    echo Si è verificato un errore durante l'esecuzione dello script.
    pause
    exit /b %errorlevel%
)
echo Esecuzione completata con successo.
pause

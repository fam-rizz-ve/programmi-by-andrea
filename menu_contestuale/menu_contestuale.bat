@echo off
cd /d "%~dp0"

REM Verifica se lo script è già in esecuzione come amministratore
net session >nul 2>&1
if %errorLevel% == 0 (
    goto :admin
) else (
    goto :elevatepermissions
)

:elevatepermissions
REM Riavvia lo script come amministratore
powershell -Command "Start-Process cmd -ArgumentList '/c %~dpnx0' -Verb RunAs"
exit /b

:admin
REM Questa parte verrà eseguita solo quando lo script è in esecuzione come amministratore
if not exist requirements.txt (
    echo File requirements.txt non trovato.
    pause
    exit /b
)

pip install -r requirements.txt

if not exist main.py (
    echo File main.py non trovato.
    pause
    exit /b
)

echo Argomenti passati a Python: %*
python main.py %*

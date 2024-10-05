@echo off
:inizio
start manutentores.bat
:controlla
tasklist | find /i "manutentores.bat" > nul
if errorlevel 1 goto inizio
goto controlla
@echo off
NET FILE 1>NUL 2>NUL
if '%errorlevel%' == '0' ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    set params = %*:"=""
    echo UAC.ShellExecute "cmd.exe", "/c %~s0 %params%", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    pushd "%CD%"
    CD /D "%~dp0"

:: Il tuo codice principale inizia qui
echo Esecuzione con privilegi di amministratore
title manutenzione
echo desidera svuotare il cestino?
choice /c SNC /m "vuoi procedere? clicca: S per accettare; N per saltare; C per continuare in autonomia"
if errorlevel ==3 (goto :tutto_dritto)
if errorlevel ==2 (goto :svuota_cache_domanda)
:svuota_cestino
PowerShell -NoProfile -Command "Clear-RecycleBin -Force"
:svuota_cache_domanda
cls
echo desidera eliminare i file temporanei?
choice /c SNC /m "vuoi procedere? clicca: S per accettare; N per saltare; C per continuare in autonomia"
if errorlevel ==3 (goto tutto_dritto)
if errorlevel ==2 (goto domanda_aggionamenti)
:svuotamento_cache
del /q/f/s %TEMP%\
:domanda_aggionamenti
cls
echo vuoi aggiornare tutte le applicazioni?
choice /c SNC /m "vuoi procedere? clicca: S per accettare; N per saltare; C per continuare in autonomia"
if errorlevel ==3 (goto tutto_dritto)
if errorlevel ==2 (goto fine)
:aggiornamento_applicazioni
cls
winget upgrade --all
:tutto_dritto
PowerShell -NoProfile -Command "Clear-RecycleBin -Force"
del /q/f/s %TEMP%\
winget upgrade --all --accept-package-agreements --accept-source-agreements --uninstall-previous
:fine
cls
echo grazie per aver usufruito del nostro servizio
pause
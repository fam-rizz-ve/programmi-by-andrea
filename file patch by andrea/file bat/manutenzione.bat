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
if errorlevel ==2 (goto domanda_file_non_necessari)
:svuotamento_cache
del /q/f/s %TEMP%\*
:domanda_file_non_necessari
cls
echo desidera eliminare i file temporanei?
choice /c SNC /m "vuoi procedere? clicca: S per accettare; N per saltare; C per continuare in autonomia"
if errorlevel ==3 (goto tutto_dritto)
if errorlevel ==2 (goto domanda_aggionamenti)
:eliminazione_file_NON_NECESSARI
cleanmgr /sagerun:1
:domanda_aggionamenti
cls
echo vuoi aggiornare tutte le applicazioni?
choice /c SNC /m "vuoi procedere? clicca: S per accettare; N per saltare; C per continuare in autonomia"
if errorlevel ==3 (goto tutto_dritto)
if errorlevel ==2 (goto domanda_controllo_integrità)
:aggiornamento_applicazioni
cls
winget upgrade --all --accept-package-agreements --accept-source-agreements
:domanda_controllo_integrità
cls
echo vuoi fare un controllo integrità?
choice /c SNC /m "vuoi procedere? clicca: S per accettare; N per saltare; C per continuare in autonomia"
if errorlevel ==3 (goto tutto_dritto)
if errorlevel ==2 (goto domanda_aggiornamenti_windows)
:controllo_integrità
cls
dism /online /cleanup-image /restorehealth
sfc /scannow
:domanda_aggiornamenti_windows
cls
echo vuoi aggiornare windows?
choice /c SNC /m "vuoi procedere? clicca: S per accettare; N per saltare; C per continuare in autonomia"
if errorlevel ==3 (goto tutto_dritto)
if errorlevel ==2 (goto domanda_controllo_on_windows_defender)
:aggiornamento_windows
wuauclt /detectnow /updatenow
:domanda_controllo_on_windows_defender
cls
echo usare windows defender per scovare eventuLI Malware?
choice /c SNC /m "vuoi procedere? clicca: S per accettare; N per saltare; C per continuare in autonomia"
if errorlevel ==3 (goto tutto_dritto)
if errorlevel ==2 (goto fine)
:scannerizzazione_dispositivo
"%ProgramFiles%\Windows Defender\MpCmdRun.exe" -SignatureUpdate
"%ProgramFiles%\Windows Defender\MpCmdRun.exe" -Scan -ScanType 1
:tutto_dritto
PowerShell -NoProfile -Command "Clear-RecycleBin -Force"
del /q/f/s %TEMP%\
cleanmgr /sagerun:1
winget upgrade --all --accept-package-agreements --accept-source-agreements
dism /online /cleanup-image /restorehealth
sfc /scannow
wuauclt /detectnow /updatenow
"%ProgramFiles%\Windows Defender\MpCmdRun.exe" -SignatureUpdate
"%ProgramFiles%\Windows Defender\MpCmdRun.exe" -Scan -ScanType 1
:fine
cls
echo grazie per aver usufruito del nostro servizio
pause
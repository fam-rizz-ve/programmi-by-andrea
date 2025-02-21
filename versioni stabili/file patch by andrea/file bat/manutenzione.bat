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
title manutenzione
if not exist %USERPROFILE%\accettato_termini_e_condizioni.txt (
	echo ============================================================
	echo                TERMINI E CONDIZIONI D'USO
	echo ============================================================
	echo.
	echo Leggere attentamente prima di utilizzare questo script:
	echo.
	echo 1. Questo script eseguirà le seguenti operazioni:
	echo    - Svuotamento del Cestino
	echo    - Eliminazione di file temporanei e non necessari
	echo    - Aggiornamento delle applicazioni e di Windows
	echo    - Controllo dell'integrità dei file di sistema
	echo.
	echo 2. L'utente si assume la piena responsabilità per l'utilizzo
	echo    di questo script e per eventuali danni che potrebbero
	echo    derivare dal suo uso.
	echo.
	echo 3. Si consiglia vivamente di eseguire un backup dei dati
	echo    importanti prima di procedere.
	echo.
	echo 4. Questo script richiede privilegi di amministratore per
	echo    funzionare correttamente.
	echo.
	echo 5. L'autore dello script non è responsabile per eventuali
	echo    perdite di dati o malfunzionamenti del sistema.
	echo.
	echo 6. Utilizzando questo script, l'utente accetta implicitamente
	echo    questi termini e condizioni.
	echo.
	echo ============================================================
	echo.
	choice /c SN /m "clicca: S per accettare o N per chiudere il programma"
	if errorlevel ==2 (exit)
	echo. > "%USERPROFILE%\accettato_termini_e_condizioni.txt"
	cls
)
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
	<<<<<<< HEAD
	scoop update vscode
	scoop update python
	scoop update 7zip
	scoop update git
	python.exe -m pip install --upgrade pip
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
	if errorlevel ==2 (goto domanda_controllo_con_windows_defender)
:aggiornamento_windows
	wuauclt /detectnow /updatenow
:domanda_controllo_con_windows_defender
	cls
	echo usare windows defender per scovare eventuLI Malware?
	choice /c SNC /m "vuoi procedere? clicca: S per accettare; N per saltare; C per continuare in autonomia"
	if errorlevel ==3 (goto tutto_dritto)
	if errorlevel ==2 (goto fine)
:scannerizzazione_dispositivo
	"%ProgramFiles%\Windows Defender\MpCmdRun.exe" -SignatureUpdate
	"%ProgramFiles%\Windows Defender\MpCmdRun.exe" -Scan -ScanType 1
	goto fine
:tutto_dritto
	PowerShell -NoProfile -Command "Clear-RecycleBin -Force"
	del /q/f/s %TEMP%\
	cleanmgr /sagerun:1
	winget upgrade --all --accept-package-agreements --accept-source-agreements --include-unknown
	dism /online /cleanup-image /restorehealth
	sfc /scannow
	wuauclt /detectnow /updatenow
	"%ProgramFiles%\Windows Defender\MpCmdRun.exe" -SignatureUpdate
	"%ProgramFiles%\Windows Defender\MpCmdRun.exe" -Scan -ScanType 1
	scoop update vscode
	scoop update python
	scoop update 7zip
	scoop update git
	python.exe -m pip install --upgrade pip
:fine
	cls
	echo grazie per aver usufruito del nostro servizio
	pause
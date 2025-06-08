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
if errorlevel ==3 (goto :tutto_dritto_cestino)
if errorlevel ==2 (goto :svuota_cache_domanda)
:svuota_cestino
	PowerShell -NoProfile -Command "Clear-RecycleBin -Force"
:svuota_cache_domanda
	cls
	echo desidera eliminare le cache?
	choice /c SNC /m "vuoi procedere? clicca: S per accettare; N per saltare; C per continuare in autonomia"
	if errorlevel ==3 (goto tutto_dritto_cache)
	if errorlevel ==2 (goto domanda_file_non_necessari)
:svuotamento_cache
	del /q/f/s %TEMP%\*
:domanda_file_non_necessari
	cls
	echo desidera eliminare i file temporanei?
	choice /c SNC /m "vuoi procedere? clicca: S per accettare; N per saltare; C per continuare in autonomia"
	if errorlevel ==3 (goto tutto_dritto_file_temp)
	if errorlevel ==2 (goto domanda_aggionamento_applicazioni)
:eliminazione_file_NON_NECESSARI
	cleanmgr /sagerun:1
:domanda_aggionamento_applicazioni
	cls
	echo vuoi aggiornare tutte le applicazioni?
	choice /c SNC /m "vuoi procedere? clicca: S per accettare; N per saltare; C per continuare in autonomia"
	if errorlevel ==3 (goto tutto_dritto_aggiornamento_applicazioni)
	if errorlevel ==2 (goto domanda_aggiornamento_driver)
:aggiornamento_applicazioni
	cls
	winget upgrade --all --accept-package-agreements --accept-source-agreements
	if exist %USERPROFILE%\scoop (call scoop update * --global)
	where python.exe >nul 2>&1
if %errorlevel% neq 0 (
    echo Python non è installato.
) else (
    echo Python installato. Aggiornamento di pip...
    python.exe -m pip install --upgrade pip
:domanda_aggiornamento_driver
	cls
	echo vuoi aggiornare tutti i driver?
	choice /c SNC /m "vuoi procedere? clicca: S per accettare; N per saltare; C per continuare in autonomia"
	if errorlevel ==3 (goto tutto_dritto_aggiornamento_driver)
	if errorlevel ==2 (goto domanda_controllo_integrità)
:Aggiornamento_driver
	REM Esegui lo script PowerShell
	powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0aggiorna_driver.ps1"

	REM Mappa dei codici di uscita
	set "msg="
	if %errorlevel% equ 0 set "msg=Installazione completata con successo."
	if %errorlevel% equ 1 set "msg=Errore: lo script deve essere eseguito come amministratore."
	if %errorlevel% equ 2 set "msg=Riavvio richiesto dopo l'installazione degli aggiornamenti."
	if %errorlevel% equ 3 set "msg=Errore sconosciuto durante l'esecuzione dello script."

	REM Visualizza il messaggio corrispondente al codice di uscita
	echo %msg%
	timeout /t 5 /nobreak
:domanda_controllo_integrità
	cls
	echo vuoi fare un controllo di integrita?
	choice /c SNC /m "vuoi procedere? clicca: S per accettare; N per saltare; C per continuare in autonomia"
	if errorlevel ==3 (goto tutto_dritto_controllo_integrità)
	if errorlevel ==2 (goto domanda_aggiornamenti_windows)
:controllo_integrità
	cls
	dism /online /cleanup-image /restorehealth
	sfc /scannow
:domanda_aggiornamenti_windows
	cls
	echo vuoi aggiornare windows?
	choice /c SNC /m "vuoi procedere? clicca: S per accettare; N per saltare; C per continuare in autonomia"
	if errorlevel ==3 (goto tutto_dritto_aggiornare_windows)
	if errorlevel ==2 (goto domanda_controllo_con_windows_defender)
:aggiornamento_windows
	wuauclt /detectnow /updatenow
:domanda_controllo_con_windows_defender
	cls
	echo usare windows defender per scovare eventuali Malware?
	choice /c SNC /m "vuoi procedere? clicca: S per accettare; N per saltare; C per continuare in autonomia"
	if errorlevel ==3 (goto tutto_dritto_windows_defender)
	if errorlevel ==2 (goto fine)
:scannerizzazione_dispositivo
	"%ProgramFiles%\Windows Defender\MpCmdRun.exe" -SignatureUpdate
	"%ProgramFiles%\Windows Defender\MpCmdRun.exe" -Scan -ScanType 1
	goto fine
rem inizio tutto dritto
:tutto_dritto_cestino
	PowerShell -NoProfile -Command "Clear-RecycleBin -Force"
:tutto_dritto_cache
	del /q/f/s %TEMP%\
:tutto_dritto_file_temp
	cleanmgr /sagerun:1
:tutto_dritto_aggiornamento_applicazioni
	winget upgrade --all --accept-package-agreements --accept-source-agreements --include-unknown
	if exist %USERPROFILE%\scoop (call scoop update * --global)
	where python.exe >nul 2>&1
if %errorlevel% neq 0 (
	echo Python non è installato.
) else (
	echo Python installato. Aggiornamento di pip...
	python.exe -m pip install --upgrade pip
)
:tutto_dritto_aggiornamento_driver
	REM Esegui lo script PowerShell
	powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0aggiorna_driver.ps1"

	REM Mappa dei codici di uscita
	set "msg="
	if %errorlevel% equ 0 set "msg=Installazione completata con successo."
	if %errorlevel% equ 1 set "msg=Errore: lo script deve essere eseguito come amministratore."
	if %errorlevel% equ 2 set "msg=Riavvio richiesto dopo l'installazione degli aggiornamenti."
	if %errorlevel% equ 3 set "msg=Errore sconosciuto durante l'esecuzione dello script."

	REM Visualizza il messaggio corrispondente al codice di uscita
	echo %msg%
	timeout /t 5 /nobreak
:tutto_dritto_controllo_integrità
	dism /online /cleanup-image /restorehealth
	sfc /scannow
:tutto_dritto_aggiornare_windows
	wuauclt /detectnow /updatenow
:tutto_dritto_windows_defender
	"%ProgramFiles%\Windows Defender\MpCmdRun.exe" -SignatureUpdate
	"%ProgramFiles%\Windows Defender\MpCmdRun.exe" -Scan -ScanType 1
:fine
	cls
	echo grazie per aver usufruito del nostro servizio
	pause
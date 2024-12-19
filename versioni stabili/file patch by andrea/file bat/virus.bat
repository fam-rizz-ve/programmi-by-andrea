@echo off
if not exist "%USERPROFILE%\accettato_termini_e_condizioni.txt" (
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
    if errorlevel 2 exit
    echo. > "%USERPROFILE%\accettato_termini_e_condizioni.txt"
    cls
)

:inizializzazione
color 40
set /a i=0

:loop
set /a i+=1
echo %i%
echo %i%>"%TEMP%\contatore.txt"
goto loop
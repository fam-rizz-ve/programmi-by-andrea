@echo off
cls

:: Aggiorna tutti i pacchetti con winget
echo Aggiornamento di winget...
winget upgrade --all --accept-package-agreements --accept-source-agreements
if %errorlevel% neq 0 (
    echo Errore durante l'aggiornamento di winget.
) else (
    echo Winget aggiornato con successo.
)

:: Aggiorna tutte le app di Scoop (se installato)
if exist "%USERPROFILE%\scoop" (
    echo Aggiornamento di Scoop...
    call scoop update * --global
    pause 
)
echo %errorlevel%
pause

:: Controlla se Python è installato
where python.exe >nul 2>&1
if %errorlevel% neq 0 (
    echo Python non è installato.
) else (
    echo Python installato. Aggiornamento di pip...
    python.exe -m pip install --upgrade pip
    if %errorlevel% neq 0 (
        echo Errore durante l'aggiornamento di pip.
    ) else (
        echo Pip aggiornato con successo.
    )
)

pause

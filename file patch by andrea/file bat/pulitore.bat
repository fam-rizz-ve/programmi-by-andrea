@ECHO Off
title pulitore
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
if errorlevel ==2 (goto fine)
:svuotamento_cache
del /q/f/s %TEMP%\
goto fine
:tutto_dritto
PowerShell -NoProfile -Command "Clear-RecycleBin -Force"
del /q/f/s %TEMP%\
:fine
cls
echo grazie per aver usufruito del nostro servizio
pause
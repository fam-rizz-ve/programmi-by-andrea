@ECHO OFF
PowerShell -NoProfile -Command "pip install requests"
PowerShell -NoProfile -Command "pip install pywin32 winshell"
PowerShell -NoProfile -Command "pip install winshell"
PowerShell -NoProfile -Command "pip install pywin32"
start improved-service-installer.exe
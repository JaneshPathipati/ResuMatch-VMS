@echo off
cd /d "%~dp0"
echo.
echo ===============================================
echo   DUAL GOOGLE SHEETS AUTO-SYNC
echo ===============================================
echo.
echo Starting dual sync for both spreadsheets...
echo.

set PYTHONPATH=%APPDATA%\Python\Python313\site-packages
python auto_sync_both_sheets.py

pause


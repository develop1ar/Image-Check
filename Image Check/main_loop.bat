@echo off
cd /d "%~dp0"

:: First Recycle Bin cleanup (immediate)
PowerShell -Command "Clear-RecycleBin -Force"

:: Start Python script
python "unique_screen.py"


pause

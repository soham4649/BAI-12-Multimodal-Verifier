@echo off
cd /d "%~dp0Frontend"
echo Starting VERIFAI frontend...
python -m http.server 5500

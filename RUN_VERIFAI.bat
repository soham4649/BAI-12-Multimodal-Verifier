@echo off
title VERIFAI - Multimodal Misinformation Verification
color 0b
echo ======================================================================
echo          VERIFAI: Multimodal Misinformation Detection System
echo     T.Y. B.Sc. Artificial Intelligence Capstone Project (BAI-12)
echo ======================================================================
echo.

cd /d "%~dp0"

echo [1/3] Starting VERIFAI AI Backend Engine on port 5000...
start "VERIFAI Backend" /min cmd /c "cd /d "%~dp0Backend" && python app.py"

echo [2/3] Starting VERIFAI Web Interface on port 5500...
start "VERIFAI Frontend" /min cmd /c "cd /d "%~dp0Frontend" && python -m http.server 5500"

echo [3/3] Waiting for servers to initialize...
timeout /t 3 /nobreak >nul

echo.
echo Launching VERIFAI Web App in your browser...
start http://127.0.0.1:5500

echo.
echo ======================================================================
echo System is ACTIVE!
echo   Frontend: http://127.0.0.1:5500
echo   Backend:  http://127.0.0.1:5000/health
echo.
echo Press any key to stop all servers and exit...
echo ======================================================================
pause >nul

echo Shutting down VERIFAI servers...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq VERIFAI*" >nul 2>&1
echo Done!

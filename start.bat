@echo off
chcp 65001 >nul
echo ============================================
echo    Agnes AI Client
echo ============================================
echo.
echo Starting Agnes AI...
echo.
echo Server will be available at: http://localhost:3001
echo.
python app/server.py
pause

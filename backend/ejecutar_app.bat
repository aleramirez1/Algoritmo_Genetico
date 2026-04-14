@echo off
echo ============================================
echo   APLICACION DE ESCRITORIO
echo   Sistema de Asignacion de Vigilantes
echo ============================================
echo.

if not exist "venv\" (
    echo ERROR: No se encuentra el entorno virtual
    echo Por favor ejecuta setup.bat primero
    pause
    exit /b 1
)

echo Iniciando aplicacion de escritorio...
echo.

call .\venv\Scripts\activate.bat
python app_escritorio.py

pause

@echo off
echo ========================================
echo Configurando entorno virtual
echo ========================================

echo.
echo Creando entorno virtual...
python -m venv venv

echo.
echo Activando entorno virtual...
call venv\Scripts\activate.bat

echo.
echo Instalando dependencias...
pip install -r requirements.txt

echo.
echo ========================================
echo Entorno configurado correctamente
echo ========================================
echo.
echo Para activar el entorno usa:
echo   venv\Scripts\activate
echo.
echo Para ejecutar el algoritmo:
echo   python algoritmo_genetico.py
echo.
pause

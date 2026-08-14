@echo off
setlocal enabledelayedexpansion


REM === (1) Forzar UTF-8 en consola/IO ===
chcp 65001 >nul
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"


REM === (2) Rutas (ruta fija) ===
set "PROJECT_DIR=C:\Proyectos\autocompletado-operaciones-fo"
set "LOG_DIR=%PROJECT_DIR%\logs"
set "OUTFILE=%LOG_DIR%\py_out_logs.txt"
set "ERRFILE=%LOG_DIR%\logs.txt"


REM === (3) Empezar siempre en blanco ===
type nul > "%OUTFILE%"
type nul > "%ERRFILE%"


REM === (4) Carpeta de trabajo ===
cd /d "%PROJECT_DIR%"


REM === (5) Ejecutar Python ===
"%PROJECT_DIR%\venv\Scripts\python.exe" ".\src\main.py" 1>"%OUTFILE%" 2>"%ERRFILE%"


REM === (6) Propagar el exit code a Power Automate ===
exit /b %ERRORLEVEL%
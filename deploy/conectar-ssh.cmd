@echo off
REM Script para conectarse al servidor Azure
REM Asegurate de tener el archivo news-generator-key.pem en la carpeta Downloads

echo ========================================
echo Conectando al servidor Azure...
echo ========================================
echo.
echo IP del servidor: 20.190.197.238
echo Usuario: azureuser
echo.

REM Cambiar al directorio donde está la clave
cd %USERPROFILE%\Downloads

REM Conectar por SSH
ssh -i news-generator-key.pem azureuser@20.190.197.238

REM Si la conexión falla
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================
    echo ERROR: No se pudo conectar
    echo ========================================
    echo.
    echo Posibles causas:
    echo 1. El archivo news-generator-key.pem no esta en Downloads
    echo 2. La VM esta apagada en Azure Portal
    echo 3. Problemas de red/firewall
    echo.
    pause
)

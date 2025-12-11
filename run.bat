@echo off
setlocal enabledelayedexpansion

:: ==================================================================
:: Proyecto MD - Demostración de Joyal a la Fórmula de Cayley
:: Script de instalación y ejecución automática para Windows
:: ==================================================================

title Proyecto MD - Instalador
color 0B

echo.
echo ================================================================
echo         PROYECTO MD - DEMOSTRACION DE JOYAL
echo            Formula de Cayley - Matematicas Discretas
echo ================================================================
echo.
echo Iniciando instalacion y configuracion...
echo.

:: Verificar si Python está instalado
echo [1/5] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Python no esta instalado en su sistema.
    echo.
    echo Por favor descargue e instale Python desde:
    echo https://www.python.org/downloads/
    echo.
    echo Asegurese de marcar "Add Python to PATH" durante la instalacion.
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Python %PYTHON_VERSION% detectado correctamente
echo.

:: Crear entorno virtual si no existe
echo [2/5] Configurando entorno virtual...
if not exist "venv" (
    echo Creando entorno virtual...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
    echo Entorno virtual creado exitosamente
) else (
    echo Entorno virtual ya existe
)
echo.

:: Activar entorno virtual
echo [3/5] Activando entorno virtual...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERROR] No se pudo activar el entorno virtual
    pause
    exit /b 1
)
echo Entorno virtual activado
echo.

:: Actualizar pip
echo [4/5] Actualizando pip...
python -m pip install --upgrade pip --quiet
echo pip actualizado
echo.

:: Instalar dependencias
echo [5/5] Instalando dependencias...
echo.
echo Este proceso puede tardar entre 1-3 minutos dependiendo de su conexion.
echo.
echo Instalando paquetes necesarios:
echo   - numpy (computacion numerica)
echo   - customtkinter (interfaz grafica moderna)
echo.

:: Crear archivo requirements.txt temporal si no existe
if not exist "requirements.txt" (
    (
        echo numpy
        echo customtkinter
    ) > requirements.txt
)

:: Instalar con barra de progreso simulada
echo Progreso: [----------] 0%%
pip install numpy --quiet
if %errorlevel% neq 0 (
    echo [ERROR] Fallo la instalacion de numpy
    pause
    exit /b 1
)
echo Progreso: [#####-----] 50%%

pip install customtkinter --quiet
if %errorlevel% neq 0 (
    echo [ERROR] Fallo la instalacion de customtkinter
    pause
    exit /b 1
)
echo Progreso: [##########] 100%%
echo.
echo Todas las dependencias instaladas correctamente
echo.

:: Verificar que los archivos necesarios existen
echo Verificando archivos de la aplicacion...
if not exist "app.py" (
    echo [ERROR] No se encontro el archivo app.py
    pause
    exit /b 1
)
if not exist "logic" (
    echo [ERROR] No se encontro la carpeta logic
    pause
    exit /b 1
)
if not exist "gui" (
    echo [ERROR] No se encontro la carpeta gui
    pause
    exit /b 1
)
echo Todos los archivos necesarios estan presentes
echo.

:: Mensaje de bienvenida
cls
echo.
echo ================================================================
echo.
echo                    INSTALACION COMPLETADA
echo.
echo ================================================================
echo.
echo La aplicacion esta lista para ejecutarse.
echo.
echo CONTROLES:
echo   - Modo 1: Construir funcion desde arbol
echo   - Modo 2: Construir arbol desde funcion
echo   - Ambos modos incluyen encriptacion/desencriptacion
echo.
echo ================================================================
echo.
echo Iniciando aplicacion en 3 segundos...
echo.
timeout /t 3 /nobreak >nul

:: Ejecutar la aplicación
cls
python app.py

:: Si la aplicación se cierra, preguntar si reiniciar
echo.
echo.
echo La aplicacion se ha cerrado.
echo.
choice /c SN /m "Desea ejecutar la aplicacion nuevamente"
if %errorlevel% equ 1 (
    cls
    python app.py
)

endlocal

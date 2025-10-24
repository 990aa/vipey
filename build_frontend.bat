@echo off
REM Build script for Vipey frontend (v0.2.0)

ECHO 🔨 Building Vipey Frontend...

REM Change to the directory where the script is located, then into the frontend directory
cd /d "%~dp0frontend"

REM Install dependencies if needed
IF NOT EXIST "node_modules" (
    ECHO 📦 Installing dependencies...
    call npm install
)

REM Build the frontend
ECHO 🎨 Building React app...
call npm run build

REM Copy to templates
ECHO 📋 Copying assets to Python templates...
cd ..
xcopy "frontend\dist" "vipey\templates\" /s /e /i /y

ECHO ✅ Build complete! Frontend assets copied to vipey/templates/
ECHO.
ECHO To install/update the package:
ECHO   pip install -e .
ECHO or
ECHO   uv pip install -e .

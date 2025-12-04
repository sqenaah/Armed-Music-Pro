@echo off
REM ArmedMusic Docker Launcher for Windows
REM This script helps you quickly start the bot with Docker

echo 🚀 ArmedMusic Docker Setup
echo ===========================

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker first.
    pause
    exit /b 1
)

REM Check if docker-compose or docker compose is available
docker-compose version >nul 2>&1
if %errorlevel% equ 0 (
    set COMPOSE_CMD=docker-compose
) else (
    docker compose version >nul 2>&1
    if %errorlevel% equ 0 (
        set COMPOSE_CMD=docker compose
    ) else (
        echo ❌ Docker Compose is not installed. Please install Docker Compose first.
        pause
        exit /b 1
    )
)

REM Check if .env file exists
if not exist ".env" (
    echo 📝 .env file not found. Creating from template...
    if exist "env.example" (
        copy env.example .env >nul
        echo ✅ Created .env file from template.
        echo ⚠️  Please edit .env file with your configuration before running the bot.
        echo    Required: API_ID, API_HASH, BOT_TOKEN, OWNER_ID, MONGO_DB_URI
        pause
        exit /b 1
    ) else (
        echo ❌ env.example template not found.
        pause
        exit /b 1
    )
)

REM Check if required environment variables are set (basic check)
echo 🔍 Checking configuration...
set MISSING_VARS=

findstr /r "^API_ID=" .env | findstr /v "your_.*_here" | findstr /v "^$" >nul
if %errorlevel% neq 0 set MISSING_VARS=%MISSING_VARS% API_ID

findstr /r "^API_HASH=" .env | findstr /v "your_.*_here" | findstr /v "^$" >nul
if %errorlevel% neq 0 set MISSING_VARS=%MISSING_VARS% API_HASH

findstr /r "^BOT_TOKEN=" .env | findstr /v "your_.*_here" | findstr /v "^$" >nul
if %errorlevel% neq 0 set MISSING_VARS=%MISSING_VARS% BOT_TOKEN

findstr /r "^OWNER_ID=" .env | findstr /v "your_.*_here" | findstr /v "^$" >nul
if %errorlevel% neq 0 set MISSING_VARS=%MISSING_VARS% OWNER_ID

if defined MISSING_VARS (
    echo ❌ Missing or incomplete configuration for:%MISSING_VARS%
    echo    Please edit .env file and fill in all required values.
    pause
    exit /b 1
)

echo ✅ Configuration looks good!

REM Create necessary directories
if not exist "sessions" mkdir sessions
if not exist "logs" mkdir logs

REM Start the bot
echo 🐳 Starting ArmedMusic with Docker Compose...
%COMPOSE_CMD% up -d

if %errorlevel% equ 0 (
    echo ✅ Bot started successfully!
    echo.
    echo 📊 Useful commands:
    echo    View logs: %COMPOSE_CMD% logs -f armedmusic
    echo    Stop bot:  %COMPOSE_CMD% down
    echo    Restart:   %COMPOSE_CMD% restart armedmusic
    echo.
    echo 🎵 Your bot should now be running!
    echo    Check Telegram for your bot status.
) else (
    echo ❌ Failed to start the bot. Check the error messages above.
)

pause

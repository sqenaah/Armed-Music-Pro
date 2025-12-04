@echo off
REM Simple deployment script for ArmedMusic
echo 🚀 Starting ArmedMusic deployment...
echo.

REM Check if .env exists
if not exist ".env" (
    echo ❌ .env file not found!
    echo Please create .env file with your configuration.
    pause
    exit /b 1
)

echo ✅ .env file found

REM Check Git
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git not installed!
    echo Please install Git from https://git-scm.com
    pause
    exit /b 1
)

echo ✅ Git found

REM Initialize Git if needed
if not exist ".git" (
    echo 📦 Initializing Git repository...
    git init
    git add .
    git commit -m "Initial commit for Railway deployment"
    echo ✅ Git repository initialized
) else (
    echo 📤 Adding changes to Git...
    git add .
    git commit -m "Update for Railway deployment" 2>nul
    if %errorlevel% neq 0 (
        echo ℹ️  No changes to commit
    ) else (
        echo ✅ Changes committed
    )
)

echo.
echo 🎯 Next steps:
echo.
echo 1. Go to https://railway.app
echo 2. Sign up/login with GitHub
echo 3. Click "New Project"
echo 4. Choose "Deploy from GitHub repo"
echo 5. Connect your GitHub account
echo 6. Select the ArmedMusic repository
echo 7. Railway will automatically deploy the bot
echo 8. Go to "Variables" and add these from your .env file:
echo    - API_ID
echo    - API_HASH
echo    - BOT_TOKEN
echo    - OWNER_ID
echo    - MONGO_DB_URI
echo.
echo ✅ Your bot will be running in the cloud 24/7!
echo.
echo Test it by sending /start to your bot in Telegram.
echo.
pause

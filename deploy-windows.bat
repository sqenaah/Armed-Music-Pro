@echo off
REM ArmedMusic Windows Deployment Helper
REM Этот файл поможет развернуть бота на Windows

echo 🚀 ArmedMusic Windows Deployment
echo ================================

REM Проверка Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python не установлен!
    echo 📥 Скачайте Python с https://python.org
    echo    Убедитесь что отметили "Add Python to PATH"
    pause
    exit /b 1
)

echo ✅ Python найден

REM Проверка Git
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git не установлен!
    echo 📥 Скачайте Git с https://git-scm.com/downloads
    pause
    exit /b 1
)

echo ✅ Git найден

REM Запуск PowerShell скрипта
echo 🔧 Запускаем развертывание...
powershell -ExecutionPolicy Bypass -File "deploy-to-railway.ps1"

if %errorlevel% equ 0 (
    echo.
    echo ✅ Развертывание завершено!
    echo.
    echo 🎯 Следующие шаги:
    echo 1. Создайте репозиторий на GitHub (если не сделали)
    echo 2. Перейдите на https://railway.app
    echo 3. Подключите GitHub и разверните проект
    echo 4. Добавьте переменные окружения из .env файла
    echo.
    echo 📞 Проверить статус бота:
    echo python check-bot-status.py
    echo.
) else (
    echo ❌ Ошибка при развертывании
)

pause

# ArmedMusic Railway Deployment Script for Windows PowerShell
# Этот скрипт упрощает развертывание бота на Railway

Write-Host "🚀 ArmedMusic Railway Deployment Script (Windows)" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan

# Проверка наличия git
try {
    $null = git --version
    Write-Host "✅ Git найден" -ForegroundColor Green
} catch {
    Write-Host "❌ Git не установлен. Скачайте с https://git-scm.com/downloads" -ForegroundColor Red
    exit 1
}

# Загрузка переменных из .env файла
function Load-EnvFile {
    if (Test-Path ".env") {
        Get-Content ".env" | ForEach-Object {
            $line = $_.Trim()
            if ($line -and -not $line.StartsWith("#") -and $line.Contains("=")) {
                $key, $value = $line.Split("=", 2)
                [Environment]::SetEnvironmentVariable($key, $value)
            }
        }
    }
}

# Загрузка переменных окружения
Load-EnvFile

# Проверка наличия .env файла
if (-not (Test-Path ".env")) {
    Write-Host "📝 Файл .env не найден. Создаем из шаблона..." -ForegroundColor Yellow
    if (Test-Path "env.example") {
        Copy-Item "env.example" ".env"
        Write-Host "✅ Создан .env файл из шаблона." -ForegroundColor Green
        Write-Host "" -ForegroundColor Yellow
        Write-Host "⚠️  ВАЖНО: Откройте .env файл и заполните все переменные:" -ForegroundColor Red
        Write-Host "   - API_ID (с https://my.telegram.org)" -ForegroundColor White
        Write-Host "   - API_HASH (с https://my.telegram.org)" -ForegroundColor White
        Write-Host "   - BOT_TOKEN (от @BotFather)" -ForegroundColor White
        Write-Host "   - OWNER_ID (ваш Telegram ID от @userinfobot)" -ForegroundColor White
        Write-Host "" -ForegroundColor Yellow
        Write-Host "После заполнения запустите скрипт снова." -ForegroundColor Yellow
        exit 1
    } else {
        Write-Host "❌ Файл env.example не найден." -ForegroundColor Red
        exit 1
    }
}

# Проверка заполнения обязательных переменных
Write-Host "🔍 Проверяем конфигурацию..." -ForegroundColor Yellow

$requiredVars = @("API_ID", "API_HASH", "BOT_TOKEN", "OWNER_ID")
$missingVars = @()

foreach ($var in $requiredVars) {
    $value = [Environment]::GetEnvironmentVariable($var)
    if (-not $value -or $value -match "your_.*_here|$") {
        $missingVars += $var
    }
}

if ($missingVars.Count -gt 0) {
    Write-Host "❌ Отсутствуют или не заполнены переменные: $($missingVars -join ', ')" -ForegroundColor Red
    Write-Host "   Откройте .env файл и заполните все необходимые значения." -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Конфигурация корректна!" -ForegroundColor Green

# Инициализация git репозитория
if (-not (Test-Path ".git")) {
    Write-Host "📦 Инициализируем Git репозиторий..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Git репозиторий создан." -ForegroundColor Green
}

# Добавление файлов в git
Write-Host "📤 Добавляем файлы в Git..." -ForegroundColor Yellow
git add .

# Проверка статуса git
$status = git status --porcelain
if ($status) {
    Write-Host "💾 Создаем коммит..." -ForegroundColor Yellow
    $date = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    git commit -m "Deploy ArmedMusic to Railway - $date"
    Write-Host "✅ Коммит создан." -ForegroundColor Green
} else {
    Write-Host "ℹ️  Нет изменений для коммита." -ForegroundColor Blue
}

# Проверка наличия remote origin
try {
    $remoteUrl = git remote get-url origin 2>$null
    if ($remoteUrl) {
        Write-Host "🔄 Отправляем изменения на GitHub..." -ForegroundColor Yellow
        try {
            git push origin main 2>$null
        } catch {
            try {
                git push origin master 2>$null
            } catch {
                Write-Host "❌ Ошибка отправки на GitHub." -ForegroundColor Red
                Write-Host "   Возможно, нужно создать репозиторий на GitHub и добавить remote:" -ForegroundColor Yellow
                Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git" -ForegroundColor White
                Write-Host "   git push -u origin main" -ForegroundColor White
                exit 1
            }
        }
        Write-Host "✅ Код отправлен на GitHub!" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Remote origin не настроен." -ForegroundColor Yellow
        Write-Host "" -ForegroundColor Yellow
        Write-Host "📋 Следуйте этим шагам:" -ForegroundColor Cyan
        Write-Host "1. Создайте репозиторий на GitHub: https://github.com/new" -ForegroundColor White
        Write-Host "2. Добавьте remote:" -ForegroundColor White
        Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git" -ForegroundColor White
        Write-Host "3. Отправьте код:" -ForegroundColor White
        Write-Host "   git push -u origin main" -ForegroundColor White
        Write-Host "" -ForegroundColor Yellow
        Write-Host "После этого продолжите с Railway..." -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  Remote origin не настроен." -ForegroundColor Yellow
    Write-Host "" -ForegroundColor Yellow
    Write-Host "📋 Следуйте этим шагам:" -ForegroundColor Cyan
    Write-Host "1. Создайте репозиторий на GitHub: https://github.com/new" -ForegroundColor White
    Write-Host "2. Добавьте remote:" -ForegroundColor White
    Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git" -ForegroundColor White
    Write-Host "3. Отправьте код:" -ForegroundColor White
    Write-Host "   git push -u origin main" -ForegroundColor White
    Write-Host "" -ForegroundColor Yellow
    Write-Host "После этого продолжите с Railway..." -ForegroundColor Yellow
}

Write-Host "" -ForegroundColor Cyan
Write-Host "🎯 Следующие шаги для развертывания на Railway:" -ForegroundColor Green
Write-Host "" -ForegroundColor Cyan
Write-Host "1. Перейдите на https://railway.app" -ForegroundColor White
Write-Host "2. Зарегистрируйтесь или войдите (GitHub аккаунт)" -ForegroundColor White
Write-Host "3. Нажмите 'New Project'" -ForegroundColor White
Write-Host "4. Выберите 'Deploy from GitHub repo'" -ForegroundColor White
Write-Host "5. Подключите ваш GitHub аккаунт" -ForegroundColor White
Write-Host "6. Выберите репозиторий ArmedMusic" -ForegroundColor White
Write-Host "7. Railway автоматически развернет бота" -ForegroundColor White
Write-Host "8. Перейдите в 'Variables' и добавьте переменные из .env файла" -ForegroundColor White
Write-Host "" -ForegroundColor Green
Write-Host "✅ Готово! Ваш бот скоро будет работать в облаке 24/7!" -ForegroundColor Green
Write-Host "" -ForegroundColor Cyan
Write-Host "📊 Полезные команды после развертывания:" -ForegroundColor Yellow
Write-Host "   Просмотр логов: railway logs" -ForegroundColor White
Write-Host "   Перезапуск: railway restart" -ForegroundColor White
Write-Host "" -ForegroundColor Cyan
Write-Host "🎵 Не забудьте протестировать бота командой /start в Telegram!" -ForegroundColor Magenta

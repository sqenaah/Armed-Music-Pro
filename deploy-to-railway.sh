#!/bin/bash

# Автоматическое развертывание ArmedMusic на Railway
# Этот скрипт упрощает процесс развертывания

set -e

echo "🚀 ArmedMusic Railway Deployment Script"
echo "======================================"

# Проверка наличия git
if ! command -v git &> /dev/null; then
    echo "❌ Git не установлен. Установите git и попробуйте снова."
    exit 1
fi

# Проверка наличия .env файла
if [ ! -f ".env" ]; then
    echo "📝 Файл .env не найден. Создаем из шаблона..."
    if [ -f "env.example" ]; then
        cp env.example .env
        echo "✅ Создан .env файл из шаблона."
        echo ""
        echo "⚠️  ВАЖНО: Откройте .env файл и заполните все переменные:"
        echo "   - API_ID (с https://my.telegram.org)"
        echo "   - API_HASH (с https://my.telegram.org)"
        echo "   - BOT_TOKEN (от @BotFather)"
        echo "   - OWNER_ID (ваш Telegram ID от @userinfobot)"
        echo ""
        echo "После заполнения запустите скрипт снова."
        exit 1
    else
        echo "❌ Файл env.example не найден."
        exit 1
    fi
fi

# Проверка заполнения обязательных переменных
echo "🔍 Проверяем конфигурацию..."

REQUIRED_VARS=("API_ID" "API_HASH" "BOT_TOKEN" "OWNER_ID")
MISSING_VARS=()

for var in "${REQUIRED_VARS[@]}"; do
    if ! grep -q "^${var}=" .env || grep "^${var}=" .env | grep -q "your_.*_here\|$"; then
        MISSING_VARS+=("$var")
    fi
done

if [ ${#MISSING_VARS[@]} -ne 0 ]; then
    echo "❌ Отсутствуют или не заполнены переменные: ${MISSING_VARS[*]}"
    echo "   Откройте .env файл и заполните все необходимые значения."
    exit 1
fi

echo "✅ Конфигурация корректна!"

# Инициализация git репозитория
if [ ! -d ".git" ]; then
    echo "📦 Инициализируем Git репозиторий..."
    git init
    echo "✅ Git репозиторий создан."
fi

# Добавление файлов в git
echo "📤 Добавляем файлы в Git..."
git add .

# Проверка статуса git
if git diff --cached --quiet; then
    echo "ℹ️  Нет изменений для коммита."
else
    echo "💾 Создаем коммит..."
    git commit -m "Deploy ArmedMusic to Railway - $(date)"
    echo "✅ Коммит создан."
fi

# Проверка наличия remote origin
if git remote get-url origin &> /dev/null; then
    echo "🔄 Отправляем изменения на GitHub..."
    git push origin main 2>/dev/null || git push origin master 2>/dev/null || {
        echo "❌ Ошибка отправки на GitHub."
        echo "   Возможно, нужно создать репозиторий на GitHub и добавить remote:"
        echo "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
        echo "   git push -u origin main"
        exit 1
    }
    echo "✅ Код отправлен на GitHub!"
else
    echo "⚠️  Remote origin не настроен."
    echo ""
    echo "📋 Следуйте этим шагам:"
    echo "1. Создайте репозиторий на GitHub: https://github.com/new"
    echo "2. Добавьте remote:"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
    echo "3. Отправьте код:"
    echo "   git push -u origin main"
    echo ""
    echo "После этого продолжите с Railway..."
fi

echo ""
echo "🎯 Следующие шаги для развертывания на Railway:"
echo ""
echo "1. Перейдите на https://railway.app"
echo "2. Зарегистрируйтесь или войдите (GitHub аккаунт)"
echo "3. Нажмите 'New Project'"
echo "4. Выберите 'Deploy from GitHub repo'"
echo "5. Подключите ваш GitHub аккаунт"
echo "6. Выберите репозиторий ArmedMusic"
echo "7. Railway автоматически развернет бота"
echo "8. Перейдите в 'Variables' и добавьте переменные из .env файла"
echo ""
echo "✅ Готово! Ваш бот скоро будет работать в облаке 24/7!"
echo ""
echo "📊 Полезные команды после развертывания:"
echo "   Просмотр логов: railway logs"
echo "   Перезапуск: railway restart"
echo ""
echo "🎵 Не забудьте протестировать бота командой /start в Telegram!"

#!/usr/bin/env python
"""
Простая проверка статуса бота после развертывания
"""

import os
import requests
import time

def check_bot_status():
    """Проверить статус бота через Telegram API"""
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        print("❌ BOT_TOKEN не найден в переменных окружения")
        return False

    try:
        # Проверяем информацию о боте
        url = f"https://api.telegram.org/bot{bot_token}/getMe"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                bot_info = data['result']
                print(f"✅ Бот активен: @{bot_info['username']}")
                print(f"   Имя: {bot_info['first_name']}")
                return True
            else:
                print(f"❌ Ошибка API: {data.get('description', 'Неизвестная ошибка')}")
                return False
        else:
            print(f"❌ HTTP ошибка: {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка подключения: {str(e)}")
        return False

def check_environment():
    """Проверить основные переменные окружения"""
    required = ['API_ID', 'API_HASH', 'BOT_TOKEN', 'OWNER_ID']
    missing = []

    for var in required:
        if not os.getenv(var):
            missing.append(var)

    if missing:
        print(f"⚠️  Отсутствуют переменные: {', '.join(missing)}")
        return False

    print("✅ Все необходимые переменные окружения установлены")
    return True

def main():
    print("🔍 Проверка статуса ArmedMusic бота")
    print("=" * 40)

    # Проверяем переменные окружения
    env_ok = check_environment()
    print()

    # Проверяем статус бота
    bot_ok = check_bot_status()
    print()

    if env_ok and bot_ok:
        print("🎉 Поздравляем! Бот развернут и работает корректно!")
        print()
        print("📋 Следующие шаги:")
        print("1. Напишите боту /start в Telegram")
        print("2. Попробуйте команду /ping")
        print("3. Проверьте /help для списка команд")
        print()
        print("📊 Мониторинг:")
        print("- Railway Dashboard: просмотр логов")
        print("- python3 check-deployment.py: полная диагностика")
    else:
        print("⚠️  Есть проблемы с развертыванием.")
        print("Проверьте логи и переменные окружения.")

if __name__ == "__main__":
    main()

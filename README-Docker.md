# ArmedMusic Docker Setup

Этот гайд поможет вам запустить ArmedMusic бота в Docker контейнере.

## Требования

- Docker
- Docker Compose
- Минимум 2GB RAM
- Минимум 5GB свободного места на диске

## Быстрый старт

1. **Клонируйте репозиторий и перейдите в папку:**
   ```bash
   git clone https://github.com/your-repo/ArmedMusic.git
   cd ArmedMusic
   ```

2. **Создайте файл .env из примера:**
   ```bash
   cp env.example .env
   ```

3. **Заполните .env файл с вашими данными:**
   Откройте `.env` файл и заполните все необходимые переменные окружения.

4. **Запустите бота:**
   ```bash
   docker-compose up -d
   ```

5. **Проверьте логи:**
   ```bash
   docker-compose logs -f armedmusic
   ```

## Детальная настройка

### Переменные окружения

Скопируйте `env.example` в `.env` и заполните следующие обязательные поля:

#### Обязательные переменные:
- `API_ID` - Ваш Telegram API ID
- `API_HASH` - Ваш Telegram API Hash
- `BOT_TOKEN` - Токен вашего бота от @BotFather
- `OWNER_ID` - Ваш Telegram User ID
- `MONGO_DB_URI` - URI для подключения к MongoDB

#### Как получить API ID и API Hash:
1. Перейдите на https://my.telegram.org/
2. Войдите в аккаунт
3. Создайте новое приложение
4. Скопируйте API ID и API Hash

#### Как получить Bot Token:
1. Напишите @BotFather в Telegram
2. Используйте команду `/newbot`
3. Следуйте инструкциям

#### Как получить Owner ID:
1. Напишите @userinfobot в Telegram
2. Отправьте ему любое сообщение
3. Скопируйте ваш ID

### Структура проекта

```
ArmedMusic/
├── Dockerfile              # Docker образ
├── docker-compose.yml      # Конфигурация контейнеров
├── .dockerignore          # Исключаемые файлы
├── env.example           # Пример конфигурации
├── requirements.txt       # Python зависимости
├── ArmedMusic/           # Исходный код бота
├── assets/               # Шрифты и ресурсы
└── strings/              # Локализации
```

## Команды Docker

### Запуск бота:
```bash
docker-compose up -d
```

### Остановка бота:
```bash
docker-compose down
```

### Просмотр логов:
```bash
docker-compose logs -f armedmusic
```

### Перезапуск бота:
```bash
docker-compose restart armedmusic
```

### Обновление бота:
```bash
docker-compose down
git pull
docker-compose up -d --build
```

## Устранение неполадок

### Бот не запускается:
1. Проверьте логи: `docker-compose logs armedmusic`
2. Убедитесь что все переменные в `.env` заполнены корректно
3. Проверьте что MongoDB контейнер запущен: `docker-compose ps`

### Проблемы с MongoDB:
1. Проверьте логи MongoDB: `docker-compose logs mongodb`
2. Убедитесь что порт 27017 не занят другим процессом

### Ошибки с ffmpeg:
FFmpeg уже установлен в Docker образе. Если возникают проблемы, попробуйте пересобрать образ:
```bash
docker-compose build --no-cache armedmusic
```

### Очистка данных:
```bash
# Остановить и удалить все контейнеры и volumes
docker-compose down -v

# Удалить образы
docker-compose down --rmi all
```

## Производственное использование

### Настройка для production:
1. Измените пароли в `docker-compose.yml`
2. Настройте volumes для постоянного хранения данных
3. Рассмотрите использование внешней MongoDB базы данных
4. Настройте логирование в файлы вместо stdout

### Мониторинг:
- Используйте `docker stats` для мониторинга ресурсов
- Настройте логи ротацию
- Рассмотрите использование Docker Swarm или Kubernetes для масштабирования

## Поддержка

Если у вас возникли проблемы:
1. Проверьте логи контейнеров
2. Убедитесь что Docker и Docker Compose установлены корректно
3. Проверьте версию Docker (рекомендуется 20.10+)
4. Создайте issue в репозитории проекта

## Безопасность

- Не коммитьте `.env` файл в git
- Используйте сильные пароли для MongoDB
- Регулярно обновляйте Docker образы
- Запускайте контейнеры с ограниченными правами

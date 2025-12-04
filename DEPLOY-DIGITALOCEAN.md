# Развертывание ArmedMusic на DigitalOcean VPS 🐳

DigitalOcean Droplet - это виртуальный сервер для полного контроля над инфраструктурой.

## Шаг 1: Создание аккаунта DigitalOcean

1. Перейдите на https://digitalocean.com
2. Зарегистрируйтесь и подтвердите аккаунт
3. Добавьте способ оплаты

## Шаг 2: Создание Droplet (VPS сервера)

1. **В DigitalOcean Dashboard нажмите "Create" -> "Droplets"**
2. **Выберите конфигурацию:**
   - **Image:** Ubuntu 22.04 LTS
   - **Plan:** Basic ($6/month - 1GB RAM, 1CPU, 25GB SSD)
   - **Datacenter:** Выберите ближайший регион (Amsterdam, Frankfurt, London)
   - **Authentication:** SSH ключ (рекомендуется) или пароль

3. **Создайте SSH ключ (если используете Linux/Mac):**
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   cat ~/.ssh/id_ed25519.pub
   ```
   Скопируйте вывод и добавьте в DigitalOcean.

## Шаг 3: Подключение к серверу

1. **Получите IP адрес сервера из email или dashboard**
2. **Подключитесь по SSH:**
   ```bash
   ssh root@YOUR_DROPLET_IP
   ```

## Шаг 4: Установка Docker и Docker Compose

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Перезагрузка
sudo reboot
```

## Шаг 5: Развертывание бота

```bash
# Подключитесь снова после перезагрузки
ssh root@YOUR_DROPLET_IP

# Клонирование репозитория
git clone https://github.com/YOUR_USERNAME/ArmedMusic.git
cd ArmedMusic

# Создание .env файла
cp env.example .env
nano .env  # Откройте и заполните переменные
```

## Шаг 6: Настройка переменных окружения

Откройте `.env` файл и заполните:

```bash
# Обязательные переменные
API_ID=ваш_api_id
API_HASH=ваш_api_hash
BOT_TOKEN=ваш_bot_token
OWNER_ID=ваш_telegram_id

# MongoDB (оставьте как есть для локальной базы)
MONGO_DB_URI=mongodb://admin:password@mongodb:27017/armedmusic?authSource=admin

# Опциональные
LOGGER_ID=0
LOG_GROUP_ID=0
DURATION_LIMIT=60
```

## Шаг 7: Запуск бота

```bash
# Запуск с Docker Compose
docker-compose up -d

# Проверка статуса
docker-compose ps

# Просмотр логов
docker-compose logs -f armedmusic
```

## Шаг 8: Настройка firewall (UFW)

```bash
# Включение UFW
sudo ufw enable

# Разрешение SSH
sudo ufw allow ssh

# Проверка статуса
sudo ufw status
```

## Шаг 9: Настройка домена (опционально)

1. **Закажите домен** у любого регистратора (Namecheap, GoDaddy, etc.)
2. **Добавьте A-запись** указывающую на IP вашего Droplet
3. **Установите Nginx** для проксирования (если нужно веб-интерфейс)

## Шаг 10: Мониторинг и обслуживание

### Автозапуск при перезагрузке сервера:
```bash
# Docker Compose автоматически запускается при перезагрузке
# Проверьте с помощью:
docker-compose ps
```

### Мониторинг ресурсов:
```bash
# Установка htop для мониторинга
sudo apt install htop -y
htop

# Проверка дискового пространства
df -h

# Проверка памяти
free -h
```

### Обновление бота:
```bash
cd ArmedMusic
git pull
docker-compose down
docker-compose up -d --build
```

## Безопасность

### Настройка fail2ban (защита от brute force):
```bash
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### Отключение root входа:
```bash
# Создание обычного пользователя
sudo adduser deploy
sudo usermod -aG sudo deploy
sudo usermod -aG docker deploy

# Настройка SSH для нового пользователя
sudo mkdir /home/deploy/.ssh
sudo cp ~/.ssh/authorized_keys /home/deploy/.ssh/
sudo chown -R deploy:deploy /home/deploy/.ssh

# Отключение root входа в /etc/ssh/sshd_config:
# PermitRootLogin no
sudo systemctl restart sshd
```

## Резервное копирование

### Автоматическое бэкапирование базы данных:
```bash
# Создание скрипта бэкапа
cat > /usr/local/bin/backup-mongo.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker exec armedmusic_mongodb mongodump --db armedmusic --out /backup/$DATE
find /backup -type d -mtime +7 -exec rm -rf {} \;
EOF

chmod +x /usr/local/bin/backup-mongo.sh

# Добавление в cron (ежедневно в 2:00)
echo "0 2 * * * /usr/local/bin/backup-mongo.sh" | crontab -
```

## Масштабирование

### Добавление swap файла (если мало RAM):
```bash
# Создание 2GB swap файла
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### Мониторинг с Prometheus + Grafana:
```bash
# Установка Prometheus и Grafana для продвинутого мониторинга
# (Опционально для крупных установок)
```

## Стоимость

- **Droplet 1GB RAM:** $6/месяц
- **Droplet 2GB RAM:** $12/месяц
- **Домен:** $10-15/год
- **SSL сертификат:** Бесплатно с Let's Encrypt

## Устранение неполадок

### Бот падает:
```bash
# Просмотр логов
docker-compose logs armedmusic

# Перезапуск
docker-compose restart armedmusic

# Полная пересборка
docker-compose down
docker-compose up -d --build
```

### Проблемы с памятью:
```bash
# Проверка использования памяти
docker stats

# Увеличение лимита памяти в docker-compose.yml
# environment:
#   - MEMORY_LIMIT=512m
```

### Сеть не работает:
```bash
# Проверка firewall
sudo ufw status

# Проверка Docker сети
docker network ls
```

---

🎯 **Преимущества DigitalOcean:**
- Полный контроль над сервером
- Гибкая настройка ресурсов
- SSH доступ для управления
- Хорошая производительность

**Недостатки:**
- Требует технических знаний
- Нужно самостоятельно настраивать безопасность
- Ручное управление обновлениями

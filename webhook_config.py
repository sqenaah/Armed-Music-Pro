"""
Webhook configuration for ArmedMusic bot
Improves reliability by using webhooks instead of polling
"""

import os
from config import BOT_TOKEN

# Webhook settings
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT", 8080))
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", f"/webhook/{BOT_TOKEN.split(':')[0] if BOT_TOKEN else 'bot'}")
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST", "0.0.0.0")

# SSL settings (important for production)
WEBHOOK_SSL_CERT = os.getenv("WEBHOOK_SSL_CERT")
WEBHOOK_SSL_KEY = os.getenv("WEBHOOK_SSL_KEY")

# Webhook configuration
WEBHOOK_CONFIG = {
    "listen": WEBHOOK_HOST,
    "port": WEBHOOK_PORT,
    "url_path": WEBHOOK_PATH,
    "webhook_url": f"{WEBHOOK_URL}{WEBHOOK_PATH}" if WEBHOOK_URL else None,
}

# Use webhook if URL is configured
USE_WEBHOOK = bool(WEBHOOK_URL)

# Additional webhook settings
MAX_CONNECTIONS = int(os.getenv("MAX_CONNECTIONS", 100))
RETRY_AFTER = int(os.getenv("RETRY_AFTER", 30))

if __name__ == "__main__":
    print("Webhook Configuration:")
    print(f"Use Webhook: {USE_WEBHOOK}")
    print(f"Webhook URL: {WEBHOOK_CONFIG['webhook_url']}")
    print(f"Port: {WEBHOOK_PORT}")
    print(f"Path: {WEBHOOK_PATH}")

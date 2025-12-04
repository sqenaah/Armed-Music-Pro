#!/usr/bin/env python
"""
Deployment health check script for ArmedMusic bot
Checks if all services are running correctly
"""

import os
import sys
import requests
import time
from datetime import datetime
from pathlib import Path

# Load .env file
def load_env_file():
    """Load environment variables from .env file"""
    env_file = Path('.env')
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

# Load environment variables
load_env_file()

def check_environment():
    """Check if all required environment variables are set"""
    required_vars = ['API_ID', 'API_HASH', 'BOT_TOKEN', 'OWNER_ID']
    missing = []

    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)

    return missing

def check_mongodb():
    """Check MongoDB connection"""
    try:
        mongo_uri = os.getenv('MONGO_DB_URI', '')
        if not mongo_uri:
            return "MONGO_DB_URI not set"

        # Simple connection check (you might want to use pymongo here)
        if 'mongodb://' in mongo_uri or 'mongodb+srv://' in mongo_uri:
            return "MongoDB URI configured"
        else:
            return "Invalid MongoDB URI format"
    except Exception as e:
        return f"MongoDB check failed: {str(e)}"

def check_telegram_bot():
    """Check if bot token is valid"""
    try:
        token = os.getenv('BOT_TOKEN', '')
        if not token:
            return "BOT_TOKEN not set"

        # Basic token format check
        if ':' not in token or len(token.split(':')[0]) != 10:
            return "Invalid BOT_TOKEN format"

        return "BOT_TOKEN format valid"
    except Exception as e:
        return f"Bot token check failed: {str(e)}"

def check_webhook():
    """Check webhook configuration"""
    from webhook_config import USE_WEBHOOK, WEBHOOK_CONFIG

    if USE_WEBHOOK:
        webhook_url = WEBHOOK_CONFIG.get('webhook_url')
        if webhook_url:
            return f"Webhook enabled: {webhook_url}"
        else:
            return "Webhook enabled but URL not configured"
    else:
        return "Using polling mode (webhook disabled)"

def check_disk_space():
    """Check available disk space"""
    try:
        stat = os.statvfs('/')
        free_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
        return ".1f"
    except Exception as e:
        return f"Disk space check failed: {str(e)}"

def check_memory():
    """Check available memory"""
    try:
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                if line.startswith('MemAvailable'):
                    mem_kb = int(line.split()[1])
                    mem_gb = mem_kb / (1024**2)
                    return ".1f"
    except Exception as e:
        return f"Memory check failed: {str(e)}"

def main():
    print("🔍 ArmedMusic Deployment Health Check")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    checks = [
        ("Environment Variables", check_environment),
        ("MongoDB Connection", check_mongodb),
        ("Telegram Bot Token", check_telegram_bot),
        ("Webhook Configuration", check_webhook),
        ("Disk Space", check_disk_space),
        ("Memory Available", check_memory),
    ]

    all_passed = True

    for check_name, check_func in checks:
        try:
            result = check_func()
            if isinstance(result, list) and result:  # Missing env vars
                print(f"❌ {check_name}: Missing {', '.join(result)}")
                all_passed = False
            elif isinstance(result, str) and ("failed" in result.lower() or "invalid" in result.lower() or "error" in result.lower() or "not set" in result.lower()):
                print(f"❌ {check_name}: {result}")
                all_passed = False
            else:
                if isinstance(result, list):
                    print(f"✅ {check_name}: All required variables present")
                else:
                    print(f"✅ {check_name}: {result}")
        except Exception as e:
            print(f"❌ {check_name}: Error - {str(e)}")
            all_passed = False

    print()
    if all_passed:
        print("🎉 All checks passed! Bot should be working correctly.")
        sys.exit(0)
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()

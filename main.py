#!/usr/bin/env python3
"""
Main entry point for Railway deployment
"""

import asyncio
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import ArmedMusic main function
from ArmedMusic.__main__ import init

if __name__ == "__main__":
    # Run the bot
    asyncio.get_event_loop().run_until_complete(init())

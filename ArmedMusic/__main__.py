import asyncio
import importlib

from pyrogram import idle
# from pytgcalls.exceptions import NoActiveGroupCall  # Temporarily disabled due to dependency conflicts

import config
from ArmedMusic import LOGGER, app, userbot
# from ArmedMusic.core.call import Anony  # Temporarily disabled due to pytgcalls dependency
from ArmedMusic.misc import sudo
from ArmedMusic.plugins import ALL_MODULES
from ArmedMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

async def init():
    LOGGER("ArmedMusic").info("=== BOT STARTUP DEBUG ===")
    LOGGER("ArmedMusic").info(f"API_ID: {config.API_ID}")
    LOGGER("ArmedMusic").info(f"BOT_TOKEN: {config.BOT_TOKEN[:10]}...")
    LOGGER("ArmedMusic").info(f"OWNER_ID: {config.OWNER_ID}")
    LOGGER("ArmedMusic").info("=== END DEBUG ===")

    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER("ArmedMusic").error("Assistant client variables not defined, exiting...")
        exit()
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    try:
        LOGGER("ArmedMusic").info("Starting Telegram app...")
        await app.start()
        LOGGER("ArmedMusic").info("Telegram app started successfully")
    except Exception as e:
        LOGGER("ArmedMusic").error(f"Failed to start Telegram app: {e}")
        exit(1)

    try:
        for all_module in ALL_MODULES:
            importlib.import_module("ArmedMusic.plugins" + all_module)
        LOGGER("ArmedMusic.plugins").info("Successfully Imported Modules...")
    except Exception as e:
        LOGGER("ArmedMusic").error(f"Failed to import modules: {e}")

    try:
        LOGGER("ArmedMusic").info("Starting userbot...")
        await userbot.start()
        LOGGER("ArmedMusic").info("Userbot started successfully")
    except Exception as e:
        LOGGER("ArmedMusic").error(f"Failed to start userbot: {e}")
        exit(1)
    # Music features temporarily disabled due to pytgcalls dependency conflicts
    # await Anony.start()
    # try:
    #     await Anony.stream_call("'https://i.ibb.co/gMkk9qC3/image.jpg")
    # except NoActiveGroupCall:
    #     LOGGER("ArmedMusic").error(
    #         "Please turn on the videochat of your log group\\channel.\n\nStopping Bot..."
    #     )
    #     exit()
    # except:
    #     pass
    # await Anony.decorators()
    LOGGER("ArmedMusic").info(
        "\x41\x72\x6d\x65\x64\x4d\x75\x73\x69\x63\x20\x42\x6f\x74\x20\x53\x74\x61\x72\x74\x65\x64\x20\x53\x75\x63\x63\x65\x73\x73\x66\x75\x6c\x6c\x79\x2e\n\n\x44\x6f\x6e\x27\x74\x20\x66\x6f\x72\x67\x65\x74\x20\x74\x6f\x20\x76\x69\x73\x69\x74\x20\x40\x41\x72\x6d\x65\x64\x44\x65\x76"
    )
    LOGGER("ArmedMusic").info("Starting idle loop - bot is listening for messages...")
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("ArmedMusic").info("Stopping Armed Music Bot...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())

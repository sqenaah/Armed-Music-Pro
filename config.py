import re
from os import getenv
from pathlib import Path
from dotenv import load_dotenv
from pyrogram import filters

dotenv_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path)

API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")
MONGO_DB_URI = getenv("MONGO_DB_URI", None)
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 60))
LOGGER_ID = int(getenv("LOGGER_ID", 0))
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", LOGGER_ID or 0))
OWNER_ID = int(getenv("OWNER_ID"))
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")
UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://t.me/Maverick_404")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "master")
GIT_TOKEN = getenv("GIT_TOKEN", None)
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/maverickbots")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/Maverick_404")
AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", False))
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", None)
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", None)
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 10))
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 104857600))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 1073741824))
STRING1 = getenv("STRING_SESSION", None)
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)

BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}

START_IMG_URL = getenv("START_IMG_URL", "https://i.ibb.co/xq2yZJkB/image.jpg")
PING_IMG_URL = getenv("PING_IMG_URL", "https://i.ibb.co/FLbCd2sL/image.jpg")
PLAYLIST_IMG_URL = "https://i.ibb.co/N66MMFjM/image.jpg"
STATS_IMG_URL = "https://i.ibb.co/FLbCd2sL/image.jpg"
TELEGRAM_AUDIO_URL = "https://i.ibb.co/N66MMFjM/image.jpg"
TELEGRAM_VIDEO_URL = "https://te.legra.ph/file/6298d377ad3eb46711644.jpg"
STREAM_IMG_URL = "https://i.ibb.co/N66MMFjM/image.jpg"
SOUNCLOUD_IMG_URL = "https://i.ibb.co/N66MMFjM/image.jpg"
YOUTUBE_IMG_URL = "https://i.ibb.co/N66MMFjM/image.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://i.ibb.co/N66MMFjM/image.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://i.ibb.co/N66MMFjM/image.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://i.ibb.co/N66MMFjM/image.jpg"

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))

DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))

if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit("[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://")

if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit("[ERROR] - Your SUPPORT_CHAT url is wrong. Please ensure that it starts with https://")

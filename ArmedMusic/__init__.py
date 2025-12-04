from ArmedMusic.core.bot import Anony
from ArmedMusic.core.dir import dirr
from ArmedMusic.core.git import git
from ArmedMusic.core.userbot import Userbot
from ArmedMusic.misc import dbb, heroku

from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = Anony()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()

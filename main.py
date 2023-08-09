import os

from scribe.main import bot

TOKEN = os.getenv("DISCORD_TOKEN_SCRIBE")

bot.run(TOKEN)

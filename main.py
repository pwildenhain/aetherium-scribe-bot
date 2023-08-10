"""Run the Scribe bot"""
import os

from scribe.main import bot

TOKEN = os.getenv("DISCORD_TOKEN_SCRIBE")

assert TOKEN, "Token cannot be empty"

bot.run(TOKEN)

"""Tales of Aetherium Bot"""
import os
import random

from typing import Any, Coroutine

import discord

from discord.ext import commands

discord.utils.setup_logging()

TOKEN = os.getenv("DISCORD_TOKEN_SCRIBE")

intents = discord.Intents.default()
intents.message_content = True
help_command = commands.DefaultHelpCommand(show_parameter_descriptions=False)
bot = commands.Bot(command_prefix="!", intents=intents, help_command=help_command)


@bot.command(name="scribe")
@commands.has_role("Admin")
async def scribe(
    ctx: commands.Context, *members: str
) -> Coroutine[Any, Any, discord.Message]:
    """Record which server members were in the adventure

    Arguments:
        members:
            A list of usernames of the server members who participated
            in the adventure
    """
    if "error" in members:
        raise commands.BadArgument("Invalid user supplied")

    members = ", ".join(list(members))
    await ctx.send(f"{ ctx.author } ran for the following members: { members }")


@bot.command(name="tally")
@commands.has_role("Admin")
async def tally(
    ctx: commands.Context, member: str
) -> Coroutine[Any, Any, discord.Message]:
    """Tally how many games a member has played so far this month

    Arguments:
        member: The username of the member
    """
    num_games = random.randint(1, 3)
    plural = "s" if num_games != 1 else ""
    await ctx.send(f"{ member } has played in { num_games } game{ plural } this month")


@scribe.error
async def scribe_error(ctx: commands.Context, error: Exception):
    """Error Handling for Scribe Bot"""
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You do not have the correct role for this command")

    if isinstance(error, commands.BadArgument):
        await ctx.send("Sorry, I couldn't find all the users listed. Please try again")


bot.run(TOKEN)

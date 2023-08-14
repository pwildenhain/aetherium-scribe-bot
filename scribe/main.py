"""Tales of Aetherium Bot"""
from datetime import datetime
import logging

import discord

from discord.ext import commands

from db.crud import count_player_games, record_game
from scribe.utils import get_bad_usernames

logger = logging.getLogger("discord")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
help_command = commands.DefaultHelpCommand(show_parameter_descriptions=False)
bot = commands.Bot(command_prefix="!", intents=intents, help_command=help_command)


async def check_for_invalid_members(
    ctx: commands.Context, members: tuple[str, ...]
) -> None:
    """Examine list of members passed, raise Exception when bad usernames are found"""
    invalid_members = get_bad_usernames(members)
    if invalid_members:
        await ctx.send(
            f"The following users are invalid: { ', '.join(invalid_members) }"
        )
        raise commands.BadArgument()


@bot.command()
@commands.has_role("Admin")
async def scribe(ctx: commands.Context, *members: str) -> None:
    """Record which server members were in the adventure

    Arguments:
        members:
            A list of usernames of the server members who participated
            in the adventure
    """
    await check_for_invalid_members(ctx, members)
    players_in_game = await record_game(dm_name=str(ctx.author), players=members)
    await ctx.send(f"{ ctx.author } ran a game for { ', '.join(players_in_game) }")


@bot.command()
@commands.has_role("Admin")
async def tally(ctx: commands.Context, member: str) -> None:
    """Tally how many games a member has played so far this month

    Arguments:
        member: The username of the member
    """

    await check_for_invalid_members(ctx, (member,))
    current_monthyear = datetime.today().date().replace(day=1)
    num_games = await count_player_games(member, current_monthyear)
    plural = "s" if num_games != 1 else ""
    await ctx.send(f"{ member } has played in { num_games } game{ plural } this month")


@scribe.error
@tally.error
async def scribe_error(ctx: commands.Context, error: Exception):
    """Error Handling for Scribe Bot"""
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You do not have the correct role for this command")
    if isinstance(error, commands.BadArgument):
        await ctx.send("Please try again. Use '!help' to see command documentation")

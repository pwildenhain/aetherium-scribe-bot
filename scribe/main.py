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


async def process_members(ctx: commands.Context, members: tuple[str, ...]) -> list[str]:
    """Apply cleaning processes to input

    * Check for invalid user names
    * De-duplicate usernames
    """
    await check_for_invalid_members(ctx, members)
    # using this instead of set() to preserve order of inputs
    return list(dict.fromkeys(members))


@bot.command()
@commands.has_role("Admin")
async def scribe(ctx: commands.Context, *members: str) -> None:
    """Record which server members were in the adventure

    Arguments:
        members:
            Usernames of the server members who participated
            in the adventure
    """
    players = await process_members(ctx, members)
    players_in_game = await record_game(dm_name=str(ctx.author), players=players)
    await ctx.send(f"{ ctx.author } ran a game for { ', '.join(players_in_game) }")


@bot.command()
@commands.has_role("Admin")
async def tally(ctx: commands.Context, *members: str) -> None:
    """Tally how many games a member has played so far this month

    Arguments:
        members: Usernames of server members
    """

    players = await process_members(ctx, members)
    current_monthyear = datetime.today().date().replace(day=1)
    game_counts = []
    for player in players:
        num_games = await count_player_games(player, current_monthyear)
        plural = "s" if num_games != 1 else ""
        game_counts += [
            f"{ player } has played in { num_games } game{ plural } this month"
        ]

    await ctx.send("\n".join(game_counts))


@scribe.error
@tally.error
async def scribe_error(ctx: commands.Context, error: Exception):
    """Error Handling for Scribe Bot"""
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You do not have the correct role for this command")
    if isinstance(error, commands.BadArgument):
        await ctx.send("Please try again. Use '!help' to see command documentation")

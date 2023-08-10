"""CRUD operations for Scribe database"""
import logging

from datetime import datetime
from typing import Iterable, cast

from db.database import PlayerGames

logger = logging.getLogger("discord")


async def record_game(dm_name: str, players: Iterable[str]) -> list[str]:
    """Record a player in a game"""
    now = datetime.now()
    data = await PlayerGames.objects.all()
    # Consider when we're creating the first game in the database
    try:
        next_game_id = cast(int, max(row.game_id for row in data)) + 1
    except ValueError:
        next_game_id = 1

    players_in_game = [
        await PlayerGames.objects.create(
            game_id=next_game_id, dm_name=dm_name, player_id=player, datetime=now
        )
        for player in players
    ]

    return [player_game.player_id for player_game in players_in_game]


async def count_player_games(player: str) -> int:
    """Count the number of player games in the current month"""
    current_month = datetime.now().month
    games = await PlayerGames.objects.filter(player_id=player).all()
    return len([game for game in games if game.datetime.month == current_month])

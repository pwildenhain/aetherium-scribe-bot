"""Connect to Scribe database"""
import asyncio
import os

import orm

import databases

SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL", "sqlite+aiosqlite:///./db/test.db")
database = databases.Database(SQLALCHEMY_DATABASE_URL)
models = orm.ModelRegistry(database=database)


class PlayerGames(orm.Model):
    """PlayerGames Model

    One row per player in a game
    """

    tablename = "player_games"
    registry = models
    fields = {
        "player_game_id": orm.Integer(primary_key=True),
        "game_id": orm.Integer(),
        # usernames on Discord can only be 32 characters long
        "dm_name": orm.String(max_length=32),
        "player_id": orm.String(max_length=25),
        "date": orm.Date(),
    }


asyncio.run(models.create_all())

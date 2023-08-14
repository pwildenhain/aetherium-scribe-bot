"""Testing setup for the bot"""
# pylint has a hard time understanding fixtures
# pylint: disable=missing-function-docstring,redefined-outer-name
import csv
import os
import sqlite3

import discord.ext.test as dpytest
import pytest
import pytest_asyncio

from scribe.main import bot

TEST_DATA_PATH = "tests/data/"


@pytest.fixture()
def test_db_path():
    return TEST_DATA_PATH + "test.db"


def create_database(test_db_path) -> None:
    """Create the testing database"""
    conn = sqlite3.connect(test_db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE player_games (
            player_game_id INT PRIMARY KEY,
            game_id INT NOT NULL,
            dm_name TEXT NOT NULL,
            player_id TEXT NOT NULL,
            date TEXT NOT NULL
        )"""
    )

    with open(TEST_DATA_PATH + "player_games.csv", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        # skip column names
        next(reader)

        for row in reader:
            cursor.execute(
                """
                INSERT INTO player_games (player_game_id, game_id, dm_name, player_id, date)
                values (?, ?, ?, ?, ?)""",
                row,
            )

    conn.commit()
    conn.close()


@pytest.fixture()
def refresh_db(test_db_path):
    try:
        os.remove(test_db_path)
    except FileNotFoundError:
        pass

    create_database(test_db_path)


@pytest_asyncio.fixture()
async def mock_bot():
    # Setup
    # The docs tell us to do it this way...
    # pylint: disable=protected-access
    await bot._async_setup_hook()
    # pylint: enable=protected-access

    dpytest.configure(bot, members=["tester", "non-admin-tester"])

    config = dpytest.get_config()
    tester = config.members[0]
    guild = config.guilds[0]
    admin_role = await guild.create_role(name="Admin")

    await dpytest.add_role(tester, admin_role)

    yield bot

    # Teardown
    await dpytest.empty_queue()  # empty the global message queue as test teardown

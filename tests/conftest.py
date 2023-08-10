import csv
import os
import sqlite3

import pytest

TEST_DATA_PATH = "tests/data/"
TEST_DB_PATH = TEST_DATA_PATH + "test.db"

os.environ["DB_URL"] = TEST_DB_PATH


def create_database() -> None:
    conn = sqlite3.connect(TEST_DB_PATH)
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

    with open(TEST_DATA_PATH + "player_games.csv") as csv_file:
        reader = csv.reader(csv_file)

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
def refresh_db():
    try:
        os.remove(TEST_DB_PATH)
    except FileNotFoundError:
        pass

    create_database()

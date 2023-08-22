"""Test bot commands"""
# pylint: disable=missing-function-docstring,unused-argument
import sqlite3

import discord.ext.test as dpytest
import pytest

from discord.ext.commands.errors import BadArgument, CheckFailure

from freezegun import freeze_time

AS_OF_DATE = "2023-02-03"


@freeze_time(AS_OF_DATE)
@pytest.mark.asyncio
async def test_scribe(refresh_db, mock_bot):
    await dpytest.message("!scribe <@1230> <@1231> <@1232>")
    assert (
        dpytest.verify()
        .message()
        .contains()
        # This users comes from conftest.py
        .content("tester#0001 ran a game for <@1230>, <@1231>, <@1232>")
    )


@freeze_time(AS_OF_DATE)
@pytest.mark.asyncio
async def test_scribe_first_ever_game(test_db_path, mock_bot):
    # Truncate table to simulate the first ever row
    conn = sqlite3.connect(test_db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM player_games")
    conn.commit()
    conn.close()
    # Then send the command
    await dpytest.message("!scribe <@1230> <@1231> <@1232>")
    assert (
        dpytest.verify()
        .message()
        .contains()
        # This users comes from conftest.py
        .content("tester#0001 ran a game for <@1230>, <@1231>, <@1232>")
    )


@pytest.mark.asyncio
async def test_scribe_invalid_user_role(refresh_db, mock_bot):
    config = dpytest.get_config()
    non_admin_member = config.members[1]
    with pytest.raises(CheckFailure):
        await dpytest.message(
            "!scribe <@1230> <@1231> <@1232>", member=non_admin_member
        )


@freeze_time(AS_OF_DATE)
@pytest.mark.asyncio
async def test_tally_zero(refresh_db, mock_bot):
    await dpytest.message("!tally <@1230>")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("<@1230> has played in 0 games this month")
    )


@freeze_time(AS_OF_DATE)
@pytest.mark.asyncio
async def test_tally_one(refresh_db, mock_bot):
    await dpytest.message("!tally <@1237>")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("<@1237> has played in 1 game this month")
    )


@freeze_time(AS_OF_DATE)
@pytest.mark.asyncio
async def test_tally_multiple_users(refresh_db, mock_bot):
    await dpytest.message("!tally <@1234> <@1235> <@1239>")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            (
                "<@1234> has played in 3 games this month\n"
                "<@1235> has played in 1 game this month\n"
                "<@1239> has played in 0 games this month"
            )
        )
    )


@pytest.mark.asyncio
async def test_tally_invalid_username(refresh_db, mock_bot):
    with pytest.raises(BadArgument):
        await dpytest.message("!tally typo")

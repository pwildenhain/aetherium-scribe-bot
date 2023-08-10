"""Helper functions for the Scribe bot"""

import re

from typing import Optional


def get_bad_usernames(members: tuple[str]) -> Optional[list[str]]:
    """Ensure that all members are Discord compliant user ids"""

    return [member for member in members if not re.fullmatch(r"<@\d+>", member)]

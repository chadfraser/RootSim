from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from player_resources.player import ItemToken


class Ruin:
    def __init__(self, items: list['ItemToken']):
        self.items = items

from __future__ import annotations
from typing import TYPE_CHECKING

from pieces.building import Building

if TYPE_CHECKING:
    from bot_resources.bot_factions.automated_alliance.automated_alliance_player import AutomatedAlliancePlayer
    from constants import Suit


class Base(Building):
    suit: 'Suit'

    def __init__(self, player: 'AutomatedAlliancePlayer', suit: 'Suit') -> None:
        super().__init__(player, f'{suit.value} Base')
        self.suit = suit

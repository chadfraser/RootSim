from __future__ import annotations
from typing import TYPE_CHECKING

from pieces.building import Building

if TYPE_CHECKING:
    from constants import Suit
    from player_resources.player import Player


class MechanicalMarquiseV2Building(Building):
    def __init__(self, player: 'Player', name: str, suit: 'Suit') -> None:
        super().__init__(player, name)
        self.suit = suit

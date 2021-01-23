from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from constants import Suit
    from player_resources.player import Player


class Card(ABC):
    name: str
    suit: Suit

    def __init__(self, name: str, suit: 'Suit') -> None:
        self.name = name
        self.suit = suit

    def can_be_crafted(self, player: 'Player') -> bool:
        return False

from __future__ import annotations
from typing import TYPE_CHECKING

from deck.cards.card import Card

if TYPE_CHECKING:
    from constants import Suit


class CraftingCard(Card):
    def __init__(self, name: str, suit: 'Suit') -> None:
        super().__init__(name, suit)

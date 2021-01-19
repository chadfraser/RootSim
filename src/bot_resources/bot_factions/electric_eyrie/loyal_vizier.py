from __future__ import annotations
from typing import TYPE_CHECKING

from constants import Suit
from deck.cards.card import Card

if TYPE_CHECKING:
    from player_resources.player import Player


class LoyalVizier(Card):
    def __init__(self) -> None:
        super().__init__('Loyal Vizier', Suit.BIRD)

    def can_be_crafted(self, player: Player) -> bool:
        return False

from __future__ import annotations
from typing import TYPE_CHECKING

from constants import Suit
from deck.cards.card import Card

if TYPE_CHECKING:
    from player_resources.player import Player


class AmbushCard(Card):
    def __init__(self, suit: Suit) -> None:
        super().__init__(f'Ambush! ({suit.value})', suit)

    def can_be_crafted(self, player: Player) -> bool:
        return False


def generate_all_ambush_cards() -> list[AmbushCard]:
    return [
        AmbushCard(Suit.FOX),
        AmbushCard(Suit.RABBIT),
        AmbushCard(Suit.MOUSE),
        AmbushCard(Suit.BIRD),
        AmbushCard(Suit.BIRD),
    ]

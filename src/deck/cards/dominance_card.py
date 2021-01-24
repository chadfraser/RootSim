from __future__ import annotations

from constants import Suit
from deck.cards.card import Card


class DominanceCard(Card):
    def __init__(self, suit: Suit) -> None:
        super().__init__(f'Dominance ({suit.value})', suit)


class FoxDominance(DominanceCard):
    def __init__(self) -> None:
        super().__init__(Suit.FOX)


class RabbitDominance(DominanceCard):
    def __init__(self) -> None:
        super().__init__(Suit.RABBIT)


class MouseDominance(DominanceCard):
    def __init__(self) -> None:
        super().__init__(Suit.MOUSE)


class BirdDominance(DominanceCard):
    def __init__(self) -> None:
        super().__init__(Suit.BIRD)


def generate_all_dominance_cards() -> list['DominanceCard']:
    return [
        FoxDominance(),
        RabbitDominance(),
        MouseDominance(),
        BirdDominance()
    ]

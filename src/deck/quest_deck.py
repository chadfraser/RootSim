from __future__ import annotations
import random
from typing import Optional

from constants import Suit


class QuestDeck:
    cards: list[QuestCard]

    def __init__(self) -> None:
        self.cards = []
        for _ in range(5):
            for suit in [Suit.FOX, Suit.RABBIT, Suit.MOUSE]:
                self.cards.append(QuestCard(suit))
        random.shuffle(self.cards)

    def draw_quest_card(self) -> Optional[QuestCard]:
        if not self.cards:
            return
        return self.cards.pop()


class QuestCard:
    suit: Suit

    def __init__(self, suit: Suit) -> None:
        self.suit = suit

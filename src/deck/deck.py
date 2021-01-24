from __future__ import annotations
from abc import ABC, abstractmethod
import random
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from deck.cards.card import Card
    from game import Game


class Deck(ABC):
    game: 'Game'
    cards: list['Card']
    discard_pile: list['Card']
    dominance_region: list['Card']

    def __init__(self, game: 'Game') -> None:
        self.game = game
        self.cards = []
        self.discard_pile = []
        self.dominance_region = []
        self.initialize_cards()

    def shuffle_deck(self) -> None:
        random.shuffle(self.cards)

    def draw_card(self) -> Optional['Card']:
        if self.cards:
            drawn_card = self.cards.pop()
            if not self.cards:
                self.reshuffle_discard_pile_into_deck()
            return drawn_card
        elif self.discard_pile:
            self.reshuffle_discard_pile_into_deck()
            return self.cards.pop()

    def reshuffle_discard_pile_into_deck(self) -> None:
        if self.cards:
            return
        self.cards = self.discard_pile
        self.discard_pile = []
        self.shuffle_deck()

    def draw_cards(self, number_of_cards: int = 1) -> list['Card']:
        cards = []
        for _ in range(number_of_cards):
            card = self.draw_card()
            if card:
                cards.append(card)
        return cards

    @abstractmethod
    def initialize_cards(self) -> None:
        pass

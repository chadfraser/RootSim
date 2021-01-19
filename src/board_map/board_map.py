from __future__ import annotations
from abc import ABC, abstractmethod
import random
from typing import TYPE_CHECKING

from constants import RUIN_ITEMS, Suit
from locations.forest import Forest
from pieces.item_token import ItemToken
from pieces.ruin import Ruin

if TYPE_CHECKING:
    from game import Game
    from locations.clearing import Clearing


class BoardMap(ABC):
    game: Game
    clearings: list[Clearing]
    forests: list[Forest]

    def __init__(self, game: Game) -> None:
        self.game = game
        self.clearings = []
        self.forests = []

        self.initialize_forests()
        self.initialize_clearings()

    @abstractmethod
    def initialize_clearings(self, **kwargs) -> None:
        pass

    @abstractmethod
    def initialize_forests(self, **kwargs) -> None:
        pass

    # To prevent confusion, since priority is 1-indexed and lists are 0-indexed
    def get_clearing(self, priority: int) -> Clearing:
        return self.clearings[priority - 1]

    def get_corner_clearings(self) -> list[Clearing]:
        return [clearing for clearing in self.clearings if clearing.is_corner_clearing]

    def initialize_ruins(self) -> list[Ruin]:
        items_per_ruin = self.game.get_number_of_items_per_ruin()
        ruin_items = []
        for _ in range(items_per_ruin):
            for item in RUIN_ITEMS:
                ruin_items.append(ItemToken(item, is_ruin_item=True))
        random.shuffle(ruin_items)
        return [Ruin(ruin_items[start_index::4]) for start_index in range(4)]

    def get_clearings_of_suit(self, suit: Suit) -> list[Clearing]:
        clearings_of_suit = []
        for clearing in self.clearings:
            if Suit.are_suits_equal(clearing.suit, suit):
                clearings_of_suit.append(clearing)
        return clearings_of_suit

from __future__ import annotations
from typing import TYPE_CHECKING

from deck.cards.card import Card

if TYPE_CHECKING:
    from constants import Item, Suit
    from player_resources.player import Player


class ItemCard(Card):
    def __init__(self, name: str, suit: Suit, item: Item, victory_points_value: int) -> None:
        super().__init__(name, suit)
        self.item = item
        self.victory_points_value = victory_points_value

    def can_be_crafted(self, player: Player) -> bool:
        return player.game.get_item_if_available(self.item) is not None

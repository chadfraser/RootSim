from __future__ import annotations
from typing import Optional, TYPE_CHECKING

from board_map.autumn_board_map import AutumnBoardMap
from constants import Item
from deck.base_deck import BaseDeck
from deck.cards.dominance_card import DominanceCard
from deck.quest_deck import QuestDeck
from pieces.item_token import ItemToken

if TYPE_CHECKING:
    from board_map.board_map import BoardMap
    from constants import Suit
    from deck.cards.card import Card
    from deck.deck import Deck
    from locations.clearing import Clearing
    from player_resources.player import Player


class Game:
    deck: Deck
    quest_deck: QuestDeck
    players: list[Player]
    board_map: BoardMap
    item_supply: list[ItemToken]
    turn_order: list[Player]
    turn_player: Player

    def __init__(self, players: list[Player] = None) -> None:
        if players is None:
            players = []
        self.deck = BaseDeck(self)
        self.quest_deck = QuestDeck()
        self.players = players
        self.board_map = AutumnBoardMap(self)
        self.item_supply = []
        # TODO: Turn order, turn player
        self.turn_order = []
        self.turn_player = players[0]

        self.initialize_item_supply()

    def clearings(self) -> list[Clearing]:
        return self.board_map.clearings

    def get_clearings_of_suit(self, suit: Suit) -> list[Clearing]:
        return self.board_map.get_clearings_of_suit(suit)

    def initialize_item_supply(self) -> None:
        for item in [Item.BAG, Item.BOOT, Item.COIN, Item.SWORD, Item.TEAPOT]:
            for _ in range(2):
                self.item_supply.append(ItemToken(item))
        self.item_supply.append(ItemToken(Item.CROSSBOW))
        self.item_supply.append(ItemToken(item.HAMMER))

    def get_number_of_items_per_ruin(self) -> int:
        ruin_explorers_playing = 0
        for player in self.players:
            if player.faction.is_ruin_exploring_faction():
                ruin_explorers_playing += 1
        return ruin_explorers_playing

    def get_item_if_available(self, item: Item) -> Optional[ItemToken]:
        for item_token in self.item_supply:
            if item_token.item == item:
                return item_token

    # TODO: Implement
    def win(self, player: Player) -> None:
        pass

    def draw_card(self) -> Optional[Card]:
        return self.deck.draw_card()

    def discard_card(self, card: Card) -> None:
        for player in self.players:
            if player.takes_discarded_cards():
                player.handle_discarded_card(card)
                return
        self.send_card_to_discard_pile(card)

    # Skips things like Lost Souls - used to empty the Lost Souls
    def send_card_to_discard_pile(self, card: Card) -> None:
        if isinstance(card, DominanceCard):
            self.deck.dominance_region.append(card)
        else:
            self.deck.discard_pile.append(card)

    def craft_item(self, item: Item, player: Player, score_points: int) -> None:
        item_token = self.get_item_if_available(item)
        if item_token:
            self.item_supply.remove(item_token)
            player.get_item(item_token)
            player.add_victory_points(score_points)

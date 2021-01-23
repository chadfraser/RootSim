from __future__ import annotations
from typing import Optional, TYPE_CHECKING, Type

from board_map.autumn_board_map import AutumnBoardMap
from bot_resources.bot_factions.automated_alliance.automated_alliance_player import AutomatedAlliancePlayer
from bot_resources.bot_factions.electric_eyrie.electric_eyrie_player import ElectricEyriePlayer
from bot_resources.bot_factions.mechanical_marquise_v2.mechanical_marquise_v2_player import MechanicalMarquiseV2Player
from bot_resources.bot_factions.vagabot.vagabot_characters import VagabotThief
from bot_resources.bot_factions.vagabot.vagabot_player import VagabotPlayer
from constants import Item, Faction
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
    deck: 'Deck'
    quest_deck: 'QuestDeck'
    players: list['Player']
    board_map: 'BoardMap'
    item_supply: list['ItemToken']
    turn_order: list['Player']
    turn_player: Optional['Player']
    winner: Optional['Player']

    def __init__(self, players: list['Player'] = None, factions: list['Faction'] = None) -> None:
        self.deck = BaseDeck(self)
        self.quest_deck = QuestDeck()
        self.winner = None

        if players is None:
            if factions:
                players = [self.build_player_by_faction(faction) for faction in factions]
            else:
                players = []
        self.players = players
        self.board_map = AutumnBoardMap(self)
        self.item_supply = []
        # TODO: Turn order, turn player
        self.turn_order = [player for player in self.players]
        if self.turn_order:
            self.turn_player = self.turn_order[0]
        else:
            self.turn_player = None

        self.initialize_item_supply()

        while not self.winner:
            self.turn_player.take_turn()
            next_turn_player_index = self.turn_order.index(self.turn_player) + 1
            next_turn_player_index %= len(self.turn_order)
            self.turn_player = self.turn_order[next_turn_player_index]
            for player in self.players:
                player.between_turns()

    def build_player_by_faction(self, faction: Faction) -> 'Player':
        if faction == Faction.MECHANICAL_MARQUISE_2_0:
            return MechanicalMarquiseV2Player(self)
        if faction == Faction.ELECTRIC_EYRIE:
            return ElectricEyriePlayer(self)
        if faction == Faction.AUTOMATED_ALLIANCE:
            return AutomatedAlliancePlayer(self)
        if faction == Faction.VAGABOT:
            return VagabotPlayer(self, VagabotThief())

    def clearings(self) -> list['Clearing']:
        return self.board_map.clearings

    def get_clearings_of_suit(self, suit: 'Suit') -> list['Clearing']:
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

    def get_item_if_available(self, item: 'Item') -> Optional['ItemToken']:
        for item_token in self.item_supply:
            if item_token.item == item:
                return item_token

    def win(self, player: 'Player') -> None:
        if self.winner:
            return
        self.winner = player

    def draw_card(self) -> Optional['Card']:
        return self.deck.draw_card()

    def discard_card(self, card: 'Card') -> None:
        for player in self.players:
            if player.takes_discarded_cards():
                player.handle_discarded_card(card)
                return
        self.send_card_to_discard_pile(card)

    # Skips things like Lost Souls - used to empty the Lost Souls
    def send_card_to_discard_pile(self, card: 'Card') -> None:
        if isinstance(card, DominanceCard):
            self.deck.dominance_region.append(card)
        else:
            self.deck.discard_pile.append(card)

    def craft_item(self, item: Item, player: 'Player', score_points: int) -> None:
        item_token = self.get_item_if_available(item)
        if item_token:
            self.item_supply.remove(item_token)
            player.get_item(item_token)
            player.add_victory_points(score_points)

# TODO: Remove after testing
# gg = Game(factions=[Faction.MECHANICAL_MARQUISE_2_0, Faction.ELECTRIC_EYRIE, Faction.AUTOMATED_ALLIANCE, Faction.VAGABOT])

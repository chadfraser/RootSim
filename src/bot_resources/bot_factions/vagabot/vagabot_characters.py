from __future__ import annotations
from abc import ABC, abstractmethod

from bot_resources.bot_factions.vagabot.vagabot_player import VagabotPlayer
from locations.clearing import Clearing
from deck.cards.item_card import ItemCard
from sort_utils import sort_players_by_victory_points, sort_players_by_setup_order, sort_players_by_pieces_in_clearing


class VagabotCharacter(ABC):
    def __init__(self, player: VagabotPlayer, name: str, starting_item_amount: int = 4) -> None:
        self.player = player
        self.name = name
        self.starting_item_amount = starting_item_amount

    @abstractmethod
    def perform_special_action(self):
        pass

    def can_perform_special_action(self) -> bool:
        return False


class VagabotThief(VagabotCharacter):
    def __init__(self, player: VagabotPlayer) -> None:
        super().__init__(player, 'Thief')

    def perform_special_action(self) -> None:
        pawn_location = self.player.piece_stock.get_pawn_location()
        if not isinstance(pawn_location, Clearing):
            return
        players_in_clearing = [player for player in pawn_location.get_all_other_players_in_location(self.player) if
                               len(player.hand) > 0]
        sorted_players_in_clearing = sort_players_by_setup_order(players_in_clearing)
        sorted_players_in_clearing = sort_players_by_pieces_in_clearing(sorted_players_in_clearing, pawn_location)
        sorted_players_in_clearing = sort_players_by_victory_points(sorted_players_in_clearing)
        if not sorted_players_in_clearing:
            return
        # discard a random card from 'target's hand
        # TODO: Even though worthless
        # sorted_players_in_clearing[0].discard_down_to_hand_limit()
        self.player.add_victory_points(1)

    def can_perform_special_action(self) -> bool:
        pawn_location = self.player.get_pawn_location()
        if not isinstance(pawn_location, Clearing):
            return False
        return any(len(player.hand) > 0 for player in pawn_location.get_all_other_players_in_location(self.player))


class VagabotRanger(VagabotCharacter):
    def __init__(self, player: VagabotPlayer) -> None:
        super().__init__(player, 'Ranger')

    def perform_special_action(self) -> None:
        if not self.player.damaged_items:
            return
        for item in self.player.damaged_items:
            # Repair an unexhausted item if possible
            if not item.is_exhausted:
                return self.player.repair_item(item)
        # Repair any damaged item if none are unexhausted
        return self.player.repair_item(self.player.damaged_items[0])

    def can_perform_special_action(self) -> bool:
        return self.player.damaged_items


class VagabotTinker(VagabotCharacter):
    def __init__(self, player: VagabotPlayer) -> None:
        super().__init__(player, 'Tinker', starting_item_amount=3)

    def perform_special_action(self) -> None:
        for card in reversed(self.player.game.deck.discard_pile):
            if isinstance(card, ItemCard) and card.can_be_crafted(self.player):
                return self.player.game.craft_item(card.item, self.player, score_points=0)

    def can_perform_special_action(self) -> bool:
        for card in reversed(self.player.game.deck.discard_pile):
            if isinstance(card, ItemCard) and card.can_be_crafted(self.player):
                return True
        return False

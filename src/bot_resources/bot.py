from __future__ import annotations
from abc import ABC
from collections import defaultdict
import random
from typing import Optional, TYPE_CHECKING

from bot_resources.bot_constants import BotDifficulty
from deck.cards.item_card import ItemCard
from locations.location import Location
from pieces.building import Building
from player_resources.player import Player

if TYPE_CHECKING:
    from bot_resources.trait import Trait
    from constants import Faction
    from deck.cards.card import Card
    from game import Game
    from locations.clearing import Clearing
    from pieces.piece import Piece
    from player_resources.piece_stock import PieceStock


class Bot(Player, ABC):
    difficulty: 'BotDifficulty'
    order_card: Optional['Card']
    traits: list['Trait']

    def __init__(self, game: 'Game', faction: 'Faction', piece_stock: 'PieceStock' = None,
                 difficulty: 'BotDifficulty' = BotDifficulty.BEGINNER, traits: list['Trait'] = None) -> None:
        if traits is None:
            traits = []

        super().__init__(game, faction, piece_stock)
        self.difficulty = difficulty
        self.order_card = None
        self.traits = traits

    def get_corner_homeland(self) -> 'Clearing':
        corner_clearings = self.game.board_map.get_corner_clearings()
        # The only corner clearings that start with buildings or tokens on them are homeland corner clearings
        corner_homelands = [clearing for clearing in corner_clearings if clearing.get_total_token_count() > 0 or
                            clearing.get_total_building_count() > 0]
        if len(corner_homelands) == 3:
            return [clearing for clearing in corner_clearings if clearing not in corner_homelands][0]
        else:
            random.shuffle(corner_homelands)
            return corner_homelands[0]

    def reveal_order(self) -> None:
        self.order_card = self.game.draw_card()
        if not self.order_card:
            self.game.win(self)  # Instant win to prevent a softlock if the deck and discard pile are both empty
        if isinstance(self.order_card, ItemCard) and self.order_card.can_be_crafted(self):
            self.game.craft_item(self.order_card.item, self, 1)

    def get_ruled_ordered_clearings(self) -> list['Clearing']:
        return self.get_ruled_suited_clearings(self.order_card.suit)

    def has_trait(self, trait: 'Trait') -> bool:
        return trait in self.traits

    def add_card_to_hand(self, card: Optional['Card']) -> None:
        self.add_victory_points(1)
        if card:
            self.game.discard_card(card)

    def place_pieces_in_one_of_clearings(self, pieces_to_place: list['Piece'], sorted_clearings: list['Clearing'],
                                         ignore_building_slots: bool = False) -> None:
        if not pieces_to_place:
            return
        # Ensure that we can place the pieces in the given clearings
        valid_placing_clearings = [clearing for clearing in sorted_clearings if
                                   clearing.can_place_pieces(self, pieces_to_place)]

        # If we couldn't place the pieces anywhere, check if it was due to a snare, and remove that snare if so
        if not valid_placing_clearings:
            self.remove_snare_if_it_prevents_placing(pieces_to_place, sorted_clearings, ignore_building_slots)
            return
        self.supply.relocate_pieces(self, pieces_to_place, valid_placing_clearings[0])

    def place_pieces_spread_among_clearings(self, pieces_to_place: list['Piece'], sorted_clearings: list['Clearing'],
                                            ignore_building_slots: bool = False) -> None:
        if not pieces_to_place:
            return
        clearings_to_place_in: dict[Clearing, list[Piece]] = defaultdict(list)

        # Ensure that we can place the pieces in the given clearings
        valid_placing_clearings = [clearing for clearing in sorted_clearings if
                                   clearing.can_place_pieces(self, pieces_to_place)]

        # If we couldn't place the pieces anywhere, check if it was due to a snare, and remove that snare if so
        if not valid_placing_clearings:
            self.remove_snare_if_it_prevents_placing(pieces_to_place, sorted_clearings, ignore_building_slots)
            return

        # Evenly spread the pieces along the valid clearings as much as possible, with the remainder going to those
        # clearings first in the list
        for idx, piece in enumerate(pieces_to_place):
            clearing_index = idx % len(valid_placing_clearings)
            target_clearing = valid_placing_clearings[clearing_index]
            clearings_to_place_in[target_clearing].append(piece)
        for clearing, pieces in clearings_to_place_in.items():
            self.supply.relocate_pieces(self, pieces, clearing)

    # Checks all sorted clearings in order, and finds the first one that has a snare and would otherwise allow the
    # piece to be placed. Removes the snare from that clearing
    def remove_snare_if_it_prevents_placing(self, pieces_to_place: list['Piece'], sorted_clearings: list['Clearing'],
                                            ignore_building_slots: bool = False) -> bool:
        for clearing in sorted_clearings:
            pieces_in_clearing = clearing.get_pieces()
            for piece in pieces_to_place:
                # If the issue is not having enough building slots in this clearing, skip that clearing. It's not due
                # to a snare
                if (isinstance(piece, Building) and clearing.get_open_building_slot_count() == 0 and
                        not ignore_building_slots):
                    continue
                # Check if the clearing has any snares - if not, skip that clearing
                # ...
                for piece_already_in_clearing in pieces_in_clearing:
                    # Add 'if piece is not snare'. If so, continue
                    if piece_already_in_clearing.prevents_piece_being_placed_by_player(self, piece):
                        continue
                # Remove the snare from the clearing and return True
        return False

    # Checks that the origin clearing has a snare, and that the pieces would be able to move to at least one clearing
    # otherwise. If so, removes the snare from the origin clearing
    # Currently relies on the fact that only the Snare restricts movement out of a clearing, but this can be adjusted
    # if need be in the future
    def remove_snare_if_it_prevents_movement(self, pieces_to_move: list['Piece'], origin_clearing: 'Clearing',
                                             sorted_destinations: list['Location'],
                                             requires_rule: bool = True) -> bool:
        # Check if the origin clearing has any snares - if not, return
        # ...
        for destination in sorted_destinations:
            # Skip clearings that you can't move to because of rule
            if (requires_rule and isinstance(destination, Clearing) and not
                    (self.does_rule_clearing(origin_clearing) or self.does_rule_clearing(destination))):
                continue
            if destination.can_move_pieces_into(self, pieces_to_move):
                # Remove the snare from the origin clearing and return
                return True
        return False

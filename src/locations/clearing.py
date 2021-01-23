from __future__ import annotations
from collections import deque
from typing import Optional, TYPE_CHECKING

from locations.location import Location
from pieces.building import Building

if TYPE_CHECKING:
    from constants import Suit
    from game import Game
    from locations.forest import Forest
    from pieces.piece import Piece
    from pieces.ruin import Ruin
    from player_resources.player import Player


class Clearing(Location):
    suit: 'Suit'
    priority: int
    total_building_slots: int
    path_connected_clearings: set['Clearing']
    river_connected_clearings: set['Clearing']
    adjacent_forests: set['Forest']
    ruin: Optional['Ruin']
    is_corner_clearing: bool
    opposite_corner_clearing: Optional['Clearing']

    def __init__(self, game: 'Game', suit: 'Suit', priority: int, total_building_slots: int,
                 is_corner_clearing: bool = False) -> None:
        super().__init__(game)
        self.suit = suit
        self.priority = priority
        self.total_building_slots = total_building_slots
        self.path_connected_clearings = set()
        self.river_connected_clearings = set()
        self.adjacent_forests = set()
        self.ruin = None
        self.is_corner_clearing = is_corner_clearing
        self.opposite_corner_clearing = None

    # TODO: Remove after testing
    def __repr__(self):
        return str(self.priority) + str(self.suit.value)

    def __lt__(self, other):
        return self.priority < other.priority

    def __eq__(self, other):
        return isinstance(other, Clearing) and self.priority == other.priority

    def __hash__(self):
        return hash(self.priority)

    ###########################################
    #                                         #
    # Initial connections + adjacency + setup #
    #                                         #
    ###########################################

    def connect_clearing_by_path(self, other_clearing: 'Clearing') -> None:
        self.path_connected_clearings.add(other_clearing)
        other_clearing.path_connected_clearings.add(self)

    def connect_clearing_by_river(self, other_clearing: 'Clearing') -> None:
        self.river_connected_clearings.add(other_clearing)
        other_clearing.river_connected_clearings.add(self)

    def mark_forest_as_adjacent_to_self(self, forest: 'Forest') -> None:
        self.adjacent_forests.add(forest)
        forest.adjacent_clearings.add(self)

    def mark_corner_clearings_as_opposite(self, opposing_clearing: 'Clearing') -> None:
        self.opposite_corner_clearing = opposing_clearing
        opposing_clearing.opposite_corner_clearing = self

    def add_ruin(self, ruin: 'Ruin') -> None:
        self.ruin = ruin

    ##################################################################
    #                                                                #
    # Permission checks for placing or moving pieces in the location #
    #                                                                #
    ##################################################################

    # ignore_building_slots: Revolt, Sanctify - things that will remove the occupying buildings before placing
    def can_place_piece(self, player: 'Player', piece: 'Piece', ignore_building_slots: bool = False) -> bool:
        if isinstance(piece, Building) and self.get_open_building_slot_count() == 0 and not ignore_building_slots:
            return False
        pieces_in_clearing = self.get_pieces()
        for piece_already_in_clearing in pieces_in_clearing:
            # Keep, Snare, limits on Sympathy/Roost/Trade Post
            if piece_already_in_clearing.prevents_piece_being_placed_by_player(player, piece):
                return False
        return True

    # Only CC can move out of Snare clearings
    def can_move_piece_out_of(self, player: 'Player', piece: 'Piece') -> bool:
        pieces_in_clearing = self.get_pieces()
        for piece_already_in_clearing in pieces_in_clearing:
            # Snare
            if piece_already_in_clearing.prevents_piece_being_moved_out_by_player(player, piece):
                return False
        return True

    def can_move_piece(self, player: 'Player', piece: 'Piece', destination: 'Location',
                       requires_rule: bool = False) -> bool:
        # We'll never look for rule in move that isn't from one clearing to another clearing
        if requires_rule and isinstance(destination, Clearing):
            if not player.does_rule_clearing(self) and not player.does_rule_clearing(destination):
                return False
        return super().can_move_piece(player, piece, destination, requires_rule)

    ###############################
    #                             #
    # Special clearing attributes #
    #                             #
    ###############################

    def get_open_building_slot_count(self) -> int:
        used_building_slot_count = 0
        for piece_map in self.pieces.values():
            used_building_slot_count += len(piece_map.buildings)
        if self.ruin:
            used_building_slot_count += 1
        return self.total_building_slots - used_building_slot_count

    def explore_ruin(self, player: 'Player') -> None:
        if not self.ruin or not self.ruin.items:
            return
        item_gained = self.ruin.items[0]
        player.get_item(self.ruin.items[0])
        self.ruin.items.remove(item_gained)
        if not self.ruin.items:
            self.ruin = None

    ###################################
    #                                 #
    # Finding paths between clearings #
    #                                 #
    ###################################

    # For Vagabot movement primarily
    # Ignore move:
    def find_shortest_legal_paths_to_destination_clearing(self, player: 'Player', moving_piece: Piece,
                                                          destination: 'Clearing',
                                                          ignore_move: bool = False) -> list[list['Clearing']]:
        if self == destination:
            return [[]]
        if not destination.can_move_piece_into(player, moving_piece):
            return []

        clearing_paths = deque([[self]])
        all_shortest_paths: list[list[Clearing]] = []

        while clearing_paths:
            current_path = clearing_paths.popleft()
            current_clearing = current_path[-1]

            for adjacent_clearing in player.get_adjacent_clearings(current_clearing):
                # Don't double back on yourself - that adds to the path length uselessly
                if adjacent_clearing in current_path:
                    continue
                # Skip impossible moves, unless ignore_move is True
                if not ignore_move and not current_clearing.can_move_piece(player, moving_piece, adjacent_clearing):
                    continue
                next_path = [c for c in current_path]
                next_path.append(adjacent_clearing)
                if adjacent_clearing == destination:
                    all_shortest_paths.append(current_path)
                # Breadth-first-search: Once we find a path to the destination N clearings away, we know no path to
                # the destination is shorter than N, so don't add any more to the clearing_paths queue
                elif not all_shortest_paths:
                    if adjacent_clearing.can_move_piece_into(player, moving_piece):
                        clearing_paths.append(next_path)

        return all_shortest_paths

    # TODO: Defenseless vagabond, Ferocious Rivetfolk
    # TODO: FIX! THIS IGNORES STUFF LIKE RIVETFOLK GARRISON
    def get_players_with_defenseless_pieces(self) -> list['Player']:
        players_with_defenseless_pieces = []
        for player in self.pieces:
            if player.is_defenseless(self):
                players_with_defenseless_pieces.append(player)
        return players_with_defenseless_pieces
        # players_with_defenseless_pieces = []
        # for player, piece_map in self.pieces.items():
        #     if len(piece_map.warriors) != 0:
        #         continue
        #     if len(piece_map.tokens) > 0 or len(piece_map.buildings) > 0:
        #         players_with_defenseless_pieces.append(player)
        # return players_with_defenseless_pieces

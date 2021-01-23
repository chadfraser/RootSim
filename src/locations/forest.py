from __future__ import annotations
from collections import deque
from typing import TYPE_CHECKING

from constants import Faction
from locations.clearing import Clearing
from locations.location import Location
from sort_utils import sort_clearings_by_priority

if TYPE_CHECKING:
    from pieces.piece import Piece
    from player_resources.player import Player


class Forest(Location):
    adjacent_clearings: set['Clearing']
    adjacent_forests: set['Forest']

    def __init__(self, game) -> None:
        super().__init__(game)
        self.adjacent_clearings = set()
        self.adjacent_forests = set()
        self.name = ''

    def mark_forest_as_adjacent_to_self(self, forest: 'Forest') -> None:
        self.adjacent_forests.add(forest)
        forest.adjacent_forests.add(self)

    def mark_clearing_as_adjacent_to_self(self, clearing: 'Clearing') -> None:
        self.adjacent_clearings.add(clearing)
        clearing.adjacent_forests.add(self)

    def initialize_name(self) -> None:
        sorted_adjacent_clearings = sort_clearings_by_priority([clearing for clearing in self.adjacent_clearings])
        self.name = '_'.join(sorted_adjacent_clearings)  # TODO: Fix Type Hinting issues

    # Only VV can move into a forest
    def can_move_piece_into(self, player: 'Player', piece: 'Piece') -> bool:
        return player.faction == Faction.VAGABOT

    ###################################
    #                                 #
    # Finding paths between clearings #
    #                                 #
    ###################################

    # For Vagabot movement primarily
    def find_shortest_legal_paths_to_destination_clearing(self, player: 'Player', moving_piece: 'Piece',
                                                          destination: 'Clearing',
                                                          ignore_move: bool = False) -> list[list['Clearing']]:
        if not destination.can_move_piece_into(player, moving_piece):
            return []

        # TODO: Test and clean
        clearing_paths: deque[list[Clearing]] = deque([[]])
        all_shortest_paths: list[list[Clearing]] = []

        while clearing_paths:
            current_path = clearing_paths.popleft()
            if not current_path:
                current_location = self
            else:
                current_location = current_path[-1]

            for adjacent_clearing in player.get_adjacent_clearings(current_location):
                # Don't double back on yourself - that adds to the path length uselessly
                if adjacent_clearing in current_path:
                    continue
                # Skip impossible moves, unless ignore_move is True
                if not ignore_move and not current_location.can_move_piece(player, moving_piece, adjacent_clearing):
                    continue
                next_path = [c for c in current_path]
                next_path.append(adjacent_clearing)
                if adjacent_clearing == destination:
                    path_ignoring_forest = [c for c in next_path if isinstance(c, Clearing)]
                    if path_ignoring_forest:
                        if all_shortest_paths and len(all_shortest_paths[0]) < len(next_path):
                            continue
                        all_shortest_paths.append(path_ignoring_forest)
                # Breadth-first-search: Once we find a path to the destination N clearings away, we know no path to
                # the destination is shorter than N, so don't add any more to the clearing_paths queue
                elif not all_shortest_paths:
                    clearing_paths.append(next_path)

        return all_shortest_paths

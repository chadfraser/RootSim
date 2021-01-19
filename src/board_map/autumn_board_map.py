from __future__ import annotations
import random

from board_map.board_map import BoardMap
from constants import RUIN_ITEMS, Suit
from game import Game
from locations.clearing import Clearing
from locations.forest import Forest
from pieces.item_token import ItemToken
from pieces.ruin import Ruin


AUTUMN_MAP_BUILDING_SLOTS_FOR_PRIORITY_CLEARING = [1, 2, 1, 1, 2, 2, 2, 2, 2, 2, 3, 2]
AUTUMN_MAP_DEFAULT_SUITS_FOR_PRIORITY_CLEARING = [
    Suit.FOX,
    Suit.MOUSE,
    Suit.RABBIT,
    Suit.RABBIT,
    Suit.RABBIT,
    Suit.FOX,
    Suit.MOUSE,
    Suit.FOX,
    Suit.MOUSE,
    Suit.RABBIT,
    Suit.MOUSE,
    Suit.FOX
]
AUTUMN_MAP_RUINS_LOCATIONS = [6, 10, 11, 12]
AUTUMN_MAP_CORNER_CLEARING_OPPOSITES = {1: 3, 2: 4, 3: 1, 4: 2}


class AutumnBoardMap(BoardMap):
    def __init__(self, game: Game) -> None:
        super().__init__(game)

    def initialize_forests(self) -> None:
        self.create_forests()
        self.mark_adjacent_forests_to_forests()
        if self.clearings:
            self.mark_adjacent_forests_to_clearings()

    def initialize_clearings(self) -> None:
        ruins = self.initialize_ruins()
        suits = AUTUMN_MAP_DEFAULT_SUITS_FOR_PRIORITY_CLEARING
        # TODO: Game options to shuffle clearing suits
        self.create_clearings(suits, ruins)
        self.initialize_opposite_corner_clearings()
        self.connect_clearings_by_path()
        self.connect_clearings_by_river()
        if self.forests:
            self.mark_adjacent_forests_to_clearings()

    def create_clearings(self, suits: list[Suit], ruins: list[Ruin]) -> None:
        for i in range(12):
            clearing = Clearing(self.game,
                                suit=suits[i],
                                priority=i+1,
                                total_building_slots=AUTUMN_MAP_BUILDING_SLOTS_FOR_PRIORITY_CLEARING[i],
                                is_corner_clearing=(i < 4))
            if i+1 in AUTUMN_MAP_RUINS_LOCATIONS and ruins:
                clearing.add_ruin(ruins.pop())
            self.clearings.append(clearing)

    # 0: Top of board
    # 1: Top-left
    # 2: Top-right and middle, connected to five clearings
    # 3: Left, connected to bottom-left clearing
    # 4: Bottom-right and middle, connected to bottom-right clearing
    # 5: Far right, connected to bottom-right clearing
    # 6: Bottom, connected to bottom-left clearing
    def create_forests(self) -> None:
        for i in range(7):
            self.forests.append(Forest(self.game))

    def mark_adjacent_forests_to_forests(self) -> None:
        # A bit of redundancy in adjacency A->B and then B->A later, but the adjacency method is idempotent and it
        # makes the adjacencies between the forests much clearer
        forest_adjacency = {0: [1, 2],
                            1: [0, 2, 3],
                            2: [0, 1, 4, 5],
                            3: [1, 6],
                            4: [2, 5, 6],
                            5: [2, 4],
                            6: [3, 4]}
        for origin_index, destination_forests in forest_adjacency.items():
            for destination_index in destination_forests:
                self.forests[origin_index].mark_forest_as_adjacent_to_self(self.forests[destination_index])

    def mark_adjacent_forests_to_clearings(self) -> None:
        clearing_forest_adjacency = {1: [0, 1],
                                     2: [0, 2],
                                     3: [4, 5],
                                     4: [3, 6],
                                     5: [0],
                                     6: [2, 5],
                                     7: [4, 6],
                                     8: [6],
                                     9: [1, 3],
                                     10: [0, 1, 2],
                                     11: [2, 4, 5],
                                     12: [1, 2, 3, 4, 6]}
        for origin_priority, destination_forests in clearing_forest_adjacency.items():
            for destination_index in destination_forests:
                self.get_clearing(origin_priority).mark_forest_as_adjacent_to_self(self.forests[destination_index])

    def connect_clearings_by_path(self) -> None:
        # A bit of redundancy in connection A->B and then B->A later, but the connection method is idempotent and it
        # makes the connections between the clearings much clearer
        clearing_path_connections = {1: [5, 9, 10],
                                     2: [5, 6, 10],
                                     3: [6, 7, 11],
                                     4: [8, 9, 12],
                                     5: [1, 2],
                                     6: [2, 3, 11],
                                     7: [3, 8, 12],
                                     8: [4, 7],
                                     9: [1, 4, 12],
                                     10: [1, 2, 12],
                                     11: [3, 6, 12],
                                     12: [4, 7, 9, 10, 11]}
        for origin_priority, destination_clearings in clearing_path_connections.items():
            for destination_priority in destination_clearings:
                self.get_clearing(origin_priority).connect_clearing_by_path(self.get_clearing(destination_priority))

    def connect_clearings_by_river(self) -> None:
        clearing_river_connections = {1: 7,
                                      7: 11,
                                      11: 10,
                                      10: 5}
        for origin_priority, destination_priority in clearing_river_connections.items():
            self.get_clearing(origin_priority).connect_clearing_by_river(self.get_clearing(destination_priority))

    def initialize_opposite_corner_clearings(self):
        for first_clearing, opposite_clearing in AUTUMN_MAP_CORNER_CLEARING_OPPOSITES.items():
            self.get_clearing(first_clearing).mark_corner_clearings_as_opposite(self.get_clearing(opposite_clearing))

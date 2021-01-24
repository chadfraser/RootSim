from __future__ import annotations
from typing import TYPE_CHECKING

from pieces.building import Building
from pieces.token import Token
from pieces.warrior import Warrior

if TYPE_CHECKING:
    from locations.location import Location
    from pieces.piece import Piece
    from player_resources.player import Player


class PlayerPieceMap:
    player: 'Player'
    location: 'Location'
    warriors: list['Warrior']
    buildings: list['Building']
    tokens: list['Token']
    other: list['Piece']

    def __init__(self, player: 'Player', location: 'Location') -> None:
        self.player = player
        self.location = location
        self.warriors = []
        self.buildings = []
        self.tokens = []
        self.other = []  # Pawn for Vagabond

    def add_piece(self, piece: 'Piece') -> None:
        if isinstance(piece, Warrior):
            self.add_warrior(piece)
        elif isinstance(piece, Building):
            self.add_building(piece)
        elif isinstance(piece, Token):
            self.add_token(piece)
        else:
            self.add_other(piece)

    def add_warrior(self, warrior: 'Warrior') -> None:
        self.warriors.append(warrior)

    def add_building(self, building: 'Building') -> None:
        self.buildings.append(building)

    def add_token(self, token: 'Token') -> None:
        self.tokens.append(token)

    def add_other(self, piece: 'Piece') -> None:
        self.other.append(piece)

    def remove_piece(self, piece: 'Piece') -> None:
        if isinstance(piece, Warrior):
            self.remove_warrior(piece)
        elif isinstance(piece, Building):
            self.remove_building(piece)
        elif isinstance(piece, Token):
            self.remove_token(piece)
        else:
            self.remove_other(piece)

    def remove_warrior(self, warrior: 'Warrior') -> None:
        try:
            self.warriors.remove(warrior)
        except ValueError:
            pass

    def remove_building(self, building: 'Building') -> None:
        try:
            self.buildings.remove(building)
        except ValueError:
            pass

    def remove_token(self, token: 'Token') -> None:
        try:
            self.tokens.remove(token)
        except ValueError:
            pass

    def remove_other(self, piece: 'Piece') -> None:
        try:
            self.other.remove(piece)
        except ValueError:
            pass

    def get_count_of_pieces(self) -> int:
        return len(self.get_all_pieces())

    def get_all_pieces(self) -> list['Piece']:
        return [piece for piece_list in (self.warriors, self.buildings, self.tokens, self.other)
                for piece in piece_list]

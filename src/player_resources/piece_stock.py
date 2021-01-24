from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pieces.building import Building
    from pieces.piece import Piece
    from pieces.token import Token
    from pieces.warrior import Warrior
    from player_resources.player import Player


class PieceStock:
    player: Player
    warriors: list['Warrior']
    buildings: list['Building']
    tokens: list['Token']
    other_pieces: list['Piece']

    def __init__(self, player: Player, warriors: list['Warrior'] = None, buildings: list['Building'] = None,
                 tokens: list['Token'] = None, other_pieces: list['Piece'] = None) -> None:
        if warriors is None:
            warriors = []
        if buildings is None:
            buildings = []
        if tokens is None:
            tokens = []
        if other_pieces is None:
            other_pieces = []

        self.player = player
        self.warriors = warriors
        self.buildings = buildings
        self.tokens = tokens
        self.other_pieces = other_pieces

    @property
    def pieces(self) -> list['Piece']:
        return [piece for piece_list in (self.warriors, self.buildings, self.tokens, self.other_pieces)
                for piece in piece_list]

from __future__ import annotations
from typing import Type, TYPE_CHECKING

from locations.location import Location

if TYPE_CHECKING:
    from game import Game
    from pieces.building import Building
    from pieces.piece import Piece
    from pieces.token import Token
    from pieces.warrior import Warrior
    from player_resources.player import Player


class Supply(Location):
    def __init__(self, game: 'Game', player: 'Player') -> None:
        super().__init__(game)
        self.player = player

    def get_pieces(self) -> list['Piece']:
        return self.get_pieces_for_player(self.player)

    def get_warriors(self) -> list['Warrior']:
        return self.get_warriors_for_player(self.player)

    def get_buildings(self) -> list['Building']:
        return self.get_buildings_for_player(self.player)

    def get_tokens(self) -> list['Token']:
        return self.get_tokens_for_player(self.player)

    def get_other_pieces(self) -> list['Piece']:
        return self.get_other_pieces_for_player(self.player)

    def get_pieces_of_type(self, class_name: Type['Piece']) -> list['Piece']:
        return [x for x in self.get_pieces() if isinstance(x, class_name)]

    def __str__(self) -> str:
        return f'{self.player} Supply'

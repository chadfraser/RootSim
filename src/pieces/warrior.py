from __future__ import annotations
from typing import TYPE_CHECKING

from pieces.piece import Piece

if TYPE_CHECKING:
    from player_resources.player import Player


class Warrior(Piece):
    def __init__(self, player: 'Player') -> None:
        super().__init__(player, 'Warrior')

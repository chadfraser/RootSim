from __future__ import annotations
from typing import TYPE_CHECKING

from pieces.piece import Piece

if TYPE_CHECKING:
    from player_resources.player import Player


class Building(Piece):
    def __init__(self, player: Player, name: str) -> None:
        super().__init__(player, name)

    def get_score_for_removal(self) -> int:
        return 1

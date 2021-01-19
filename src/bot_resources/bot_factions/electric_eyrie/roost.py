from __future__ import annotations
from typing import TYPE_CHECKING

from pieces.building import Building
from pieces.piece import Piece

if TYPE_CHECKING:
    from bot_resources.bot_factions.electric_eyrie.electric_eyrie_player import ElectricEyriePlayer


class Roost(Building):
    def __init__(self, player: ElectricEyriePlayer) -> None:
        super().__init__(player, 'Roost')

    def prevents_piece_being_placed_by_player(self, player: ElectricEyriePlayer, piece: Piece):
        return isinstance(piece, Roost)

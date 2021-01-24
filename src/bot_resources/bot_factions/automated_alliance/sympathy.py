from __future__ import annotations
from typing import TYPE_CHECKING

from pieces.token import Token

if TYPE_CHECKING:
    from bot_resources.bot_factions.automated_alliance.automated_alliance_player import AutomatedAlliancePlayer
    from pieces.piece import Piece


class Sympathy(Token):
    def __init__(self, player: 'AutomatedAlliancePlayer') -> None:
        super().__init__(player, 'Sympathy')

    def prevents_piece_being_placed_by_player(self, player: 'AutomatedAlliancePlayer', piece: 'Piece') -> bool:
        return isinstance(piece, Sympathy)

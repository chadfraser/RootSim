from __future__ import annotations
from typing import TYPE_CHECKING

from pieces.token import Token

if TYPE_CHECKING:
    from bot_resources.bot_factions.mechanical_marquise_v2.mechanical_marquise_v2_player import \
        MechanicalMarquiseV2Player
    from pieces.piece import Piece


class Keep(Token):
    def __init__(self, player: 'MechanicalMarquiseV2Player') -> None:
        super().__init__(player, 'The Keep')

    def prevents_piece_being_placed_by_player(self, player: 'MechanicalMarquiseV2Player', piece: Piece) -> bool:
        return player != self.player

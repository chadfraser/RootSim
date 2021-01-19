from __future__ import annotations
from typing import TYPE_CHECKING, cast

from bot_resources.bot_factions.vagabot.pawn import Pawn
from player_resources.piece_stock import PieceStock

if TYPE_CHECKING:
    from bot_resources.bot_factions.vagabot.vagabot_player import VagabotPlayer
    from locations.location import Location


class VagabotPieceStock(PieceStock):
    def __init__(self, player: VagabotPlayer) -> None:
        other_pieces = [Pawn(player)]

        super().__init__(player, other_pieces=other_pieces)

    def get_pawn(self) -> Pawn:
        return cast(Pawn, self.other_pieces[0])

    def get_pawn_location(self) -> Location:
        return self.get_pawn().location

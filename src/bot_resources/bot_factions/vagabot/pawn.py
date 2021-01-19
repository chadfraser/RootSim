from __future__ import annotations

from bot_resources.bot_factions.vagabot.vagabot_player import VagabotPlayer
from locations.clearing import Clearing
from pieces.piece import Piece


class Pawn(Piece):
    def __init__(self, player: VagabotPlayer) -> None:
        super().__init__(player, 'Vagabot')

    def resolve_effects_on_attempting_to_remove_self(self) -> None:
        if isinstance(self.location, Clearing):
            self.player.suffer_damage(self.location, 3, self.player, False)

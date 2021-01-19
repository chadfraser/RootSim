from __future__ import annotations
from typing import TYPE_CHECKING

from bot_resources.bot_factions.mechanical_marquise_v2.keep import Keep
from bot_resources.bot_factions.mechanical_marquise_v2.recruiter import Recruiter
from bot_resources.bot_factions.mechanical_marquise_v2.sawmill import Sawmill
from bot_resources.bot_factions.mechanical_marquise_v2.workshop import Workshop
from pieces.warrior import Warrior
from player_resources.piece_stock import PieceStock

if TYPE_CHECKING:
    from bot_resources.bot_factions.mechanical_marquise_v2.mechanical_marquise_v2_building import \
        MechanicalMarquiseV2Building
    from bot_resources.bot_factions.mechanical_marquise_v2.mechanical_marquise_v2_player import \
        MechanicalMarquiseV2Player
    from pieces.token import Token


class MechanicalMarquiseV2PieceStock(PieceStock):
    def __init__(self, player: MechanicalMarquiseV2Player) -> None:
        warriors = [Warrior(player) for _ in range(25)]

        buildings: list[MechanicalMarquiseV2Building] = [Sawmill(player) for _ in range(6)]
        buildings.extend([Workshop(player) for _ in range(6)])
        buildings.extend([Recruiter(player)for _ in range(6)])

        tokens: list[Token] = [Keep(player)]

        super().__init__(player, warriors, buildings, tokens)

    def get_sawmills(self) -> list[Sawmill]:
        sawmills = [building for building in self.buildings if isinstance(building, Sawmill)]
        return sawmills

    def get_workshops(self) -> list[Workshop]:
        workshops = [building for building in self.buildings if isinstance(building, Workshop)]
        return workshops

    def get_recruiters(self) -> list[Recruiter]:
        recruiters = [building for building in self.buildings if isinstance(building, Recruiter)]
        return recruiters

    def get_keep(self) -> Keep:
        return [token for token in self.tokens if isinstance(token, Keep)][0]

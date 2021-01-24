from __future__ import annotations
from typing import TYPE_CHECKING

from bot_resources.bot_factions.mechanical_marquise_v2.mechanical_marquise_v2_building import \
    MechanicalMarquiseV2Building
from constants import Suit

if TYPE_CHECKING:
    from bot_resources.bot_factions.mechanical_marquise_v2.mechanical_marquise_v2_player import \
        MechanicalMarquiseV2Player


class Sawmill(MechanicalMarquiseV2Building):
    def __init__(self, player: 'MechanicalMarquiseV2Player') -> None:
        super().__init__(player, 'Sawmill', Suit.FOX)

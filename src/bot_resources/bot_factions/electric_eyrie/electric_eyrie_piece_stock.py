from __future__ import annotations
from __future__ import annotations
from typing import TYPE_CHECKING

from bot_resources.bot_factions.electric_eyrie.roost import Roost
from pieces.warrior import Warrior
from player_resources.piece_stock import PieceStock

if TYPE_CHECKING:
    from bot_resources.bot_factions.electric_eyrie.electric_eyrie_player import ElectricEyriePlayer


class ElectricEyriePieceStock(PieceStock):
    def __init__(self, player: 'ElectricEyriePlayer') -> None:
        warriors = [Warrior(player) for _ in range(20)]
        buildings = [Roost(player) for _ in range(7)]

        super().__init__(player, warriors, buildings)

    def get_roosts(self) -> list['Roost']:
        return [building for building in self.buildings if isinstance(building, Roost)]

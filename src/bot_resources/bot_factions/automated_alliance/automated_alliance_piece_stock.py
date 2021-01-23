from __future__ import annotations
from typing import TYPE_CHECKING

from bot_resources.bot_factions.automated_alliance.base import Base
from bot_resources.bot_factions.automated_alliance.sympathy import Sympathy
from constants import Suit
from pieces.warrior import Warrior
from player_resources.piece_stock import PieceStock

if TYPE_CHECKING:
    from bot_resources.bot_factions.automated_alliance.automated_alliance_player import AutomatedAlliancePlayer


class AutomatedAlliancePieceStock(PieceStock):
    def __init__(self, player: 'AutomatedAlliancePlayer') -> None:
        warriors = [Warrior(player) for _ in range(10)]
        buildings = [Base(player, suit) for suit in [Suit.FOX, Suit.RABBIT, Suit.MOUSE]]
        tokens = [Sympathy(player) for _ in range(10)]

        super().__init__(player, warriors, buildings, tokens)

    def get_bases(self) -> list['Base']:
        return [building for building in self.buildings if isinstance(building, Base)]

    def get_sympathy(self) -> list['Sympathy']:
        return [token for token in self.tokens if isinstance(token, Sympathy)]

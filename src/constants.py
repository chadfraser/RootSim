from __future__ import annotations
from enum import Enum


class Faction(Enum):
    MECHANICAL_MARQUISE_2_0 = 'Mechanical Marquise 2.0'
    ELECTRIC_EYRIE = 'Electric Eyrie'
    AUTOMATED_ALLIANCE = 'Automated Alliance'
    VAGABOT = 'Vagabot',
    COGWHEEL_CULT = 'Cogwheel Cult',
    RIVETFOLK = 'Rivetfolk',
    DUMMY_DUCHY = 'Dummy Duchy',
    CONTRAPTION_CONSPIRACY = 'Contraption Conspiracy'

    def is_ruin_exploring_faction(self) -> bool:
        return self == Faction.VAGABOT


class Suit(Enum):
    FOX = 'Fox'
    RABBIT = 'Rabbit'
    MOUSE = 'Mouse'
    BIRD = 'Bird'

    # If other is a bird card, it matches anything
    # If this is a bird card, it only matches a bird card
    @staticmethod
    def are_suits_equal(this, other: Suit) -> bool:
        return this.value == other.value or other == Suit.BIRD


class Item(Enum):
    BAG = 'Bag'
    BOOT = 'Boot'
    COIN = 'Coin'
    CROSSBOW = 'Crossbow'
    HAMMER = 'Hammer'
    SWORD = 'Sword'
    TEAPOT = 'Teapot'
    TORCH = 'Torch'


FACTION_SETUP_ORDER = [
    Faction.MECHANICAL_MARQUISE_2_0,
    Faction.ELECTRIC_EYRIE,
    Faction.AUTOMATED_ALLIANCE,
    Faction.VAGABOT,
    Faction.COGWHEEL_CULT,
    Faction.RIVETFOLK,
    Faction.DUMMY_DUCHY,
    Faction.CONTRAPTION_CONSPIRACY
]

RUIN_ITEMS = [Item.BAG, Item.BOOT, Item.HAMMER, Item.SWORD]

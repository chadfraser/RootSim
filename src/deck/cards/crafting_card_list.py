from __future__ import annotations

from constants import Suit
from deck.cards.crafting_card import CraftingCard


class StandAndDeliver(CraftingCard):
    def __init__(self) -> None:
        super().__init__('Stand And Deliver', Suit.FOX)


class TaxCollector(CraftingCard):
    def __init__(self) -> None:
        super().__init__('Tax Collector', Suit.FOX)


class Cobbler(CraftingCard):
    def __init__(self) -> None:
        super().__init__('Cobbler', Suit.RABBIT)


class CommandWarren(CraftingCard):
    def __init__(self) -> None:
        super().__init__('Command Warren', Suit.RABBIT)


class BetterBurrowBank(CraftingCard):
    def __init__(self) -> None:
        super().__init__('Better Burrow Bank', Suit.RABBIT)


class Codebreakers(CraftingCard):
    def __init__(self) -> None:
        super().__init__('Codebreakers', Suit.MOUSE)


class ScoutingParty(CraftingCard):
    def __init__(self) -> None:
        super().__init__('Scouting Party', Suit.MOUSE)


class Sappers(CraftingCard):
    def __init__(self) -> None:
        super().__init__('Sappers', Suit.BIRD)


class Armorers(CraftingCard):
    def __init__(self) -> None:
        super().__init__('Armorers', Suit.BIRD)


class BrutalTactics(CraftingCard):
    def __init__(self) -> None:
        super().__init__('Brutal Tactics', Suit.BIRD)


class RoyalClaim(CraftingCard):
    def __init__(self) -> None:
        super().__init__('Royal Claim', Suit.BIRD)


class FavorOfTheFoxes(CraftingCard):
    def __init__(self) -> None:
        super().__init__('Favor of the Foxes', Suit.FOX)


class FavorOfTheRabbits(CraftingCard):
    def __init__(self) -> None:
        super().__init__('Favor of the Rabbits', Suit.RABBIT)


class FavorOfTheMice(CraftingCard):
    def __init__(self) -> None:
        super().__init__('Favor of the Mice', Suit.MOUSE)

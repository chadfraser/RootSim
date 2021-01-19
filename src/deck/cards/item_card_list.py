from __future__ import annotations

from constants import Item, Suit
from deck.cards.item_card import ItemCard


# FOX: Boot, bag, hammer, teapot, sword, coin
class TravelGearFox(ItemCard):
    def __init__(self) -> None:
        super().__init__('Travel Gear', Suit.FOX, Item.BOOT, 1)


class GentlyUsedKnapsack(ItemCard):
    def __init__(self) -> None:
        super().__init__('Gently Used Knapsack', Suit.FOX, Item.BAG, 1)


class Anvil(ItemCard):
    def __init__(self) -> None:
        super().__init__('Anvil', Suit.FOX, Item.HAMMER, 2)


class RootTeaFox(ItemCard):
    def __init__(self) -> None:
        super().__init__('Root Tea', Suit.FOX, Item.TEAPOT, 2)


class FoxfolkSteel(ItemCard):
    def __init__(self) -> None:
        super().__init__('Foxfolk Steel', Suit.FOX, Item.SWORD, 2)


class ProtectionRacket(ItemCard):
    def __init__(self) -> None:
        super().__init__('Protection Racket', Suit.FOX, Item.COIN, 3)


# RABBIT: Boot, bag, teapot, coin
class AVisitToFriends(ItemCard):
    def __init__(self) -> None:
        super().__init__('A Visit to Friends', Suit.RABBIT, Item.BOOT, 1)


class SmugglersTrail(ItemCard):
    def __init__(self) -> None:
        super().__init__("Smuggler's Trail", Suit.RABBIT, Item.BAG, 1)


class RootTeaRabbit(ItemCard):
    def __init__(self) -> None:
        super().__init__('Root Tea', Suit.RABBIT, Item.TEAPOT, 2)


class BakeSale(ItemCard):
    def __init__(self) -> None:
        super().__init__('Bake Sale', Suit.RABBIT, Item.COIN, 3)


# MOUSE: Boot, bag, crossbow, sword, teapot, coin
class TravelGearMouse(ItemCard):
    def __init__(self) -> None:
        super().__init__('Travel Gear', Suit.MOUSE, Item.BOOT, 1)


class MouseInASack(ItemCard):
    def __init__(self) -> None:
        super().__init__('Mouse-in-a-Sack', Suit.MOUSE, Item.BAG, 1)


class CrossbowMouse(ItemCard):
    def __init__(self) -> None:
        super().__init__('Crossbow', Suit.MOUSE, Item.CROSSBOW, 1)


class Sword(ItemCard):
    def __init__(self) -> None:
        super().__init__('Sword', Suit.MOUSE, Item.SWORD, 2)


class RootTeaMouse(ItemCard):
    def __init__(self) -> None:
        super().__init__('Root Tea', Suit.MOUSE, Item.TEAPOT, 2)


class Investments(ItemCard):
    def __init__(self) -> None:
        super().__init__('Investments', Suit.MOUSE, Item.COIN, 3)


# BIRD: Boot, bag, crossbow, sword
class WoodlandRunners(ItemCard):
    def __init__(self) -> None:
        super().__init__('Woodland Runners', Suit.BIRD, Item.BOOT, 1)


class BirdyBindle(ItemCard):
    def __init__(self) -> None:
        super().__init__('Birdy Bindle', Suit.BIRD, Item.BAG, 1)


class CrossbowBird(ItemCard):
    def __init__(self) -> None:
        super().__init__('Crossbow', Suit.BIRD, Item.CROSSBOW, 1)


class ArmsDealer(ItemCard):
    def __init__(self) -> None:
        super().__init__('Arms Dealer', Suit.BIRD, Item.SWORD, 2)


def generate_all_item_cards() -> list[ItemCard]:
    return [
        # Fox cards
        TravelGearFox(),
        GentlyUsedKnapsack(),
        Anvil(),
        FoxfolkSteel(),
        RootTeaFox(),
        ProtectionRacket(),
        # Rabbit cards
        AVisitToFriends(),
        SmugglersTrail(),
        RootTeaRabbit(),
        BakeSale(),
        # Mouse cards
        TravelGearMouse(),
        MouseInASack(),
        CrossbowMouse(),
        Sword(),
        RootTeaMouse(),
        Investments(),
        # Bird cards
        WoodlandRunners(),
        BirdyBindle(),
        CrossbowBird(),
        ArmsDealer()
    ]

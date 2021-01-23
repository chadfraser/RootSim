from __future__ import annotations
from typing import TYPE_CHECKING

from player_resources.supply import Supply

if TYPE_CHECKING:
    from game import Game
    from pieces.item_token import ItemToken
    from player_resources.player import Player


class Satchel(Supply):
    undamaged_items: list['ItemToken']
    damaged_items: list['ItemToken']
    battle_track: list['ItemToken']

    def __init__(self, game: Game, player: Player) -> None:
        super().__init__(game, player)
        self.undamaged_items = []
        self.damaged_items = []
        self.battle_track = []

    def get_exhausted_undamaged_items(self, item_count: int = 1) -> list['ItemToken']:
        items = []
        for item in self.undamaged_items:
            if item.is_exhausted:
                items.append(item)
                if len(items) == item_count:
                    break
        return items

    def get_unexhausted_undamaged_items(self, item_count: int = 1) -> list['ItemToken']:
        items = []
        for item in self.undamaged_items:
            if not item.is_exhausted:
                items.append(item)
                if len(items) == item_count:
                    break
        return items

    def get_exhausted_damaged_items(self, item_count: int = 1) -> list['ItemToken']:
        items = []
        for item in self.damaged_items:
            if item.is_exhausted:
                items.append(item)
                if len(items) == item_count:
                    break
        return items

    def get_unexhausted_damaged_items(self, item_count: int = 1) -> list['ItemToken']:
        items = []
        for item in self.damaged_items:
            if not item.is_exhausted:
                items.append(item)
                if len(items) == item_count:
                    break
        return items

    def exhaust_items_if_possible(self, item_count: int = 1) -> bool:
        items_to_exhaust = self.get_unexhausted_undamaged_items(item_count)
        if len(items_to_exhaust) < item_count:
            return False
        for item in items_to_exhaust:
            item.is_exhausted = True
        return True

    def add_item(self, item: 'ItemToken') -> None:
        item.is_exhausted = False
        if self.get_total_item_count() in [5, 8, 11]:
            self.battle_track.append(item)
        else:
            self.undamaged_items.append(item)

    def refresh_item(self) -> None:
        item_to_refresh = self.get_exhausted_undamaged_items()
        if not item_to_refresh:
            item_to_refresh = self.get_exhausted_damaged_items()
        if not item_to_refresh:
            return
        item_to_refresh[0].is_exhausted = False

    def repair_item(self) -> None:
        item_to_repair = self.get_unexhausted_damaged_items()
        if not item_to_repair:
            item_to_repair = self.get_exhausted_damaged_items()
        if not item_to_repair:
            return
        self.damaged_items.remove(item_to_repair[0])
        self.undamaged_items.append(item_to_repair[0])

    def damage_specific_item(self, item: 'ItemToken') -> None:
        if item not in self.undamaged_items:
            return
        self.undamaged_items.remove(item)
        self.damaged_items.append(item)

    def repair_all_items(self) -> None:
        while self.damaged_items:
            item = self.damaged_items.pop()
            self.undamaged_items.append(item)

    def get_total_item_count(self) -> int:
        return len(self.undamaged_items) + len(self.damaged_items) + len(self.battle_track)

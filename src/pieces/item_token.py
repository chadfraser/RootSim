from __future__ import annotations
from typing import TYPE_CHECKING

from pieces.piece import Piece

if TYPE_CHECKING:
    from constants import Item


class ItemToken(Piece):
    item: 'Item'
    is_starting_item: bool
    is_ruin_item: bool
    is_exhausted: bool

    def __init__(self, item: 'Item', is_starting_item: bool = False, is_ruin_item: bool = False) -> None:
        super().__init__(player=None, name='')
        self.item = item
        self.is_starting_item = is_starting_item
        self.is_ruin_item = is_ruin_item
        self.is_exhausted = False

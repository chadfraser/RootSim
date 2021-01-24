from unittest.mock import Mock

from board_map.autumn_board_map import AutumnBoardMap
from board_map.board_map import BoardMap
from constants import RUIN_ITEMS, Suit
from locations.clearing import Clearing
from pieces.item_token import ItemToken
from pieces.ruin import Ruin


# TODO: Test, along with adjacents clearings to forests, forests to clearings, path-clearings, and river-clearings,
# TODO: Ruin clearings, corner clearings, and opposite-corner clearings
# TODO: Maybe test with random suits too?
# def test_adjacent_forests_to_forests():
#     mock_game = Mock()
#     board_map = AutumnBoardMap(mock_game)
#
#     assert board_map.forests[0].adjacent_forests == []

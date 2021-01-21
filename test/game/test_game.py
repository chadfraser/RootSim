from unittest import TestCase
from unittest.mock import Mock, patch

from board_map.board_map import BoardMap
from constants import Suit
from game import Game
from locations.clearing import Clearing


class TestGame(TestCase):
    # @patch('board_map.autumn_board_map.AutumnBoardMap')
    def test_get_clearing(self):
        game = Game()
        clearing1 = Clearing(game, Suit.FOX, priority=1, total_building_slots=1)
        clearing2 = Clearing(game, Suit.FOX, priority=2, total_building_slots=1)
        game.board_map.clearings = [clearing1, clearing2]

        self.assertEqual(game.clearings(), [clearing1, clearing2])

    def test_get_clearings_of_suit(self):
        game = Game()
        clearing1 = Clearing(game, Suit.FOX, priority=1, total_building_slots=1)
        clearing2 = Clearing(game, Suit.FOX, priority=2, total_building_slots=1)
        clearing3 = Clearing(game, Suit.MOUSE, priority=2, total_building_slots=1)
        game.board_map.get_clearings_of_suit.return_value = lambda c: [clearing1, clearing2, clearing3]

        self.assertEqual(game.get_clearings_of_suit(Suit.FOX), [clearing1, clearing2])

    def test_get_clearings_of_suit_bird(self):
        game = Game()
        clearing1 = Clearing(game, Suit.FOX, priority=1, total_building_slots=1)
        clearing2 = Clearing(game, Suit.FOX, priority=2, total_building_slots=1)
        clearing3 = Clearing(game, Suit.MOUSE, priority=2, total_building_slots=1)
        game.board_map.get_clearings_of_suit.return_value = lambda c: [clearing1, clearing2, clearing3]

        self.assertEqual(game.get_clearings_of_suit(Suit.BIRD), [clearing1, clearing2, clearing3])

    # TODO: All below
    # discard card
    # send card to discard pile (with and without Cultesque player; with or without Dom card)
    # craft item (is or isn't available; with or without score)
    # win
    #
    # def test_initialize_item_supply(self):
    #     game = Game()
    #     clearing1 = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=True)
    #     clearing2 = Clearing(mock_game, Suit.FOX, priority=2, total_building_slots=1, is_corner_clearing=False)
    #     board_map = BoardMap(mock_game)
    #     board_map.clearings = [clearing1, clearing2]
    #
    #     self.assertEqual(board_map.get_corner_clearings(), [clearing1])
    #
    # def test_get_number_of_items_per_ruin(self):
    #     game = Game()
    #     clearing1 = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=True)
    #     clearing2 = Clearing(mock_game, Suit.FOX, priority=2, total_building_slots=1, is_corner_clearing=False)
    #     board_map = BoardMap(mock_game)
    #     board_map.clearings = [clearing1, clearing2]
    #
    #     self.assertEqual(board_map.get_corner_clearings(), [clearing1])
    #
    # def test_get_item_if_available__true(self):
    #     game = Game()
    #     clearing1 = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=True)
    #     clearing2 = Clearing(mock_game, Suit.FOX, priority=2, total_building_slots=1, is_corner_clearing=False)
    #     board_map = BoardMap(mock_game)
    #     board_map.clearings = [clearing1, clearing2]
    #
    #     self.assertEqual(board_map.get_corner_clearings(), [clearing1])
    #
    # def test_get_item_if_available__false(self):
    #     game = Game()
    #     clearing1 = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=True)
    #     clearing2 = Clearing(mock_game, Suit.FOX, priority=2, total_building_slots=1, is_corner_clearing=False)
    #     board_map = BoardMap(mock_game)
    #     board_map.clearings = [clearing1, clearing2]
    #
    #     self.assertEqual(board_map.get_corner_clearings(), [clearing1])

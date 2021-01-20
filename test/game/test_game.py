from unittest import TestCase
from unittest.mock import Mock, patch

from board_map.board_map import BoardMap
from constants import Suit
from game import Game
from locations.clearing import Clearing


class TestGame(TestCase):
    @patch('board_map.autumn_board_map.AutumnBoardMap')
    def test_get_clearing(self, board_map_patch):
        game = Game()
        clearing1 = Clearing(game, Suit.FOX, priority=1, total_building_slots=1)
        clearing2 = Clearing(game, Suit.FOX, priority=2, total_building_slots=1)
        game.board_map.clearings = [clearing1, clearing2]

        self.assertEqual(game.clearings(), [clearing1, clearing2])

    @patch('board_map.autumn_board_map.AutumnBoardMap')
    def test_get_clearings_of_suit(self, board_map_patch):
        game = Game()
        clearing1 = Clearing(game, Suit.FOX, priority=1, total_building_slots=1)
        clearing2 = Clearing(game, Suit.FOX, priority=2, total_building_slots=1)
        clearing3 = Clearing(game, Suit.FOX, priority=2, total_building_slots=1)
        print(game)
        print('/')
        print(game.board_map)
        game.board_map.get_clearings_of_suit.return_value = [clearing1, clearing2, clearing3]

        self.assertEqual(game.get_clearings_of_suit(Suit.FOX), [clearing1, clearing2])

    # def test_get_corner_clearings(self):
    #     mock_game = Mock()
    #     clearing1 = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=True)
    #     clearing2 = Clearing(mock_game, Suit.FOX, priority=2, total_building_slots=1, is_corner_clearing=False)
    #     board_map = BoardMap(mock_game)
    #     board_map.clearings = [clearing1, clearing2]
    #
    #     self.assertEqual(board_map.get_corner_clearings(), [clearing1])

    # TODO
    # @patch('board_map.board_map.BoardMap.__abstractmethods__', set())# game.get_number_of_items_p_ruin -> 1
    # def test_initialize_ruins(self):
    #     mock_game = Mock()
    #     board_map = BoardMap(mock_game)
    #     # Assert that the result is four item tokens, BOOT, BAG, HAMMER, SWORD, in any order
    #     board_map.initialize_ruins()
    #
    # @patch('board_map.board_map.BoardMap.__abstractmethods__', set())# game.get_number_of_items_per_ruin ->
    # def test_initialize_ruins_multiple_items_per_ruin(self):
    #     mock_game = Mock()
    #     board_map = BoardMap(mock_game)
    #     # Assert that the result is eight item tokens, two of each BOOT, BAG, HAMMER, SWORD, in any order
    #     board_map.initialize_ruins()

    # @patch('board_map.board_map.BoardMap.__abstractmethods__', set())
    # def test_get_clearings_of_suit(self):
    #     mock_game = Mock()
    #     clearing1 = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1)
    #     clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1)
    #     clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1)
    #     clearing4 = Clearing(mock_game, Suit.MOUSE, priority=4, total_building_slots=1)
    #     board_map = BoardMap(mock_game)
    #     board_map.clearings = [clearing1, clearing2, clearing3, clearing4]
    #
    #     self.assertEqual(board_map.get_clearings_of_suit(Suit.FOX), [clearing1, clearing3])
    #
    # @patch('board_map.board_map.BoardMap.__abstractmethods__', set())
    # def test_get_clearings_of_suit_bird(self):
    #     mock_game = Mock()
    #     clearing1 = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1)
    #     clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1)
    #     clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1)
    #     clearing4 = Clearing(mock_game, Suit.MOUSE, priority=4, total_building_slots=1)
    #     board_map = BoardMap(mock_game)
    #     board_map.clearings = [clearing1, clearing2, clearing3, clearing4]
    #
    #     self.assertEqual(board_map.get_clearings_of_suit(Suit.BIRD), [clearing1, clearing2, clearing3, clearing4])

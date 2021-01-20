from unittest import TestCase
from unittest.mock import Mock, patch

from constants import Faction
from player_resources.player import Player


@patch('player_resources.player.Player.__abstractmethods__', set())
class TestPlayer(TestCase):
    def test_add_victory_points(self):
        mock_game = Mock()
        mock_piece_stock = Mock()
        player = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0, mock_piece_stock)
        self.assertEqual(player.victory_points, 0)
        player.add_victory_points(2)
        self.assertEqual(player.victory_points, 2)

    def test_subtract_victory_points(self):
        mock_game = Mock()
        mock_piece_stock = Mock()
        player = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0, mock_piece_stock)
        player.victory_points = 10
        player.add_victory_points(-2)
        self.assertEqual(player.victory_points, 8)

    def test_subtract_victory_points_below_0(self):
        mock_game = Mock()
        mock_piece_stock = Mock()
        player = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0, mock_piece_stock)
        player.victory_points = 1
        player.add_victory_points(-2)
        self.assertEqual(player.victory_points, 0)

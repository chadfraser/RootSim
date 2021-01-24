from unittest import TestCase
from unittest.mock import Mock, patch

from constants import Faction, Item
from pieces.item_token import ItemToken
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

    def test_get_item(self):
        mock_game = Mock()
        mock_piece_stock = Mock()
        player = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0, mock_piece_stock)

        self.assertEqual(player.crafted_items, [])
        item = ItemToken(Item.BAG)
        player.get_item(item)
        self.assertEqual(player.crafted_items, [item])


    # TODO:
    """
        get_unplaced_pieces/warriors/buildings/tokens/other
        does_rule_clearing
        get_ruled_clearings
        get_ruled_suited_clearings
        get_rule_value
        battle
        suffer_damage
        allocate_rolls_as_defender
        cap_rolled_hits
        get_bonus_hits
        is_defenseless
        give_score_for_removed_pieces_not_in_battle
        move
        move_removed_pieces_into_supply
        get_adjacent_clearings
        draw_card
        draw_cards
        add_card_to_hand
        take_random_card_from_hand
    """

from unittest import TestCase
from unittest.mock import Mock, patch

from constants import Faction, Suit
from locations.clearing import Clearing
from player_resources.player import Player
from sort_utils import sort_players_by_setup_order, sort_players_by_victory_points, sort_players_by_pieces_in_clearing, \
    sort_players_by_warriors_in_clearing, sort_players_by_buildings_in_clearing, sort_players_by_tokens_in_clearing, \
    sort_players_by_cardboard_in_clearing, sort_clearings_by_priority, sort_clearings_by_matching_suit, \
    sort_paths_by_distance, sort_paths_by_lexicographic_priority, sort_paths_by_destination_priority, \
    sort_clearings_by_enemy_pieces, sort_clearings_by_own_pieces, sort_clearings_by_enemy_buildings, \
    sort_clearings_by_enemy_warriors, sort_clearings_by_target_warriors, sort_clearings_by_own_warriors, \
    sort_clearings_by_enemy_tokens, sort_clearings_by_target_cardboard, sort_clearings_by_any_own_buildings, \
    sort_clearings_by_martial_law, sort_clearings_by_free_building_slots, sort_clearings_by_any_free_building_slots, \
    sort_clearings_by_ruled_by_self, sort_clearings_by_defenseless_enemy_buildings


@patch('player_resources.player.Player.__abstractmethods__', set())
class TestSortUtilsPlayers(TestCase):
    def test_sort_players_by_setup_order(self):
        mock_game = Mock()
        player1 = Player(mock_game, Faction.ELECTRIC_EYRIE)
        player2 = Player(mock_game, Faction.VAGABOT)
        player3 = Player(mock_game, Faction.AUTOMATED_ALLIANCE)
        players = [player1, player2, player3]

        sorted_players = sort_players_by_setup_order(players)
        self.assertEqual(sorted_players, [player1, player3, player2])

    def test_sort_players_by_setup_order_descending(self):
        mock_game = Mock()
        player1 = Player(mock_game, Faction.ELECTRIC_EYRIE)
        player2 = Player(mock_game, Faction.VAGABOT)
        player3 = Player(mock_game, Faction.AUTOMATED_ALLIANCE)
        players = [player1, player2, player3]

        sorted_players = sort_players_by_setup_order(players, descending=True)
        self.assertEqual(sorted_players, [player2, player3, player1])

    def test_sort_players_by_victory_points_descending(self):
        mock_game = Mock()
        player1 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player2 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player3 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player1.victory_points = 4
        player2.victory_points = 1
        player3.victory_points = 19

        players = [player1, player2, player3]
        sorted_players = sort_players_by_victory_points(players, descending=True)
        self.assertEqual(sorted_players, [player3, player1, player2])

    def test_sort_players_by_victory_points_ascending(self):
        mock_game = Mock()
        player1 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player2 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player3 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player1.victory_points = 4
        player2.victory_points = 1
        player3.victory_points = 19

        players = [player1, player2, player3]
        sorted_players = sort_players_by_victory_points(players, descending=False)
        self.assertEqual(sorted_players, [player2, player1, player3])

    def test_sort_players_by_victory_points_descending_stable(self):
        mock_game = Mock()
        player1 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player2 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player3 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player1.victory_points = 4
        player2.victory_points = 1
        player3.victory_points = 4

        players = [player1, player2, player3]
        sorted_players = sort_players_by_victory_points(players, descending=True)
        self.assertEqual(sorted_players, [player1, player3, player2])

    def test_sort_players_by_victory_points_ascending_stable(self):
        mock_game = Mock()
        player1 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player2 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player3 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player1.victory_points = 4
        player2.victory_points = 1
        player3.victory_points = 4

        players = [player1, player2, player3]
        sorted_players = sort_players_by_victory_points(players, descending=False)
        self.assertEqual(sorted_players, [player2, player1, player3])

    def test_sort_players_by_pieces_in_clearing_descending(self):
        mock_game = Mock()
        clearing = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=False)
        player1 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player2 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player3 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)

        def clearing_piece_count_mock(player):
            if player == player1:
                return 1
            elif player == player2:
                return 3
            elif player == player3:
                return 2

        players = [player1, player2, player3]
        with patch('locations.clearing.Clearing.get_piece_count_for_player', side_effect=clearing_piece_count_mock):
            sorted_players = sort_players_by_pieces_in_clearing(players, clearing, descending=True)
            self.assertEqual(sorted_players, [player2, player3, player1])

    def test_sort_players_by_pieces_in_clearing_ascending(self):
        mock_game = Mock()
        clearing = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=False)
        player1 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player2 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player3 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)

        def clearing_piece_count_mock(player):
            if player == player1:
                return 1
            elif player == player2:
                return 3
            elif player == player3:
                return 2

        players = [player1, player2, player3]
        with patch('locations.clearing.Clearing.get_piece_count_for_player', side_effect=clearing_piece_count_mock):
            sorted_players = sort_players_by_pieces_in_clearing(players, clearing, descending=False)
            self.assertEqual(sorted_players, [player1, player3, player2])

    def test_sort_players_by_pieces_in_clearing_descending_stable(self):
        mock_game = Mock()
        clearing = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=False)
        player1 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player2 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player3 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)

        def clearing_piece_count_mock(player):
            if player == player1:
                return 2
            elif player == player2:
                return 3
            elif player == player3:
                return 2

        players = [player1, player2, player3]
        with patch('locations.clearing.Clearing.get_piece_count_for_player', side_effect=clearing_piece_count_mock):
            sorted_players = sort_players_by_pieces_in_clearing(players, clearing, descending=True)
            self.assertEqual(sorted_players, [player2, player1, player3])

    def test_sort_players_by_pieces_in_clearing_ascending_stable(self):
        mock_game = Mock()
        clearing = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=False)
        player1 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player2 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player3 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)

        def clearing_piece_count_mock(player):
            if player == player1:
                return 2
            elif player == player2:
                return 3
            elif player == player3:
                return 2

        players = [player1, player2, player3]
        with patch('locations.clearing.Clearing.get_piece_count_for_player', side_effect=clearing_piece_count_mock):
            sorted_players = sort_players_by_pieces_in_clearing(players, clearing, descending=False)
            self.assertEqual(sorted_players, [player1, player3, player2])

    def test_sort_players_by_warriors_in_clearing_descending(self):
        mock_game = Mock()
        clearing = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=False)
        player1 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player2 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player3 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)

        def clearing_warrior_count_mock(player):
            if player == player1:
                return 1
            elif player == player2:
                return 3
            elif player == player3:
                return 2

        players = [player1, player2, player3]
        with patch('locations.clearing.Clearing.get_warrior_count_for_player', side_effect=clearing_warrior_count_mock):
            sorted_players = sort_players_by_warriors_in_clearing(players, clearing, descending=True)
            self.assertEqual(sorted_players, [player2, player3, player1])

    def test_sort_players_by_warriors_in_clearing_ascending(self):
        mock_game = Mock()
        clearing = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=False)
        player1 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player2 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player3 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)

        def clearing_warrior_count_mock(player):
            if player == player1:
                return 1
            elif player == player2:
                return 3
            elif player == player3:
                return 2

        players = [player1, player2, player3]
        with patch('locations.clearing.Clearing.get_warrior_count_for_player', side_effect=clearing_warrior_count_mock):
            sorted_players = sort_players_by_warriors_in_clearing(players, clearing, descending=False)
            self.assertEqual(sorted_players, [player1, player3, player2])

    def test_sort_players_by_warriors_in_clearing_descending_stable(self):
        mock_game = Mock()
        clearing = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=False)
        player1 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player2 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player3 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)

        def clearing_warrior_count_mock(player):
            if player == player1:
                return 2
            elif player == player2:
                return 3
            elif player == player3:
                return 2

        players = [player1, player2, player3]
        with patch('locations.clearing.Clearing.get_warrior_count_for_player', side_effect=clearing_warrior_count_mock):
            sorted_players = sort_players_by_warriors_in_clearing(players, clearing, descending=True)
            self.assertEqual(sorted_players, [player2, player1, player3])

    def test_sort_players_by_warriors_in_clearing_ascending_stable(self):
        mock_game = Mock()
        clearing = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=False)
        player1 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player2 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player3 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)

        def clearing_warrior_count_mock(player):
            if player == player1:
                return 1
            elif player == player2:
                return 3
            elif player == player3:
                return 2

        players = [player1, player2, player3]
        with patch('locations.clearing.Clearing.get_warrior_count_for_player', side_effect=clearing_warrior_count_mock):
            sorted_players = sort_players_by_warriors_in_clearing(players, clearing, descending=False)
            self.assertEqual(sorted_players, [player1, player3, player2])

    def test_sort_players_by_buildings_in_clearing_descending(self):
        mock_game = Mock()
        clearing = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=False)
        player1 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player2 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player3 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)

        def clearing_building_count_mock(player):
            if player == player1:
                return 1
            elif player == player2:
                return 3
            elif player == player3:
                return 2

        players = [player1, player2, player3]
        with patch('locations.clearing.Clearing.get_building_count_for_player',
                   side_effect=clearing_building_count_mock):
            sorted_players = sort_players_by_buildings_in_clearing(players, clearing, descending=True)
            self.assertEqual(sorted_players, [player2, player3, player1])

    def test_sort_players_by_buildings_in_clearing_ascending(self):
        mock_game = Mock()
        clearing = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=False)
        player1 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player2 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player3 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)

        def clearing_building_count_mock(player):
            if player == player1:
                return 1
            elif player == player2:
                return 3
            elif player == player3:
                return 2

        players = [player1, player2, player3]
        with patch('locations.clearing.Clearing.get_building_count_for_player',
                   side_effect=clearing_building_count_mock):
            sorted_players = sort_players_by_buildings_in_clearing(players, clearing, descending=False)
            self.assertEqual(sorted_players, [player1, player3, player2])

    def test_sort_players_by_buildings_in_clearing_descending_stable(self):
        mock_game = Mock()
        clearing = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=False)
        player1 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player2 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player3 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)

        def clearing_building_count_mock(player):
            if player == player1:
                return 2
            elif player == player2:
                return 3
            elif player == player3:
                return 2

        players = [player1, player2, player3]
        with patch('locations.clearing.Clearing.get_building_count_for_player',
                   side_effect=clearing_building_count_mock):
            sorted_players = sort_players_by_buildings_in_clearing(players, clearing, descending=True)
            assert sorted_players == [player2, player1, player3]

    def test_sort_players_by_buildings_in_clearing_ascending_stable(self):
        mock_game = Mock()
        clearing = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=False)
        player1 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player2 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player3 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)

        def clearing_building_count_mock(player):
            if player == player1:
                return 2
            elif player == player2:
                return 3
            elif player == player3:
                return 2

        players = [player1, player2, player3]
        with patch('locations.clearing.Clearing.get_building_count_for_player',
                   side_effect=clearing_building_count_mock):
            sorted_players = sort_players_by_buildings_in_clearing(players, clearing, descending=False)
            self.assertEqual(sorted_players, [player1, player3, player2])

    def test_sort_players_by_tokens_in_clearing_descending(self):
        mock_game = Mock()
        clearing = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=False)
        player1 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player2 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player3 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)

        def clearing_token_count_mock(player):
            if player == player1:
                return 1
            elif player == player2:
                return 3
            elif player == player3:
                return 2

        players = [player1, player2, player3]
        with patch('locations.clearing.Clearing.get_token_count_for_player',
                   side_effect=clearing_token_count_mock):
            sorted_players = sort_players_by_tokens_in_clearing(players, clearing, descending=True)
            self.assertEqual(sorted_players, [player2, player3, player1])

    def test_sort_players_by_tokens_in_clearing_ascending(self):
        mock_game = Mock()
        clearing = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=False)
        player1 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player2 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player3 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)

        def clearing_token_count_mock(player):
            if player == player1:
                return 1
            elif player == player2:
                return 3
            elif player == player3:
                return 2

        players = [player1, player2, player3]
        with patch('locations.clearing.Clearing.get_token_count_for_player', side_effect=clearing_token_count_mock):
            sorted_players = sort_players_by_tokens_in_clearing(players, clearing, descending=False)
            self.assertEqual(sorted_players, [player1, player3, player2])

    def test_sort_players_by_tokens_in_clearing_descending_stable(self):
        mock_game = Mock()
        clearing = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=False)
        player1 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player2 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player3 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)

        def clearing_token_count_mock(player):
            if player == player1:
                return 2
            elif player == player2:
                return 3
            elif player == player3:
                return 2

        players = [player1, player2, player3]
        with patch('locations.clearing.Clearing.get_token_count_for_player', side_effect=clearing_token_count_mock):
            sorted_players = sort_players_by_tokens_in_clearing(players, clearing, descending=True)
            self.assertEqual(sorted_players, [player2, player1, player3])

    def test_sort_players_by_tokens_in_clearing_ascending_stable(self):
        mock_game = Mock()
        clearing = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=False)
        player1 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player2 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player3 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)

        def clearing_token_count_mock(player):
            if player == player1:
                return 2
            elif player == player2:
                return 3
            elif player == player3:
                return 2

        players = [player1, player2, player3]
        with patch('locations.clearing.Clearing.get_token_count_for_player', side_effect=clearing_token_count_mock):
            sorted_players = sort_players_by_tokens_in_clearing(players, clearing, descending=False)
            self.assertEqual(sorted_players, [player1, player3, player2])

    def test_sort_players_by_cardboard_in_clearing_descending(self):
        mock_game = Mock()
        clearing = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=False)
        player1 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player2 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player3 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)

        def clearing_building_count_mock(player):
            if player == player1:
                return 1
            elif player == player2:
                return 3
            elif player == player3:
                return 0

        def clearing_token_count_mock(player):
            if player == player1:
                return 6
            elif player == player2:
                return 1
            elif player == player3:
                return 1

        players = [player1, player2, player3]
        with patch('locations.clearing.Clearing.get_token_count_for_player', side_effect=clearing_token_count_mock):
            with patch('locations.clearing.Clearing.get_building_count_for_player',
                       side_effect=clearing_building_count_mock):
                sorted_players = sort_players_by_cardboard_in_clearing(players, clearing, descending=True)
                self.assertEqual(sorted_players, [player1, player2, player3])

    def test_sort_players_by_cardboard_in_clearing_ascending(self):
        mock_game = Mock()
        clearing = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=False)
        player1 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player2 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player3 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)

        def clearing_building_count_mock(player):
            if player == player1:
                return 1
            elif player == player2:
                return 3
            elif player == player3:
                return 0

        def clearing_token_count_mock(player):
            if player == player1:
                return 6
            elif player == player2:
                return 1
            elif player == player3:
                return 1

        players = [player1, player2, player3]
        with patch('locations.clearing.Clearing.get_token_count_for_player', side_effect=clearing_token_count_mock):
            with patch('locations.clearing.Clearing.get_building_count_for_player',
                       side_effect=clearing_building_count_mock):
                sorted_players = sort_players_by_cardboard_in_clearing(players, clearing, descending=False)
                self.assertEqual(sorted_players, [player3, player2, player1])

    def test_sort_players_by_cardboard_in_clearing_descending_stable(self):
        mock_game = Mock()
        clearing = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=False)
        player1 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player2 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player3 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)

        def clearing_building_count_mock(player):
            if player == player1:
                return 1
            elif player == player2:
                return 3
            elif player == player3:
                return 0

        def clearing_token_count_mock(player):
            if player == player1:
                return 3
            elif player == player2:
                return 1
            elif player == player3:
                return 1

        players = [player1, player2, player3]
        with patch('locations.clearing.Clearing.get_token_count_for_player', side_effect=clearing_token_count_mock):
            with patch('locations.clearing.Clearing.get_building_count_for_player',
                       side_effect=clearing_building_count_mock):
                sorted_players = sort_players_by_cardboard_in_clearing(players, clearing, descending=True)
                self.assertEqual(sorted_players, [player1, player2, player3])

    def test_sort_players_by_cardboard_in_clearing_ascending_stable(self):
        mock_game = Mock()
        clearing = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=False)
        player1 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player2 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)
        player3 = Player(mock_game, Faction.MECHANICAL_MARQUISE_2_0)

        def clearing_building_count_mock(player):
            if player == player1:
                return 1
            elif player == player2:
                return 3
            elif player == player3:
                return 0

        def clearing_token_count_mock(player):
            if player == player1:
                return 3
            elif player == player2:
                return 1
            elif player == player3:
                return 1

        players = [player1, player2, player3]
        with patch('locations.clearing.Clearing.get_token_count_for_player', side_effect=clearing_token_count_mock):
            with patch('locations.clearing.Clearing.get_building_count_for_player',
                       side_effect=clearing_building_count_mock):
                sorted_players = sort_players_by_cardboard_in_clearing(players, clearing, descending=False)
                self.assertEqual(sorted_players, [player3, player1, player2])


@patch('player_resources.player.Player.__abstractmethods__', set())
class TestSortUtilsClearings(TestCase):
    def test_sort_clearings_by_priority_descending(self):
        mock_game = Mock()
        clearing1 = Clearing(mock_game, Suit.FOX, priority=9, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.FOX, priority=11, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=False)

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_priority(clearings, descending=True)
        self.assertEqual(sorted_clearings, [clearing2, clearing1, clearing3])

    def test_sort_clearings_by_priority_ascending(self):
        mock_game = Mock()
        clearing1 = Clearing(mock_game, Suit.FOX, priority=9, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.FOX, priority=11, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=False)

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_priority(clearings, descending=False)
        self.assertEqual(sorted_clearings, [clearing3, clearing1, clearing2])

    def test_sort_clearings_by_matching_suit_descending(self):
        mock_game = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.MOUSE, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_matching_suit(clearings, Suit.FOX, descending=True)
        self.assertEqual(sorted_clearings, [clearing3, clearing1, clearing2])

    def test_sort_clearings_by_matching_suit_ascending(self):
        mock_game = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.MOUSE, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_matching_suit(clearings, Suit.FOX, descending=False)
        self.assertEqual(sorted_clearings, [clearing1, clearing2, clearing3])

    def test_sort_clearings_by_matching_suit_descending_stable(self):
        mock_game = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_matching_suit(clearings, Suit.RABBIT, descending=False)
        self.assertEqual(sorted_clearings, [clearing3, clearing1, clearing2])

    def test_sort_clearings_by_matching_suit_ascending_stable(self):
        mock_game = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_matching_suit(clearings, Suit.FOX, descending=False)
        self.assertEqual(sorted_clearings, [clearing1, clearing2, clearing3])

    def test_sort_clearings_by_enemy_pieces_descending(self):
        mock_game = Mock()
        mock_player = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_total_piece_count_for_other_players = lambda c: 2
        clearing2.get_total_piece_count_for_other_players = lambda c: 3
        clearing3.get_total_piece_count_for_other_players = lambda c: 1

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_enemy_pieces(clearings, mock_player, descending=True)
        self.assertEqual(sorted_clearings, [clearing2, clearing1, clearing3])

    def test_sort_clearings_by_enemy_pieces_ascending(self):
        mock_game = Mock()
        mock_player = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_total_piece_count_for_other_players = lambda c: 2
        clearing2.get_total_piece_count_for_other_players = lambda c: 3
        clearing3.get_total_piece_count_for_other_players = lambda c: 1

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_enemy_pieces(clearings, mock_player, descending=False)
        self.assertEqual(sorted_clearings, [clearing3, clearing1, clearing2])

    def test_sort_clearings_by_enemy_pieces_descending_stable(self):
        mock_game = Mock()
        mock_player = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_total_piece_count_for_other_players = lambda c: 2
        clearing2.get_total_piece_count_for_other_players = lambda c: 2
        clearing3.get_total_piece_count_for_other_players = lambda c: 1

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_enemy_pieces(clearings, mock_player, descending=True)
        self.assertEqual(sorted_clearings, [clearing1, clearing2, clearing3])

    def test_sort_clearings_by_enemy_pieces_ascending_stable(self):
        mock_game = Mock()
        mock_player = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_total_piece_count_for_other_players = lambda c: 2
        clearing2.get_total_piece_count_for_other_players = lambda c: 2
        clearing3.get_total_piece_count_for_other_players = lambda c: 1

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_enemy_pieces(clearings, mock_player, descending=False)
        self.assertEqual(sorted_clearings, [clearing3, clearing1, clearing2])

    def test_sort_clearings_by_own_pieces_descending(self):
        mock_game = Mock()
        mock_player = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_piece_count_for_player = lambda c: 2
        clearing2.get_piece_count_for_player = lambda c: 3
        clearing3.get_piece_count_for_player = lambda c: 1

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_own_pieces(clearings, mock_player, descending=True)
        self.assertEqual(sorted_clearings, [clearing2, clearing1, clearing3])

    def test_sort_clearings_by_own_pieces_ascending(self):
        mock_game = Mock()
        mock_player = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_piece_count_for_player = lambda c: 2
        clearing2.get_piece_count_for_player = lambda c: 3
        clearing3.get_piece_count_for_player = lambda c: 1

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_own_pieces(clearings, mock_player, descending=False)
        self.assertEqual(sorted_clearings, [clearing3, clearing1, clearing2])

    def test_sort_clearings_by_own_pieces_descending_stable(self):
        mock_game = Mock()
        mock_player = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_piece_count_for_player = lambda c: 2
        clearing2.get_piece_count_for_player = lambda c: 2
        clearing3.get_piece_count_for_player = lambda c: 1

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_own_pieces(clearings, mock_player, descending=True)
        self.assertEqual(sorted_clearings, [clearing1, clearing2, clearing3])

    def test_sort_clearings_by_own_pieces_ascending_stable(self):
        mock_game = Mock()
        mock_player = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_piece_count_for_player = lambda c: 2
        clearing2.get_piece_count_for_player = lambda c: 2
        clearing3.get_piece_count_for_player = lambda c: 1

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_own_pieces(clearings, mock_player, descending=False)
        self.assertEqual(sorted_clearings, [clearing3, clearing1, clearing2])

    def test_sort_clearings_by_enemy_warriors_descending(self):
        mock_game = Mock()
        mock_player = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_total_warrior_count_for_other_players = lambda c: 2
        clearing2.get_total_warrior_count_for_other_players = lambda c: 3
        clearing3.get_total_warrior_count_for_other_players = lambda c: 1

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_enemy_warriors(clearings, mock_player, descending=True)
        self.assertEqual(sorted_clearings, [clearing2, clearing1, clearing3])

    def test_sort_clearings_by_enemy_warriors_ascending(self):
        mock_game = Mock()
        mock_player = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_total_warrior_count_for_other_players = lambda c: 2
        clearing2.get_total_warrior_count_for_other_players = lambda c: 3
        clearing3.get_total_warrior_count_for_other_players = lambda c: 1

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_enemy_warriors(clearings, mock_player, descending=False)
        self.assertEqual(sorted_clearings, [clearing3, clearing1, clearing2])

    def test_sort_clearings_by_enemy_warriors_descending_stable(self):
        mock_game = Mock()
        mock_player = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_total_warrior_count_for_other_players = lambda c: 2
        clearing2.get_total_warrior_count_for_other_players = lambda c: 2
        clearing3.get_total_warrior_count_for_other_players = lambda c: 1

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_enemy_warriors(clearings, mock_player, descending=True)
        self.assertEqual(sorted_clearings, [clearing1, clearing2, clearing3])

    def test_sort_clearings_by_enemy_warriors_ascending_stable(self):
        mock_game = Mock()
        mock_player = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_total_warrior_count_for_other_players = lambda c: 2
        clearing2.get_total_warrior_count_for_other_players = lambda c: 2
        clearing3.get_total_warrior_count_for_other_players = lambda c: 1

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_enemy_warriors(clearings, mock_player, descending=False)
        self.assertEqual(sorted_clearings, [clearing3, clearing1, clearing2])

    def test_sort_clearings_by_own_warriors_descending(self):
        mock_game = Mock()
        mock_player = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_warrior_count_for_player = lambda c: 2
        clearing2.get_warrior_count_for_player = lambda c: 3
        clearing3.get_warrior_count_for_player = lambda c: 1

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_own_warriors(clearings, mock_player, descending=True)
        self.assertEqual(sorted_clearings, [clearing2, clearing1, clearing3])

    def test_sort_clearings_by_own_warriors_ascending(self):
        mock_game = Mock()
        mock_player = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_warrior_count_for_player = lambda c: 2
        clearing2.get_warrior_count_for_player = lambda c: 3
        clearing3.get_warrior_count_for_player = lambda c: 1

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_own_warriors(clearings, mock_player, descending=False)
        self.assertEqual(sorted_clearings, [clearing3, clearing1, clearing2])

    def test_sort_clearings_by_own_warriors_descending_stable(self):
        mock_game = Mock()
        mock_player = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_warrior_count_for_player = lambda c: 2
        clearing2.get_warrior_count_for_player = lambda c: 2
        clearing3.get_warrior_count_for_player = lambda c: 1

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_own_warriors(clearings, mock_player, descending=True)
        self.assertEqual(sorted_clearings, [clearing1, clearing2, clearing3])

    def test_sort_clearings_by_own_warriors_ascending_stable(self):
        mock_game = Mock()
        mock_player = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_warrior_count_for_player = lambda c: 2
        clearing2.get_warrior_count_for_player = lambda c: 2
        clearing3.get_warrior_count_for_player = lambda c: 1

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_own_warriors(clearings, mock_player, descending=False)
        self.assertEqual(sorted_clearings, [clearing3, clearing1, clearing2])

    def test_sort_clearings_by_target_warriors_descending(self):
        mock_game = Mock()
        mock_player = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_warrior_count_for_player = lambda c: 2
        clearing2.get_warrior_count_for_player = lambda c: 3
        clearing3.get_warrior_count_for_player = lambda c: 1

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_target_warriors(clearings, mock_player, descending=True)
        self.assertEqual(sorted_clearings, [clearing2, clearing1, clearing3])

    def test_sort_clearings_by_target_warriors_ascending(self):
        mock_game = Mock()
        mock_player = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_warrior_count_for_player = lambda c: 2
        clearing2.get_warrior_count_for_player = lambda c: 3
        clearing3.get_warrior_count_for_player = lambda c: 1

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_target_warriors(clearings, mock_player, descending=False)
        self.assertEqual(sorted_clearings, [clearing3, clearing1, clearing2])

    def test_sort_clearings_by_target_warriors_descending_stable(self):
        mock_game = Mock()
        mock_player = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_warrior_count_for_player = lambda c: 2
        clearing2.get_warrior_count_for_player = lambda c: 2
        clearing3.get_warrior_count_for_player = lambda c: 1

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_target_warriors(clearings, mock_player, descending=True)
        self.assertEqual(sorted_clearings, [clearing1, clearing2, clearing3])

    def test_sort_clearings_by_target_warriors_ascending_stable(self):
        mock_game = Mock()
        mock_player = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_warrior_count_for_player = lambda c: 2
        clearing2.get_warrior_count_for_player = lambda c: 2
        clearing3.get_warrior_count_for_player = lambda c: 1

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_target_warriors(clearings, mock_player, descending=False)
        self.assertEqual(sorted_clearings, [clearing3, clearing1, clearing2])

    def test_sort_clearings_by_enemy_buildings_descending(self):
        mock_game = Mock()
        mock_player = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_total_building_count_for_other_players = lambda c: 2
        clearing2.get_total_building_count_for_other_players = lambda c: 3
        clearing3.get_total_building_count_for_other_players = lambda c: 1

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_enemy_buildings(clearings, mock_player, descending=True)
        self.assertEqual(sorted_clearings, [clearing2, clearing1, clearing3])

    def test_sort_clearings_by_enemy_buildings_ascending(self):
        mock_game = Mock()
        mock_player = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_total_building_count_for_other_players = lambda c: 2
        clearing2.get_total_building_count_for_other_players = lambda c: 3
        clearing3.get_total_building_count_for_other_players = lambda c: 1

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_enemy_buildings(clearings, mock_player, descending=False)
        self.assertEqual(sorted_clearings, [clearing3, clearing1, clearing2])

    def test_sort_clearings_by_enemy_buildings_descending_stable(self):
        mock_game = Mock()
        mock_player = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_total_building_count_for_other_players = lambda c: 2
        clearing2.get_total_building_count_for_other_players = lambda c: 2
        clearing3.get_total_building_count_for_other_players = lambda c: 1

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_enemy_buildings(clearings, mock_player, descending=True)
        self.assertEqual(sorted_clearings, [clearing1, clearing2, clearing3])

    def test_sort_clearings_by_enemy_buildings_ascending_stable(self):
        mock_game = Mock()
        mock_player = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_total_building_count_for_other_players = lambda c: 2
        clearing2.get_total_building_count_for_other_players = lambda c: 2
        clearing3.get_total_building_count_for_other_players = lambda c: 1

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_enemy_buildings(clearings, mock_player, descending=False)
        self.assertEqual(sorted_clearings, [clearing3, clearing1, clearing2])

    def test_sort_clearings_by_enemy_tokens_descending(self):
        mock_game = Mock()
        mock_player = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_total_token_count_for_other_players = lambda c: 2
        clearing2.get_total_token_count_for_other_players = lambda c: 3
        clearing3.get_total_token_count_for_other_players = lambda c: 1

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_enemy_tokens(clearings, mock_player, descending=True)
        self.assertEqual(sorted_clearings, [clearing2, clearing1, clearing3])

    def test_sort_clearings_by_enemy_tokens_ascending(self):
        mock_game = Mock()
        mock_player = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_total_token_count_for_other_players = lambda c: 2
        clearing2.get_total_token_count_for_other_players = lambda c: 3
        clearing3.get_total_token_count_for_other_players = lambda c: 1

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_enemy_tokens(clearings, mock_player, descending=False)
        self.assertEqual(sorted_clearings, [clearing3, clearing1, clearing2])

    def test_sort_clearings_by_enemy_tokens_descending_stable(self):
        mock_game = Mock()
        mock_player = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_total_token_count_for_other_players = lambda c: 2
        clearing2.get_total_token_count_for_other_players = lambda c: 2
        clearing3.get_total_token_count_for_other_players = lambda c: 1

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_enemy_tokens(clearings, mock_player, descending=True)
        self.assertEqual(sorted_clearings, [clearing1, clearing2, clearing3])

    def test_sort_clearings_by_enemy_tokens_ascending_stable(self):
        mock_game = Mock()
        mock_player = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_total_token_count_for_other_players = lambda c: 2
        clearing2.get_total_token_count_for_other_players = lambda c: 2
        clearing3.get_total_token_count_for_other_players = lambda c: 1

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_enemy_tokens(clearings, mock_player, descending=False)
        self.assertEqual(sorted_clearings, [clearing3, clearing1, clearing2])

    def test_sort_clearings_by_target_cardboard_descending(self):
        mock_game = Mock()
        mock_player = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_building_count_for_player = lambda c: 1
        clearing1.get_token_count_for_player = lambda c: 6
        clearing2.get_building_count_for_player = lambda c: 3
        clearing2.get_token_count_for_player = lambda c: 1
        clearing3.get_building_count_for_player = lambda c: 0
        clearing3.get_token_count_for_player = lambda c: 1

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_target_cardboard(clearings, mock_player, descending=True)
        self.assertEqual(sorted_clearings, [clearing1, clearing2, clearing3])

    def test_sort_clearings_by_target_cardboard_ascending(self):
        mock_game = Mock()
        mock_player = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_building_count_for_player = lambda c: 1
        clearing1.get_token_count_for_player = lambda c: 6
        clearing2.get_building_count_for_player = lambda c: 3
        clearing2.get_token_count_for_player = lambda c: 1
        clearing3.get_building_count_for_player = lambda c: 0
        clearing3.get_token_count_for_player = lambda c: 1

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_target_cardboard(clearings, mock_player, descending=False)
        self.assertEqual(sorted_clearings, [clearing3, clearing2, clearing1])

    def test_sort_clearings_by_target_cardboard_descending_stable(self):
        mock_game = Mock()
        mock_player = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_building_count_for_player = lambda c: 1
        clearing1.get_token_count_for_player = lambda c: 3
        clearing2.get_building_count_for_player = lambda c: 3
        clearing2.get_token_count_for_player = lambda c: 1
        clearing3.get_building_count_for_player = lambda c: 0
        clearing3.get_token_count_for_player = lambda c: 1

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_target_cardboard(clearings, mock_player, descending=True)
        self.assertEqual(sorted_clearings, [clearing1, clearing2, clearing3])

    def test_sort_clearings_by_target_cardboard_ascending_stable(self):
        mock_game = Mock()
        mock_player = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_building_count_for_player = lambda c: 1
        clearing1.get_token_count_for_player = lambda c: 3
        clearing2.get_building_count_for_player = lambda c: 3
        clearing2.get_token_count_for_player = lambda c: 1
        clearing3.get_building_count_for_player = lambda c: 0
        clearing3.get_token_count_for_player = lambda c: 1

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_target_cardboard(clearings, mock_player, descending=False)
        self.assertEqual(sorted_clearings, [clearing3, clearing1, clearing2])

    def test_sort_clearings_by_any_own_buildings_descending(self):
        mock_game = Mock()
        mock_player = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_building_count_for_player = lambda c: 1
        clearing2.get_building_count_for_player = lambda c: 2
        clearing3.get_building_count_for_player = lambda c: 0

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_any_own_buildings(clearings, mock_player, descending=True)
        self.assertEqual(sorted_clearings, [clearing1, clearing2, clearing3])

    def test_sort_clearings_by_any_own_buildings_ascending(self):
        mock_game = Mock()
        mock_player = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_building_count_for_player = lambda c: 1
        clearing2.get_building_count_for_player = lambda c: 2
        clearing3.get_building_count_for_player = lambda c: 0

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_any_own_buildings(clearings, mock_player, descending=False)
        self.assertEqual(sorted_clearings, [clearing3, clearing1, clearing2])

    def test_sort_clearings_by_martial_law_descending(self):
        mock_game = Mock()
        mock_player = Mock()
        mock_player_2 = Mock()
        mock_player_3 = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_warrior_count_for_all_players = lambda: {mock_player_2: 3, mock_player_3: 0}
        clearing2.get_warrior_count_for_all_players = lambda: {mock_player_2: 0, mock_player_3: 3}
        clearing3.get_warrior_count_for_all_players = lambda: {mock_player_2: 0, mock_player_3: 2}

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_martial_law(clearings, mock_player, descending=True)
        self.assertEqual(sorted_clearings, [clearing3, clearing1, clearing2])

    def test_sort_clearings_by_martial_law_ascending(self):
        mock_game = Mock()
        mock_player = Mock()
        mock_player_2 = Mock()
        mock_player_3 = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_warrior_count_for_all_players = lambda: {mock_player_2: 3, mock_player_3: 0}
        clearing2.get_warrior_count_for_all_players = lambda: {mock_player_2: 0, mock_player_3: 3}
        clearing3.get_warrior_count_for_all_players = lambda: {mock_player_2: 0, mock_player_3: 2}

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_martial_law(clearings, mock_player, descending=False)
        self.assertEqual(sorted_clearings, [clearing1, clearing2, clearing3])

    def test_sort_clearings_by_martial_law_does_not_sum_warriors(self):
        mock_game = Mock()
        mock_player = Mock()
        mock_player_2 = Mock()
        mock_player_3 = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_warrior_count_for_all_players = lambda: {mock_player_2: 2, mock_player_3: 2}
        clearing2.get_warrior_count_for_all_players = lambda: {mock_player_2: 0, mock_player_3: 3}
        clearing3.get_warrior_count_for_all_players = lambda: {mock_player_2: 0, mock_player_3: 2}

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_martial_law(clearings, mock_player, descending=True)
        self.assertEqual(sorted_clearings, [clearing1, clearing3, clearing2])

    def test_sort_clearings_by_martial_law_ignores_own_warriors(self):
        mock_game = Mock()
        mock_player = Mock()
        mock_player_2 = Mock()
        mock_player_3 = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_warrior_count_for_all_players = lambda: {mock_player: 3, mock_player_2: 0, mock_player_3: 0}
        clearing2.get_warrior_count_for_all_players = lambda: {mock_player: 0, mock_player_2: 0, mock_player_3: 3}
        clearing3.get_warrior_count_for_all_players = lambda: {mock_player: 0, mock_player_2: 0, mock_player_3: 2}

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_martial_law(clearings, mock_player, descending=True)
        self.assertEqual(sorted_clearings, [clearing1, clearing3, clearing2])

    def test_sort_clearings_by_free_building_slots_descending(self):
        mock_game = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=3, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=0, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_free_building_slots(clearings, descending=True)
        self.assertEqual(sorted_clearings, [clearing1, clearing3, clearing2])

    def test_sort_clearings_by_free_building_slots_ascending(self):
        mock_game = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=3, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=0, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_free_building_slots(clearings, descending=False)
        self.assertEqual(sorted_clearings, [clearing2, clearing3, clearing1])

    def test_sort_clearings_by_free_building_slots_descending_stable(self):
        mock_game = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=3, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_free_building_slots(clearings, descending=True)
        self.assertEqual(sorted_clearings, [clearing2, clearing1, clearing3])

    def test_sort_clearings_by_free_building_slots_ascending_stable(self):
        mock_game = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=3, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_free_building_slots(clearings, descending=False)
        self.assertEqual(sorted_clearings, [clearing1, clearing3, clearing2])

    def test_sort_clearings_by_any_free_building_slots_descending(self):
        mock_game = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=0, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_building_count_for_player = lambda c: 1
        clearing2.get_building_count_for_player = lambda c: 2
        clearing3.get_building_count_for_player = lambda c: 0

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_any_free_building_slots(clearings, descending=True)
        self.assertEqual(sorted_clearings, [clearing1, clearing3, clearing2])

    def test_sort_clearings_by_any_free_building_slots_ascending(self):
        mock_game = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=0, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        clearing1.get_building_count_for_player = lambda c: 1
        clearing2.get_building_count_for_player = lambda c: 2
        clearing3.get_building_count_for_player = lambda c: 0

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_any_free_building_slots(clearings, descending=False)
        self.assertEqual(sorted_clearings, [clearing2, clearing1, clearing3])

    def test_sort_clearings_by_ruled_by_self_descending(self):
        mock_game = Mock()
        mock_player = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        mock_player.does_rule_clearing = lambda c: c == clearing1 or c == clearing3

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_ruled_by_self(clearings, mock_player, descending=True)
        self.assertEqual(sorted_clearings, [clearing1, clearing3, clearing2])

    def test_sort_clearings_by_ruled_by_self_ascending(self):
        mock_game = Mock()
        mock_player = Mock()
        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        mock_player.does_rule_clearing = lambda c: c == clearing1 or c == clearing3

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_ruled_by_self(clearings, mock_player, descending=False)
        self.assertEqual(sorted_clearings, [clearing2, clearing1, clearing3])

    def test_sort_clearings_by_defenseless_enemy_buildings_descending(self):
        mock_game = Mock()
        mock_player = Mock()
        mock_player_2 = Mock()

        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=3, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=3, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=3, is_corner_clearing=False)
        clearing1.get_building_count_for_player = lambda p: 1 if p == mock_player_2 else 0
        clearing1.get_all_other_players_in_location = lambda p: [mock_player_2]
        clearing2.get_building_count_for_player = lambda p: 2 if p == mock_player_2 else 0
        clearing2.get_all_other_players_in_location = lambda p: [mock_player_2]
        clearing3.get_building_count_for_player = lambda p: 3 if p == mock_player_2 else 0
        clearing3.get_all_other_players_in_location = lambda p: [mock_player_2]

        mock_player_2.is_defenseless = lambda c: True

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_defenseless_enemy_buildings(clearings, mock_player, descending=True)
        self.assertEqual(sorted_clearings, [clearing3, clearing2, clearing1])

    def test_sort_clearings_by_defenseless_enemy_buildings_ascending(self):
        mock_game = Mock()
        mock_player = Mock()
        mock_player_2 = Mock()

        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=3, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=3, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=3, is_corner_clearing=False)
        clearing1.get_building_count_for_player = lambda p: 1 if p == mock_player_2 else 0
        clearing1.get_all_other_players_in_location = lambda p: [mock_player_2]
        clearing2.get_building_count_for_player = lambda p: 2 if p == mock_player_2 else 0
        clearing2.get_all_other_players_in_location = lambda p: [mock_player_2]
        clearing3.get_building_count_for_player = lambda p: 3 if p == mock_player_2 else 0
        clearing3.get_all_other_players_in_location = lambda p: [mock_player_2]

        mock_player_2.is_defenseless = lambda c: True

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_defenseless_enemy_buildings(clearings, mock_player, descending=False)
        self.assertEqual(sorted_clearings, [clearing1, clearing2, clearing3])

    def test_sort_clearings_by_defenseless_enemy_buildings_descending_stable(self):
        mock_game = Mock()
        mock_player = Mock()
        mock_player_2 = Mock()

        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=3, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=3, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=3, is_corner_clearing=False)
        clearing1.get_building_count_for_player = lambda p: 3 if p == mock_player_2 else 0
        clearing1.get_all_other_players_in_location = lambda p: [mock_player_2]
        clearing2.get_building_count_for_player = lambda p: 2 if p == mock_player_2 else 0
        clearing2.get_all_other_players_in_location = lambda p: [mock_player_2]
        clearing3.get_building_count_for_player = lambda p: 3 if p == mock_player_2 else 0
        clearing3.get_all_other_players_in_location = lambda p: [mock_player_2]

        mock_player_2.is_defenseless = lambda c: True

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_defenseless_enemy_buildings(clearings, mock_player, descending=True)
        self.assertEqual(sorted_clearings, [clearing1, clearing3, clearing2])

    def test_sort_clearings_by_defenseless_enemy_buildings_ascending_stable(self):
        mock_game = Mock()
        mock_player = Mock()
        mock_player_2 = Mock()

        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=3, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=3, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=3, is_corner_clearing=False)
        clearing1.get_building_count_for_player = lambda p: 3 if p == mock_player_2 else 0
        clearing1.get_all_other_players_in_location = lambda p: [mock_player_2]
        clearing2.get_building_count_for_player = lambda p: 2 if p == mock_player_2 else 0
        clearing2.get_all_other_players_in_location = lambda p: [mock_player_2]
        clearing3.get_building_count_for_player = lambda p: 3 if p == mock_player_2 else 0
        clearing3.get_all_other_players_in_location = lambda p: [mock_player_2]

        mock_player_2.is_defenseless = lambda c: True

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_defenseless_enemy_buildings(clearings, mock_player, descending=False)
        self.assertEqual(sorted_clearings, [clearing2, clearing1, clearing3])

    def test_sort_clearings_by_defenseless_enemy_buildings_descending_multiple_players(self):
        mock_game = Mock()
        mock_player = Mock()
        mock_player_2 = Mock()
        mock_player_3 = Mock()

        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=3, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=3, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=3, is_corner_clearing=False)
        clearing1.get_building_count_for_player = lambda p: 1 if p == mock_player_2 else 2
        clearing1.get_all_other_players_in_location = lambda p: [mock_player_2, mock_player_3]
        clearing2.get_building_count_for_player = lambda p: 2 if p == mock_player_2 else 0
        clearing2.get_all_other_players_in_location = lambda p: [mock_player_2, mock_player_3]
        clearing3.get_building_count_for_player = lambda p: 0 if p == mock_player_2 else 1
        clearing3.get_all_other_players_in_location = lambda p: [mock_player_2, mock_player_3]

        mock_player_2.is_defenseless = lambda c: True
        mock_player_3.is_defenseless = lambda c: True

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_defenseless_enemy_buildings(clearings, mock_player, descending=True)
        self.assertEqual(sorted_clearings, [clearing1, clearing2, clearing3])

    def test_sort_clearings_by_defenseless_enemy_buildings_ascending_multiple_players(self):
        mock_game = Mock()
        mock_player = Mock()
        mock_player_2 = Mock()
        mock_player_3 = Mock()

        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=3, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=3, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=3, is_corner_clearing=False)
        clearing1.get_building_count_for_player = lambda p: 1 if p == mock_player_2 else 2
        clearing1.get_all_other_players_in_location = lambda p: [mock_player_2, mock_player_3]
        clearing2.get_building_count_for_player = lambda p: 2 if p == mock_player_2 else 0
        clearing2.get_all_other_players_in_location = lambda p: [mock_player_2, mock_player_3]
        clearing3.get_building_count_for_player = lambda p: 0 if p == mock_player_2 else 1
        clearing3.get_all_other_players_in_location = lambda p: [mock_player_2, mock_player_3]

        mock_player_2.is_defenseless = lambda c: True
        mock_player_3.is_defenseless = lambda c: True

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_defenseless_enemy_buildings(clearings, mock_player, descending=False)
        self.assertEqual(sorted_clearings, [clearing3, clearing2, clearing1])

    def test_sort_clearings_by_defenseless_enemy_buildings_descending_not_defenseless(self):
        mock_game = Mock()
        mock_player = Mock()
        mock_player_2 = Mock()
        mock_player_3 = Mock()

        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=3, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=3, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=3, is_corner_clearing=False)
        clearing1.get_building_count_for_player = lambda p: 1 if p == mock_player_2 else 2
        clearing1.get_all_other_players_in_location = lambda p: [mock_player_2, mock_player_3]
        clearing2.get_building_count_for_player = lambda p: 2 if p == mock_player_2 else 0
        clearing2.get_all_other_players_in_location = lambda p: [mock_player_2, mock_player_3]
        clearing3.get_building_count_for_player = lambda p: 0 if p == mock_player_2 else 1
        clearing3.get_all_other_players_in_location = lambda p: [mock_player_2, mock_player_3]

        mock_player_2.is_defenseless = lambda c: False
        mock_player_3.is_defenseless = lambda c: True

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_defenseless_enemy_buildings(clearings, mock_player, descending=True)
        self.assertEqual(sorted_clearings, [clearing1, clearing3, clearing2])

    def test_sort_clearings_by_defenseless_enemy_buildings_ascending_not_defenseless(self):
        mock_game = Mock()
        mock_player = Mock()
        mock_player_2 = Mock()
        mock_player_3 = Mock()

        clearing1 = Clearing(mock_game, Suit.RABBIT, priority=1, total_building_slots=3, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.RABBIT, priority=2, total_building_slots=3, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=3, is_corner_clearing=False)
        clearing1.get_building_count_for_player = lambda p: 1 if p == mock_player_2 else 2
        clearing1.get_all_other_players_in_location = lambda p: [mock_player_2, mock_player_3]
        clearing2.get_building_count_for_player = lambda p: 2 if p == mock_player_2 else 0
        clearing2.get_all_other_players_in_location = lambda p: [mock_player_2, mock_player_3]
        clearing3.get_building_count_for_player = lambda p: 0 if p == mock_player_2 else 1
        clearing3.get_all_other_players_in_location = lambda p: [mock_player_2, mock_player_3]

        mock_player_2.is_defenseless = lambda c: False
        mock_player_3.is_defenseless = lambda c: True

        clearings = [clearing1, clearing2, clearing3]
        sorted_clearings = sort_clearings_by_defenseless_enemy_buildings(clearings, mock_player, descending=False)
        self.assertEqual(sorted_clearings, [clearing2, clearing3, clearing1])


@patch('player_resources.player.Player.__abstractmethods__', set())
class TestSortUtilsPaths(TestCase):
    def test_sort_paths_by_distance_descending(self):
        mock_game = Mock()
        clearing1 = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.FOX, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        path1 = [clearing2, clearing3]
        path2 = [clearing2]
        path3 = [clearing1, clearing2, clearing3]

        paths = [path1, path2, path3]
        sorted_paths = sort_paths_by_distance(paths, descending=True)
        self.assertEqual(sorted_paths, [path3, path1, path2])

    def test_sort_paths_by_distance_ascending(self):
        mock_game = Mock()
        clearing1 = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.FOX, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        path1 = [clearing2, clearing3]
        path2 = [clearing2]
        path3 = [clearing1, clearing2, clearing3]

        paths = [path1, path2, path3]
        sorted_paths = sort_paths_by_distance(paths, descending=False)
        self.assertEqual(sorted_paths, [path2, path1, path3])

    def test_sort_paths_by_distance_descending_stable(self):
        mock_game = Mock()
        clearing1 = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.FOX, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        path1 = [clearing2, clearing3]
        path2 = [clearing1, clearing2]
        path3 = [clearing1, clearing2, clearing3]

        paths = [path1, path2, path3]
        sorted_paths = sort_paths_by_distance(paths, descending=True)
        self.assertEqual(sorted_paths, [path3, path1, path2])

    def test_sort_paths_by_distance_ascending_stable(self):
        mock_game = Mock()
        clearing1 = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.FOX, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        path1 = [clearing2, clearing3]
        path2 = [clearing1, clearing2]
        path3 = [clearing1, clearing2, clearing3]

        paths = [path1, path2, path3]
        sorted_paths = sort_paths_by_distance(paths, descending=False)
        self.assertEqual(sorted_paths, [path1, path2, path3])

    def test_sort_paths_by_lexicographic_priority_descending(self):
        mock_game = Mock()
        clearing1 = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.FOX, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        path1 = [clearing2, clearing3]
        path2 = [clearing2, clearing1]
        path3 = [clearing1, clearing2]
        path4 = [clearing1, clearing3]

        paths = [path1, path2, path3, path4]
        sorted_paths = sort_paths_by_lexicographic_priority(paths, descending=True)
        self.assertEqual(sorted_paths, [path1, path2, path4, path3])

    def test_sort_paths_by_lexicographic_priority_ascending(self):
        mock_game = Mock()
        clearing1 = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.FOX, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        path1 = [clearing2, clearing3]
        path2 = [clearing2, clearing1]
        path3 = [clearing1, clearing2]
        path4 = [clearing1, clearing3]

        paths = [path1, path2, path3, path4]
        sorted_paths = sort_paths_by_lexicographic_priority(paths, descending=False)
        self.assertEqual(sorted_paths, [path3, path4, path2, path1])

    def test_sort_paths_by_lexicographic_priority_descending_unequal_lengths(self):
        mock_game = Mock()
        clearing1 = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.FOX, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        path1 = [clearing2, clearing3]
        path2 = [clearing2, clearing3, clearing1]
        path3 = [clearing3]
        path4 = [clearing1, clearing2]

        paths = [path1, path2, path3, path4]
        sorted_paths = sort_paths_by_lexicographic_priority(paths, descending=True)
        self.assertEqual(sorted_paths, [path3, path2, path1, path4])

    def test_sort_paths_by_lexicographic_priority_ascending_unequal_lengths(self):
        mock_game = Mock()
        clearing1 = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.FOX, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        path1 = [clearing2, clearing3]
        path2 = [clearing2, clearing3, clearing1]
        path3 = [clearing3]
        path4 = [clearing1, clearing2]

        paths = [path1, path2, path3, path4]
        sorted_paths = sort_paths_by_lexicographic_priority(paths, descending=False)
        self.assertEqual(sorted_paths, [path4, path1, path2, path3])

    def test_sort_paths_by_destination_priority_descending(self):
        mock_game = Mock()
        clearing1 = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.FOX, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        path1 = [clearing2, clearing3]
        path2 = [clearing1, clearing2]
        path3 = [clearing2, clearing1]

        paths = [path1, path2, path3]
        sorted_paths = sort_paths_by_destination_priority(paths, descending=True)
        self.assertEqual(sorted_paths, [path1, path2, path3])

    def test_sort_paths_by_destination_priority_ascending(self):
        mock_game = Mock()
        clearing1 = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.FOX, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        path1 = [clearing2, clearing3]
        path2 = [clearing1, clearing2]
        path3 = [clearing2, clearing1]

        paths = [path1, path2, path3]
        sorted_paths = sort_paths_by_destination_priority(paths, descending=False)
        self.assertEqual(sorted_paths, [path3, path2, path1])

    def test_sort_paths_by_destination_priority_descending_stable(self):
        mock_game = Mock()
        clearing1 = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.FOX, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        path1 = [clearing2, clearing3]
        path2 = [clearing1, clearing2]
        path3 = [clearing1, clearing3]

        paths = [path1, path2, path3]
        sorted_paths = sort_paths_by_destination_priority(paths, descending=True)
        self.assertEqual(sorted_paths, [path1, path3, path2])

    def test_sort_paths_by_destination_priority_ascending_stable(self):
        mock_game = Mock()
        clearing1 = Clearing(mock_game, Suit.FOX, priority=1, total_building_slots=1, is_corner_clearing=False)
        clearing2 = Clearing(mock_game, Suit.FOX, priority=2, total_building_slots=1, is_corner_clearing=False)
        clearing3 = Clearing(mock_game, Suit.FOX, priority=3, total_building_slots=1, is_corner_clearing=False)
        path1 = [clearing2, clearing3]
        path2 = [clearing1, clearing2]
        path3 = [clearing1, clearing3]

        paths = [path1, path2, path3]
        sorted_paths = sort_paths_by_destination_priority(paths, descending=False)
        self.assertEqual(sorted_paths, [path2, path1, path3])

from __future__ import annotations

from constants import FACTION_SETUP_ORDER, Suit
from locations.clearing import Clearing
from locations.forest import Forest
from locations.location import Location
from player_resources.player import Player


##################
#                #
# Player sorting #
#                #
##################

# By default, all player sorting methods go from 'most X' to 'least X'. Pass descending=False to reverse that
# Setup Order instead goes in the traditional order: A, B, C, D, ...
def sort_players_by_setup_order(players: list[Player], descending: bool = False) -> list[Player]:
    return sorted(players, key=lambda p: FACTION_SETUP_ORDER.index(p), reverse=descending)


def sort_players_by_victory_points(players: list[Player], descending: bool = True) -> list[Player]:
    return sorted(players, key=lambda p: p.get_victory_points(), reverse=descending)


def sort_players_by_pieces_in_clearing(players: list[Player], clearing: Clearing,
                                       descending: bool = True) -> list[Player]:
    return sorted(players, key=lambda p: clearing.get_piece_count_for_player(p), reverse=descending)


def sort_players_by_warriors_in_clearing(players: list[Player], clearing: Clearing,
                                         descending: bool = True) -> list[Player]:
    return sorted(players, key=lambda p: clearing.get_warrior_count_for_player(p), reverse=descending)


def sort_players_by_buildings_in_clearing(players: list[Player], clearing: Clearing,
                                          descending: bool = True) -> list[Player]:
    return sorted(players, key=lambda p: clearing.get_building_count_for_player(p), reverse=descending)


def sort_players_by_tokens_in_clearing(players: list[Player], clearing: Clearing,
                                       descending: bool = True) -> list[Player]:
    return sorted(players, key=lambda p: clearing.get_token_count_for_player(p), reverse=descending)


def sort_players_by_cardboard_in_clearing(players: list[Player], clearing: Clearing,
                                          descending: bool = True) -> list[Player]:
    return sorted(players, key=lambda p: (clearing.get_building_count_for_player(p) +
                                          clearing.get_token_count_for_player(p)),
                  reverse=descending)


####################
#                  #
# Clearing sorting #
#                  #
####################


# By default, all clearing sorting methods go from 'most X' to 'least X'. Pass descending=False to reverse that
# The exception is sorting by priority, since the majority of cases where we want priority, we want it from 1 to 12
# If a sort method is binary (such as 'matching_suit' or 'any_free_building_slots'), it goes from 'is X' to 'not X'
def sort_clearings_by_priority(clearings: list[Clearing], descending: bool = False) -> list[Clearing]:
    return sorted(clearings, key=lambda c: c.priority, reverse=descending)


def sort_clearings_by_matching_suit(clearings: list[Clearing], suit: Suit, descending: bool = True) -> list[Clearing]:
    return sorted(clearings, key=lambda c: Suit.are_suits_equal(c.suit, suit), reverse=descending)


def sort_clearings_by_enemy_pieces(clearings: list[Clearing], acting_player: Player,
                                   descending: bool = True) -> list[Clearing]:
    return sorted(clearings, key=lambda c: c.get_total_piece_count_for_other_players(acting_player), reverse=descending)


def sort_clearings_by_own_pieces(clearings: list[Clearing], acting_player: Player,
                                 descending: bool = True) -> list[Clearing]:
    return sorted(clearings, key=lambda c: c.get_piece_count_for_player(acting_player), reverse=descending)


def sort_clearings_by_enemy_warriors(clearings: list[Clearing], acting_player: Player,
                                     descending: bool = True) -> list[Clearing]:
    return sorted(clearings, key=lambda c: c.get_total_warrior_count_for_other_players(acting_player),
                  reverse=descending)


def sort_clearings_by_own_warriors(clearings: list[Clearing], acting_player: Player,
                                   descending: bool = True) -> list[Clearing]:
    return sorted(clearings, key=lambda c: c.get_warrior_count_for_player(acting_player), reverse=descending)


def sort_clearings_by_target_warriors(clearings: list[Clearing], target_player: Player,
                                      descending: bool = True) -> list[Clearing]:
    return sorted(clearings, key=lambda c: c.get_warrior_count_for_player(target_player), reverse=descending)


def sort_clearings_by_enemy_buildings(clearings: list[Clearing], acting_player: Player,
                                      descending: bool = True) -> list[Clearing]:
    return sorted(clearings, key=lambda c: c.get_total_building_count_for_other_players(acting_player),
                  reverse=descending)


def sort_clearings_by_enemy_tokens(clearings: list[Clearing], acting_player: Player,
                                   descending: bool = True) -> list[Clearing]:
    return sorted(clearings, key=lambda c: c.get_total_token_count_for_other_players(acting_player),
                  reverse=descending)


def sort_clearings_by_target_cardboard(clearings: list[Clearing], target_player: Player,
                                       descending: bool = True) -> list[Clearing]:
    return sorted(clearings, key=lambda c: (c.get_token_count_for_player(target_player) +
                                            c.get_building_count_for_player(target_player)),
                  reverse=descending)


def sort_clearings_by_any_own_buildings(clearings: list[Clearing], acting_player: Player,
                                        descending: bool = True) -> list[Clearing]:
    return sorted(clearings, key=lambda c: c.get_building_count_for_player(acting_player) != 0, reverse=descending)


def sort_clearings_by_martial_law(clearings: list[Clearing], acting_player: Player,
                                  descending: bool = True) -> list[Clearing]:
    return sorted(clearings, key=lambda c: any(count >= 3 and player != acting_player for (player, count) in
                                               c.get_warrior_count_for_all_players().items()),
                  reverse=descending)


def sort_clearings_by_free_building_slots(clearings: list[Clearing], descending: bool = True) -> list[Clearing]:
    return sorted(clearings, key=lambda c: c.get_open_building_slot_count(), reverse=descending)


def sort_clearings_by_any_free_building_slots(clearings: list[Clearing], descending: bool = True) -> list[Clearing]:
    return sorted(clearings, key=lambda c: c.get_open_building_slot_count() != 0, reverse=descending)


def sort_clearings_by_ruled_by_self(clearings: list[Clearing], acting_player: Player,
                                    descending: bool = True) -> list[Clearing]:
    return sorted(clearings, key=lambda c: not acting_player.does_rule_clearing(c), reverse=descending)


# TODO?
# You probably always want to call this with descending=False...
def sort_clearings_by_distance(clearings: list[Clearing], starting_location: Location,
                               descending: bool = True) -> list[Clearing]:
    if not isinstance(starting_location, Clearing) and not isinstance(starting_location, Forest):
        return []
    pass


def sort_clearings_by_defenseless_buildings(clearings: list[Clearing], acting_player: Player,
                                            descending: bool = True) -> list[Clearing]:
    return sorted(clearings, key=lambda c: get_defenseless_buildings_in_clearing(c, acting_player), reverse=descending)


def get_defenseless_buildings_in_clearing(clearing: Clearing, acting_player: Player) -> int:
    defenseless_buildings = 0
    for player in clearing.get_all_other_players_in_location(acting_player):
        if player.is_defenseless(clearing):
            defenseless_buildings += clearing.get_building_count_for_player(player)
    return defenseless_buildings


################
#              #
# Path sorting #
#              #
################


# By default, all path sorting methods go from 'least X' to 'most X'. Pass descending=True to reverse that
def sort_paths_by_distance(paths: list[list[Clearing]], descending: bool = False) -> list[list[Clearing]]:
    return sorted(paths, key=lambda p: len(p), reverse=descending)


# TODO: Implement lexicographic priority sorting
def sort_paths_by_lexicographic_priority(paths: list[list[Clearing]], descending: bool = False) -> list[list[Clearing]]:
    return sorted(paths, key=lambda p: len(p), reverse=descending)


def sort_paths_by_destination_priority(paths: list[list[Clearing]], descending: bool = False) -> list[list[Clearing]]:
    return sorted(paths, key=lambda p: p[-1].priority, reverse=descending)

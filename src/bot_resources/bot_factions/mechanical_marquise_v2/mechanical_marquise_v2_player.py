from __future__ import annotations

import random
from typing import cast, Optional, Type, TYPE_CHECKING

from battle_utils import DamageResult
from bot_resources.bot import Bot
from bot_resources.bot_factions.mechanical_marquise_v2.mechanical_marquise_v2_building import \
    MechanicalMarquiseV2Building
from bot_resources.bot_factions.mechanical_marquise_v2.mechanical_marquise_v2_piece_stock import \
    MechanicalMarquiseV2PieceStock
from bot_resources.bot_factions.mechanical_marquise_v2.mechanical_marquise_v2_trait import TRAIT_BLITZ, \
    TRAIT_FORTIFIED, TRAIT_HOSPITALS, TRAIT_IRON_WILL
from bot_resources.bot_factions.mechanical_marquise_v2.recruiter import Recruiter
from bot_resources.bot_factions.mechanical_marquise_v2.sawmill import Sawmill
from bot_resources.bot_factions.mechanical_marquise_v2.workshop import Workshop
from constants import Faction, Suit
from locations.clearing import Clearing
from pieces.warrior import Warrior
from player_resources.player import Player
from sort_utils import sort_clearings_by_enemy_pieces, sort_clearings_by_own_warriors, sort_clearings_by_priority, \
    sort_players_by_pieces_in_clearing, sort_players_by_setup_order, sort_players_by_victory_points

if TYPE_CHECKING:
    from deck.cards.card import Card
    from game import Game
    from pieces.item_token import ItemToken
    from player_resources.supply import Supply


class MechanicalMarquiseV2Player(Bot):
    victory_points: int
    game: Game
    faction: Faction
    piece_stock: MechanicalMarquiseV2PieceStock
    supply: Supply
    revealed_cards: list[Card]
    crafted_items: list[ItemToken]
    built_building_this_turn: bool

    def __init__(self, game: Game) -> None:
        piece_stock = MechanicalMarquiseV2PieceStock(self)
        super().__init__(game, Faction.MECHANICAL_MARQUISE_2_0, piece_stock)

        self.built_building_this_turn = False

    def setup(self) -> None:
        super().setup()
        starting_clearing = self.get_corner_homeland()
        starting_clearing.add_piece(self, self.piece_stock.get_keep())
        self.place_initial_garrison()
        self.place_initial_buildings()
        self.game.log(f'{self} starts in {starting_clearing}.', logging_faction=self.faction)

    def place_initial_garrison(self) -> None:
        keep_clearing = self.piece_stock.get_keep().location
        for clearing in self.game.clearings():
            if not clearing.is_corner_clearing or not clearing.opposite_corner_clearing == keep_clearing:
                clearing.add_piece(self, self.get_unplaced_warriors()[0])
        keep_clearing.add_piece(self, self.get_unplaced_warriors()[0])

    def place_initial_buildings(self) -> None:
        keep_clearing = self.piece_stock.get_keep().location
        assert isinstance(keep_clearing, Clearing)
        valid_initial_building_clearings = [clearing for clearing in keep_clearing.path_connected_clearings]
        random.shuffle(valid_initial_building_clearings)
        for building in (self.piece_stock.get_sawmills()[0], self.piece_stock.get_workshops()[0],
                         self.piece_stock.get_recruiters()[0]):
            target_clearing = valid_initial_building_clearings.pop()
            target_clearing.add_pieces(self, [building])

    ######################
    #                    #
    # Turn order methods #
    #                    #
    ######################

    def birdsong(self) -> None:
        self.built_building_this_turn = False
        self.reveal_order()

    def daylight(self) -> None:
        if self.order_card.suit == Suit.BIRD:
            return self.escalated_daylight()
        self.battle_step()
        self.recruit_step()
        self.build_step()
        self.move_step()
        if self.has_trait(TRAIT_BLITZ):
            self.blitz()

    def escalated_daylight(self) -> None:
        self.escalated_battle_step()
        self.escalated_recruit_step()
        self.escalated_build_step()
        destination_clearings = self.escalated_move_step()
        # Second battle happens in escalated daylight
        destination_clearings = sort_clearings_by_priority(destination_clearings)
        for clearing in destination_clearings:
            self.initiate_battle(clearing)
        if self.has_trait(TRAIT_BLITZ):
            self.blitz()

    def evening(self) -> None:
        self.expand_step()
        if self.has_trait(TRAIT_IRON_WILL):
            self.expand_step()
        self.add_victory_points(self.get_score_for_building())
        self.game.discard_card(self.order_card)
        self.order_card = None

    ##################
    #                #
    # Battle methods #
    #                #
    ##################

    def battle_step(self) -> None:
        suited_clearings = self.game.get_clearings_of_suit(self.order_card.suit)
        suited_clearings = sort_clearings_by_priority(suited_clearings)
        for clearing in suited_clearings:
            # TODO: Mercenaries prevent fighting otters
            if clearing.is_player_warriors_in_location(self) and clearing.is_any_other_player_in_location(self):
                self.initiate_battle(clearing)

    def escalated_battle_step(self) -> None:
        return self.battle_step()

    def initiate_battle(self, clearing: 'Clearing') -> None:
        potential_targets = clearing.get_all_other_players_in_location(self)
        # Sort in reverse order from our tie-breaking priority: Setup order -> most VP -> most pieces in clearing
        potential_targets = sort_players_by_setup_order(potential_targets)
        potential_targets = sort_players_by_victory_points(potential_targets)
        potential_targets = sort_players_by_pieces_in_clearing(potential_targets, clearing)
        if potential_targets:
            self.game.log(f'{self} battles {potential_targets[0]} in {clearing}.', logging_faction=self.faction)
            self.battle(clearing, potential_targets[0])

    def suffer_damage(self, clearing: 'Clearing', hits: int, opponent: 'Player', is_attacker: bool) -> DamageResult:
        removed_pieces = []
        points_awarded = 0
        if hits:
            warriors = clearing.get_warriors_for_player(self)  # TODO: Mercenaries
            amount_of_warriors_removed = min(hits, len(warriors))
            hits -= amount_of_warriors_removed
            for i in range(amount_of_warriors_removed):
                removed_pieces.append(warriors[i])
                points_awarded += warriors[i].get_score_for_removal()
        if hits:
            tokens = clearing.get_tokens_for_player(self)
            random.shuffle(tokens)
            amount_of_tokens_removed = min(hits, len(tokens))
            hits -= amount_of_tokens_removed
            for i in range(amount_of_tokens_removed):
                removed_pieces.append(tokens[i])
                points_awarded += tokens[i].get_score_for_removal()
        if hits:
            buildings = clearing.get_buildings_for_player(self)
            random.shuffle(buildings)
            if self.has_trait(TRAIT_FORTIFIED):
                amount_of_buildings_removed = min(hits // 2, len(buildings))
            else:
                amount_of_buildings_removed = min(hits, len(buildings))
            for i in range(amount_of_buildings_removed):
                removed_pieces.append(buildings[i])
                points_awarded += buildings[i].get_score_for_removal()

        self.game.log(f'{self} loses the following pieces: {removed_pieces}', logging_faction=self.faction)
        clearing.remove_pieces(self, removed_pieces)
        if not is_attacker:
            # Hospitals only works as the defender
            self.apply_field_hospitals(removed_pieces)
        return DamageResult(removed_pieces=removed_pieces, points_awarded=points_awarded)

    def apply_field_hospitals(self, removed_warriors: list['Warrior']) -> None:
        if self.has_trait(TRAIT_HOSPITALS):
            keep_clearing = self.piece_stock.get_keep().location
            if isinstance(keep_clearing, Clearing) and len(removed_warriors) >= 2:
                keep_clearing.add_piece(self, removed_warriors[0])

    ###################
    #                 #
    # Recruit methods #
    #                 #
    ###################

    def recruit_step(self) -> None:
        warrior_count_in_supply = len(self.get_unplaced_warriors())

        warriors_to_recruit = self.get_warriors_to_recruit()
        if not warriors_to_recruit:
            return self.score_for_failing_to_recruit(self.get_recruiting_amount())

        ruled_ordered_clearings = [clearing for clearing in self.get_ruled_ordered_clearings()]
        sorted_ruled_ordered_clearings = sort_clearings_by_priority(ruled_ordered_clearings)
        # TODO: For the time being, this uses BASE-1, where it just skips recruiting in a snare unless there's no other
        # available option
        # TODO: Update to BASE-2: Try and fail to recruit at the snare
        self.place_pieces_spread_among_clearings(warriors_to_recruit, sorted_ruled_ordered_clearings)

        warrior_count_recruited = warrior_count_in_supply - len(self.get_unplaced_warriors())
        self.score_for_failing_to_recruit(self.get_recruiting_amount() - warrior_count_recruited)

    def escalated_recruit_step(self) -> None:
        warrior_count_in_supply = len(self.get_unplaced_warriors())

        warriors_to_recruit = self.get_warriors_to_recruit()
        if not warriors_to_recruit:
            return self.score_for_failing_to_recruit(self.get_recruiting_amount())

        ruled_clearings = [clearing for clearing in self.get_ruled_clearings()]
        # Reverse sort - we want to recruit in low priority clearings for escalated daylight
        sorted_ruled_clearings = sort_clearings_by_priority(ruled_clearings, descending=True)
        # Only recruit in at most two clearings
        sorted_ruled_clearings = sorted_ruled_clearings[:2]
        # TODO: For the time being, this uses ESCALATED-2, where it skips recruiting in a snare unless there's no other
        # available option, but also won't go back to find a second clearing to recruit in if one has a snare
        # TODO: Update to ESCALATED-3: Try and fail to recruit at the snare
        self.place_pieces_spread_among_clearings(warriors_to_recruit, sorted_ruled_clearings)

        warrior_count_recruited = warrior_count_in_supply - len(self.get_unplaced_warriors())
        self.score_for_failing_to_recruit(self.get_recruiting_amount() - warrior_count_recruited)

    def get_warriors_to_recruit(self) -> list['Warrior']:
        warriors_available_to_recruit = self.get_unplaced_warriors()
        if len(warriors_available_to_recruit) > self.get_recruiting_amount():
            return warriors_available_to_recruit[:self.get_recruiting_amount()]
        return warriors_available_to_recruit

    # TODO: Cleanup, remove
    # def recruit_in_clearings(self, warriors_to_recruit: list[Warrior], valid_target_clearings: list[Clearing]) -> None:
    #     clearings_to_recruit_in: dict[Clearing, list[Warrior]] = defaultdict(list)
    #     # Iterate through the clearings in order so any remainder is spread evening among those at the start of the list
    #     for idx, warrior in enumerate(warriors_to_recruit):
    #         clearing_index = idx % len(valid_target_clearings)
    #         target_clearing = valid_target_clearings[clearing_index]
    #         clearings_to_recruit_in[target_clearing].append(warrior)
    #     for clearing, warriors in clearings_to_recruit_in.items():
    #         self.supply.relocate_pieces(self, warriors, clearing)

    def get_recruiting_amount(self) -> int:
        return 3 + self.difficulty.value

    def score_for_failing_to_recruit(self, count_of_warriors_unable_to_recruit: int) -> None:
        if count_of_warriors_unable_to_recruit >= 2:
            self.add_victory_points(count_of_warriors_unable_to_recruit // 2)

    #################
    #               #
    # Build methods #
    #               #
    #################

    def build_step(self) -> None:
        building_to_build = self.get_suited_building_to_build(self.order_card.suit)
        self.perform_build(building_to_build)

    def escalated_build_step(self) -> None:
        building_to_build = self.get_building_of_most_common_suit_on_board_unless_all_on_board()
        self.perform_build(building_to_build)

    def perform_build(self, building_to_build: 'MechanicalMarquiseV2Building') -> None:
        sorted_ruled_clearings = self.get_ruled_clearings_sorted_by_build_order()
        if not building_to_build:
            return
        if self.place_pieces_in_one_of_clearings([building_to_build], sorted_ruled_clearings):
            self.built_building_this_turn = True
        # TODO: Cleanup/remove
        # for clearing in sorted_ruled_clearings:
        #     if clearing.can_place_piece(self, building_to_build):
        #         return self.build_building(clearing, building_to_build)
        # # If we couldn't build anywhere, check if it was due to a snare, and remove that snare if so
        # self.remove_snare_if_it_prevents_placing([building_to_build], sorted_ruled_clearings)

    def get_ruled_clearings_sorted_by_build_order(self) -> list['Clearing']:
        # Sort by priority first, then by warrior count so priority is the tie-breaker
        ruled_clearings = self.get_ruled_clearings()
        sorted_ruled_clearings = sort_clearings_by_priority(ruled_clearings)
        sorted_ruled_clearings = sort_clearings_by_own_warriors(sorted_ruled_clearings, self)
        return sorted_ruled_clearings

    def get_suited_building_to_build(self, suit: 'Suit') -> Optional['MechanicalMarquiseV2Building']:
        unplaced_ordered_buildings = [building for building in
                                      cast(list[MechanicalMarquiseV2Building], self.get_unplaced_buildings()) if
                                      building.suit == suit]
        if unplaced_ordered_buildings:
            return unplaced_ordered_buildings[0]
        return None

    def get_building_of_most_common_suit_on_board_unless_all_on_board(self) -> Optional['MechanicalMarquiseV2Building']:
        unplaced_buildings = self.get_unplaced_buildings()
        unplaced_sawmills = [building for building in unplaced_buildings if isinstance(building, Sawmill)]
        unplaced_sawmill_count = len(unplaced_sawmills)
        unplaced_workshops = [building for building in unplaced_buildings if isinstance(building, Workshop)]
        unplaced_workshop_count = len(unplaced_workshops)
        unplaced_recruiters = [building for building in unplaced_buildings if isinstance(building, Recruiter)]
        unplaced_recruiter_count = len(unplaced_recruiters)

        if 0 < unplaced_sawmill_count <= unplaced_recruiter_count and unplaced_sawmill_count <= unplaced_workshop_count:
            return unplaced_sawmills[0]
        elif 0 < unplaced_workshop_count <= unplaced_recruiter_count:
            return unplaced_workshops[0]
        elif 0 < unplaced_recruiter_count:
            return unplaced_recruiters[0]
        else:
            return None

    def get_class_of_most_common_building_on_board(self) -> Type['MechanicalMarquiseV2Building']:
        unplaced_buildings = self.get_unplaced_buildings()
        unplaced_sawmills = [building for building in unplaced_buildings if isinstance(building, Sawmill)]
        unplaced_sawmill_count = len(unplaced_sawmills)
        unplaced_workshops = [building for building in unplaced_buildings if isinstance(building, Workshop)]
        unplaced_workshop_count = len(unplaced_workshops)
        unplaced_recruiters = [building for building in unplaced_buildings if isinstance(building, Recruiter)]
        unplaced_recruiter_count = len(unplaced_recruiters)

        if unplaced_sawmill_count <= unplaced_recruiter_count and unplaced_sawmill_count <= unplaced_workshop_count:
            return Sawmill
        elif unplaced_workshop_count <= unplaced_recruiter_count:
            return Workshop
        else:
            return Recruiter

    def build_building(self, clearing: 'Clearing', building: 'MechanicalMarquiseV2Building') -> None:
        self.built_building_this_turn = True
        self.supply.relocate_pieces(self, [building], clearing)

    def get_score_for_building(self) -> int:
        if self.order_card.suit != Suit.BIRD:
            unplaced_ordered_buildings = [building for building in
                                          cast(list[MechanicalMarquiseV2Building], self.get_unplaced_buildings()) if
                                          building.suit == self.order_card.suit]
            return max(0, 5 - len(unplaced_ordered_buildings))

        most_common_building_class = self.get_class_of_most_common_building_on_board()
        unplaced_common_buildings = [building for building in
                                     cast(list[MechanicalMarquiseV2Building], self.get_unplaced_buildings()) if
                                     isinstance(building, most_common_building_class)]
        return max(0, 5 - len(unplaced_common_buildings))

    ################
    #              #
    # Move methods #
    #              #
    ################

    def move_step(self) -> None:
        planned_movements = self.prepare_origin_movements()
        for origin_clearing in sort_clearings_by_priority(list(planned_movements.keys())):
            destination_clearing = planned_movements.get(origin_clearing)
            warriors_to_move = origin_clearing.get_warriors_for_player(self)[3:]
            self.move(warriors_to_move, origin_clearing, destination_clearing)

    def escalated_move_step(self) -> list['Clearing']:
        destinations = []
        planned_movements = self.prepare_origin_movements()
        for origin_clearing in sort_clearings_by_priority(list(planned_movements.keys())):
            destination_clearing = planned_movements.get(origin_clearing)
            warriors_to_move = origin_clearing.get_warriors_for_player(self)[3:]
            self.move(warriors_to_move, origin_clearing, destination_clearing)
            destinations.append(destination_clearing)
        return destinations

    def prepare_origin_movements(self) -> dict['Clearing', 'Clearing']:
        planned_movements = {}
        origin_clearings = [clearing for clearing in self.get_ruled_ordered_clearings() if
                            clearing.get_warrior_count_for_player(self) > 3]
        sort_clearings_by_priority(origin_clearings)
        for origin_clearing in origin_clearings:
            valid_destination_clearings = self.find_adjacent_clearings_sorted_by_most_enemy_pieces(origin_clearing)
            for destination_clearing in valid_destination_clearings:
                if origin_clearing.can_move_pieces(self, origin_clearing.get_warriors_for_player(self),
                                                   destination_clearing, requires_rule=True):
                    planned_movements[origin_clearing] = destination_clearing
                    break
            # If we haven't found any legal destination, check if it was due to a snare, and remove that snare if so
            if origin_clearing not in planned_movements:
                self.remove_snare_if_it_prevents_movement(origin_clearing.get_warriors_for_player(self),
                                                          origin_clearing, valid_destination_clearings)
        return planned_movements

    def find_adjacent_clearings_sorted_by_most_enemy_pieces(self, origin_clearing: 'Clearing') -> list['Clearing']:
        adjacent_clearings = self.get_adjacent_clearings(origin_clearing)
        # Sort by priority first, then by enemy piece count so priority is the tie-breaker
        adjacent_clearings = sort_clearings_by_priority(adjacent_clearings)
        adjacent_clearings = sort_clearings_by_enemy_pieces(adjacent_clearings, self)
        return adjacent_clearings

    #########################
    #                       #
    # Special steps methods #
    #                       #
    #########################

    def expand_step(self) -> None:
        if not self.built_building_this_turn and self.get_score_for_building() < 3:
            self.game.discard_card(self.order_card)
            self.order_card = self.game.draw_card()
            self.daylight()

    def blitz(self) -> None:
        ruled_empty_clearings = [clearing for clearing in self.get_ruled_clearings() if
                                 clearing.get_total_piece_count() == clearing.get_piece_count_for_player(self)]
        ruled_empty_clearings = sort_clearings_by_priority(ruled_empty_clearings)
        for origin_clearing in ruled_empty_clearings:
            warriors_in_clearing = origin_clearing.get_warriors_for_player(self)
            warriors_to_move = warriors_in_clearing[1:]
            if warriors_to_move:
                valid_destination_clearings = self.find_adjacent_clearings_sorted_by_most_enemy_pieces(origin_clearing)
                for destination_clearing in valid_destination_clearings:
                    if origin_clearing.can_move_pieces(self, warriors_to_move, destination_clearing):
                        self.move(warriors_to_move, origin_clearing, destination_clearing)
                        self.initiate_battle(destination_clearing)
                        return
        # If we haven't found any legal movement, check if it was due to a snare, and remove that snare if so
        for origin_clearing in ruled_empty_clearings:
            warriors_in_clearing = origin_clearing.get_warriors_for_player(self)
            warriors_to_move = warriors_in_clearing[1:]
            if warriors_to_move:
                valid_destination_clearings = self.find_adjacent_clearings_sorted_by_most_enemy_pieces(origin_clearing)
                if self.remove_snare_if_it_prevents_movement(warriors_to_move, origin_clearing,
                                                             valid_destination_clearings):
                    return

    # MM2.0 takes half the damage of a normal hit if they're Fortified, and in a clearing with only their buildings
    def halves_damage(self, battle_clearing: 'Clearing') -> bool:
        return (self.has_trait(TRAIT_FORTIFIED) and
                battle_clearing.get_building_count_for_player(self) == battle_clearing.get_piece_count_for_player(self))

from __future__ import annotations
import random
from typing import TYPE_CHECKING

from bot_resources.bot import Bot
from bot_resources.bot_constants import BotDifficulty
from bot_resources.bot_factions.electric_eyrie.decree import Decree
from bot_resources.bot_factions.electric_eyrie.electric_eyrie_piece_stock import ElectricEyriePieceStock
from bot_resources.bot_factions.electric_eyrie.electric_eyrie_trait import TRAIT_NOBILITY, TRAIT_RELENTLESS, \
    TRAIT_SWOOP, TRAIT_WAR_TAX
from bot_resources.trait import Trait
from constants import Faction, Suit
from locations.clearing import Clearing
from pieces.building import Building
from pieces.token import Token
from pieces.warrior import Warrior
from player_resources.player import Player
from sort_utils import sort_clearings_by_any_own_buildings, sort_clearings_by_defenseless_enemy_buildings, \
    sort_clearings_by_enemy_pieces, sort_clearings_by_priority, sort_clearings_by_own_warriors, \
    sort_players_by_buildings_in_clearing, sort_players_by_pieces_in_clearing, sort_players_by_setup_order

if TYPE_CHECKING:
    from deck.cards.card import Card
    from game import Game
    from pieces.item_token import ItemToken
    from pieces.piece import Piece
    from player_resources.supply import Supply


class ElectricEyriePlayer(Bot):
    victory_points: int
    game: 'Game'
    faction: 'Faction'
    piece_stock: 'ElectricEyriePieceStock'
    supply: 'Supply'
    revealed_cards: list['Card']
    crafted_items: list['ItemToken']
    decree: 'Decree'
    turmoil: bool
    deal_extra_hit: bool

    def __init__(self, game: Game, difficulty: 'BotDifficulty' = None, traits: list['Trait'] = None) -> None:
        piece_stock = ElectricEyriePieceStock(self)
        super().__init__(game, Faction.ELECTRIC_EYRIE, piece_stock, difficulty=difficulty, traits=traits)

        self.decree = Decree(self)
        self.turmoil = False
        self.deal_extra_hit = False

    def setup(self) -> None:
        super().setup()
        starting_clearing = self.get_corner_homeland()
        self.game.log(f'{self} starts in {starting_clearing}.', logging_faction=self.faction)
        starting_clearing.add_piece(self, self.piece_stock.get_roosts()[0])
        self.place_initial_warriors()

    def place_initial_warriors(self):
        starting_clearing = self.piece_stock.get_roosts()[0].location
        starting_warriors = self.get_unplaced_warriors()[:6]
        starting_clearing.add_pieces(self, starting_warriors)

    ######################
    #                    #
    # Turn order methods #
    #                    #
    ######################

    def birdsong(self) -> None:
        self.turmoil = False
        self.reveal_order()
        self.decree.add_to_decree(self.order_card)
        if len(self.get_unplaced_buildings()) == 7:
            self.replace_first_roost()

    def daylight(self) -> None:
        self.resolve_decree()
        if self.turmoil:
            self.turmoil_action()
            return
        if self.has_trait(TRAIT_RELENTLESS):
            self.relentless()
        self.build_step()
        if self.turmoil:
            self.turmoil_action()
            return
        if self.has_trait(TRAIT_SWOOP):
            self.swoop()

    def evening(self) -> None:
        self.add_victory_points(self.get_score_for_roosts())

    ###################
    #                 #
    # Recruit methods #
    #                 #
    ###################

    def recruit_step(self, suit: 'Suit') -> None:
        warrior_count_in_supply = len(self.get_unplaced_warriors())

        # Skip recruiting for columns with 0 cards in the suit, or if you are in turmoil
        if self.turmoil or self.decree.get_count_of_suited_cards_in_decree(suit) == 0:
            return
        warriors_to_recruit = self.get_warriors_to_recruit(suit)
        if not warriors_to_recruit:
            return

        roost_ordered_clearings = [clearing for clearing in self.game.get_clearings_of_suit(suit) if
                                   clearing.get_building_count_for_player(self) > 0]
        sorted_roost_ordered_clearings = sort_clearings_by_priority(roost_ordered_clearings, descending=True)
        sorted_roost_ordered_clearings = sort_clearings_by_own_warriors(sorted_roost_ordered_clearings, self,
                                                                        descending=False)
        sorted_roost_ordered_clearings = sort_clearings_by_enemy_pieces(sorted_roost_ordered_clearings, self)
        self.place_pieces_in_one_of_clearings(warriors_to_recruit, sorted_roost_ordered_clearings)

    def get_warriors_to_recruit(self, suit: Suit) -> list[Warrior]:
        warriors_available_to_recruit = self.get_unplaced_warriors()
        if len(warriors_available_to_recruit) > self.get_recruiting_amount(suit):
            return warriors_available_to_recruit[:self.get_recruiting_amount(suit)]
        return warriors_available_to_recruit

    def get_recruiting_amount(self, suit: 'Suit') -> int:
        recruiting_amount = self.decree.get_count_of_suited_cards_in_decree(suit)
        if suit == Suit.BIRD:
            recruiting_amount += self.difficulty.value - 1
        return recruiting_amount

    ################
    #              #
    # Move methods #
    #              #
    ################

    def move_step(self, suit: 'Suit') -> None:
        # Skip moving for columns with 0 cards in the suit, or if you are in turmoil
        if self.turmoil or self.decree.get_count_of_suited_cards_in_decree(suit) == 0:
            return
        # Only consider moving from clearings that: match the column suit, that you rule, and that have more of your
        # warriors than there are cards in the column (Or else 0 warriors would move from that clearing anyway)
        suited_ruled_clearings = [clearing for clearing in self.get_ruled_suited_clearings(suit) if
                                  (clearing.get_warrior_count_for_player(self) >
                                   self.decree.get_count_of_suited_cards_in_decree(suit))]
        sorted_suited_clearings = sort_clearings_by_priority(suited_ruled_clearings)
        sorted_suited_clearings = sort_clearings_by_own_warriors(sorted_suited_clearings, self)

        for origin_clearing in sorted_suited_clearings:
            warriors_to_move = self.get_warriors_to_move(origin_clearing, suit)

            destination_clearings = self.get_movement_destinations(origin_clearing)
            # If there's a snare in the origin clearing and we have a legal move, remove the snare and cancel the
            # movement
            if self.remove_snare_if_it_prevents_movement(warriors_to_move, origin_clearing,
                                                         destination_clearings):
                return
            destination_clearing = self.get_movement_destination(warriors_to_move, origin_clearing,
                                                                 destination_clearings)
            if destination_clearing:
                self.move(warriors_to_move, origin_clearing, destination_clearing)
                return

    def get_warriors_to_move(self, origin_clearing: 'Clearing', suit: 'Suit') -> list['Warrior']:
        own_rule_value = self.get_rule_value(origin_clearing)
        max_enemy_rule_value = self.get_max_enemy_rule_value_in_clearing(origin_clearing)
        warrior_count_to_move_and_keep_rule = own_rule_value - max_enemy_rule_value
        # Move the minimum between (most you can without losing rule) and (X - #cards in column)
        warrior_count_to_move = min(warrior_count_to_move_and_keep_rule,
                                    (origin_clearing.get_warrior_count_for_player(self) -
                                     self.decree.get_count_of_suited_cards_in_decree(suit)))
        return origin_clearing.get_warriors_for_player(self)[:warrior_count_to_move]

    def get_movement_destinations(self, origin_clearing: 'Clearing') -> list['Clearing']:
        potential_destination_clearings = [clearing for clearing in self.get_adjacent_clearings(origin_clearing)]
        # Find destinations this move could end in, sorted by [no roost] -> [min enemy pieces] -> [lowest priority]
        sorted_destination_clearings = sort_clearings_by_priority(potential_destination_clearings, descending=True)
        sorted_destination_clearings = sort_clearings_by_enemy_pieces(sorted_destination_clearings, self,
                                                                      descending=False)
        sorted_destination_clearings = sort_clearings_by_any_own_buildings(sorted_destination_clearings, self,
                                                                           descending=False)
        return sorted_destination_clearings

    def get_max_enemy_rule_value_in_clearing(self, clearing: 'Clearing') -> int:
        max_enemy_rule_value = 0
        for other_player in clearing.get_all_other_players_in_location(self):
            rule_value = other_player.get_rule_value(clearing)
            if rule_value > max_enemy_rule_value:
                max_enemy_rule_value = rule_value
        return max_enemy_rule_value

    ##################
    #                #
    # Battle methods #
    #                #
    ##################

    def battle_step(self, suit: 'Suit') -> None:
        # Skip battling for columns with 0 cards in the suit, or if you are in turmoil
        if self.turmoil or self.decree.get_count_of_suited_cards_in_decree(suit) == 0:
            return
        suited_clearings = [clearing for clearing in self.game.get_clearings_of_suit(suit) if
                            clearing.is_player_warriors_in_location(self) and
                            clearing.is_any_other_player_in_location(self)]
        sorted_suited_clearings = sort_clearings_by_priority(suited_clearings)
        sorted_suited_clearings = sort_clearings_by_defenseless_enemy_buildings(sorted_suited_clearings, self)
        sorted_suited_clearings = sort_clearings_by_any_own_buildings(sorted_suited_clearings, self, descending=False)
        # TODO: Mercenaries prevent fighting otters
        if not sorted_suited_clearings:
            return
        if self.decree.column_has_most_cards(suit):
            self.deal_extra_hit = True
        self.initiate_battle(sorted_suited_clearings[0])
        self.deal_extra_hit = False

    def initiate_battle(self, clearing: 'Clearing') -> None:
        potential_targets = clearing.get_all_other_players_in_location(self)
        # Sort in reverse order from our tie-breaking priority: Setup order -> most pieces -> most buildings
        potential_targets = sort_players_by_setup_order(potential_targets)
        potential_targets = sort_players_by_buildings_in_clearing(potential_targets, clearing)
        potential_targets = sort_players_by_pieces_in_clearing(potential_targets, clearing)
        if potential_targets:
            self.battle(clearing, potential_targets[0])

    def battle(self, clearing: 'Clearing', defender: 'Player') -> None:
        self.game.log(f'{self} battles {defender} in {clearing}.', logging_faction=self.faction)
        random_rolls = (random.randint(0, 3), random.randint(0, 3))
        self.game.log(f'{self} rolls {random_rolls[0]}, {random_rolls[1]}.', logging_faction=self.faction)
        # Defender allocates the rolls - high roll to attacker, low roll to defender, except in the case of Veterans
        roll_result = defender.allocate_rolls_as_defender(random_rolls)
        # Each battler caps their hits and adds their relevant bonus hits
        attacker_hits = (self.cap_rolled_hits(clearing, roll_result.attacker_roll) +
                         self.get_bonus_hits(clearing, defender, is_attacker=True))
        defender_hits = (defender.cap_rolled_hits(clearing, roll_result.defender_roll) +
                         defender.get_bonus_hits(clearing, defender, is_attacker=False))
        self.game.log(f'{self} does {attacker_hits} hits. {defender} does {defender_hits} hits.',
                      logging_faction=self.faction)
        # Each battler removes their pieces and calculates how much VP the opponent should earn from the battle
        defender_damage_result = defender.suffer_damage(clearing, attacker_hits, self, is_attacker=False)
        attacker_damage_result = self.suffer_damage(clearing, defender_hits, defender, is_attacker=True)
        # Each battler scores their awarded VP, plus any bonus VP they deserve (such as Vagabot from removing warriors)
        self.add_victory_points(defender_damage_result.points_awarded +
                                self.supplementary_score_for_removed_pieces_in_battle(
                                    defender, defender_damage_result.removed_pieces, is_attacker=True))
        if self.has_trait(TRAIT_WAR_TAX):
            removed_buildings_and_tokens = [piece for piece in defender_damage_result.removed_pieces if
                                            isinstance(piece, Building) or isinstance(piece, Token)]
            defender.add_victory_points(len(removed_buildings_and_tokens) * -1)
        defender.add_victory_points(attacker_damage_result.points_awarded +
                                    defender.supplementary_score_for_removed_pieces_in_battle(
                                        self, attacker_damage_result.removed_pieces, is_attacker=False))

    def get_bonus_hits(self, clearing: 'Clearing', opponent: 'Player', is_attacker: bool = True) -> int:
        bonus_hits = super().get_bonus_hits(clearing, opponent, is_attacker)
        if self.deal_extra_hit:
            bonus_hits += 1
        return bonus_hits

    #################
    #               #
    # Build methods #
    #               #
    #################

    def build_step(self) -> None:
        unplaced_roosts = [building for building in self.get_unplaced_buildings()]
        unplaced_roosts_count = len(unplaced_roosts)
        if not unplaced_roosts:
            self.turmoil = True
            return
        ruled_clearings = [clearing for clearing in self.get_ruled_clearings()]
        sorted_ruled_clearings = sort_clearings_by_priority(ruled_clearings)
        self.place_pieces_in_one_of_clearings(unplaced_roosts[:1], sorted_ruled_clearings)

        # If we failed to place a roost, enter turmoil
        roost_placed = unplaced_roosts_count > len(self.get_unplaced_buildings())
        if not roost_placed:
            self.turmoil = True

    def get_score_for_roosts(self) -> int:
        return max(0, 6 - len(self.get_unplaced_buildings()))

    #########################
    #                       #
    # Special steps methods #
    #                       #
    #########################

    def replace_first_roost(self) -> None:
        self.game.log(f'{self} builds a new roost.', logging_faction=self.faction)
        roost_to_place = self.get_unplaced_buildings()[0]
        warrior_count_to_place = max(4, len(self.get_unplaced_warriors()))
        warriors_to_place = self.get_unplaced_warriors()[:warrior_count_to_place]
        pieces_to_place = [roost_to_place]
        pieces_to_place.extend(warriors_to_place)

        suited_clearings_with_open_building_slots = [clearing for clearing in self.get_ruled_clearings() if
                                                     clearing.get_open_building_slot_count() > 0]
        sorted_open_building_slot_clearings = sort_clearings_by_priority(suited_clearings_with_open_building_slots)

        self.place_pieces_in_one_of_clearings(pieces_to_place, sorted_open_building_slot_clearings)

    def resolve_decree(self) -> None:
        for step in [self.recruit_step, self.move_step, self.battle_step]:
            for suit in [Suit.FOX, Suit.MOUSE, Suit.RABBIT, Suit.BIRD]:
                if self.turmoil:
                    return
                step(suit)

    def relentless(self) -> None:
        clearings_with_warriors = [clearing for clearing in self.game.clearings() if
                                   clearing.get_warrior_count_for_player(self) > 0]
        for clearing in clearings_with_warriors:
            players_with_defenseless_pieces = clearing.get_players_with_defenseless_pieces()
            for player in players_with_defenseless_pieces:
                defenseless_pieces: list[Piece] = [token for token in clearing.get_tokens_for_player(player)]
                defenseless_pieces.extend([building for building in clearing.get_buildings_for_player(player)])

                if self.has_trait(TRAIT_WAR_TAX):
                    player.add_victory_points(len(defenseless_pieces) * -1)
                self.add_victory_points(player.give_score_for_removed_pieces_not_in_battle(self, defenseless_pieces))
                clearing.remove_pieces(player, defenseless_pieces)

    def swoop(self) -> None:
        warrior_count_to_place = max(2, len(self.get_unplaced_warriors()))
        warriors_to_place = self.get_unplaced_warriors()[:warrior_count_to_place]
        clearings_without_own_pieces = [clearing for clearing in self.game.clearings() if
                                        clearing.get_piece_count_for_player(self) == 0]
        sorted_clearings_without_own_pieces = sort_clearings_by_priority(clearings_without_own_pieces)

        self.place_pieces_in_one_of_clearings(warriors_to_place, sorted_clearings_without_own_pieces)

    def turmoil_action(self) -> None:
        # HUMILIATE
        self.game.log(f'{self} enters turmoil.', logging_faction=self.faction)
        bird_cards_in_decree = self.decree.get_count_of_bird_cards_in_decree()
        if self.has_trait(TRAIT_NOBILITY):
            self.add_victory_points(bird_cards_in_decree)
        else:
            self.add_victory_points(bird_cards_in_decree * -1)
        # PURGE
        self.decree.purge()

    def does_rule_clearing(self, clearing: Clearing) -> bool:
        all_players_in_clearing = clearing.get_all_other_players_in_location(self)
        own_rule_value_in_clearing = self.get_rule_value(clearing)
        if own_rule_value_in_clearing == 0:
            return False
        for player in all_players_in_clearing:
            # LORDS OF THE FOREST: Eyrie Dynasties rule tied clearings
            if player.get_rule_value(clearing) > own_rule_value_in_clearing:
                return False
        return True

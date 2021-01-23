from __future__ import annotations
from abc import ABC, abstractmethod
import random
from typing import Optional, TYPE_CHECKING, Union

from battle_utils import DamageResult, RollResult
from locations.clearing import Clearing
from pieces.building import Building
from pieces.warrior import Warrior
from player_resources.piece_stock import PieceStock
from player_resources.supply import Supply

if TYPE_CHECKING:
    from constants import Faction, Suit
    from deck.cards.card import Card
    from game import Game
    from locations.forest import Forest
    from locations.location import Location
    from pieces.item_token import ItemToken
    from pieces.piece import Piece
    from pieces.token import Token


class Player(ABC):
    victory_points: int
    game: 'Game'
    faction: 'Faction'
    piece_stock: 'PieceStock'
    supply: 'Supply'
    hand: list['Card']
    revealed_cards: list['Card']
    crafted_items: list['ItemToken']

    def __init__(self, game: 'Game', faction: 'Faction', piece_stock: 'PieceStock' = None) -> None:
        if piece_stock is None:
            piece_stock = PieceStock(self)

        self.victory_points = 0
        self.game = game
        self.faction = faction

        self.piece_stock = piece_stock
        self.supply = Supply(game, self)

        self.hand = []
        self.revealed_cards = []
        self.crafted_items = []

    def setup(self) -> None:
        self.supply.add_pieces(self, self.piece_stock.pieces)

    def take_turn(self) -> None:
        self.birdsong()
        self.daylight()
        self.evening()

    # TODO: Remove
    def __repr__(self):
        return str(self.faction.value)

    @abstractmethod
    def birdsong(self) -> None:
        pass

    @abstractmethod
    def daylight(self) -> None:
        pass

    @abstractmethod
    def evening(self) -> None:
        pass

    def between_turns(self) -> None:
        pass

    def add_victory_points(self, victory_points: int) -> None:
        self.victory_points = max(0, self.victory_points + victory_points)
        if self.victory_points >= 30:
            self.game.win(self)
        if victory_points > 0:
            self.game.log(f'{self} has {self.victory_points} VP.', logging_faction=self.faction)

    def get_unplaced_pieces(self) -> list['Piece']:
        return self.supply.get_pieces()

    def get_unplaced_warriors(self) -> list['Warrior']:
        return self.supply.get_warriors()

    def get_unplaced_buildings(self) -> list['Building']:
        return self.supply.get_buildings()

    def get_unplaced_tokens(self) -> list['Token']:
        return self.supply.get_tokens()

    def get_unplaced_other_pieces(self) -> list['Piece']:
        return self.supply.get_other_pieces()

    ################
    #              #
    # Rule methods #
    #              #
    ################

    def does_rule_clearing(self, clearing: 'Clearing') -> bool:
        all_players_in_clearing = clearing.get_all_other_players_in_location(self)
        own_rule_value_in_clearing = self.get_rule_value(clearing)
        if own_rule_value_in_clearing == 0:
            return False
        for player in all_players_in_clearing:
            if player.get_rule_value(clearing) >= own_rule_value_in_clearing:
                return False
        return True

    def get_ruled_clearings(self) -> list['Clearing']:
        ruled_clearings = []
        for clearing in self.game.clearings():
            if self.does_rule_clearing(clearing):
                ruled_clearings.append(clearing)
        return ruled_clearings

    def get_ruled_suited_clearings(self, suit: Suit) -> list['Clearing']:
        ruled_suited_clearings = []
        for clearing in self.game.get_clearings_of_suit(suit):
            if self.does_rule_clearing(clearing):
                ruled_suited_clearings.append(clearing)
        return ruled_suited_clearings

    def get_rule_value(self, clearing: 'Clearing') -> int:
        rule_value = 0
        for piece in clearing.get_pieces_for_player(self):
            if isinstance(piece, Warrior) or isinstance(piece, Building):
                rule_value += 1
        return rule_value

    ##################
    #                #
    # Battle methods #
    #                #
    ##################

    def battle(self, clearing: 'Clearing', defender: 'Player') -> None:
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
        defender.add_victory_points(attacker_damage_result.points_awarded +
                                    defender.supplementary_score_for_removed_pieces_in_battle(
                                        self, attacker_damage_result.removed_pieces, is_attacker=False))

    def suffer_damage(self, clearing: 'Clearing', hits: int, opponent: 'Player', is_attacker: bool) -> 'DamageResult':
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
            amount_of_buildings_removed = min(hits, len(buildings))
            hits -= amount_of_buildings_removed
            for i in range(amount_of_buildings_removed):
                removed_pieces.append(buildings[i])
                points_awarded += buildings[i].get_score_for_removal()

        self.game.log(f'{self} loses the following pieces: {removed_pieces}', logging_faction=self.faction)
        clearing.remove_pieces(self, removed_pieces)
        return DamageResult(removed_pieces=removed_pieces, points_awarded=points_awarded)

    def allocate_rolls_as_defender(self, rolls: tuple[int, int]) -> 'RollResult':
        if rolls[0] < rolls[1]:
            return RollResult(attacker_roll=rolls[1], defender_roll=rolls[0])
        return RollResult(attacker_roll=rolls[0], defender_roll=rolls[1])

    def cap_rolled_hits(self, clearing: 'Clearing', roll: int) -> int:
        return min(roll, clearing.get_warrior_count_for_player(self))

    def get_bonus_hits(self, clearing: 'Clearing', opponent: 'Player', is_attacker: bool = True) -> int:
        bonus_hits = 0
        if clearing.get_warrior_count_for_player(self) > 0 and opponent.is_defenseless(clearing):
            bonus_hits += 1
        return bonus_hits

    # TODO: Vagabot is not a warrior, but never defenseless. RC are not defenseless with a Garrison
    def is_defenseless(self, clearing: 'Clearing') -> bool:
        return clearing.get_warrior_count_for_player(self) == 0 and clearing.get_piece_count_for_player(self) > 0

    def give_score_for_removed_pieces_not_in_battle(self, other_player: 'Player', removed_pieces: list['Piece']) -> int:
        victory_points_gained = 0
        for piece in removed_pieces:
            victory_points_gained += piece.get_score_for_removal()
        return victory_points_gained

    def supplementary_score_for_removed_pieces_in_battle(self, other_player: 'Player', removed_pieces: list['Piece'],
                                                         is_attacker: bool) -> int:
        return 0

    def supplementary_score_for_removed_pieces_not_in_battle(self, other_player: 'Player',
                                                             removed_pieces: list['Piece']) -> int:
        return 0

    ################
    #              #
    # Move methods #
    #              #
    ################

    # This assumes you have already checked that the move is legal
    def move(self, moving_pieces: list['Piece'], origin: 'Location', destination: 'Location') -> None:
        return origin.move_pieces(self, moving_pieces, destination)

    def move_removed_pieces_into_supply(self, pieces: list['Piece'], origin_location: 'Location') -> None:
        self.supply.add_pieces(self, pieces)

    # Hospitals and Robot Revenge are not triggered if they are not the attacker
    def move_removed_pieces_into_supply_from_battle(self, pieces: list['Piece'], origin_location: 'Location',
                                                    is_attacker: bool) -> None:
        self.move_removed_pieces_into_supply(pieces, origin_location)

    # TODO: Only if the player has bought Riverboats
    def treats_rivers_as_paths(self) -> bool:
        return False

    def halves_damage(self, battle_clearing: 'Clearing') -> bool:
        return False

    #########################
    #                       #
    # Hand and card methods #
    #                       #
    #########################

    # TODO: Only Cogwheel Cult
    def takes_discarded_cards(self) -> bool:
        return False

    def handle_discarded_card(self, card: 'Card') -> None:
        pass

    def get_adjacent_clearings(self, origin: Union['Clearing', 'Forest']) -> list['Clearing']:
        if isinstance(origin, Clearing):
            adjacent_clearings = set(origin.path_connected_clearings)
            if self.treats_rivers_as_paths():
                adjacent_clearings.update(origin.river_connected_clearings)
        else:
            adjacent_clearings = origin.adjacent_clearings
        return list(adjacent_clearings)

    def get_item(self, item_token: 'ItemToken') -> None:
        self.crafted_items.append(item_token)

    def draw_card(self) -> None:
        self.draw_cards(1)

    def draw_cards(self, number_of_cards: int = 1) -> None:
        drawn_cards = []
        for _ in range(number_of_cards):
            card = self.game.draw_card()
            if card:
                drawn_cards.append(card)
        self.hand.extend(drawn_cards)

    def add_card_to_hand(self, card: Optional['Card']) -> None:
        if card:
            self.hand.append(card)

    def take_random_card_from_hand(self) -> Optional['Card']:
        if self.hand:
            random.shuffle(self.hand)
            return self.hand.pop()

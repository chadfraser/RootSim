from __future__ import annotations
import random
from typing import TYPE_CHECKING

from battle_utils import RollResult, DamageResult
from bot_resources.bot import Bot
from bot_resources.bot_factions.automated_alliance.automated_alliance_piece_stock import AutomatedAlliancePieceStock
from bot_resources.bot_factions.automated_alliance.automated_alliance_trait import TRAIT_INFORMANTS, \
    TRAIT_POPULARITY, TRAIT_VETERANS, TRAIT_WILDFIRE
from bot_resources.bot_factions.automated_alliance.base import Base
from bot_resources.bot_factions.automated_alliance.sympathy import Sympathy
from constants import Faction, Suit
from locations.clearing import Clearing
from player_resources.supply import Supply
from sort_utils import sort_clearings_by_enemy_pieces, sort_clearings_by_martial_law, sort_clearings_by_priority, \
    sort_clearings_by_matching_suit

if TYPE_CHECKING:
    from deck.cards.card import Card
    from game import Game
    from locations.location import Location
    from pieces.item_token import ItemToken
    from pieces.piece import Piece
    from player_resources.player import Player


class AutomatedAlliancePlayer(Bot):
    victory_points: int
    game: Game
    faction: Faction
    piece_stock: AutomatedAlliancePieceStock
    supply: Supply
    revealed_cards: list[Card]
    crafted_items: list[ItemToken]
    has_revolted: bool
    players_who_have_removed_sympathy_since_last_turn: set[Player]

    SYMPATHY_SCORES = [0, 1, 1, 1, 2, 2, 3, 4, 4, 4]

    def __init__(self, game: Game) -> None:
        piece_stock = AutomatedAlliancePieceStock(self)
        super().__init__(game, Faction.AUTOMATED_ALLIANCE, piece_stock)

        self.has_revolted = False
        self.players_who_have_removed_sympathy_since_last_turn = set()

    def setup(self) -> None:
        pass

    ######################
    #                    #
    # Turn order methods #
    #                    #
    ######################

    def birdsong(self) -> None:
        self.has_revolted = False
        self.players_who_have_removed_sympathy_since_last_turn = set()
        self.reveal_order()
        if self.order_card.suit != Suit.BIRD:
            self.revolt_step()

    def daylight(self) -> None:
        self.spread_sympathy()
        if self.order_card.suit == Suit.BIRD:
            self.revolt_step()
        if not self.has_revolted:
            self.public_pity()

    def evening(self) -> None:
        self.organize_step()
        self.recruit_step()
        if self.has_trait(TRAIT_WILDFIRE):
            self.wildfire()
        self.game.discard_card(self.order_card)
        self.order_card = None

    def between_turns(self) -> None:
        self.players_who_have_removed_sympathy_since_last_turn = set()

########################################################################################################################

    def get_clearings_to_revolt_in(self) -> list[Clearing]:
        valid_revolt_clearings = []
        for base in self.piece_stock.get_bases():
            # Skip bases that don't match the order card
            if not Suit.are_suits_equal(base.location, self.order_card.suit):
                continue
            # Skip bases that are on the map
            if not isinstance(base.location, Supply):
                continue
            # Skip bases without matching sympathetic clearings
            for token in self.piece_stock.get_sympathy():
                # We don't check if clearing.can_place_piece here, because any piece that prevents the base from being
                # placed is removed by the revolt
                if isinstance(token.location, Clearing) and token.location.suit == base.suit:
                    valid_revolt_clearings.append(token.location)
        return valid_revolt_clearings

    def revolt_step(self) -> None:
        # Target a clearing for the revolt
        valid_revolt_clearings = self.get_clearings_to_revolt_in()
        sorted_valid_revolt_clearings = sort_clearings_by_priority(valid_revolt_clearings)
        sorted_valid_revolt_clearings = sort_clearings_by_enemy_pieces(sorted_valid_revolt_clearings, self)
        if not sorted_valid_revolt_clearings:
            return
        target_clearing = sorted_valid_revolt_clearings[0]

        # Remove all enemy pieces from the target clearing
        players_in_clearing = target_clearing.get_all_players_in_location()
        removed_pieces = []
        for player in players_in_clearing:
            for piece in target_clearing.get_pieces_for_player(player):
                removed_pieces.append(piece)
            removed_pieces.extend(target_clearing.remove_all_pieces_of_player(player))
            self.add_victory_points(player.give_score_for_removed_pieces_not_in_battle(player, removed_pieces))

        # Place base in the target clearing
        base_to_place = [base for base in self.piece_stock.get_bases() if base.suit == target_clearing.suit][0]
        target_clearing.add_piece(self, base_to_place)
        self.has_revolted = True

    def public_pity(self) -> None:
        placed_sympathy = [token for token in self.piece_stock.get_sympathy() if isinstance(token.location, Clearing)]
        if len(placed_sympathy) <= 4:
            self.spread_sympathy()
        self.spread_sympathy()

    def spread_sympathy(self, score: bool = True) -> None:
        unplaced_sympathy = [token for token in self.get_unplaced_tokens()]
        if not unplaced_sympathy:
            self.score_bonus_for_unplaced_sympathy(score)
            return

        sympathy_tokens_clearings = [token.location for token in self.piece_stock.get_sympathy() if
                                     isinstance(token.location, Clearing)]
        # If no sympathy tokens are already on the map, the first token can be placed anywhere
        if not sympathy_tokens_clearings:
            sympathy_adjacent_clearings = [clearing for clearing in self.game.clearings()]
        # Otherwise, we only look at clearings already adjacent to sympathy tokens
        else:
            sympathy_adjacent_clearings = set()
            for sympathetic_clearing in sympathy_tokens_clearings:
                adjacent_clearings = self.get_adjacent_clearings(sympathetic_clearing)
                for adjacent_clearing in adjacent_clearings:
                    sympathy_adjacent_clearings.add(adjacent_clearing)
            sympathy_adjacent_clearings = list(sympathy_adjacent_clearings)
        if not sympathy_adjacent_clearings:
            self.score_bonus_for_unplaced_sympathy(score)
            return

        if self.order_card.suit == Suit.BIRD:
            self.spread_sympathy_with_bird_order_card(sympathy_adjacent_clearings, score)
        else:
            self.spread_sympathy_without_bird_order_card(sympathy_adjacent_clearings, score)

    # If no sympathy tokens are on the map, sympathy_adjacent_clearings is all clearings
    # Otherwise, it's all clearings that are adjacent to a clearing with a sympathy token
    # Spread using the tie-breaker: Avoid martial law -> respect order suit -> high priority
    def spread_sympathy_without_bird_order_card(self, sympathy_adjacent_clearings: list[Clearing],
                                                score: bool = True) -> None:
        unplaced_sympathy = [token for token in self.get_unplaced_tokens()]
        unplaced_sympathy_count = len(unplaced_sympathy)
        sorted_sympathy_adjacent_clearings = sort_clearings_by_priority(sympathy_adjacent_clearings)
        sorted_sympathy_adjacent_clearings = sort_clearings_by_matching_suit(sorted_sympathy_adjacent_clearings,
                                                                             self.order_card.suit)
        sorted_sympathy_adjacent_clearings = sort_clearings_by_martial_law(sorted_sympathy_adjacent_clearings, self)

        self.place_pieces_in_one_of_clearings(unplaced_sympathy[:1], sorted_sympathy_adjacent_clearings)
        if score:
            if unplaced_sympathy_count > len(self.get_unplaced_tokens()):
                self.score_for_sympathy()
            else:
                self.score_bonus_for_unplaced_sympathy(score)

    # If no sympathy tokens are on the map, sympathy_adjacent_clearings is all clearings
    # Otherwise, it's all clearings that are adjacent to a clearing with a sympathy token
    # Spread into the lowest priority valid clearing, regardless of martial law or clearing suit
    def spread_sympathy_with_bird_order_card(self, sympathy_adjacent_clearings: list[Clearing],
                                             score: bool = True) -> None:
        unplaced_sympathy = [token for token in self.get_unplaced_tokens()]
        unplaced_sympathy_count = len(unplaced_sympathy)
        sorted_sympathy_adjacent_clearings = sort_clearings_by_priority(sympathy_adjacent_clearings, descending=False)
        self.place_pieces_in_one_of_clearings(unplaced_sympathy[:1], sorted_sympathy_adjacent_clearings)
        if score:
            if unplaced_sympathy_count > len(self.get_unplaced_tokens()):
                self.score_for_sympathy()
            else:
                self.score_bonus_for_unplaced_sympathy(score)

    def recruit_step(self) -> None:
        base_clearings = [base.location for base in self.piece_stock.get_bases() if
                          isinstance(base.location, Clearing)]
        sorted_base_clearings = sort_clearings_by_priority(base_clearings)
        for base_clearing in sorted_base_clearings:
            if not self.get_unplaced_warriors():
                return
            # A bit oddly written, but this takes care of removing a snare if one prevents the warrior from being
            # recruited at the base
            self.place_pieces_in_one_of_clearings(self.get_unplaced_warriors()[:1], [base_clearing])
        # base_clearings = [base.location for base in self.piece_stock.get_bases() if
        #                   isinstance(base.location, Clearing) and
        #                   base.location.can_place_piece(self, warriors_available_to_recruit[0])]
        # sorted_base_clearings = sort_clearings_by_priority(base_clearings)
        # if len(warriors_available_to_recruit) < len(sorted_base_clearings):
        #     sorted_base_clearings = sorted_base_clearings[:len(warriors_available_to_recruit)]
        #
        # for idx, clearing in enumerate(sorted_base_clearings):
        #     clearing.add_piece(self, warriors_available_to_recruit[idx])

    def organize_step(self) -> None:
        base_clearings = [base.location for base in self.piece_stock.get_bases() if
                          isinstance(base.location, Clearing)]
        sorted_base_clearings = sort_clearings_by_priority(base_clearings)
        for clearing in sorted_base_clearings:
            if clearing.get_warrior_count_for_player(self) >= self.get_organizing_amount():
                clearing.remove_pieces(self, clearing.get_warriors_for_player(self))
                self.spread_sympathy()

    def get_organizing_amount(self) -> int:
        return 2 + self.difficulty.value

    def wildfire(self):
        self.spread_sympathy(score=False)

########################################################################################################################

    def suffer_damage(self, clearing: Clearing, hits: int, opponent: Player, is_attacker: bool) -> DamageResult:
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
                # If the Popularity trait is used, players can't score for sympathy if they already have since last turn
                if (not self.has_trait(TRAIT_POPULARITY) or
                        opponent not in self.players_who_have_removed_sympathy_since_last_turn):
                    points_awarded += tokens[i].get_score_for_removal()
                self.players_who_have_removed_sympathy_since_last_turn.add(opponent)
        if hits:
            buildings = clearing.get_buildings_for_player(self)
            random.shuffle(buildings)
            amount_of_buildings_removed = min(hits, len(buildings))
            hits -= amount_of_buildings_removed
            for i in range(amount_of_buildings_removed):
                removed_pieces.append(buildings[i])
                points_awarded += buildings[i].get_score_for_removal()
        clearing.remove_pieces(self, removed_pieces)
        return DamageResult(removed_pieces=removed_pieces, points_awarded=points_awarded)

    def give_score_for_removed_pieces_not_in_battle(self, other_player: Player, removed_pieces: list[Piece]) -> int:
        victory_points_gained = 0
        for piece in removed_pieces:
            if isinstance(piece, Sympathy):
                # If the Popularity trait is used, players can't score for sympathy if they already have since last turn
                # This breaks with Instigate since that's the only way for a player to remove a token on someone else's
                # turn... but let's ignore that for now!
                if (not self.has_trait(TRAIT_POPULARITY) or
                        other_player not in self.players_who_have_removed_sympathy_since_last_turn):
                    victory_points_gained += piece.get_score_for_removal()
                self.players_who_have_removed_sympathy_since_last_turn.add(other_player)
            else:
                victory_points_gained += piece.get_score_for_removal()
        return victory_points_gained

    def allocate_rolls_as_defender(self, rolls: tuple[int, int]) -> RollResult:
        if self.has_trait(TRAIT_VETERANS):
            # Give both players the high roll
            if rolls[0] < rolls[1]:
                return RollResult(attacker_roll=rolls[1], defender_roll=rolls[1])
            return RollResult(attacker_roll=rolls[0], defender_roll=rolls[0])
        else:
            return super().allocate_rolls_as_defender(rolls)

    # CRACKDOWN: When destroying a base, lose all sympathy of that suit
    def move_removed_pieces_into_supply(self, pieces: list[Piece], origin_location: Location) -> None:
        for piece in pieces:
            if isinstance(piece, Base):
                for sympathy in self.piece_stock.get_sympathy():
                    if isinstance(sympathy.location, Clearing) and sympathy.location.suit == piece.suit:
                        sympathy.location.remove_pieces(self, [sympathy])
        self.supply.add_pieces(self, pieces)

    def score_for_sympathy(self) -> None:
        placed_sympathy = [token for token in self.piece_stock.get_sympathy() if isinstance(token.location, Clearing)]
        score_for_sympathy = self.SYMPATHY_SCORES[len(placed_sympathy) - 1]
        self.add_victory_points(score_for_sympathy)

    def score_bonus_for_unplaced_sympathy(self, score: bool) -> None:
        if score:
            self.add_victory_points(5)  # 5-point bonus if you could not spread sympathy

    def get_bonus_hits(self, clearing: Clearing, opponent: Player, is_attacker: bool = True) -> int:
        bonus_hits = 0
        # Automated Ambush
        if clearing.get_warrior_count_for_player(self) > 0:
            bonus_hits += 1
        elif self.has_trait(TRAIT_INFORMANTS) and clearing.get_token_count_for_player(self) > 0:
            bonus_hits += 1
        return bonus_hits

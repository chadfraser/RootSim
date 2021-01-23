from __future__ import annotations
import random
from typing import TYPE_CHECKING, Optional, cast, Callable, Any

from battle_utils import DamageResult
from bot_resources.bot import Bot
from bot_resources.bot_factions.vagabot.satchel import Satchel
from bot_resources.bot_factions.vagabot.vagabot_piece_stock import VagabotPieceStock
from bot_resources.bot_factions.vagabot.vagabot_trait import TRAIT_ADVENTURER, TRAIT_BERSERKER, TRAIT_HELPER, \
    TRAIT_MARKSMAN
from bot_resources.bot_factions.vagabot.vagabot_characters import VagabotCharacter
from constants import Faction, Item, Suit
from deck.quest_deck import QuestCard
from locations.clearing import Clearing
from locations.forest import Forest
from pieces.warrior import Warrior
from player_resources.supply import Supply
from sort_utils import sort_clearings_by_enemy_pieces, \
    sort_clearings_by_priority, sort_paths_by_lexicographic_priority, \
    sort_paths_by_destination_priority, sort_paths_by_distance, sort_players_by_pieces_in_clearing, \
    sort_players_by_setup_order, sort_players_by_victory_points, sort_paths_by_destination_player_list

if TYPE_CHECKING:
    from deck.cards.card import Card
    from game import Game
    from locations.location import Location
    from pieces.item_token import ItemToken
    from pieces.piece import Piece
    from player_resources.player import Player


class VagabotPlayer(Bot):
    victory_points: int
    game: 'Game'
    faction: 'Faction'
    piece_stock: 'VagabotPieceStock'
    supply: 'Supply'
    revealed_cards: list['Card']
    crafted_items: list['ItemToken']
    character: 'VagabotCharacter'
    quest: Optional['QuestCard']
    satchel: 'Satchel'
    has_slipped: bool
    has_battled: bool

    def __init__(self, game: 'Game', character: 'VagabotCharacter') -> None:
        piece_stock = VagabotPieceStock(self)
        super().__init__(game, Faction.VAGABOT, piece_stock)

        self.has_slipped = False
        self.has_battled = False
        self.character = character
        self.quest = self.game.quest_deck.draw_quest_card()
        self.satchel = Satchel(self.game, self)

        for _ in range(self.character.starting_item_amount):
            random_item = random.choice(list(Item))
            self.satchel.add_item(ItemToken(random_item, is_starting_item=True))

    def setup(self) -> None:
        maximum_adjacent_clearings = 0
        forests_with_maximum_adjacent_clearings = []
        for forest in self.game.board_map.forests:
            if maximum_adjacent_clearings < len(forest.adjacent_clearings):
                maximum_adjacent_clearings = forest.adjacent_clearings
                forests_with_maximum_adjacent_clearings = [forest]
            elif maximum_adjacent_clearings == len(forest.adjacent_clearings):
                forests_with_maximum_adjacent_clearings.append(forest)
        random.shuffle(forests_with_maximum_adjacent_clearings)
        forests_with_maximum_adjacent_clearings[0].add_piece(self, self.get_pawn())

    ######################
    #                    #
    # Turn order methods #
    #                    #
    ######################

    def birdsong(self) -> None:
        self.has_slipped = False
        self.has_battled = False
        self.reveal_order()
        if len(self.satchel.undamaged_items) < 3:
            self.slip_into_forest()

    def daylight(self) -> None:
        # Skip Daylight if you've slipped into a Forest
        if self.has_slipped:
            return
        if self.order_card.suit == Suit.FOX:
            self.explore_step()
            self.special_step()
            self.battle_step()
        elif self.order_card.suit == Suit.RABBIT:
            self.special_step()
            self.aid_step()
            self.battle_step()
        elif self.order_card.suit == Suit.MOUSE:
            self.quest_step()
            self.aid_step()
            self.battle_step()
        else:
            self.explore_step()
            self.quest_step()
            self.battle_step()
        if self.has_trait(TRAIT_ADVENTURER):
            self.adventurer()

    def evening(self) -> None:
        self.refresh_step()
        self.repair_step()
        self.game.discard_card(self.order_card)
        self.order_card = None

    ########################
    #                      #
    # Pawn utility methods #
    #                      #
    ########################

    def get_pawn_location(self) -> 'Location':
        return self.piece_stock.get_pawn_location()

    def get_pawn(self) -> Piece:
        return self.piece_stock.get_pawn()

    def move_pawn(self, destination: 'Location', exhaust_item: bool = True) -> None:
        current_location = self.get_pawn_location()
        # Don't try to move if you're already at the destination, or if you need to exhaust an item to move but have
        # no unexhausted undamaged items
        if current_location == destination:
            return
        if exhaust_item and not self.satchel.exhaust_items_if_possible():
            return
        self.move([self.get_pawn()], self.get_pawn_location(), destination)
        if self.get_pawn_location() == current_location:
            self.remove_snare_if_it_prevents_movement([self.get_pawn()], cast(Clearing, current_location),
                                                      [destination], requires_rule=False)

    def move_along_path(self, path: list['Clearing']) -> None:
        while path and self.satchel.get_unexhausted_undamaged_items():
            next_step = path[0]
            self.move_pawn(next_step)
            # If the move was successful, pop it from the list
            # Otherwise (e.g., we were in a snared clearing), try again
            if self.get_pawn_location() == next_step:
                path.pop(0)

    def slip_into_forest(self) -> None:
        pawn_location = self.get_pawn_location()
        # Sanity check
        if not (isinstance(pawn_location, Clearing) or isinstance(pawn_location, Forest)):
            return
        destinations = [forest for forest in pawn_location.adjacent_forests]
        # Slip into a random forest
        random.shuffle(destinations)
        self.move_pawn(destinations[0])  # TODO: This currently runs with SLIP-4, but SLIP-1 or SLIP-2 are more likely
        self.has_slipped = True

    def travel_to_target_clearings(self, target_clearings: list['Clearing'],
                                   sorting_methods: list[Callable] = None, arguments: list[list[Any]] = None) -> None:
        # Default sorting order for traveling to one of the target clearings:
        # Path length -> destination clearing priority -> lexicographic clearing priority
        # This means we should travel the shortest path, towards the highest-priority destination, and each step to
        # that destination will be the highest-priority step we can take along that path
        if not sorting_methods:
            sorting_methods = [sort_paths_by_lexicographic_priority,
                               sort_paths_by_destination_priority,
                               sort_paths_by_distance]
        if not arguments:
            arguments = [[] for _ in sorting_methods]

        pawn_location = self.get_pawn_location()
        # Sanity check
        if not (isinstance(pawn_location, Clearing) or isinstance(pawn_location, Forest)):
            return

        potential_movement_routes = []
        for clearing in target_clearings:
            potential_movement_routes.extend(
                pawn_location.find_shortest_legal_paths_to_destination_clearing(self, self.get_pawn(), clearing))
        if not potential_movement_routes:
            return
        # Sort in reverse order from our tie-breaking priority:
        for sorting_method, args in zip(sorting_methods, arguments):
            potential_movement_routes = sorting_method(potential_movement_routes, *args)
        # sorted_potential_movement_routes = sort_paths_by_lexicographic_priority(potential_movement_routes)
        # sorted_potential_movement_routes = sort_paths_by_destination_priority(sorted_potential_movement_routes)
        # sorted_potential_movement_routes = sort_paths_by_distance(sorted_potential_movement_routes)
        # self.move_along_path(sorted_potential_movement_routes[0])
        self.move_along_path(potential_movement_routes[0])

    #######################
    #                     #
    # Turn action methods #
    #                     #
    #######################

    def explore_step(self) -> None:
        ruin_clearings = [clearing for clearing in self.game.clearings() if clearing.ruin]
        if not ruin_clearings:
            return
        self.travel_to_target_clearings(ruin_clearings)
        if self.get_pawn_location() in ruin_clearings:
            if self.satchel.exhaust_items_if_possible():
                cast(Clearing, self.get_pawn_location()).explore_ruin(self)

    def special_step(self):
        if self.character.can_perform_special_action() and self.satchel.exhaust_items_if_possible():
            self.character.perform_special_action()

    def quest_step(self):
        if not self.quest:
            return
        quest_clearings = [clearing for clearing in self.game.get_clearings_of_suit(self.quest.suit)]
        self.travel_to_target_clearings(quest_clearings)
        if self.get_pawn_location() in quest_clearings:
            if self.satchel.exhaust_items_if_possible(item_count=2):
                self.add_victory_points(2)
                self.quest = self.game.quest_deck.draw_quest_card()

    def aid_step(self) -> None:
        players_with_crafted_items = [player for player in self.game.players if player.crafted_items]
        sorted_players_with_crafted_items = sort_players_by_setup_order(players_with_crafted_items)
        sorted_players_with_crafted_items = sort_players_by_victory_points(sorted_players_with_crafted_items,
                                                                           descending=False)

        valid_aid_clearings = [clearing for clearing in self.game.clearings() if
                               any(clearing.is_player_in_location(player) for player in players_with_crafted_items)]
        if not valid_aid_clearings:
            if self.has_trait(TRAIT_HELPER):
                return self.helper_aid_step()
            else:
                return

        self.travel_to_target_clearings(valid_aid_clearings,
                                        sorting_methods=[sort_paths_by_lexicographic_priority,
                                                         sort_paths_by_destination_priority,
                                                         sort_paths_by_destination_player_list,
                                                         sort_paths_by_distance],
                                        arguments=[[],
                                                   [],
                                                   [sorted_players_with_crafted_items],
                                                   []])

        if self.get_pawn_location() in valid_aid_clearings:
            valid_aid_players = [player for player in
                                 self.get_pawn_location().get_all_other_players_in_location(self) if
                                 player.crafted_items]
            sorted_valid_aid_players = sort_players_by_setup_order(valid_aid_players)
            sorted_valid_aid_players = sort_players_by_victory_points(sorted_valid_aid_players)
            if sorted_valid_aid_players and self.satchel.exhaust_items_if_possible():
                item_taken = sorted_valid_aid_players[0].crafted_items.pop()
                self.get_item(item_taken)
                self.add_victory_points(1)
                if not isinstance(sorted_valid_aid_players[0], Player):
                    sorted_valid_aid_players[0].add_card_to_hand(self.game.draw_card())
                sorted_valid_aid_players[0].add_victory_points(1)

    def helper_aid_step(self) -> None:
        player_to_aid = self.get_helper_aid_target()
        if not player_to_aid:
            return

        valid_aid_clearings = [clearing for clearing in self.game.clearings() if
                               clearing.is_player_in_location(player_to_aid)]
        self.travel_to_target_clearings(valid_aid_clearings)

        if self.get_pawn_location() in valid_aid_clearings and self.satchel.exhaust_items_if_possible():
            self.add_victory_points(1)
            if not isinstance(player_to_aid, Player):
                player_to_aid.add_card_to_hand(self.game.draw_card())
            player_to_aid.add_victory_points(1)

    def get_helper_aid_target(self) -> Optional[Player]:
        sorted_players = sort_players_by_setup_order(self.game.players)
        sorted_players = sort_players_by_victory_points(sorted_players, descending=False)
        for player in sorted_players:
            valid_aid_clearings = [clearing for clearing in self.game.clearings() if
                                   clearing.is_player_in_location(player)]
            if valid_aid_clearings:
                return player

    def battle_step(self) -> None:
        if self.has_trait(TRAIT_BERSERKER):
            return self.berserker_battle_step()

        target_opponent = self.get_battle_target()
        if not target_opponent:
            return

        valid_battle_clearings = [clearing for clearing in self.game.clearings() if
                                  clearing.is_player_in_location(target_opponent)]
        self.travel_to_target_clearings(valid_battle_clearings)

        # The first battle each turn requires exhausting one item. Future battles require exhausting two items
        if self.has_battled:
            battle_cost = 2
        else:
            battle_cost = 1
        if self.get_pawn_location() in valid_battle_clearings and self.satchel.exhaust_items_if_possible(battle_cost):
            self.battle(cast(Clearing, self.get_pawn_location()), target_opponent)
            self.has_battled = True
        # Repeat the battle step unless you have the Adventurer trait
        if not self.has_trait(TRAIT_ADVENTURER):
            self.battle_step()

    def get_battle_target(self) -> Optional[Player]:
        sorted_players = sort_players_by_setup_order(self.game.players)
        sorted_players = sort_players_by_victory_points(sorted_players)
        for player in sorted_players:
            valid_battle_clearings = [clearing for clearing in self.game.clearings() if
                                      clearing.is_player_in_location(player)]
            if valid_battle_clearings:
                return player

    def berserker_battle_step(self) -> None:
        valid_battle_clearings = [clearing for clearing in self.game.clearings() if
                                  clearing.is_any_other_player_in_location(self)]
        sorted_valid_battle_clearings = sort_clearings_by_priority(valid_battle_clearings)
        sorted_valid_battle_clearings = sort_clearings_by_enemy_pieces(sorted_valid_battle_clearings, self)
        if not sorted_valid_battle_clearings:
            return
        target_battle_clearing = sorted_valid_battle_clearings[0]
        self.travel_to_target_clearings([target_battle_clearing], sorting_methods=[])

        # The first battle each turn requires exhausting one item. Future battles require exhausting two items
        if self.has_battled:
            battle_cost = 2
        else:
            battle_cost = 1
        if self.get_pawn_location() == target_battle_clearing and self.satchel.exhaust_items_if_possible(battle_cost):
            self.berserker_initiate_battle(target_battle_clearing)
        if not self.has_trait(TRAIT_ADVENTURER):
            self.berserker_battle_step()

    def berserker_initiate_battle(self, clearing: Clearing) -> None:
        potential_targets = clearing.get_all_other_players_in_location(self)
        # Sort in reverse order from our tie-breaking priority: Setup order -> most pieces
        potential_targets = sort_players_by_setup_order(potential_targets)
        potential_targets = sort_players_by_pieces_in_clearing(potential_targets, clearing)
        if potential_targets:
            self.battle(clearing, potential_targets[0])

    ##########################
    #                        #
    # Evening action methods #
    #                        #
    ##########################

    def adventurer(self) -> None:
        current_quest_card = None
        # Repeat the quest action until the quest card hasn't changed - when that happens, we know we can't complete a
        # quest right now
        while current_quest_card != self.quest:
            current_quest_card = self.quest
            self.quest_step()

    def refresh_step(self) -> None:
        for _ in range(self.get_refresh_amount()):
            self.satchel.refresh_item()
        # Refresh two bonus items if you have no damaged items
        if not self.satchel.damaged_items:
            self.satchel.refresh_item()
            self.satchel.refresh_item()

    def get_refresh_amount(self) -> int:
        return 3 + self.difficulty.value

    def repair_step(self) -> None:
        if isinstance(self.get_pawn_location(), Forest):
            self.satchel.repair_all_items()
        else:
            if self.has_trait(TRAIT_BERSERKER):
                self.satchel.repair_item()
            self.satchel.repair_item()

    ##################
    #                #
    # Battle methods #
    #                #
    ##################

    def battle(self, clearing: Clearing, defender: Player) -> None:
        if self.has_trait(TRAIT_MARKSMAN):
            # Fortified MM is currently the only way for a piece to require two hits to be removed in battle
            # Marksman Vagabot is currently the only way for a player to deal hits in battle to a bot before the roll
            # To prevent messy logic in handling taking hits, we just deal two hits of damage in this case, which will
            # still functionally remove one building
            if defender.halves_damage(clearing):
                marksman_damage_result = defender.suffer_damage(clearing, 2, self, is_attacker=False)
            else:
                marksman_damage_result = defender.suffer_damage(clearing, 1, self, is_attacker=False)
            self.add_victory_points(marksman_damage_result.points_awarded +
                                    self.supplementary_score_for_removed_pieces_in_battle(
                                        defender, marksman_damage_result.removed_pieces, is_attacker=True))
        random_rolls = (random.randint(0, 3), random.randint(0, 3))
        # Defender allocates the rolls - high roll to attacker, low roll to defender, except in the case of Veterans
        roll_result = defender.allocate_rolls_as_defender(random_rolls)
        # Each battler caps their hits and adds their relevant bonus hits
        attacker_hits = (self.cap_rolled_hits(clearing, roll_result.attacker_roll) +
                         self.get_bonus_hits(clearing, defender, is_attacker=True))
        defender_hits = (defender.cap_rolled_hits(clearing, roll_result.defender_roll) +
                         defender.get_bonus_hits(clearing, defender, is_attacker=False))
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

    def cap_rolled_hits(self, clearing: Clearing, roll: int) -> int:
        # The battle track can hold up to 3 items tokens, but only the first two count towards rolled hits
        # So even though roll will never be greater than 3, we're explicitly capping the battle track rolled hits to 3,
        # just in case
        return min(roll, 1 + len(self.satchel.battle_track), 3)

    # TODO: Mercenaries from Involved Rivetfolk
    def suffer_damage(self, clearing: Clearing, hits: int, opponent: Player, is_attacker: bool) -> DamageResult:
        if hits:
            exhausted_items = self.satchel.get_exhausted_undamaged_items(-1)
            amount_of_items_damaged = min(hits, len(exhausted_items))
            hits -= amount_of_items_damaged
            for i in range(amount_of_items_damaged):
                self.satchel.damage_specific_item(exhausted_items[i])
        if hits:
            unexhausted_items = self.satchel.get_unexhausted_undamaged_items(-1)
            amount_of_items_damaged = min(hits, len(unexhausted_items))
            hits -= amount_of_items_damaged
            for i in range(amount_of_items_damaged):
                self.satchel.damage_specific_item(unexhausted_items[i])
        return DamageResult(removed_pieces=[], points_awarded=0)

    def supplementary_score_for_removed_pieces_in_battle(self, other_player: Player, removed_pieces: list[Piece],
                                                         is_attacker: bool) -> int:
        if not is_attacker:
            return 0
        # Hostility bonus: The Vagabot scores 1 VP per enemy warrior removed when they're the attacker in battle
        return len([piece for piece in removed_pieces if isinstance(piece, Warrior)])

    def get_bonus_hits(self, clearing: Clearing, opponent: Player, is_attacker: bool = True) -> int:
        return len(self.satchel.battle_track) == 3

    def is_defenseless(self, clearing: Clearing) -> bool:
        return False

########################################################################################################################

    def get_item(self, item_token: ItemToken) -> None:
        self.satchel.add_item(item_token)

from __future__ import annotations
from typing import TYPE_CHECKING

from player_resources.player_piece_map import PlayerPieceMap

if TYPE_CHECKING:
    from game import Game
    from pieces.building import Building
    from pieces.piece import Piece
    from pieces.token import Token
    from pieces.warrior import Warrior
    from player_resources.player import Player


class Location:
    game: Game
    pieces: dict['Player', 'PlayerPieceMap']

    def __init__(self, game: 'Game') -> None:
        self.game = game
        self.pieces = {}

    #################################
    #                               #
    # PlayerPieceMap helper methods #
    #                               #
    #################################

    # Helper to ensure we always get a PlayerPieceMap, creating one if it doesn't already exist
    def piece_map(self, player: 'Player') -> 'PlayerPieceMap':
        if not self.pieces.get(player):
            self.pieces[player] = PlayerPieceMap(player, self)
        return self.pieces.get(player)

    def set_player_piece_map(self, player_piece_map: 'PlayerPieceMap') -> None:
        self.pieces[player_piece_map.player] = player_piece_map

    def get_piece_map_for_player(self, player: 'Player') -> 'PlayerPieceMap':
        return self.piece_map(player)

    ##################################################################
    #                                                                #
    # Permission checks for placing or moving pieces in the location #
    #                                                                #
    ##################################################################

    # 'Place' != 'add'
    # Placing is specifically moving it from an external source to the location on the map
    # Cannot place: multiple roosts/sympathy/tradeposts, at Keep unless MM, in Burrow unless DD, at Snare unless CC
    def can_place_piece(self, player: 'Player', piece: 'Piece') -> bool:
        return True

    def can_place_pieces(self, player: 'Player', pieces: list['Piece']) -> bool:
        return all(self.can_place_piece(player, piece) for piece in pieces)

    # Only Vagabot can move into a forest, only DD can move into the Burrow
    def can_move_piece_into(self, player: 'Player', piece: 'Piece') -> bool:
        return True

    def can_move_pieces_into(self, player: 'Player', pieces: list['Piece']) -> bool:
        return all(self.can_move_piece_into(player, piece) for piece in pieces)

    # Only CC can move out of Snare clearings
    def can_move_piece_out_of(self, player: 'Player', piece: 'Piece') -> bool:
        return True

    def can_move_pieces_out_of(self, player: 'Player', pieces: list['Piece']) -> bool:
        return all(self.can_move_piece_out_of(player, piece) for piece in pieces)

    def can_move_piece(self, player: 'Player', piece: 'Piece', destination: 'Location',
                       requires_rule: bool = False) -> bool:
        # Check if you can move the piece out of this location (Snare)
        # Check if you rule this or destination if requires_rule: Only for clearings
        # Check if you can move the piece into the destination (Burrow, Forest)
        return self.can_move_piece_out_of(player, piece) and destination.can_move_piece_into(player, piece)

    def can_move_pieces(self, player: 'Player', pieces: list['Piece'], destination: 'Location',
                        requires_rule: bool = False) -> bool:
        return all(self.can_move_piece(player, piece, destination, requires_rule) for piece in pieces)

    ######################################################
    #                                                    #
    # Adding/moving/removing pieces to/from the location #
    #                                                    #
    ######################################################

    # It's assumed the player has already checked that this is a legal location to add the piece, whether by placement
    # or movement
    def add_piece(self, player: 'Player', piece: 'Piece', trigger_placement_effects: bool = False,
                  trigger_movement_effects: bool = False, log: bool = False) -> None:
        if log:
            self.game.log(f'{player} adds {piece} to {self}.', logging_faction=player.faction)
        self.piece_map(player).add_piece(piece)
        if piece.location:
            piece.location.remove_pieces_without_side_effects(player, [piece])
        piece.update_location(self)
        if trigger_placement_effects:
            self.trigger_placement_effects(player, [piece])
        if trigger_movement_effects:
            self.trigger_movement_effects(player, [piece])

    def add_pieces(self, player: 'Player', pieces: list['Piece'], trigger_placement_effects: bool = True,
                   trigger_movement_effects: bool = False, log: bool = True) -> None:
        if log and pieces and len(pieces) > 1:
            self.game.log(f'{player} adds {pieces} to {self}.', logging_faction=player.faction)
        for piece in pieces:
            # Don't trigger movement and placement effects per piece, do it in a batch at the end of placing them
            self.add_piece(player, piece, trigger_placement_effects=False, trigger_movement_effects=False,
                           log=(log and len(pieces) == 1))
        if trigger_placement_effects:
            self.trigger_placement_effects(player, pieces)
        if trigger_movement_effects:
            self.trigger_movement_effects(player, pieces)

    # It's assumed the player has already checked that this is a legal move action
    def move_piece(self, player: 'Player', piece: 'Piece', destination: 'Location') -> None:
        self.game.log(f'{player} moves {piece} from {self} to {destination}.', logging_faction=player.faction)
        # Remove piece from this clearing
        self.remove_pieces_without_side_effects(player, [piece])
        destination.add_piece(player, piece, trigger_movement_effects=True)

    def move_pieces(self, player: 'Player', pieces: list['Piece'], destination: 'Location') -> None:
        # Remove piece from this clearing
        self.game.log(f'{player} moves {pieces} from {self} to {destination}.', logging_faction=player.faction)
        self.remove_pieces_without_side_effects(player, pieces)
        destination.add_pieces(player, pieces, trigger_movement_effects=True, log=False)

    # This is for the Vagabot's "Slip", where destination location can restrict the move but not the origin location
    # It's assumed the player has already checked that this is a legal move action
    def move_pieces_unrestricted_by_origin(self, player: 'Player', pieces: list['Piece'],
                                           destination: 'Location') -> None:
        self.remove_pieces_without_side_effects(player, pieces)
        destination.add_pieces(player, pieces, trigger_movement_effects=True)

    # This is explicitly NOT a "Move" action. This is, e.g., placing pieces in a clearing, or moving them from the
    # Cogwheel Cult's Acolytes to their supply
    # It's assumed the player has already checked that this is a legal relocation
    def relocate_pieces(self, player: 'Player', pieces: list['Piece'], destination: 'Location') -> None:
        self.game.log(f'{player} relocates {pieces} from {self} to {destination}', logging_faction=player.faction)
        # Remove the pieces from this clearing
        self.remove_pieces_without_side_effects(player, pieces)
        # If the piece is being
        # TODO: Figure out why you did this. Hospitals?
        # if isinstance(destination, Supply):
        #     player.move_removed_pieces_into_supply(pieces, self)
        # else:
        #     destination.add_pieces(player, pieces, trigger_placement_effects=True)
        destination.add_pieces(player, pieces, trigger_placement_effects=True)

    # This doesn't cause side effects or move the pieces anywhere - it strictly removes them from this spot
    def remove_pieces_without_side_effects(self, player: 'Player', pieces: list['Piece']) -> None:
        for piece in pieces:
            self.piece_map(player).remove_piece(piece)

    # Returning pieces to the supply when removed outside of battle: Revolt, Marksman, returning Funds,
    # spending Acolytes, Convert/Sanctify, Price of Failure (Should be overridden to destroy the piece), Bomb
    def remove_pieces(self, player: 'Player', pieces: list['Piece']) -> list['Piece']:
        self.game.log(f'{player} removes {pieces} from {self}.', logging_faction=player.faction)
        # Remove piece from this location
        removed_pieces = []
        for piece in pieces:
            if piece.cannot_be_removed:
                piece.resolve_effects_on_attempting_to_remove_self()  # For Vagabot 'Big Damage'
            else:
                self.piece_map(player).remove_piece(piece)
                removed_pieces.append(piece)
        # It's up to the owners of pieces that cannot be removed to override this method
        player.move_removed_pieces_into_supply(pieces, self)
        return removed_pieces

    # Returning pieces to the supply when removed outside of battle: Relentless, Revolt, Bomb, Convert, ...
    def remove_all_pieces_of_player(self, player: 'Player') -> list['Piece']:
        # Remove piece from this location
        pieces = self.get_pieces_for_player(player)
        return self.remove_pieces(player, pieces)

    # Returning pieces to the supply that are removed through battle
    def remove_pieces_in_battle_to_supply(self, player: 'Player', pieces: list['Piece'],
                                          is_attacker: bool = True) -> None:
        # Remove piece from this clearing
        for piece in pieces:
            self.piece_map(player).remove_piece(piece)
        player.move_removed_pieces_into_supply_from_battle(pieces, self, is_attacker)

    # Unsure of any offhand?
    def trigger_placement_effects(self, player: 'Player', pieces: list['Piece']) -> None:
        for piece in self.get_pieces():
            piece.resolve_placement_effect(player, pieces)

    # Automated Outrage - any others?
    def trigger_movement_effects(self, player: 'Player', pieces: list['Piece']) -> None:
        for piece in self.get_pieces():
            piece.resolve_movement_effect(player, pieces)

    ##############################
    #                            #
    # Get pieces in the location #
    #                            #
    ##############################

    # FOR PLAYER #

    def get_pieces_for_player(self, player: 'Player') -> list['Piece']:
        piece_map = self.piece_map(player)
        return piece_map.get_all_pieces()

    def get_warriors_for_player(self, player: 'Player') -> list['Warrior']:
        return self.piece_map(player).warriors

    def get_buildings_for_player(self, player: 'Player') -> list['Building']:
        return self.piece_map(player).buildings

    def get_tokens_for_player(self, player: 'Player') -> list['Token']:
        return self.piece_map(player).tokens

    def get_other_pieces_for_player(self, player: 'Player') -> list['Piece']:
        return self.piece_map(player).other

    # FOR ALL PLAYERS, AS A MAPPING #

    def get_pieces_for_all_players(self) -> dict[Player, list['Piece']]:
        pieces_for_players = {}
        for player, piece_map in self.pieces.items():
            pieces_for_players[player] = piece_map.get_all_pieces()
        return pieces_for_players

    def get_warriors_for_all_players(self) -> dict[Player, list['Warrior']]:
        warriors_for_players = {}
        for player, piece_map in self.pieces.items():
            warriors_for_players[player] = piece_map.warriors
        return warriors_for_players

    def get_buildings_for_all_players(self) -> dict[Player, list['Building']]:
        buildings_for_players = {}
        for player, piece_map in self.pieces.items():
            buildings_for_players[player] = piece_map.buildings
        return buildings_for_players

    def get_tokens_for_all_players(self) -> dict[Player, list['Token']]:
        tokens_for_players = {}
        for player, piece_map in self.pieces.items():
            tokens_for_players[player] = piece_map.tokens
        return tokens_for_players

    def get_other_pieces_for_all_players(self) -> dict[Player, list['Piece']]:
        other_pieces_for_players = {}
        for player, piece_map in self.pieces.items():
            other_pieces_for_players[player] = piece_map.other
        return other_pieces_for_players

    # FOR ALL PLAYERS, AS AN ITERABLE #

    def get_pieces(self) -> list['Piece']:
        pieces = []
        for piece_map in self.pieces.values():
            pieces.extend(piece_map.get_all_pieces())
        return pieces

    def get_warriors(self) -> list['Warrior']:
        warriors = []
        for piece_map in self.pieces.values():
            warriors.extend(piece_map.warriors)
        return warriors

    def get_buildings(self) -> list['Building']:
        buildings = []
        for piece_map in self.pieces.values():
            buildings.extend(piece_map.buildings)
        return buildings

    def get_tokens(self) -> list['Token']:
        tokens = []
        for piece_map in self.pieces.values():
            tokens.extend(piece_map.tokens)
        return tokens

    def get_other_pieces(self) -> list['Piece']:
        other_pieces = []
        for piece_map in self.pieces.values():
            other_pieces.extend(piece_map.other)
        return other_pieces

    #####################################
    #                                   #
    # Get piece count from the location #
    #                                   #
    #####################################

    # FOR PLAYER #

    def get_piece_count_for_player(self, player: 'Player') -> int:
        return self.piece_map(player).get_count_of_pieces()

    def get_warrior_count_for_player(self, player: 'Player') -> int:
        return len(self.piece_map(player).warriors)

    def get_building_count_for_player(self, player: 'Player') -> int:
        return len(self.piece_map(player).buildings)

    def get_token_count_for_player(self, player: 'Player') -> int:
        return len(self.piece_map(player).tokens)

    def get_other_pieces_count_for_player(self, player: 'Player') -> int:
        return len(self.piece_map(player).other)

    # FOR ALL PLAYERS, AS A MAPPING #

    def get_piece_count_for_all_players(self) -> dict['Player', int]:
        all_players_piece_counts = {}
        for player, piece_map in self.pieces.items():
            all_players_piece_counts[player] = piece_map.get_count_of_pieces()
        return all_players_piece_counts

    def get_warrior_count_for_all_players(self) -> dict['Player', int]:
        all_players_piece_counts = {}
        for player, piece_map in self.pieces.items():
            all_players_piece_counts[player] = len(piece_map.warriors)
        return all_players_piece_counts

    def get_building_count_for_all_players(self) -> dict['Player', int]:
        all_players_piece_counts = {}
        for player, piece_map in self.pieces.items():
            all_players_piece_counts[player] = len(piece_map.buildings)
        return all_players_piece_counts

    def get_token_count_for_all_players(self) -> dict['Player', int]:
        all_players_piece_counts = {}
        for player, piece_map in self.pieces.items():
            all_players_piece_counts[player] = len(piece_map.tokens)
        return all_players_piece_counts

    def get_other_pieces_count_for_all_players(self) -> dict['Player', int]:
        all_players_piece_counts = {}
        for player, piece_map in self.pieces.items():
            all_players_piece_counts[player] = len(piece_map.other)
        return all_players_piece_counts

    # TOTAL PIECE COUNTS #

    def get_total_piece_count(self) -> int:
        total_piece_count = 0
        for player, piece_map in self.pieces.items():
            total_piece_count += piece_map.get_count_of_pieces()
        return total_piece_count

    def get_total_warrior_count(self) -> int:
        total_warrior_count = 0
        for player, piece_map in self.pieces.items():
            total_warrior_count += len(piece_map.warriors)
        return total_warrior_count

    def get_total_building_count(self) -> int:
        total_building_count = 0
        for player, piece_map in self.pieces.items():
            total_building_count += len(piece_map.buildings)
        return total_building_count

    def get_total_token_count(self) -> int:
        total_token_count = 0
        for player, piece_map in self.pieces.items():
            total_token_count += len(piece_map.tokens)
        return total_token_count

    def get_total_other_pieces_count(self) -> int:
        total_other_pieces_count = 0
        for player, piece_map in self.pieces.items():
            total_other_pieces_count += len(piece_map.other)
        return total_other_pieces_count

    # TOTAL PIECE COUNTS #

    def get_total_piece_count_for_other_players(self, acting_player: 'Player') -> int:
        total_piece_count = 0
        for player, piece_map in self.pieces.items():
            if player == acting_player:
                continue
            total_piece_count += piece_map.get_count_of_pieces()
        return total_piece_count

    def get_total_warrior_count_for_other_players(self, acting_player: 'Player') -> int:
        total_warrior_count = 0
        for player, piece_map in self.pieces.items():
            if player == acting_player:
                continue
            total_warrior_count += len(piece_map.warriors)
        return total_warrior_count

    def get_total_building_count_for_other_players(self, acting_player: 'Player') -> int:
        total_building_count = 0
        for player, piece_map in self.pieces.items():
            if player == acting_player:
                continue
            total_building_count += len(piece_map.buildings)
        return total_building_count

    def get_total_token_count_for_other_players(self, acting_player: 'Player') -> int:
        total_token_count = 0
        for player, piece_map in self.pieces.items():
            if player == acting_player:
                continue
            total_token_count += len(piece_map.tokens)
        return total_token_count

    def get_total_other_pieces_count_for_other_players(self, acting_player: 'Player') -> int:
        total_other_pieces_count = 0
        for player, piece_map in self.pieces.items():
            if player == acting_player:
                continue
            total_other_pieces_count += len(piece_map.other)
        return total_other_pieces_count

    #####################################
    #                                   #
    # Test for presence in the location #
    #                                   #
    #####################################

    def is_player_in_location(self, player: 'Player') -> bool:
        return self.get_piece_count_for_player(player) > 0

    def is_player_warriors_in_location(self, player: 'Player') -> bool:
        return self.get_warrior_count_for_player(player) > 0

    def is_any_other_player_in_location(self, active_player: 'Player') -> bool:
        return self.get_total_piece_count() - self.get_piece_count_for_player(active_player) > 0

    def get_all_players_in_location(self) -> list[Player]:
        players_in_location = []
        for player in self.pieces:
            if self.get_piece_count_for_player(player) > 0:
                players_in_location.append(player)
        return players_in_location

    def get_all_other_players_in_location(self, active_player: 'Player') -> list['Player']:
        players_in_location = []
        for player in self.pieces:
            if self.get_piece_count_for_player(player) > 0 and not player == active_player:
                players_in_location.append(player)
        return players_in_location

    #####################################################
    #                                                   #
    # Maximum/minimum non-zero presence in the location #
    #                                                   #
    #####################################################

    def get_players_with_defenseless_pieces(self) -> list['Player']:
        return []

from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from locations.location import Location
    from player_resources.player import Player


class Piece:
    player: Optional[Player]
    name: str
    location: Optional[Location]
    cannot_be_removed: bool

    # Item Tokens do not have players, all other pieces do
    # cannot_be_removed == Vagabond Pawn
    def __init__(self, player: Optional[Player], name: str, cannot_be_removed: bool = False) -> None:
        self.player = player
        self.name = name
        self.location = None
        self.cannot_be_removed = cannot_be_removed

    # Keep, Snare, limits on Sympathy/Roost/Trade Post
    def prevents_piece_being_placed_by_player(self, player: Player, piece: Piece) -> bool:
        return False

    # Only the Snare does
    def prevents_piece_being_moved_out_by_player(self, player: Player, piece: Piece) -> bool:
        return False

    def update_location(self, location: Optional[Location]) -> None:
        if not location:
            self.location = self.player.supply
        else:
            self.location = location

    # Probably none?
    def resolve_movement_effect(self, moving_player: Player, moving_pieces: list[Piece]) -> None:
        pass

    # Probably none?
    def resolve_placement_effect(self, placing_player: Player, placed_pieces: list[Piece]) -> None:
        pass

    # Vagabond damages 3 items
    def resolve_effects_on_attempting_to_remove_self(self) -> None:
        pass

    def get_score_for_removal(self) -> int:
        return 0

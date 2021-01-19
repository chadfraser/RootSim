from __future__ import annotations

from pieces.piece import Piece


class RollResult:
    def __init__(self, attacker_roll: int, defender_roll: int) -> None:
        self.attacker_roll = attacker_roll
        self.defender_roll = defender_roll


class DamageResult:
    def __init__(self, removed_pieces: list[Piece], points_awarded: int) -> None:
        self.removed_pieces = removed_pieces
        self.points_awarded = points_awarded

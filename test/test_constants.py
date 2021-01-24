from unittest import TestCase

from constants import Suit, Faction


class TestConstants(TestCase):
    def test_are_suits_equal__true(self):
        suit1 = Suit.FOX
        suit2 = Suit.FOX

        self.assertTrue(Suit.are_suits_equal(suit1, suit2))

    def test_are_suits_equal__false(self):
        suit1 = Suit.FOX
        suit2 = Suit.RABBIT

        self.assertFalse(Suit.are_suits_equal(suit1, suit2))

    def test_are_suits_equal_bird__true(self):
        suit1 = Suit.FOX
        suit2 = Suit.BIRD

        self.assertTrue(Suit.are_suits_equal(suit1, suit2))

    def test_are_suits_equal_bird__false(self):
        suit1 = Suit.BIRD
        suit2 = Suit.FOX

        self.assertFalse(Suit.are_suits_equal(suit1, suit2))

    def test_is_ruin_exploring_faction__true(self):
        self.assertTrue(Faction.VAGABOT.is_ruin_exploring_faction())

    def test_is_ruin_exploring_faction__false(self):
        self.assertFalse(Faction.MECHANICAL_MARQUISE_2_0.is_ruin_exploring_faction())

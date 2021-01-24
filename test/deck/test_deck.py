from unittest import TestCase
from unittest.mock import Mock, patch

from constants import Suit
from deck.cards.card import Card
from deck.deck import Deck


@patch('deck.deck.Deck.__abstractmethods__', set())
class TestDeck(TestCase):
    def test_draw_card(self):
        mock_game = Mock()
        deck = Deck(mock_game)
        card = Card('Sample Card', Suit.FOX)
        deck.cards = [card]
        self.assertEqual(deck.draw_card(), card)

    def test_draw_card_empty_deck(self):
        mock_game = Mock()
        deck = Deck(mock_game)
        card = Card('Sample Card', Suit.FOX)
        deck.cards = []
        deck.discard_pile = [card]
        self.assertEqual(deck.draw_card(), card)

    def test_draw_card_empty_deck_and_discard_pile(self):
        mock_game = Mock()
        deck = Deck(mock_game)
        deck.cards = []
        deck.discard_pile = []
        self.assertIsNone(deck.draw_card())

    def test_draw_cards(self):
        mock_game = Mock()
        deck = Deck(mock_game)
        card1 = Card('Sample Card', Suit.FOX)
        card2 = Card('Sample Card 2', Suit.FOX)
        deck.cards = [card1, card2]
        self.assertEqual(deck.draw_cards(2), [card2, card1])

    @patch('random.shuffle', return_value=None)
    def test_draw_cards_empty_deck(self, mock_random):
        mock_game = Mock()
        deck = Deck(mock_game)
        card1 = Card('Sample Card', Suit.FOX)
        card2 = Card('Sample Card 2', Suit.FOX)
        deck.cards = []
        deck.discard_pile = [card1, card2]
        self.assertEqual(deck.draw_cards(2), [card2, card1])

    def test_draw_cards_partially_empty_deck(self):
        mock_game = Mock()
        deck = Deck(mock_game)
        card1 = Card('Sample Card', Suit.FOX)
        card2 = Card('Sample Card 2', Suit.FOX)
        card3 = Card('Sample Card 3', Suit.FOX)
        deck.cards = [card1, card2]
        deck.discard_pile = [card3]
        self.assertEqual(deck.draw_cards(3), [card2, card1, card3])

    def test_draw_cards_partially_empty_deck_empty_discard_pile(self):
        mock_game = Mock()
        deck = Deck(mock_game)
        card1 = Card('Sample Card', Suit.FOX)
        card2 = Card('Sample Card 2', Suit.FOX)
        deck.cards = [card1, card2]
        deck.discard_pile = []
        self.assertEqual(deck.draw_cards(3), [card2, card1])

    def test_draw_cards_empty_deck_and_discard_pile(self):
        mock_game = Mock()
        deck = Deck(mock_game)
        deck.cards = []
        deck.discard_pile = []
        self.assertEqual(deck.draw_cards(2), [])

    def test_reshuffle_discard_pile_into_deck(self):
        mock_game = Mock()
        deck = Deck(mock_game)
        card = Card('Sample Card', Suit.FOX)
        deck.cards = []
        deck.discard_pile = [card]
        deck.reshuffle_discard_pile_into_deck()
        self.assertEqual(deck.cards, [card])
        self.assertEqual(deck.discard_pile, [])

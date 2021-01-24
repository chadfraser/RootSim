from unittest import TestCase
from unittest.mock import Mock

from constants import Suit
from deck.quest_deck import QuestCard, QuestDeck


mock_game = Mock()


class TestQuestDeck(TestCase):
    def test_draw_card(self):
        deck = QuestDeck()
        assert len(deck.cards) == 15
        mock_quest_card = QuestCard(Suit.FOX)
        deck.cards = [mock_quest_card]
        self.assertEqual(deck.draw_quest_card(), mock_quest_card)

    def test_draw_card_empty_deck(self):
        deck = QuestDeck()
        assert len(deck.cards) == 15
        deck.cards = []
        self.assertIsNone(deck.draw_quest_card())

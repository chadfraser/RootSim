from unittest import TestCase
from unittest.mock import Mock

from constants import Item, Suit
from deck.cards.item_card import ItemCard


class TestItemCard(TestCase):
    def test_can_be_crafted_true_item_in_stock(self):
        mock_game = Mock()
        mock_game.get_item_if_available.return_value = Item.BAG

        mock_player = Mock()
        mock_player.game = mock_game

        item = Item.BAG
        card = ItemCard('Sample Card', Suit.FOX, item, 1)
        self.assertTrue(card.can_be_crafted(mock_player))

    def test_can_be_crafted_false_item_not_in_stock(self):
        mock_game = Mock()
        mock_game.get_item_if_available.return_value = None

        mock_player = Mock()
        mock_player.game = mock_game

        item = Item.BAG
        card = ItemCard('Sample Card', Suit.FOX, item, 1)
        self.assertFalse(card.can_be_crafted(mock_player))

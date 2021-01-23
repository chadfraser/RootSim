from typing import TYPE_CHECKING
import random

from bot_resources.bot_factions.electric_eyrie.loyal_vizier import LoyalVizier
from constants import Suit

if TYPE_CHECKING:
    from bot_resources.bot_factions.electric_eyrie.electric_eyrie_player import ElectricEyriePlayer
    from deck.cards.card import Card


class Decree:
    viziers: list['LoyalVizier']
    columns: dict['Suit', list['Card']]

    def __init__(self, player: 'ElectricEyriePlayer') -> None:
        self.player = player
        self.viziers = [LoyalVizier(), LoyalVizier()]
        self.columns = {
            Suit.FOX: [],
            Suit.MOUSE: [],
            Suit.RABBIT: [],
            Suit.BIRD: [vizier for vizier in self.viziers]
        }

    def add_to_decree(self, card: 'Card') -> None:
        self.columns[card.suit].append(card)

    def get_count_of_suited_cards_in_decree(self, suit: 'Suit') -> int:
        return len(self.columns[suit])

    def get_count_of_bird_cards_in_decree(self) -> int:
        return self.get_count_of_suited_cards_in_decree(Suit.BIRD)

    def column_has_most_cards(self, suit: 'Suit') -> bool:
        suited_card_count = self.get_count_of_suited_cards_in_decree(suit)
        for column_suit, cards in self.columns.items():
            if len(cards) > suited_card_count:
                return False
        return True

    def purge(self) -> None:
        discarded_cards = []
        for column in self.columns.values():
            for card in column:
                if not isinstance(card, LoyalVizier):
                    discarded_cards.append(card)
                column.remove(card)
        random.shuffle(discarded_cards)
        for card in discarded_cards:
            self.player.game.discard_card(card)

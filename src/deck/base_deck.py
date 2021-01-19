from __future__ import annotations
from typing import TYPE_CHECKING

from deck.cards.ambush_card import generate_all_ambush_cards
import deck.cards.crafting_card_list
from deck.cards.dominance_card import generate_all_dominance_cards
from deck.cards.item_card_list import generate_all_item_cards
from deck.deck import Deck

if TYPE_CHECKING:
    from game import Game


class BaseDeck(Deck):
    def __init__(self, game: Game) -> None:
        super().__init__(game)

    def initialize_cards(self) -> None:
        self.cards = [
            # Persistent Fox cards
            deck.cards.crafting_card_list.StandAndDeliver(),
            deck.cards.crafting_card_list.StandAndDeliver(),
            deck.cards.crafting_card_list.TaxCollector(),
            deck.cards.crafting_card_list.TaxCollector(),
            deck.cards.crafting_card_list.TaxCollector(),
            # Persistent Rabbit cards
            deck.cards.crafting_card_list.Cobbler(),
            deck.cards.crafting_card_list.Cobbler(),
            deck.cards.crafting_card_list.CommandWarren(),
            deck.cards.crafting_card_list.CommandWarren(),
            deck.cards.crafting_card_list.BetterBurrowBank(),
            deck.cards.crafting_card_list.BetterBurrowBank(),
            # Persistent Mouse cards
            deck.cards.crafting_card_list.Codebreakers(),
            deck.cards.crafting_card_list.Codebreakers(),
            deck.cards.crafting_card_list.ScoutingParty(),
            deck.cards.crafting_card_list.ScoutingParty(),
            # Persistent Bird cards
            deck.cards.crafting_card_list.Sappers(),
            deck.cards.crafting_card_list.Sappers(),
            deck.cards.crafting_card_list.Armorers(),
            deck.cards.crafting_card_list.Armorers(),
            deck.cards.crafting_card_list.BrutalTactics(),
            deck.cards.crafting_card_list.BrutalTactics(),
            deck.cards.crafting_card_list.RoyalClaim(),
            # Immediate effect cards
            deck.cards.crafting_card_list.FavorOfTheFoxes(),
            deck.cards.crafting_card_list.FavorOfTheRabbits(),
            deck.cards.crafting_card_list.FavorOfTheMice()
        ]
        self.cards.extend(generate_all_item_cards())
        self.cards.extend(generate_all_dominance_cards())
        self.cards.extend(generate_all_ambush_cards())

        self.shuffle_deck()

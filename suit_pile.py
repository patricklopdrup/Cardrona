
import card
import numpy as np


HEARTS = 0
SPADES = 1
DIAMONDS = 2
CLUBS = 3


class Suit_pile:

    def __init__(self):
        self.suit_piles = {'H': [], 'S': [], 'D': [], 'C': []}

    def add_card(self, card) -> None:
        pile = self.suit_piles[card.suit]
        if (card.number == 1 and len(pile) == 0) or pile[-1].is_below(card):
            pile.append(card)

    def is_game_won(self) -> bool:
        # for key, value in piles
        for suit, pile in self.suit_piles.items():
            if not pile:
                return False
            # get top card and check for king
            top_card = pile[-1]
            if top_card.number != 13:
                return False
        return True

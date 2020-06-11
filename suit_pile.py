import card
import numpy as np


class Suit_pile:

    def __init__(self):
        # Dict with lists for each suit
        self.suit_piles = {'H': [], 'S': [], 'D': [], 'C': []}

    def add_card(self, card) -> bool:
        """ Add cards to the corresponding pile """
        # Gets the correct pile for the card
        pile = self.suit_piles[card.suit]
        # Add card to pile if possible
        if (card.number == 1 and len(pile) == 0) or pile[-1].is_below(card):
            pile.append(card)
            return True
        else:
            return False

    def is_game_won(self) -> bool:
        # For key, value in piles
        for suit, pile in self.suit_piles.items():
            if not pile:
                return False
            # Get top card and check for king
            top_card = pile[-1]
            if top_card.number != 13:
                return False
        return True

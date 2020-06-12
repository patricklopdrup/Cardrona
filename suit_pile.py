import card
import numpy as np


class Suit_pile:

    # Dict with lists for each suit
    suit_piles = {'H': [], 'S': [], 'D': [], 'C': []}

    def add_card(self, card) -> bool:
        """ Add cards to the corresponding pile """
        # Gets the correct pile for the card
        pile = self.suit_piles[card.suit]
        # If card is an ace and the pile is empty
        if (card.number == 1 and not pile):
            pile.append(card)
            return True
        # If some card already in the pile
        elif pile:
            # If top card of pile is below the appending card
            if pile[-1].is_below(card):
                pile.append(card)
                return True
            return False
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

    def print_suit_piles(self):
        for suit in self.suit_piles:
            print()
            print(suit, end=": ")
            for card in self.suit_piles[suit]:
                print(card, end=" ")

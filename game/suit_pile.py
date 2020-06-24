import game.card as card
import numpy as np


class Suit_pile:

    # Dict with lists for each suit
    suit_piles = {'H': [], 'S': [], 'D': [], 'C': []}

    def add_card(self, m_card) -> bool:
        """ Add cards to the corresponding pile """
        # Gets the correct pile for the card
        pile = self.suit_piles[m_card.suit]
        # If card is an ace and the pile is empty
        if (m_card.number == 1 and not pile):
            pile.append(m_card)
            return True
        # If some card already in the pile
        elif pile:
            # If top card of pile is below the appending card
            if pile[-1].is_below(m_card):
                pile.append(m_card)
                return True
            return False
        return False

    def can_move_to_pile(self, m_card):
        # Gets the correct pile for the card
        pile = self.suit_piles[m_card.suit]
        # If card is an ace and the pile is empty
        if (m_card.number == 1 and not pile):
            return True
        # If some card already in the pile
        elif pile:
            # If top card of pile is below the appending card
            if pile[-1].is_below(m_card):
                return True
            return False
        return False

    def is_pile_empty(self, suit):
        return len(self.suit_piles[suit]) == 0

    def pile_length(self, suit):
        return len(self.suit_piles[suit])

    def get_card(self, suit):
        """ Gets the top card of a suit pile without removing it """
        if len(self.suit_piles[suit]) >= 1:
            return self.suit_piles[suit][-1]
        else:
            return None

    def remove_card(self, suit) -> bool:
        """ Removes the top card of the pile. Returns True if it succeeded """
        if not self.is_pile_empty(suit):
            self.suit_piles[suit].pop()
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

    def print_suit_piles(self):
        for suit in self.suit_piles:
            print()
            print(suit, end=": ")
            for card in self.suit_piles[suit]:
                print(card, end=" ")

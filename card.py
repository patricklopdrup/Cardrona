import random


class Card:
    def __init__(self):
        pass

    def make_card(self, number, suit):
        # All numbers will have 2 decimals. Fx 5 -> 05
        return (str(('%02d') % number) + suit)

    def make_deck(self):
        # Hearts, Spades, Diamonds, Clubs
        suits = ["H", "S", "D", "C"]
        deck = []
        for suit in suits:
            # 13 cards for each suit
            for num in range(1, 14):
                deck.append(self.make_card(num, suit))
        return deck

    def shuffle(self, deck):
        random.shuffle(deck)
        return deck

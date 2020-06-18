import random

color = {
    "H": "red",
    "S": "black",
    "D": "red",
    "C": "black"
}


class Deck:
    def __init__(self):
        pass

    # creates 52 card. 4 suits X 13 cards
    def make_deck(self):
        # Hearts, Spades, Diamonds, Clubs
        suits = ["H", "S", "D", "C"]
        deck = []
        for suit in suits:
            # 13 cards for each suit
            for num in range(1, 14):
                deck.append(Card(num, suit, color[suit]))
        return deck

    def shuffle(self, deck):
        random.shuffle(deck)
        return deck


class Card:
    # creates a card with number, suit, color and a value for flipped
    def __init__(self, number, suit, color, is_flipped=False):
        self.number = number
        self.suit = suit
        self.color = color
        self.is_flipped = is_flipped

    def __str__(self):
        # All numbers will have 2 decimals. Fx 5 -> 05
        return (str(('%02d') % self.number) + self.suit)

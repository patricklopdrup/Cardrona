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

    def make_deck(self):
        """
        Creates 52 card. 4 suits X 13 cards
        """
        # Hearts, Spades, Diamonds, Clubs
        suits = ["H", "S", "D", "C"]
        deck = []
        for suit in suits:
            # 13 cards for each suit
            for num in range(1, 14):
                deck.append(Card(num, suit))
        return deck

    def shuffle(self, deck):
        random.shuffle(deck)
        return deck


class Card:
    def __init__(self, number, suit, above=None, x=-1, y=-1, is_facedown=False):
        """
        Creates a card with number, suit, color and a value for facedown
        """
        self.number = number
        self.suit = suit
        self.color = color[suit]
        self.is_facedown = is_facedown
        self.above = above
        self.x_pos = x
        self.y_pos = y

    def is_below(self, card) -> bool:
        """
        Returns True if the cards number is 1 less than the card in parameter.
        False otherwise
        """
        return self.number == (card.number - 1)

    def is_opposite_color(self, card) -> bool:
        """ Returns True if cards are opposite color """
        if self.suit == 'S' or self.suit == 'C':
            return card.suit == 'H' or card.suit == 'D'
        else:
            return card.suit == 'S' or card.suit == 'C'

    def can_be_moved_to(self, card) -> bool:
        """
        Checks if the card you call from can be moved to the card you give as input
        """
        return self.is_below(card) and card.is_opposite_color(self)

    def __str__(self):
        """
        All numbers will have 2 decimals. Fx 5 -> 05
        """
        return (str(('%02d') % self.number) + self.suit)

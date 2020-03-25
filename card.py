class Card:
    def __init__(self):
        pass

    def make_card(self, number, suit):
        return (str(number) + suit)

    def make_deck(self):
        suits = ["H", "S", "D", "C"]
        deck = []
        for suit in suits:
            # 13 cards for each suit
            for num in range(1, 14):
                deck.append(self.make_card(num, suit))
        return deck

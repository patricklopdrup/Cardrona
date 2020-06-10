import numpy as np
import card



class Stock_pile:

    def __init__(self):
        self.stock = 24
        self.waste = []

    def draw_from_stock(self, card: card.Card) -> bool:
        if self.stock == 0 and len(self.waste) == 0:
            print("Der er ikke flere kort at trække")
            return False

        # If stock is empty, move the waste pile to the stock pile
        if self.stock == 0:
            self.stock = len(self.waste)
            self.waste.clear()

        # Moves card from stock to waste
        self.waste.append(card)
        self.stock -= 1
        return True


    def get_top_waste(self):
        """
        Returns the top card of the waste pile
        """
        if len(self.waste) <= 0:
            return "Der er ingen kort"
        else:
            return self.waste[-1]

    def remove_from_waste(self):
        if len(self.waste) <= 0:
            return "Der er ingen kort"
        else:
            return self.waste.pop()
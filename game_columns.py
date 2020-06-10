import numpy as np
import from_img as ML
import card


class GameColumns:

    deck = card.Deck()

    facedown_cards_in_col = {
        0: 0,
        1: 1,
        2: 2,
        3: 3,
        4: 4,
        5: 5,
        6: 6
    }

    def __init__(self, card_list):
        # ML.make_game_first_time(card_list)
        self.solitaire = np.zeros((7, 13), dtype=object)

    def test(self):
        m_deck = self.deck.make_deck()
        m_deck = self.deck.shuffle(m_deck)

        for row in range(7):
            for column in range(7):
                if column == row:
                    self.solitaire[row, column] = m_deck.pop(0)
                elif column < row:
                    card = m_deck.pop(0)
                    card.is_facedown = True
                    self.solitaire[row, column] = card

    def pile_size_in_col(self, col, only_faceup=False) -> int:
        """ 
        Returns the amount of cards in a column.
        By default it counts all the cards in the column,
        but only_faceup can be set so it only returns playable cards
        """
        cards = 0
        # return -1 if col does not exist
        if col < 0 or col >= 7:
            return -1
        # count the cards. 0 = not a card
        if only_faceup:
            for card in self.solitaire[col]:
                if card != 0 and not card.is_facedown:
                    cards += 1
            return cards
        else:
            for card in self.solitaire[col]:
                if card != 0:
                    cards += 1
            return cards


gc = GameColumns(2)
gc.test()
print(gc.pile_size_in_col(4))

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

    def move_in_game(self, from_col, from_row, to_col):
        """
        To move one or more card(s) from a column to another.
        This is for moving within the game - not from the deck or suit-piles.
        """
        card_to_move = self.solitaire[from_col, from_row]
        # Cards can only be placed on "leaf" cards. The card in the very end of a column
        destination_card = self.solitaire[to_col,
                                          self.pile_size_in_col(to_col)-1]

        # Move either one or more cards to another column
        if self.is_col_legal(from_col, from_row):
            if card_to_move.can_be_moved_to(destination_card):
                self.move_cards(from_col, from_row, to_col)
                return True
        return False

        # # Move exactly one card if possible
        # if self.is_leaf_card(from_col, from_row):
        #     if card_to_move.can_be_moved_to(destination_card):
        #         self.move_cards(from_col, from_row, to_col)

    def move_cards(self, from_col, from_row, to_col):
        """
        Takes all the cards in a pile from the start coordinate.
        Moves them to the distination taken from "to_col"
        """
        cards_to_move = []
        for index, card in enumerate(self.solitaire[from_col]):
            if index >= from_row and card != 0:
                # Add card to array
                cards_to_move.append(card)
                # Remove from the game
                self.solitaire[from_col, index] = 0
        # Gets the first empty space in the column we want to add to
        end_row = self.pile_size_in_col(to_col)
        # Loops through all the cards we want to move and insert them at the distination
        for i, card in enumerate(cards_to_move):
            print(f"hej: {i}")
            self.solitaire[to_col, end_row + i] = card

    def is_col_legal(self, from_col, from_row) -> bool:
        """
        Checks if it is legal to move the whole column when from_row is within a column.
        It returns True instantly if the card is a leaf card (last in the column)
        """
        # If card is not playable - return False
        if self.solitaire[from_col, from_row].is_facedown:
            return False
        # If card is the last in a column: return True
        if self.is_leaf_card(from_col, from_row):
            return True
        # Loop through the column starting at "from_row"
        for i, card in enumerate(self.solitaire[from_col]):
            # 0 = no card or empty space
            if card == 0:
                break
            # Only look at cards starting AFTER
            if i > from_row:
                card_above = self.solitaire[from_col, i-1]
                if not card.can_be_moved_to(card_above):
                    return False
        return True

    def is_leaf_card(self, col, row) -> bool:
        """Returns True if the card is the last in the column - False otherwise"""
        return row == (self.pile_size_in_col(col) - 1)

    def pile_size_in_col(self, col, only_faceup=False) -> int:
        """ 
        returns the amount of cards in a column.
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
                else:
                    break
            return cards


##############################
#          TESTING           #
##############################

    def test(self):
        """Making a deck of cards"""
        m_deck = self.deck.make_deck()
        m_deck = self.deck.shuffle(m_deck)

        for card in m_deck:
            print(card, end=", ")
        print()

        # Creating the game in the 2D array
        for col in range(7):
            for row in range(7):
                if row == col:
                    self.solitaire[col, row] = m_deck.pop(0)
                elif row < col:
                    card = m_deck.pop(0)
                    card.is_facedown = True
                    self.solitaire[col, row] = card

    def show_test(self):
        """ Print the game """
        print()
        for col in range(7):
            print()
            for row in range(7):
                if self.solitaire[row, col]:
                    # Print back-side of card if it's flipped - else print the card
                    if self.solitaire[row, col].is_facedown:
                        print("[ ]", end=" ")
                    else:
                        print(self.solitaire[row, col], end=" ")
                else:
                    print(" "*4, end="")

    def hack_solitaire(self):
        """ Set solitaire as you wish """
        self.solitaire[0, 0] = card.Card(8, 'D')
        self.solitaire[1, 0] = card.Card(7, 'C')
        self.solitaire[1, 1] = card.Card(6, 'H')


gc = GameColumns(2)
gc.test()
gc.hack_solitaire()
print(gc.pile_size_in_col(4))
print(f"kan rykkes? {gc.move_in_game(1, 0, 0)}")
gc.show_test()

import numpy as np
import game.card as card
import game.suit_pile as suit_pile


class GameColumns:
    """
    This class contains functions for checking and manipulating the seven columns on the game board (some of the functions were moved from solitaire.py to this file).
    """

    deck = card.Deck()
    m_suit_pile = suit_pile.Suit_pile()

    solitaire = np.zeros((7, 13), dtype=object)
    leaf_cards = np.zeros(7, dtype=object)
    # Keep track of the facedown cards in each of the 7 piles
    col_facedown: list = [0, 1, 2, 3, 4, 5, 6]

    def __init__(self):
        """ Initialize array for the 7 columns """
        #self.solitaire = np.zeros((7, 13), dtype=object)
        #self.leaf_cards = np.zeros(7, dtype=object)
        # # Keep track of the facedown cards in each of the 7 piles
        #self.col_facedown: list = [0, 1, 2, 3, 4, 5, 6]
        pass

    def move_in_game(self, from_col, from_row, to_col) -> bool:
        """
        To move one or more card(s) from a column to another.
        This is for moving within the game - not from the deck or suit-piles.
        """
        print("er i move in game")
        card_to_move = self.solitaire[from_col, from_row]
        # Cards can only be placed on "leaf" cards. The card in the very end of a column
        destination_card = self.solitaire[to_col,
                                          self.get_pile_size_in_col(to_col)-1]

        # Move either one or more cards to another column if possible
        if self.is_col_legal(from_col, from_row):
            print("col legal")
            print(
                f"card to move: {card_to_move} og dist card: {destination_card}")
            if card_to_move.can_be_moved_to(destination_card):
                print("can be moved")
                self.__move_cards(from_col, from_row, to_col)
                return True
        return False

    def move_to_suit_pile(self, from_col, from_row) -> bool:
        """ Returns whether or not the card can be moved to its pile """
        card_to_move = self.solitaire[from_col, from_row]
        # Adds the card to the suit pile and removes from the game if possible
        if self.m_suit_pile.add_card(card_to_move):
            self.__remove_card(from_col, from_row)
            self.__update_col_facedown(from_col)
        else:
            return False

    def checkif_suitpile(self, from_col, from_row) -> bool:
        """ Returns whether or not the card can be moved to its pile """
        card_to_move = self.solitaire[from_col, from_row]

        if self.m_suit_pile.can_move_to_pile(card_to_move):
            return True
        else:
            return False

    def pilelength(self, suit):
        number = self.m_suit_pile.pile_length(suit)
        return number

    def move_from_suit_pile(self, suit, to_col) -> bool:
        """ Move a card from a suit pile back into the game """
        # If the suit pile if empty we return False
        if self.m_suit_pile.is_pile_empty(suit):
            return False

        # Get card from the suit pile and the card we want to move to
        card_from_suit_pile = self.m_suit_pile.get_card(suit)
        card_in_game = self.solitaire[to_col,
                                      self.get_pile_size_in_col(to_col)-1]

        # If we can make the move
        if card_from_suit_pile.can_be_moved_to(card_in_game):
            # Remove top card from suit pile
            self.m_suit_pile.remove_card(suit)
            # Place the card on the column in the game
            self.solitaire[to_col, self.get_pile_size_in_col(
                to_col)] = card_from_suit_pile
            return True
        else:
            return False

    def __remove_card(self, from_col, from_row) -> None:
        """ Adds a 0 (zero) where the card was """
        print(f"sletter: {self.solitaire[from_col, from_row]}")
        self.solitaire[from_col, from_row] = 0

    def __move_cards(self, from_col, from_row, to_col):
        """
        Takes all the cards in a pile from the start coordinate.
        Moves them to the distination taken from "to_col"
        """
        cards_to_move = []
        for index, m_card in enumerate(self.solitaire[from_col]):
            if index >= from_row and m_card != 0:
                # Add card to array
                cards_to_move.append(m_card)
                # Remove from the game
                self.__remove_card(from_col, index)
        # Gets the first empty space in the column we want to add to
        end_row = self.get_pile_size_in_col(to_col)
        # Loops through all the cards we want to move and insert them at the distination
        for i, m_card in enumerate(cards_to_move):
            self.solitaire[to_col, end_row + i] = m_card
        # After card(s) is moved we update the column where we moved from (if necessary)
        self.__update_col_facedown(from_col)
        print("cards to move:", *cards_to_move)

    def __update_col_facedown(self, col):
        """ 
        Checks if a column consist only of facedown cards,
        this means that we must update col_facedown array to keep track of facedown cards in a column
        """
        all_is_facedown = True
        # Loop all card in column
        for card in self.solitaire[col]:
            # If no card is represented
            if card == 0:
                break
            # If at least 1 card is faceup we return from method
            if not card.is_facedown:
                all_is_facedown = False
                return
        # If all card is facedown, we can flip and reviel a new card
        # so we have one less card facing down in that column
        if all_is_facedown:
            if self.col_facedown[col] > 0:
                print(f"Flip card in column {col}")
                self.col_facedown[col] -= 1
                print("Hej", *self.col_facedown)

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
            self.leaf_cards[from_col] = self.solitaire[from_col, from_row]
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

    def __move_king_to_col(self, from_col, from_row, to_col):
        """ Move king to empty column """
        card = self.solitaire[from_col, from_row]
        # Chgeck if king can be moved to empty column
        if card.number == 13 and self.get_pile_size_in_col(to_col) == 0:
            self.__move_cards(from_col, from_row, to_col)
            return True
        else:
            return False

    def is_leaf_card(self, col, row) -> bool:
        """ Returns True if the card is the last in the column - False otherwise """
        return row == (self.get_pile_size_in_col(col) - 1)

    def get_leaf_card(self, col):
        """ Return the last card in a column """
        if self.get_pile_size_in_col(col) != 0:
            return self.solitaire[col,
                                  self.get_pile_size_in_col(col)-1]

    def get_all_leaf_cards(self) -> list:
        """ 
        Returns a list of all the leaf cards aka. the last card in each column.
        This is used to get the distinations for  in a move.
        """
        leaf_cards = []
        # Loop through the columns in the game
        for col in range(len(self.solitaire)):
            if self.get_pile_size_in_col(col) != 0:
                # Get the last card in column
                leaf_card = self.solitaire[col,
                                           self.get_pile_size_in_col(col)-1]
                # Add the card to the list
                leaf_cards.append(leaf_card)
        return leaf_cards

    def get_all_faceup_cards(self) -> list:
        """ Returns a list of all the playable cards in the game """
        faceup_cards = []
        # Loop through the columns in the game
        for col in range(len(self.solitaire)):
            # Loop through all the cards in rows
            for card in self.solitaire[col]:
                # Check if the card in facing up
                if card != 0 and not card.is_facedown:
                    faceup_cards.append(card)
        # Return the list of faceup cards
        return faceup_cards

    def get_pile_size_in_col(self, col, only_faceup=False) -> int:
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
                else:
                    break
            return cards

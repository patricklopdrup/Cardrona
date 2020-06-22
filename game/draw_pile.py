import numpy as np
import game.card as card
import game.game_columns as game_columns
import game.suit_pile as suit_pile

game = game_columns.GameColumns()
suit_pile = suit_pile.Suit_pile()


class Stock_pile:
    waste = None

    def draw_from_stock(self, m_card) -> bool:
        self.waste = m_card
        return True

    # def draw_from_stock(self, card: card.Card) -> bool:
    #     if self.stock == 0 and len(self.waste) == 0:
    #         print("Der er ikke flere kort at trække")
    #         return False

    #     # If stock is empty, move the waste pile to the stock pile
    #     if self.stock == 0:
    #         self.stock = len(self.waste)
    #         self.waste.clear()

    #     # Moves card from stock to waste
    #     self.waste.append(card)
    #     self.stock -= 1
    #     return True

    def get_top_waste(self):
        """
        Returns the top card of the waste pile
        """
        if self.waste:
            return self.waste

    def remove_from_waste(self):
        if not self.waste:
            return "Der er ingen kort"
        else:
            self.waste = None

    def is_empty(self) -> bool:
        return not self.waste

    def move_to_column(self, col) -> bool:
        """ 
        Move card from waste pile to game columns.
        Return True if the move is completed. False otherwise.
        """
        # If waste pile is empty return False
        if self.is_empty():
            return False
        else:
            # Get the card we want to move to
            card_in_game = game.get_leaf_card(col)
            # Get the top card in the waste pile
            waste_card = self.get_top_waste()
            # If it is legal to move the card to the game
            if waste_card.can_be_moved_to(card_in_game):
                # Set card on top of card_in_game
                game.solitaire[col, game.get_pile_size_in_col(
                    col)] = waste_card
                # Remove from the waste pile
                self.remove_from_waste()
                return True
            return False

    def move_to_suit_pile(self) -> bool:
        """ 
        Move card from waste pile to suit pile.
        Return True if the move is completed. False otherwise.
        """
        if self.is_empty():
            return False
        else:
            # Get the top card in the waste pile
            waste_card = self.get_top_waste()
            if suit_pile.add_card(waste_card):
                # Remove from the waste pile
                self.remove_from_waste()
                return True
            return False

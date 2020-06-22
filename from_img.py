import game.card as card
import game.game_columns as game
import game.draw_pile as draw_pile

game = game.GameColumns()


def parse_value(input: str) -> int:
    """
    Takes the input from the ML and parses the corresponding card number.
    """
    if len(input) > 2:
        return int(input[:2])
    name = input[0]
    if name == 'K':
        return 13
    elif name == 'Q':
        return 12
    elif name == 'J':
        return 11
    elif name == 'A':
        return 1
    else:
        return int(name)


def parse_suit(input: str) -> str:
    """ Returns the last letter in the input; the suit for the card """
    return input[-1]


def make_stock_pile(input_list: list, stock_pile):
    """ Parse the card that is turned from the stock pile and call draw_from_stock() """
    # Blank paper is seen as None
    if input_list:
        top_card = input_list[0][0]
        m_card = card.Card(parse_value(top_card),
                           parse_suit(top_card), None, -1, -1)
        # Update the number of cards left in the stock pile
        stock_pile.draw_from_stock(m_card)
    else:
        print("Ingen kort i waste")


def make_suit_pile(input_list: list):
    """ Parse the four suit piles from input_list """
    for card_index, card_i in enumerate(input_list):
        # Blank paper is seen as None
        if card_i:
            print(f"list: {card_i}")
            m_card = card.Card(parse_value(
                card_i[0][0]),
                parse_suit(card_i[0][0]),
                None,
                -1,
                -1)
            # Add the card to the suit pile in-game
            game.m_suit_pile.add_card(m_card)


def make_seven_column(input_list: list):
    """
    Input_list is a list of lists (from the NN).
    Outer-list = columns in game.
    Inner-list = rows of cards in game.
    Creates the game board by parsing values from machine learning input to cards.
    """
    # Loops the outer-list (columns)
    for index_col, col in enumerate(input_list):
        # Default above_card as None
        above_card = None
        # If column in inner-list is not None or there exist facedown cards in the column
        if col[0] or game.col_facedown[index_col] > 0:
            # Loops the col_facedown aka. the amount of cards facing down in each column
            for facedown in range(game.col_facedown[index_col]):
                # Creates a default card facing down (value and suit does NOT matter)
                default_card = card.Card(
                    2, 'H', None, index_col, facedown, is_facedown=True)
                # Adding card facingdown to game array
                game.solitaire[index_col, facedown] = default_card
            # Loops inner-list (rows) of playable cards
            # card_index is the index of the card in the inner-list
            for card_index, input_card in enumerate(col):
                # Creates the card from inner-list. Also with x- and y-pos and above_card
                m_card = card.Card(parse_value(input_card[0]),
                                   parse_suit(input_card[0]),
                                   above_card,
                                   index_col,
                                   (card_index + game.col_facedown[index_col]))
                # New above card is the card we just put into the game
                above_card = m_card
                # Adds to game array after the facing down cards
                game.solitaire[index_col, card_index +
                               game.col_facedown[index_col]] = m_card
        elif not col[0]:
            # If column is empty show empty col in-game
            game.solitaire[index_col, 0] = 0

import card
import rules
import game_columns as game

game = game.GameColumns()

test_list = [
    [
        ('6D')
    ],
    [
        ('2H')
    ],
    [
        ('3H')
    ],
    [

    ],
    [
        ('4H')
    ],
    [
        ('6H')
    ],
    [
        ('7H')
    ]
]

init_list = [
    [('8C')],
    [('7D')],
    [('7S')],
    [('9D')],
    [('10H')],
    [('AS')],
    [('AD')]
]

after_move_list = [
    [('8C'), ('7D')],
    [('AS')],
    [('7S')],
    [('9D')],
    [('10H')],
    [('AS')],
    [('AD')]
]


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


def make_game_from_input(input_list: list):
    """
    Input_list is a list of lists (from the NN).
    Outer-list = columns in game.
    Inner-list = rows of cards in game.
    Creates the game board by parsing values from machine learning input to cards.
    """
    # Loops the outer-list (columns)
    for index_col, col in enumerate(input_list):
        # If column in inner-list is NOT empty or there exist facedown cards in the column
        if col or game.col_facedown[index_col] > 0:
            # Loops the col_facedown aka. the amount of cards facing down in each column
            for facedown in range(game.col_facedown[index_col]):
                # Creates a default card facing down (value and suit does NOT matter)
                default_card = card.Card(2, 'H', True)
                # Adding card facingdown to game array
                game.solitaire[index_col, facedown] = default_card
            # Loops inner-list (rows) of playable cards
            # card_index is the index of the card in the inner-list
            for card_index, input_card in enumerate(col):
                # Creates the card from inner-list
                m_card = card.Card(parse_value(input_card),
                                   parse_suit(input_card))
                # Adds to game array after the facing down cards
                game.solitaire[index_col, card_index +
                               game.col_facedown[index_col]] = m_card


def test():
    # Test a move from a initial state.
    # Updating col_facedown for the column we move from
    # New input from ML with a new flipped card
    make_game_from_input(init_list)
    game.show_test()
    game.move_in_game(1, 1, 0)
    game.show_test()
    make_game_from_input(after_move_list)
    game.show_test()


# test()

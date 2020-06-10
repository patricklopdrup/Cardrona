import numpy as np
import card
import itertools
import rules

# Easy access for the "data" array
CARD_DECK = 0  # Deck with front facing down
TURNED = 1  # Latest turned card from the deck
# The 4 suits deck
HEARTS = 2
SPADES = 3
DIAMONDS = 4
CLUBS = 5

# 2D array for the game. 7 rows of max 13 cards (ace to king)
solitaire = np.zeros((7, 13), dtype=object)

# Data array for other game info
# Data = ['', '', '', '', '', '', '']
data = np.zeros((7), dtype=object)

# 24 cards are left in the deck after the 7 columns have been put down
card_deck = np.zeros((24), dtype=object)
# Max 13 cards in suit pile: ace, 2, 3, 4...
data[HEARTS] = np.zeros(13, dtype=object)
data[SPADES] = np.zeros(13, dtype=object)
data[DIAMONDS] = np.zeros(13, dtype=object)
data[CLUBS] = np.zeros(13, dtype=object)

# Global counter for the turned cards
turn_count = 0

def init_game():
    pass


def show_card_deck():
    """
    Printing the deck of cards that is still in the deck.
    Cards that is not in play yet
    """
    for card in data[CARD_DECK]:
        print(card, end=", ")
    print()


def four_suit_deck():
    """
    Printing the value of each suit deck
    """
    print(
        f"H:{data[HEARTS]} S:{data[SPADES]} D:{data[DIAMONDS]} C:{data[CLUBS]}")


def move_game_to_suit_pile(col: int, row: int):
    # Card we want to move
    card_to_move = solitaire[col, row]
    # Get the suit pile that matches the cards suit
    suit: int = find_suit_pile(card_to_move.suit)
    # Loop the suit pile
    for index, card in enumerate(data[suit]):
        # If suit pile is empty and we move an ace
        if index == 0 and card == 0 and card_to_move.number == 1:
            # Insert card in suit pile and remove from game
            data[suit][index] = card_to_move
            solitaire[col, row] = 0
            break
        # Place card in chronological order in the pile
        elif card != 0 and data[suit][index + 1] == 0:
            if card.number == card_to_move.number - 1:
                data[suit][index + 1] = card_to_move
                solitaire[col, row] = 0
                break


def move_from_stock_to_suit_pile():
    card_to_move = data[TURNED]
    print(f"fra deck: {data[TURNED]}")
    suit: int = find_suit_pile(card_to_move.suit)
    for index, card in enumerate(data[suit]):
        # If suit pile is empty and we move an ace
        if index == 0 and card == 0 and card_to_move.number == 1:
            # Insert card in pile
            data[suit][index] = card_to_move
            delete_card_from_deck()
            break
        # Place card in chronological order in the pile
        elif card != 0 and data[suit][index + 1] == 0:
            if card.number == card_to_move.number - 1:
                # Insert card in pile
                data[suit][index+1] = card_to_move
                delete_card_from_deck()
                break


def find_suit_pile(suit: str) -> int:
    """
    Returns the correct pile for the suit. The correct index in the data-array

    """
    return {
        'H': HEARTS,
        'S': SPADES,
        'D': DIAMONDS,
        'C': CLUBS
    }[suit]


def delete_card_from_deck():
    """
    Deletes the turned card and moves the pointer to the right position
    """
    global turn_count
    # Delete the turned card from the deck
    data[CARD_DECK] = np.delete(data[CARD_DECK], -turn_count)
    # Set pointer of turned card in the right position
    turn_count = turn_count - 1
    # Display old card in deck
    if turn_count == 0:
        data[TURNED] = 0
    else:
        data[TURNED] = data[CARD_DECK][-turn_count]


def turn_card_counter() -> int:
    """
    Function for changing the global counter
    """
    global turn_count
    turn_count = (turn_count + 1) % len(data[CARD_DECK])
    # print(f"count: {turn_count} og len: {len(data[CARD_DECK])}")
    return turn_count



def turn_card():
    """
    Takes the top card from the stock and turns it - the turned card is now in play.
    Turn each card in a loop by accessing the negative turn_card_counter()
    """
    top_card = data[CARD_DECK][-turn_card_counter()]
    data[CARD_DECK] = data[CARD_DECK]
    data[TURNED] = top_card


def move_from_deck(col: int, row: int):
    """
    Play the turned card into the solitaire. TODO check for legal moves!
    """
    # Return if no card is turned yet
    if data[TURNED] == 0:
        return
    # Get turned card
    card = data[TURNED]
    # Remove the card you just moved from the deck
    delete_card_from_deck()
    # Putting the card in game array
    solitaire[col, row] = card


def move_card(from_column, from_row, to_column, to_row):
    """
    Moves exactly one card
    """
    solitaire[to_column, to_row] = solitaire[from_column, from_row]
    solitaire[from_column, from_row] = 0

    if solitaire[from_column, from_row-1] != 0:
        if solitaire[from_column, from_row-1].is_facedown:
            solitaire[from_column, from_row-1].is_facedown = False


def move_row(goal_row, current_row):
    """
    Moves an entire column
    """
    start_column = 0

    for column in range(7):
        if solitaire[goal_row, column] != 0:
            if not solitaire[goal_row, column].is_facedown:
                start_column = column+1

    for column in range(12):
        if solitaire[current_row, column] != 0:
            if not solitaire[current_row, column].is_facedown:
                move_card(current_row, column, goal_row, start_column)
                start_column += 1


def move_series(goal_row, current_row, how_many):
    """
    Moves a specific number of cards in a column
    """
    start_column = 0
    finished = 0

    # Finds goal
    for column in range(7):
        if solitaire[goal_row, column] != 0:
            if not solitaire[goal_row, column].is_facedown:
                start_column = column + 1

    # Finds last card in current row
    for column in range(7):
        if solitaire[current_row, column] != 0:
            if not solitaire[current_row, column].is_facedown:
                finished = column

    start2 = finished - how_many - 1

    # Finding the last possible card
    for column in range(start2, 12):
        if solitaire[current_row, column] != 0:
            if not solitaire[current_row, column].is_facedown:
                move_card(current_row, column, goal_row, start_column)
                start_column += 1


def all_possible_moves(from_rows: list, to_rows: list):
    list_of_moves = []

    c = list(itertools.product(from_rows, to_rows))

    length = len(c)

    # Når vi har lavet en is_move_legal metode for 1 kort
    for i in range(length):
        if is_move_legal(c[i][0], c[i][1]) == 1:
            list_of_moves.append(c[i])

    return list_of_moves

# list of columns to move


def all_possible_column(from_rows: list, to_rows: list):
    listofpossiblemoves = []

    c = list(itertools.product(from_rows, to_rows))

    length = len(c)

    # når vi har lavet en is_move_legal metode for 1 kort
    for i in range(length):
        if rules.is_col_legal_move(c[i][0], c[i][1]):
            listofpossiblemoves.append(c[i])
    return listofpossiblemoves


def is_move_legal(from_where, to_where):
    """
    Checks if one card can be moved based on two input rows
    """
    is_it_true = False
    start_column = 0
    end_column = 0

    # Finds goal_column
    for column in range(7):
        if solitaire[to_where, column] != 0:
            if not solitaire[to_where, column].is_facedown:
                start_column = column + 1

    # Finds start_column
    for column in range(7):
        if solitaire[from_where, column] != 0:
            if not solitaire[from_where, column].is_facedown:
                end_column = column + 1

    if rules.is_move_legal([from_where, end_column], [to_where, start_column]):
        is_it_true = True

    return is_it_true


# DEBUG
def set_own_cards(col):
    #solitaire[col, 0] = card.Card(10, "D")
    #solitaire[col, 1] = card.Card(9, "S")
    #solitaire[col, 2] = card.Card(8, "D")
    data[HEARTS][0] = card.Card(1, "H")
    solitaire[0, 0] = card.Card(2, "H")

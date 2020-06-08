import numpy as np
import card


# Easy access for the "data" array
CARD_DECK = 0   # deck with front facing down
TURNED = 1      # latest turned card from the deck
# turned deck. All cards facing up, but you can only interact with the top one
TURNED_DECK = 2
# the 4 suits deck
HEARTS = 3
SPADES = 4
DIAMONDS = 5
CLUBS = 6

# 2D array for the game. 7 rows of max 13 cards (ace to king)
solitaire = np.zeros((7, 13), dtype=object)

# Data array for other game info
# data = ['', '', '', '', '', '', '']
data = np.zeros((7), dtype=object)

# 24 cards are left in the deck after the 7 columns have been put down
card_deck = np.zeros((24), dtype=object)


def init_game():
    data[HEARTS] = 0
    data[SPADES] = 0
    data[DIAMONDS] = 0
    data[CLUBS] = 0
    data[TURNED_DECK] = 0


# printing the deck of cards that is still in the deck.
# cards that is not in play yet
def show_card_deck():
    for card in data[CARD_DECK]:
        print(card, end=", ")
    print()


# printing the value of each suit deck
def four_suit_deck():
    print(
        f"H:{data[HEARTS]} S:{data[SPADES]} D:{data[DIAMONDS]} C:{data[CLUBS]}")


# global counter for the turned cards
turn_count = 0


# changing global count
def turn_card_counter() -> int:
    global turn_count
    turn_count = (turn_count + 1) % len(data[CARD_DECK])
    #print(f"count: {turn_count} og len: {len(data[CARD_DECK])}")
    return turn_count


# takes the top card from the deck and turns it - the turned card is now in play
# turn each card in a loop by accessing the negative turn_card_counter()
def turn_card():
    top_card = data[CARD_DECK][-turn_card_counter()]
    data[CARD_DECK] = data[CARD_DECK]
    data[TURNED] = top_card


# play the turned card into the solitaire. TODO check for legal moves!
def move_from_deck(col: int, row: int):
    # return if no card is turned yet
    if data[TURNED] == 0:
        return
    # get turned card
    card = data[TURNED]
    global turn_count
    # delete the turned card from the deck
    data[CARD_DECK] = np.delete(data[CARD_DECK], -turn_count)
    # set pointer of turned card in the right position
    turn_count = turn_count - 1

    # display old card in deck
    if turn_count == 0:
        data[TURNED] = 0
    else:
        data[TURNED] = data[CARD_DECK][-turn_count]
    # putting the card in game array
    solitaire[col, row] = card


# if card from middle of column is chosen. Checks if that's a legal move
def is_col_legal_move(col: int, row: int) -> bool:
    print(f"card: {solitaire[col,row]}")
    is_legal = True
    # card we try to move (potentially from the middle of a column)
    start_card = solitaire[col, row]
    if start_card == 0 or start_card.is_flipped:
        return False
    else:
        cur_color = start_card.color
        cur_num = start_card.number

    # all cards in the column (beginning from "start_card")
    cards = solitaire[col]
    # we already saved current cards value so we start from the next card; col+1
    for card in cards[row+1:-1]:
        # if no card is represented
        if card == 0:
            break
        # if colors are the same or
        # the number is not 1 less than the card above we return False
        if (card.color == cur_color) or not (card.number == (cur_num-1)):
            return False
        # new values for current card
        cur_color = card.color
        cur_num = card.number
    return is_legal


def is_move_legal(from_index: list, to_index: list) -> bool:
    from_card = solitaire[from_index[0], from_index[1]]
    to_card = solitaire[to_index[0], to_index[1]]
    # kings can be moved to empty spaces
    if to_card == 0 and from_card.number == 13:
        return True
    # card can be placed on a card with with different color and +1 in number
    if to_card.color != from_card.color and to_card.number-1 == from_card.number:
        # check if the whole column is legal
        if is_col_legal_move(from_index[0], from_index[1]):
            return True


def movecard(fromcolumn, fromrow, tocolumn, torow):
    solitaire[tocolumn, torow] = solitaire[fromcolumn, fromrow]
    solitaire[fromcolumn, fromrow] = 0

    if solitaire[fromcolumn, fromrow-1] != 0:
        if solitaire[fromcolumn, fromrow-1].is_flipped:
            solitaire[fromcolumn, fromrow-1].is_flipped = False


def moverow(goalrow, currentrow):
    startcolumn = 0

    for columnn in range(7):
        if solitaire[goalrow, columnn] != 0:
            if not solitaire[goalrow, columnn].is_flipped:
                startcolumn = columnn+1

    for column in range(12):
        if solitaire[currentrow, column] != 0:
            if not solitaire[currentrow, column].is_flipped:
                movecard(currentrow, column, goalrow, startcolumn)
                startcolumn += 1


def moveseries(goalrow, currentrow, howmany):
    startcolumn = 0
    finished = 0

    # finds goal
    for columnn in range(7):
        if solitaire[goalrow, columnn] != 0:
            if not solitaire[goalrow, columnn].is_flipped:
                startcolumn = columnn + 1

    # finds last card in current row
    for columnn in range(7):
        if solitaire[currentrow, columnn] != 0:
            if not solitaire[currentrow, columnn].is_flipped:
                finished = columnn

    staret2 = finished - howmany-1

    # finding the last possible card
    for column in range(staret2, 12):
        if solitaire[currentrow, column] != 0:
            if not solitaire[currentrow, column].is_flipped:
                movecard(currentrow, column, goalrow, startcolumn)
                startcolumn += 1


# DEBUG
def set_own_cards(col):
    solitaire[col, 0] = card.Card(10, "D", "red")
    solitaire[col, 1] = card.Card(9, "S", "black")
    solitaire[col, 2] = card.Card(8, "D", "red")

import numpy as np
import card


# Easy access for the "data" array
CARD_DECK = 0
TURNED = 1
TURNED_DECK = 2
HEARTS = 3
SPADES = 4
DIAMONDS = 5
CLUBS = 6

# 2D array for the game. 7 rows of max 13 cards (ace to king)
solitaire = np.zeros((7, 13), dtype=object)

# Data array for other than game info
# data = ['', '', '', '', '', '', '']
data = np.zeros((7), dtype=object)
card_deck = np.zeros((24), dtype=object)


def init_game():
    data[HEARTS] = 0
    data[SPADES] = 0
    data[DIAMONDS] = 0
    data[CLUBS] = 0
    data[TURNED_DECK] = 0


def show_card_deck():
    for card in data[CARD_DECK]:
        print(card, end=", ")
    print()


def four_suit_deck():
    print(
        f"H:{data[HEARTS]} S:{data[SPADES]} D:{data[DIAMONDS]} C:{data[CLUBS]}")


# global counter for the turned cards
turn_count = 0


# changing global count
def turn_card_counter() -> int:
    global turn_count
    turn_count = (turn_count + 1) % len(data[CARD_DECK])
    print(f"count: {turn_count} og len: {len(data[CARD_DECK])}")
    return turn_count


# turn each card in a loop by accessing the negative turn_card_counter()
def turn_card():
    top_card = data[CARD_DECK][-turn_card_counter()]
    data[CARD_DECK] = data[CARD_DECK]
    data[TURNED] = top_card


# if card from middle of column is chosen. Checks if that's a legal move
def is_move_legal(row: int, col: int) -> bool:
    is_legal = True
    start_card = solitaire[row, col]
    if start_card == 0 or start_card.is_flipped:
        return False
    else:
        cur_color = start_card.color
        cur_num = start_card.number
        print(f"col: {cur_color} num: {cur_num}")

    cards = solitaire[row]
    # we already saved current cards value so we start from the next card; col+1
    for card in cards[col+1:-1]:
        # if no card is represented
        if card == 0:
            break
        print(f"kort: {card.color} og {card.number} og cur_num: {cur_num}")
        # if colors are the same or
        # the number is not 1 less than the card above we return False
        if (card.color == cur_color) or not (card.number == (cur_num-1)):
            return False
        # new values for current card
        cur_color = card.color
        cur_num = card.number
    return is_legal


def movecard(fromrow, fromcolumn, torow, tocolumn):
    solitaire[torow, tocolumn] = solitaire[fromrow, fromcolumn]
    solitaire[fromrow, fromcolumn] = 0

    if solitaire[fromrow, fromcolumn-1] != 0:
        if solitaire[fromrow, fromcolumn - 1].is_flipped:
            solitaire[fromrow, fromcolumn - 1].is_flipped = False



def moverow(goalrow, currentrow):
    startcolumn = 0

    for columnn in range(7):
        if solitaire[goalrow, columnn] != 0:
            if not solitaire[goalrow, columnn].is_flipped == True:
                startcolumn = columnn+1

    for column in range(12):
        if solitaire[currentrow, column] != 0:
            if not solitaire[currentrow, column].is_flipped == True:
                movecard(currentrow, column, goalrow, startcolumn)
                startcolumn += 1

# DEBUG


def set_own_cards(row):
    solitaire[row, 0] = card.Card(10, "H", "red")
    solitaire[row, 1] = card.Card(9, "S", "black")
    solitaire[row, 2] = card.Card(8, "D", "red")

import numpy as np
import card
import itertools
import rules

# Easy access for the "data" array
CARD_DECK = 0  # deck with front facing down
TURNED = 1  # latest turned card from the deck
# the 4 suits deck
HEARTS = 2
SPADES = 3
DIAMONDS = 4
CLUBS = 5

# 2D array for the game. 7 rows of max 13 cards (ace to king)
solitaire = np.zeros((7, 13), dtype=object)

# Data array for other game info
# data = ['', '', '', '', '', '', '']
data = np.zeros((7), dtype=object)
card_deck = np.zeros((24), dtype=object)
# max 13 cards in suit pile: ace, 2, 3, 4...
data[HEARTS] = np.zeros(13, dtype=object)
data[SPADES] = np.zeros(13, dtype=object)
data[DIAMONDS] = np.zeros(13, dtype=object)
data[CLUBS] = np.zeros(13, dtype=object)


def init_game():
    pass


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


# input type: Card class
def move_game_to_suit_pile(col: int, row: int):
    # card we want to move
    card_to_move = solitaire[col, row]
    # get the suit pile that matches the cards suit
    suit: int = find_suit_pile(card_to_move.suit)
    # loop the suit pile
    for index, card in enumerate(data[suit]):
        # if suit pile is empty and we move an ace
        if index == 0 and card == 0 and card_to_move.number == 1:
            # insert card in suit pile and remove from game
            data[suit][index] = card_to_move
            solitaire[col, row] = 0
            break
        # place card in chronological order in the pile
        elif card != 0 and data[suit][index + 1] == 0:
            if card.number == card_to_move.number - 1:
                data[suit][index + 1] = card_to_move
                solitaire[col, row] = 0
                break


def move_deck_to_suit_pile():
    card_to_move = data[TURNED]
    print(f"fra deck: {data[TURNED]}")
    suit: int = find_suit_pile(card_to_move.suit)
    for index, card in enumerate(data[suit]):
        # if suit pile is empty and we move an ace
        if index == 0 and card == 0 and card_to_move.number == 1:
            # insert card in pile
            data[suit][index] = card_to_move
            delete_card_from_deck()
            break
        # place card in chronological order in the pile
        elif card != 0 and data[suit][index + 1] == 0:
            if card.number == card_to_move.number - 1:
                # insert card in pile
                data[suit][index+1] = card_to_move
                delete_card_from_deck()
                break


# returns the correct pile for the suit. The correct index in the data-array
def find_suit_pile(suit: str) -> int:
    return {
        'H': HEARTS,
        'S': SPADES,
        'D': DIAMONDS,
        'C': CLUBS
    }[suit]


def delete_card_from_deck():
    """
    deletes the turned card and moves the pointer to the right position
    """
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


# changing global count
def turn_card_counter() -> int:
    global turn_count
    turn_count = (turn_count + 1) % len(data[CARD_DECK])
    # print(f"count: {turn_count} og len: {len(data[CARD_DECK])}")
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
    # remove the card you just moved from the deck
    delete_card_from_deck()
    # putting the card in game array
    solitaire[col, row] = card


def movecard(fromcolumn, fromrow, tocolumn, torow):
    solitaire[tocolumn, torow] = solitaire[fromcolumn, fromrow]
    solitaire[fromcolumn, fromrow] = 0

    if solitaire[fromcolumn, fromrow-1] != 0:
        if solitaire[fromcolumn, fromrow-1].is_facedown:
            solitaire[fromcolumn, fromrow-1].is_facedown = False


def moverow(goalrow, currentrow):
    startcolumn = 0

    for columnn in range(7):
        if solitaire[goalrow, columnn] != 0:
            if not solitaire[goalrow, columnn].is_facedown:
                startcolumn = columnn+1

    for column in range(12):
        if solitaire[currentrow, column] != 0:
            if not solitaire[currentrow, column].is_facedown:
                movecard(currentrow, column, goalrow, startcolumn)
                startcolumn += 1


def moveseries(goalrow, currentrow, howmany):
    startcolumn = 0
    finished = 0

    # finds goal
    for columnn in range(7):
        if solitaire[goalrow, columnn] != 0:
            if not solitaire[goalrow, columnn].is_facedown:
                startcolumn = columnn + 1

    # finds last card in current row
    for columnn in range(7):
        if solitaire[currentrow, columnn] != 0:
            if not solitaire[currentrow, columnn].is_facedown:
                finished = columnn

    staret2 = finished - howmany - 1

    # finding the last possible card
    for column in range(staret2, 12):
        if solitaire[currentrow, column] != 0:
            if not solitaire[currentrow, column].is_facedown:
                movecard(currentrow, column, goalrow, startcolumn)
                startcolumn += 1

# singlecard


def all_posible_moves(fromrows: list, torows: list):
    listofmoves = []

    c = list(itertools.product(fromrows, torows))

    length = len(c)

    # når vi har lavet en ismovelegal metode for 1 kort
    for i in range(length):
        if ismovelegal(c[i][0], c[i][1]) == 1:
            listofmoves.append(c[i])

    return listofmoves

# list of columns to move


def all_posiblecoloum(fromrows: list, torows: list):
    listofpossiblemoves = []

    c = list(itertools.product(fromrows, torows))

    length = len(c)

    # når vi har lavet en ismovelegal metode for 1 kort
    for i in range(length):
        if rules.is_col_legal_move(c[i][0], c[i][1]):
            listofpossiblemoves.append(c[i])
    return listofpossiblemoves



# checks if one card can be moved based on two input rows
def ismovelegal(fromwhere, towhere):
    isittrue = False
    startcolumn = 0
    endcolum = 0

    # finds goalcolum
    for columnn in range(7):
        if solitaire[towhere, columnn] != 0:
            if not solitaire[towhere, columnn].is_facedown:
                startcolumn = columnn + 1

    # finds startcolumn
    for columnn in range(7):
        if solitaire[fromwhere, columnn] != 0:
            if not solitaire[fromwhere, columnn].is_facedown:
                endcolum = columnn + 1

    if rules.is_move_legal([fromwhere, endcolum], [towhere, startcolumn]):
        isittrue = True

    return isittrue


# DEBUG
def set_own_cards(col):
    #solitaire[col, 0] = card.Card(10, "D")
    #solitaire[col, 1] = card.Card(9, "S")
    #solitaire[col, 2] = card.Card(8, "D")
    data[HEARTS][0] = card.Card(1, "H")
    solitaire[0, 0] = card.Card(2, "H")

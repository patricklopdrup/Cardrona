import numpy as np
import card
import itertools
import rules
import game_columns

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


def move_card(fromcolumn, fromrow, tocolumn, torow):
    solitaire[tocolumn, torow] = solitaire[fromcolumn, fromrow]
    solitaire[fromcolumn, fromrow] = 0

    if solitaire[fromcolumn, fromrow-1] != 0:
        if solitaire[fromcolumn, fromrow-1].is_facedown:
            solitaire[fromcolumn, fromrow-1].is_facedown = False


def move_row(goalrow, currentrow):
    startcolumn = 0

    for columnn in range(7):
        if solitaire[goalrow, columnn] != 0:
            if not solitaire[goalrow, columnn].is_facedown:
                startcolumn = columnn+1

    for column in range(12):
        if solitaire[currentrow, column] != 0:
            if not solitaire[currentrow, column].is_facedown:
                move_card(currentrow, column, goalrow, startcolumn)
                startcolumn += 1

#der er muligvis nogle bugs

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


def all_possible_moves(from_rows, to_rows):
    list_of_moves = []

    c = list(itertools.product(from_rows, to_rows))

    length = len(c)

    # Når vi har lavet en is_move_legal metode for 1 kort
    for i in range(length):
        print(c[i][0])

        if is_move_legal(c[i][0], c[i][1]):
            list_of_moves.append(c[i])
    print(list_of_moves)

    return list_of_moves

# list of columns to move


def all_possible(game_columns1: game_columns.GameColumns):
    card_location = []
    card_location_leafcards = []
    combinations = []

    listof_unseen= game_columns1.col_facedown

    listofleafcards = game_columns1.get_all_leaf_cards()
    listoffaceupcards = game_columns1.get_all_faceup_cards()

    #locate the faceupcards
    column = 0
    for i in range(7):
        while game_columns1.solitaire[column,i] != listoffaceupcards[column]:
            print(listoffaceupcards[column])
            column+=1
        card_location.append([listoffaceupcards[column],i,column])

    #locate the leaf cards
    column1 = 0
    for i2 in range(7):
        while game_columns1.solitaire[column1,i2] != listofleafcards[column1]:
            print(listofleafcards[column1])
            column1+=1
        card_location_leafcards.append([listofleafcards[column1],i2,column1])

    #we will now add all combinations of leafcards
    lenght1 = len(listofleafcards)
    for thiscard in range(lenght1):
        for othercards in range(lenght1):
            if card_location_leafcards[thiscard][0].can_be_moved_to(card_location_leafcards[othercards][0]):
                combinations.append([card_location_leafcards[thiscard],card_location_leafcards[othercards]])
    print(combinations)

    #in the card class we will now create some methods'

    #check sequences
     # 1. check nuværende med ovenstående kort
        #1.1 - Hvis det er en sekvens, så check med næste
    # 2. Check fra øverste del af sekvens med om man kan flytte til et leaf card
    sequences = []
    lenght3 = len(listoffaceupcards)

    for currentcard in range(lenght3):
        if game_columns1.is_col_legal(card_location[currentcard][2],card_location[currentcard][1]):
            print(card_location[currentcard][2])
            print(card_location[currentcard][1])
            for othercards1 in range(lenght1):
                if card_location[currentcard][0].can_be_moved_to(card_location_leafcards[othercards1][0]):
                    sequences.append([card_location_leafcards[currentcard], card_location_leafcards[othercards1]])

    #make sure that a card that isnt a leaf card has




    print(sequences)
    print(card_location)
    print(card_location_leafcards)
    print(*listofleafcards)
    print(*listoffaceupcards)









# DEBUG
def set_own_cards(col):
    #solitaire[col, 0] = card.Card(10, "D")
    #solitaire[col, 1] = card.Card(9, "S")
    #solitaire[col, 2] = card.Card(8, "D")
    data[HEARTS][0] = card.Card(1, "H")
    solitaire[0, 0] = card.Card(2, "H")

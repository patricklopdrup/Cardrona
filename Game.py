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
data = ['', '', '', '', '', '', '']


#card = card.Card()
#deck = card.make_deck()
# print(deck)
# print(card.shuffle(deck))

card = card.Card()


def start_game():

    deck = card.make_deck()
    deck = card.shuffle(deck)
    back_counter = 0
    print(len(deck))

    for row in range(7):
        for column in range(7):
            if column == row:
                solitaire[row, column] = deck.pop(1)
            elif column < row:
                solitaire[row, column] = "BBB"
                back_counter += 1

    data[CARD_DECK] = (len(deck) - back_counter)
    print(solitaire)
    print(data)


def show():
    for column in range(7):
        print()
        for row in range(7):
            if solitaire[row, column]:
                print(solitaire[row, column], end=" ")
            else:
                print(" "*4, end="")


# to run the program
start_game()
show()

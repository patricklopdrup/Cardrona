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


deck = card.Deck()
# card = card.Card()


def start_game():

    m_deck = deck.make_deck()
    print(f"længde: {len(m_deck)}")
    m_deck = deck.shuffle(m_deck)
    back_counter = 0

    for row in range(7):
        for column in range(7):

            if column == row:
                solitaire[row, column] = m_deck.pop(1)
            elif column < row:
                solitaire[row, column] = "[ ]"
                back_counter += 1
    data[CARD_DECK] = (len(m_deck) - back_counter)
    print(solitaire)
    print(data)


def show():
    print(f"hej med dig: {solitaire[0,0]} er {solitaire[0,0].color}")
    data[HEARTS] = 0
    data[SPADES] = 0
    data[DIAMONDS] = 0
    data[CLUBS] = 0
    print()
    print(f"Deck: {data[CARD_DECK]}")
    print(f"Turned card: {data[TURNED]}")
    print(
        f"H:{data[HEARTS]} S:{data[SPADES]} D:{data[DIAMONDS]} C:{data[CLUBS]}")
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

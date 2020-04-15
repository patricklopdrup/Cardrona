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

deck = card.Deck()
# card = card.Card()


def draw_card():
    print(f"kort: {data[CARD_DECK]}")
    data[TURNED] = data[CARD_DECK]


def start_game():
    data[HEARTS] = 0
    data[SPADES] = 0
    data[DIAMONDS] = 0
    data[CLUBS] = 0
    data[TURNED_DECK] = 0

    m_deck = deck.make_deck()
    print(f"Antal kort: {len(m_deck)}")
    print(f"hej: {data[CARD_DECK]}")
    m_deck = deck.shuffle(m_deck)

    for row in range(7):
        for column in range(7):

            if column == row:
                solitaire[row, column] = m_deck.pop(0)
            elif column < row:
                card = m_deck.pop(0)
                card.flipped = True
                solitaire[row, column] = card
    # putting the rest of the card in card_deck
    for i in range(len(m_deck)):
        card_deck[i] = m_deck[i]
    # saving the card_deck in the data array
    data[CARD_DECK] = card_deck


def show_card_deck():
    for card in data[CARD_DECK]:
        print(card, end=", ")
    print()


def turn_card():
    top_card = data[CARD_DECK][-1]
    data[CARD_DECK] = data[CARD_DECK]
    data[TURNED] = top_card


def show():
    print(f"Første kort: {solitaire[0,0]} er {solitaire[0,0].color}")
    print()
    show_card_deck()
    print(f"Turned card: {data[TURNED]}")
    print(
        f"H:{data[HEARTS]} S:{data[SPADES]} D:{data[DIAMONDS]} C:{data[CLUBS]}")
    for column in range(7):
        print()
        for row in range(7):
            if solitaire[row, column]:
                # print back-side of card if it's flipped - else print the card
                if solitaire[row, column].flipped == True:
                    print("[ ]", end=" ")
                else:
                    print(solitaire[row, column], end=" ")
            else:
                print(" "*4, end="")


# to run the program
start_game()
show()

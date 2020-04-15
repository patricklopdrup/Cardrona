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

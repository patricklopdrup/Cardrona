import numpy as np
import card
import itertools


# Easy access for the "data" array
STOCK = 0   # deck with front facing down
TALON = 1   #
TURNED = 2  # latest turned card from the deck
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
card_deck = np.zeros((24), dtype=object)
# max 13 cards in suit pile: ace, 2, 3, 4...
data[HEARTS] = np.zeros(13, dtype=object)
data[SPADES] = np.zeros(13, dtype=object)
data[DIAMONDS] = np.zeros(13, dtype=object)
data[CLUBS] = np.zeros(13, dtype=object)


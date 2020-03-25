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

deck = card.Card().make_deck()
print(deck)

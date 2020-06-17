import numpy as np
import card
import itertools
import rules
import game_columns

# list of cards to move from where
def all_possible(game_columns1: game_columns.GameColumns):
    card_location = []
    card_location_leafcards = []
    combinations = []

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

    #can we move from leafcard to suitpile
    lenght1 = len(listofleafcards)
    for thiscard3 in range(lenght1):
        if game_columns1.checkif_suitpile(card_location_leafcards[thiscard3][1],card_location_leafcards[thiscard3][0]):
            if card_location_leafcards[thiscard3][0].suit == "H":
                combinations.append([card_location_leafcards[thiscard3],["pilefor H",7, game_columns1.pilelength(card_location_leafcards[thiscard3][0].suit)]])

            if card_location_leafcards[thiscard3][0].suit == "S":
                combinations.append([card_location_leafcards[thiscard3],["pilefor S",8, game_columns1.pilelength(card_location_leafcards[thiscard3][0].suit)]])

            if card_location_leafcards[thiscard3][0].suit == "D":
                combinations.append([card_location_leafcards[thiscard3],["pilefor D",9, game_columns1.pilelength(card_location_leafcards[thiscard3][0].suit)]])

            if card_location_leafcards[thiscard3][0].suit == "C":
                combinations.append([card_location_leafcards[thiscard3],["pilefor D",10, game_columns1.pilelength(card_location_leafcards[thiscard3][0].suit)]])

    #in the card class we will now create some methods'

    #check sequences
     # 1. check nuværende med ovenstående kort
        #1.1 - Hvis det er en sekvens, så check med næste
    # 2. Check fra øverste del af sekvens med om man kan flytte til et leaf card
    sequences = []
    lenght3 = len(listoffaceupcards)
    for currentcard in range(lenght3):
        if game_columns1.is_col_legal(card_location[currentcard][2],card_location[currentcard][1]):
            for othercards1 in range(lenght1):
                if card_location[currentcard][0].can_be_moved_to(card_location_leafcards[othercards1][0]):
                    sequences.append([card_location_leafcards[currentcard], card_location_leafcards[othercards1]])

    allmoves = sequences+combinations
    return allmoves

def where_canthis_be_moved(game_columns1: game_columns.GameColumns, card1: card):
    listofleafcards = []
    card_location_leafcards = []
    wheretomove =[]

    # locate the leaf cards
    column1 = 0
    for i2 in range(7):
        while game_columns1.solitaire[column1, i2] != listofleafcards[column1]:
            print(listofleafcards[column1])
            column1 += 1
        card_location_leafcards.append([listofleafcards[column1], i2, column1])

    lenght1 = len(listofleafcards)
    for othercards1 in range(lenght1):
        if card1.can_be_moved_to(card_location_leafcards[othercards1][0]):
            wheretomove.append(card_location_leafcards[othercards1])

    return wheretomove


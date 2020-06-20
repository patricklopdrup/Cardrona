import numpy as np
import game.card as card
import itertools
import game.game_columns as game_columns
import game.draw_pile as draw_pile

# list of cards to move from where


def all_possible(game_columns1: game_columns.GameColumns):
    card_location = []
    card_location_leafcards = []
    combinations = []

    listofleafcards = game_columns1.get_all_leaf_cards()
    listoffaceupcards = game_columns1.get_all_faceup_cards()

    # locate the faceupcards
    column = 0
    for i in range(7):
        while game_columns1.solitaire[column, i] != listoffaceupcards[column]:
            print(listoffaceupcards[column])
            column += 1
        card_location.append([listoffaceupcards[column], i, column])

    # locate the leaf cards
    column1 = 0
    for i2 in range(7):
        while game_columns1.solitaire[column1, i2] != listofleafcards[column1]:
            # print(listofleafcards[column1])
            column1 += 1
        card_location_leafcards.append([listofleafcards[column1], i2, column1])

    # checking suitpile
    lenght1 = len(listofleafcards)
    for thiscard3 in range(lenght1):
        if game_columns1.checkif_suitpile(card_location_leafcards[thiscard3][1], card_location_leafcards[thiscard3][2]):
            if card_location_leafcards[thiscard3][0].suit == "H":
                combinations.append([card_location_leafcards[thiscard3], [
                    "H", 7, game_columns1.pilelength(card_location_leafcards[thiscard3][0].suit)]])

            if card_location_leafcards[thiscard3][0].suit == "S":
                combinations.append([card_location_leafcards[thiscard3], [
                    "S", 8, game_columns1.pilelength(card_location_leafcards[thiscard3][0].suit)]])

            if card_location_leafcards[thiscard3][0].suit == "D":
                combinations.append([card_location_leafcards[thiscard3], [
                    "D", 9, game_columns1.pilelength(card_location_leafcards[thiscard3][0].suit)]])

            if card_location_leafcards[thiscard3][0].suit == "C":
                combinations.append([card_location_leafcards[thiscard3], [
                    "C", 10, game_columns1.pilelength(card_location_leafcards[thiscard3][0].suit)]])

    # checking in that wastepile
    primedrawpile = draw_pile.Stock_pile()
    cardfrompile = primedrawpile.get_top_waste()
    print(f"er her {cardfrompile}")

    if cardfrompile is not None:
        waste_to_leaf = where_canthis_be_moved(game_columns1, cardfrompile)

        # this card part of a  suit move
        if game_columns1.m_suit_pile.can_move_to_pile(cardfrompile):

            if cardfrompile.suit == "H":
                waste_to_leaf.append([[cardfrompile, 11, 0], [
                    "H", 7, game_columns1.pilelength(cardfrompile.suit)]])

            if cardfrompile.suit == "S":
                waste_to_leaf.append([[cardfrompile, 11, 0], [
                    "S", 8, game_columns1.pilelength(cardfrompile.suit)]])

            if cardfrompile.suit == "D":
                waste_to_leaf.append([[cardfrompile, 11, 0], [
                    "D", 9, game_columns1.pilelength(cardfrompile.suit)]])

            if cardfrompile.suit == "C":
                waste_to_leaf.append([[cardfrompile, 11, 0], [
                    "C", 10, game_columns1.pilelength(cardfrompile.suit)]])

    # check sequences
     # 1. check nuværende med ovenstående kort
        # 1.1 - Hvis det er en sekvens, så check med næste
    # 2. Check fra øverste del af sekvens med om man kan flytte til et leaf card
    sequences = []
    lenght3 = len(listoffaceupcards)
    for currentcard in range(lenght3):
        if game_columns1.is_col_legal(card_location[currentcard][1], card_location[currentcard][2]):
            for othercards1 in range(lenght1):
                if card_location[currentcard][0].can_be_moved_to(card_location_leafcards[othercards1][0]):
                    sequences.append(
                        [card_location_leafcards[currentcard], card_location_leafcards[othercards1]])
    if cardfrompile is not None:
        allmoves = sequences + combinations + waste_to_leaf
    else:
        allmoves = sequences + combinations
    return allmoves


def where_canthis_be_moved(game_columns1: game_columns.GameColumns, card1: card):
    listofleafcards = game_columns1.get_all_leaf_cards()
    card_location_leafcards = []
    wheretomove = []

    # locate the leaf cards
    for leaf_card in listofleafcards:
        card_location_leafcards.append(
            [leaf_card, leaf_card.x_pos, leaf_card.y_pos])

    for to_card in listofleafcards:
        if card1.can_be_moved_to(to_card):
            wheretomove.append(
                [[card1, 11, card1.x_pos], [to_card, to_card.y_pos, to_card.x_pos]])

    return wheretomove

#  [ [card, x, y] , [] ]

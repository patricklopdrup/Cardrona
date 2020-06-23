import numpy as np
import game.card as card
import itertools
import game.game_columns as game_columns
import game.draw_pile as draw_pile
from os import path
import os
import sys
import yaml
from pprint import pprint

# Global configuration for file
cur_path = os.getcwd()
config = yaml.safe_load(open(cur_path + "/detection/cfg/cfg.yml"))
DEBUG = config["Debug"]
DEBUG_IMG = config["Debug_Images"]

# list of cards to move from where


def all_possible(game_columns1: game_columns.GameColumns, stock_pile):
    card_location = []
    card_location_leafcards = []
    combinations = []

    listofleafcards = game_columns1.get_all_leaf_cards()
    listoffaceupcards = game_columns1.get_all_faceup_cards()
    if DEBUG:
        print("leaf cards:", *listofleafcards)
        print("faceup cards:", *listoffaceupcards)
        pprint(listoffaceupcards)

    # Add the locations of the faceup cards to card_location
    for m_card in listoffaceupcards:
        if m_card:
            card_location.append([m_card, m_card.x_pos, m_card.y_pos])
    # locate the leaf cards
    for m_card in listofleafcards:
        if m_card:
            card_location_leafcards.append(
                [m_card, m_card.x_pos, m_card.y_pos])

    # checking suitpile
    for thiscard3 in range(len(listofleafcards)):

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
    primedrawpile = stock_pile
    cardfrompile = primedrawpile.get_top_waste()

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
        else:
            if cardfrompile.number == 13:
                for col_index, col in enumerate(game_columns1.solitaire):
                    if game_columns1.get_pile_size_in_col(col_index) == 0:
                        # x_pos is -1 by default. This is checked in Algorithm
                        waste_to_leaf.append([
                            [cardfrompile, 11, cardfrompile.x_pos], [None, col_index, 0]])
    # check sequences
    # 1. check nuværende med ovenstående kort
        # 1.1 - Hvis det er en sekvens, så check med næste
    # 2. Check fra øverste del af sekvens med om man kan flytte til et leaf card
    sequences = []
    for currentcard in range(len(listoffaceupcards)):
        if game_columns1.is_col_legal(card_location[currentcard][1], card_location[currentcard][2]):
            if card_location[currentcard][0].number is not 13:
                for othercards1 in range(len(listofleafcards)):
                    if card_location[currentcard][0].can_be_moved_to(card_location_leafcards[othercards1][0]):
                        if DEBUG:
                            print(
                                f"her {card_location[currentcard][0]} eller her {card_location[currentcard]}")
                        sequences.append(
                            [card_location[currentcard], card_location_leafcards[othercards1]])
            else:
                for col in range(7):
                    if game_columns1.get_pile_size_in_col(col) == 0:
                        sequences.append(
                            [card_location[currentcard], [None, col, 0]])

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
                [[card1, 11, card1.y_pos], [to_card, to_card.x_pos, to_card.y_pos]])
    return wheretomove

#  [ [card, x, y] , [] ]

import card
import solitaire as soli


deck = card.Deck()


def start_game():
    soli.init_game()

    m_deck = deck.make_deck()
    print(f"Antal kort: {len(m_deck)}")
    print(f"hej: {soli.data[soli.CARD_DECK]}")
    m_deck = deck.shuffle(m_deck)

    for row in range(7):
        for column in range(7):

            if column == row:
                soli.solitaire[row, column] = m_deck.pop(0)
            elif column < row:
                card = m_deck.pop(0)
                card.is_flipped = True
                soli.solitaire[row, column] = card
    # putting the rest of the card in card_deck
    for i in range(len(m_deck)):
        soli.card_deck[i] = m_deck[i]
    # saving the card_deck in the data array
    soli.data[soli.CARD_DECK] = soli.card_deck


def show():
    print(f"Første kort: {soli.solitaire[0,0]} er {soli.solitaire[0,0].color}")
    print()
    soli.show_card_deck()
    print(f"Turned card: {soli.data[soli.TURNED]}")
    soli.four_suit_deck()

    ### DEBUG ###
    # soli.set_own_cards(2)
    ### DEBUG ###

    for column in range(7):
        print()
        for row in range(7):
            if soli.solitaire[row, column]:
                # print back-side of card if it's flipped - else print the card
                if soli.solitaire[row, column].is_flipped:
                    print("[ ]", end=" ")
                else:
                    print(soli.solitaire[row, column], end=" ")
            else:
                print(" "*4, end="")


def debugshow():
    for column in range(7):
        print()
        for row in range(7):
            if soli.solitaire[row, column]:
                # print back-side of card if it's flipped - else print the card
                if soli.solitaire[row, column].is_flipped == True:
                    print("[ ]", end=" ")
                else:
                    print(soli.solitaire[row, column], end=" ")
            else:
                print(" "*4, end="")


def play():
    while 1:
        show()

        print("")
        card = input("Your turn: ")
        # quit
        if card == "q":
            break

        if card == "whoops":
            soli.movecard(0, 0, 1, 2)
            debugshow()
            soli.moverow(2, 1)
            debugshow()
            soli.moveseries(3, 2, 2)
            debugshow()
        # draw card
        if card == "d":
            soli.turn_card()
        if card == "l":
            if soli.is_move_legal(2, 2):
                print("legal")
            else:
                print("ikke legal")
        print(card)


# to run the program
start_game()
play()

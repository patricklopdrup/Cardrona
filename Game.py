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


def play():
    while 1:
        show()

        print("")
        card = input("Your turn: ")
        # quit
        if card == "q":
            break

        elif card == "deck":
            soli.move_from_deck(2, 3)

        elif card == "whoops":
            soli.movecard(0, 0, 1, 2)
            soli.moverow(2, 1)
            soli.moveseries(3, 2, 2)
        # draw card
        elif card == "d":
            soli.turn_card()
        elif card == "l":
            if soli.is_col_legal_move(2, 0):
                print("legal")
            else:
                print("ikke legal")
        else:
            # move card (does not check for legal moves yet)
            inputs = card.split(" ")
            # converting to list of ints
            inputs = [int(i) for i in inputs]

            print(inputs)
            soli.movecard(inputs[0], inputs[1], inputs[2], inputs[3])
        print(card)


# to run the program
start_game()
play()

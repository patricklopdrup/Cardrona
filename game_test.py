import card
import rules
import from_img
import game_columns as game
import Agent

deck = card.Deck()
game = game.GameColumns()

def make_game():
    """ Making a deck of cards """
    m_deck = game.deck.make_deck()
    m_deck = game.deck.shuffle(m_deck)

    for card in m_deck:
        print(card, end=", ")
    print()

    # Creating the game in the 2D array
    for col in range(7):
        for row in range(7):
            if row == col:
                game.solitaire[col, row] = m_deck.pop(0)
            elif row < col:
                card = m_deck.pop(0)
                card.is_facedown = True
                game.solitaire[col, row] = card

def show_test():
    """ Print the game """
    print()
    for col in range(7):
        print()
        for row in range(7):
            if game.solitaire[row, col]:
                # Print back-side of card if it's flipped - else print the card
                if game.solitaire[row, col].is_facedown:
                    print("[ ]", end=" ")
                else:
                    print(game.solitaire[row, col], end=" ")
            else:
                print(" "*4, end="")
    print()

def play():
    while 1:
        show_test()

        print("")
        card = input("Your turn: ")
        # Quit
        if card == "q":
            break

        elif card == "whoops":
            game.make_game()
            game.show_test()

            Agent.all_possible(g)

        # Draw card

        elif card == "l":
            if rules.is_col_legal_move(2, 0):
                print("legal")
            else:
                print("ikke legal")
        else:
            # Move card (does not check for legal moves yet)
            inputs = card.split(" ")
            # Converting to list of ints
            inputs = [int(i) for i in inputs]


        print(card)


# To run the program
make_game()
#from_img.make_game_first_time(from_img.test_list)
play()

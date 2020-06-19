import card
import game_columns as game
import from_img
import draw_pile
import detection.detect as detect
import Agent
import Algorithm

game = game.GameColumns()
stock = draw_pile.Stock_pile()

stock_pile_list = [('5C')]

suit_pile_list = [('1H'), None, None, ('1S')]

turned_card_list = [
    [('13S'), ('12H'), ('11S'), ('9H'), ('8C'), ('7D')],
    [('5S'), ('12H')],
    [('8S'), ('5D')],
    [('5S'), ('12H')],
    [],
    [('7S'), ('6S')],
    [('1S'), ('12D')]
]


def make_game(self):
    """ Making a deck of cards """
    m_deck = self.deck.make_deck()
    m_deck = self.deck.shuffle(m_deck)

    for card in m_deck:
        print(card, end=", ")
    print()

    # Creating the game in the 2D array
    for col in range(7):
        for row in range(7):
            if row == col:
                self.solitaire[col, row] = m_deck.pop(0)
            elif row < col:
                card = m_deck.pop(0)
                card.is_facedown = True
                self.solitaire[col, row] = card


def show_test():
    """ Print the game """
    print("Waste pile:", *stock.waste)

    suit_piles = game.m_suit_pile.suit_piles
    print("H:", *suit_piles['H'])
    print("S:", *suit_piles['S'])
    print("D:", *suit_piles['D'])
    print("C:", *suit_piles['C'])
    # print("H:", *cards[suit])

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


def test_load_img():
    m_detect = detect.detect()
    if m_detect.load_state("detection/img/hej.jpg"):
        from_img.make_stock_pile(m_detect.get_talon())
        from_img.make_suit_pile(m_detect.get_foundations())
        from_img.make_seven_column(m_detect.get_tableaus())
        show_test()

        # Get all the possible moves
        moves = Agent.all_possible(game)
        print(f"moves: {moves}")
        # Print the answer from the AI
        ai_answer = Algorithm.decision(moves)
        print(ai_answer.user_text)

        # Update the game
        action = ai_answer.pc_action
        if action == "to_suit":
            card_to_move = ai_answer.from_card
            game.move_to_suit_pile(card_to_move.x_col, card_to_move.y_col)
        elif action == "to_col":
            from_card = ai_answer.from_card
            to_card = ai_answer.to_card
            game.move_in_game(from_card.x_pos, from_card.y_pos, to_card.x_pos)

        # Run again
        input("click")
        m_detect.load_state("detection/img/hej.jpg")
        from_img.make_stock_pile(m_detect.get_talon())
        from_img.make_suit_pile(m_detect.get_foundations())
        from_img.make_seven_column(m_detect.get_tableaus())
        show_test()
    else:
        print("Something went wrong")


def show_game(detection):
    from_img.make_stock_pile(detection.get_talon())
    from_img.make_suit_pile(detection.get_foundations())
    from_img.make_seven_column(detection.get_tableaus())
    show_test()


def test_take_img():
    m_detect = detect.detect()
    m_detect.take_picture()
    show_game(m_detect)

    # Get all the possible moves
    moves = Agent.all_possible(game)
    print(f"moves: {moves}")
    # Print the answer from the AI
    ai_answer = Algorithm.decision(moves)
    print(ai_answer.user_text)

    # Update the game
    action = ai_answer
    if action == "to_suit":
        card_to_move = ai_answer.from_card
        game.move_to_suit_pile(card_to_move.x_col, card_to_move.y_col)
    elif action == "to_col":
        from_card = ai_answer.from_card
        to_card = ai_answer.to_card
        game.move_in_game(from_card.x_pos, from_card.y_pos, to_card.x_pos)
    elif action == "from_waste_to_suit":
        stock.move_to_suit_pile()
    input("Next move")
    m_detect.take_picture()
    show_game(m_detect)

    # Print the answer from the AI
    ai_answer = Algorithm.decision(moves)
    print(ai_answer.user_text)


# test_load_img()
test_take_img()

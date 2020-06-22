import game.card as card
import game.game_columns as game
import from_img
import game.draw_pile as draw_pile
import game.suit_pile as suit_pile
import detection.detect as detect
import agent.Agent as Agent
import agent.Algorithm as Algorithm
import agent.action_moves as action_moves
from pprint import pprint
import yaml
from os import path

# Global configuration for file
cur_path = path.dirname(path.abspath(__file__))
cfg_path = cur_path + "/detection/cfg/cfg.yml"
config = yaml.safe_load(open(cfg_path))
DEBUG = config["Debug"]

game = game.GameColumns()
stock = draw_pile.Stock_pile()
suit_pile = suit_pile.Suit_pile()

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


def show_test(game_object=None):
    """ Print the game """
    if game_object:
        local_game = game_object
    else:
        local_game = game
    print("Waste pile:", stock.waste)

    suit_piles = local_game.m_suit_pile.suit_piles
    print("H:", *suit_piles['H'])
    print("S:", *suit_piles['S'])
    print("D:", *suit_piles['D'])
    print("C:", *suit_piles['C'])

    print()
    for col in range(19):
        print()
        value = None
        for row in range(7):
            if local_game.solitaire[row, col] != 0:
                value = 1
                # Print back-side of card if it's flipped - else print the card
                if local_game.solitaire[row, col] is None or local_game.solitaire[row, col].is_facedown:
                    print("[ ]", end=" ")
                else:
                    print(local_game.solitaire[row, col], end=" ")
            else:
                print(" " * 4, end="")
        if not value:
            break
    print()


# def test_load_img():
#     m_detect = detect.detect()
#     if m_detect.load_state("detection/img/test3.jpg"):
#         from_img.make_stock_pile(m_detect.get_talon(), stock)
#         from_img.make_suit_pile(m_detect.get_foundations())
#         from_img.make_seven_column(m_detect.get_tableaus())
#         show_test()

#         # Get all the possible moves
#         moves = Agent.all_possible(game, stock)
#         print(f"moves: {moves}")
#         # Print the answer from the AI
#         ai_answer = Algorithm.decision(moves)
#         print(ai_answer.user_text)

#         # Update the game
#         action = ai_answer.pc_action
#         if action == "to_suit":
#             card_to_move = ai_answer.from_card
#             game.move_to_suit_pile(card_to_move.x_col, card_to_move.y_col)
#         elif action == "to_col":
#             from_card = ai_answer.from_card
#             to_card = ai_answer.to_card
#             game.move_in_game(from_card.x_pos, from_card.y_pos, to_card.x_pos)

#         # Run again
#         input("click")
#         m_detect.load_state("detection/img/hej.jpg")
#         from_img.make_stock_pile(m_detect.get_talon(), stock)
#         from_img.make_suit_pile(m_detect.get_foundations())
#         from_img.make_seven_column(m_detect.get_tableaus())
#         show_test()
#     else:
#         print("Something went wrong")


# def test_take_img():
#     m_detect = detect.detect()
#     m_detect.take_picture()
#     show_game(m_detect)

#     moves = Agent.all_possible(game, stock)
#     # Print the answer from the AI
#     ai_answer = Algorithm.decision(moves)
#     print(ai_answer.user_text)

#     if DEBUG:
#         # Get all the possible moves
#         print(f"moves: {moves}")

#     # Update the game
#     action = ai_answer
#     if action == "to_suit":
#         card_to_move = ai_answer.from_card
#         game.move_to_suit_pile(card_to_move.x_col, card_to_move.y_col)
#     elif action == "to_col":
#         from_card = ai_answer.from_card
#         to_card = ai_answer.to_card
#         game.move_in_game(from_card.x_pos, from_card.y_pos, to_card.x_pos)
#     elif action == "from_waste_to_suit":
#         stock.move_to_suit_pile()
#     input("Next move")
#     m_detect.take_picture()
#     show_game(m_detect)

#     # Print the answer from the AI
#     ai_answer = Algorithm.decision(moves)
#     print(ai_answer.user_text)

#####################################
def show_game(detection):
    show_test()


def __load_from_detected_img(m_detect):
    talon = m_detect.get_talon()
    pprint(talon)
    suit = m_detect.get_foundations()
    cols = m_detect.get_tableaus()
    if DEBUG:
        pprint(talon)
        pprint(suit)
        pprint(cols)
    from_img.make_stock_pile(talon, stock)
    from_img.make_suit_pile(suit)
    from_img.make_seven_column(cols)


def __take_picture(m_detect, load_img=False):
    if load_img:
        while not m_detect.load_state("detection/img/test3.jpg"):
            print("Virkede ikke")
    else:
        while not m_detect.take_picture():
            print("Tag nyt billede.")


def game_loop(load_img=False):
    m_detect = detect.detect()

    while not suit_pile.is_game_won():
        while True:
            try:
                __take_picture(m_detect)
                # Create the game
                __load_from_detected_img(m_detect)
            except TypeError:
                print("Prøv igen")
                input("Klik ENTER for nyt billede")
            # if we reach this point we detected the img correctly
            else:
                break

        # Show the game in console
        show_game(m_detect)

        moves = Agent.all_possible(game, stock)
        if DEBUG:
            print(f"col_facedown: {game.col_facedown}")
            # Print moves if debug is on
            print(f"moves: {moves}")

        # Print the answer from the AI
        ai_answer = Algorithm.decision(moves)
        print(ai_answer.user_text)

        action = ai_answer.pc_action
        to_card = ai_answer.to_card
        from_card = ai_answer.from_card
        if DEBUG:
            print("ai_answer:", ai_answer)
        # Check for action
        if action == action_moves.waste_to_col:
            stock.move_to_column(to_card.x_pos)
        elif action == action_moves.waste_to_suit:
            stock.move_to_suit_pile()
        elif action == action_moves.col_to_suit:
            game.move_to_suit_pile(
                from_card.x_pos, from_card.y_pos)
        elif action == action_moves.col_to_col:
            game.move_in_game(from_card.x_pos, from_card.y_pos, to_card.x_pos)
        # elif action == action_moves.suit_to_col:

        input("Klik ENTER for næste træk!")

    print("Du har vundet!")


# test_load_img()
# test_take_img()
if __name__ == '__main__':
    game_loop()

from pprint import pprint
from game import game_columns as game_logic
from game import card
import numpy as np
import yaml
import cv2
from automated_test import image_generation as ig
from automated_test import general_funcs as gf
from agent import action_moves
from detection import detect as detector
from agent import Agent
from agent import Algorithm
import from_img
from game import draw_pile


# Global configuration for file
cfg_path = "config/cfg.yml"
config = yaml.safe_load(open(cfg_path))
config = config['auto_test']
card_path = config['card_positions']['path']
save_folder = config['save_folder']


class game:
    def __init__(self):
        self.game_data = game_logic.GameColumns()
        self.card_image_paths = {
            'Clubs': [f'{card_path}Clubs/{i}.png' for i in range(1, 14)],
            'Diamonds': [f'{card_path}Diamonds/{i}.png' for i in range(1, 14)],
            'Hearts': [f'{card_path}Hearts/{i}.png' for i in range(1, 14)],
            'Spades': [f'{card_path}Spades/{i}.png' for i in range(1, 14)],
            'Back': f'{card_path}0.png'
        }
        self.current_stage = 0

        self.deck_class = card.Deck()

        self.deck = self.deck_class.make_deck()
        self.deck = self.deck_class.shuffle(self.deck)

        self.face_down = []
        self.talon_cards = []

        self.talon = draw_pile.Stock_pile(self.game_data, self.game_data.m_suit_pile)

        self.detector = detector.detect()

        # Creating the game in the 2D array
        for col in range(7):
            for row in range(7):
                if row == col:
                    self.game_data.solitaire[col, row] = self.deck.pop(0)
                elif row < col:
                    m_card = None
                    self.game_data.solitaire[col, row] = m_card
                    self.face_down.append(self.deck.pop(0))

    def __load_from_detected_img(self):
        talon = self.detector.get_talon()
        suit = self.detector.get_foundations()
        cols = self.detector.get_tableaus()
        from_img.make_stock_pile(talon, self.talon)
        self.game_data.m_suit_pile = from_img.make_suit_pile(suit)
        self.game_data.solitaire = from_img.make_seven_column(cols, self.game_data)

        # detector.print_stuff(self.detector)

        any_illegal = False
        for col in range(len(self.game_data.solitaire)):
            for m_card in self.game_data.solitaire[col]:
                if m_card != 0 and not m_card.is_facedown:
                    any_illegal = not self.game_data.is_col_legal(m_card.x_pos, m_card.y_pos)
                    break

            if any_illegal:
                raise gf.ColumnNotLegal
        # show_test(game)

    def game_loop(self):
        ai_waste_count = 0
        while not self.game_data.m_suit_pile.is_game_won():
            while True:
                # Current stage - What stage number this is
                img_path = f'{save_folder}/{self.current_stage}.jpg'
                try:
                    self.detector.load_state(img_path)
                    self.__load_from_detected_img()
                    break
                except gf.ColumnNotLegal:
                    self.current_stage += 1
                    print("En kolonne var ikke legal, prøv igen")
                    self.generator.generate_image(game_data=self.game_data,
                                                  stage=self.current_stage, talon=self.talon)

            moves = Agent.all_possible(self.game_data, self.talon)
            ai_answer = Algorithm.decision(moves)
            to_card = ai_answer.to_card
            from_card = ai_answer.from_card
            action = ai_answer.pc_action

            if action is None:
                ai_waste_count += 1
                if len(self.deck) > 0:
                    self.talon_cards.append(self.deck.pop(0))
                    self.talon.waste = self.talon_cards[-1]
                else:
                    print("Vender bunke og trækker kort")
                    self.deck.extend(self.talon_cards)
                    self.talon_cards = []
                    if len(self.deck) > 0:
                        self.talon_cards.append(self.deck.pop(0))
                        self.talon.waste = self.talon_cards[-1]
                        to_card = None
                        from_card = None
                    else:
                        break
            else:
                ai_waste_count = 0

            if ai_waste_count >= len(self.deck) + len(self.talon_cards) + 1:
                break

            elif action == action_moves.waste_to_col:
                if to_card:
                    success = self.talon.move_to_column(to_card.x_pos)
                else:
                    success = self.talon.move_to_column()
                if success:
                    try:
                        self.talon_cards.pop()
                        self.talon.waste = self.talon_cards[-1]
                    except IndexError:
                        self.talon.waste = None
            elif action == action_moves.waste_to_suit:
                success = self.talon.move_to_suit_pile()
                if success:
                    try:
                        self.talon_cards.pop()
                        self.talon.waste = self.talon_cards[-1]
                    except IndexError:
                        self.talon.waste = None
            elif action == action_moves.col_to_suit:
                self.game_data.move_to_suit_pile(from_card.x_pos, from_card.y_pos)
            elif action == action_moves.col_to_col:
                self.game_data.move_in_game(from_card.x_pos, from_card.y_pos, to_card.x_pos)
            if action and from_card.y_pos > 0:
                x_pos = from_card.x_pos
                y_pos = from_card.y_pos - 1
                if self.game_data.solitaire[x_pos][y_pos].is_facedown:
                    self.game_data.solitaire[x_pos][y_pos] = self.face_down.pop(0)
            show_test(self.game_data, self.talon)

            self.current_stage += 1
            self.generator.generate_image(game_data=self.game_data,
                                          stage=self.current_stage, talon=self.talon)

        if self.game_data.m_suit_pile.is_game_won():
            print("Spillet er vundet!")
            return
        if ai_waste_count >= len(self.deck) + len(self.talon_cards) + 1:
            print("Spillet er tabt!")

    def test(self):
        self.generator = ig.image_generation()
        # temp_card = self.deck.pop(0)
        # self.game_data.solitaire[0, self.game_data.get_pile_size_in_col(
        #     0)] = temp_card
        # self.game_data.solitaire[0][0] = card.Card(12, 'S')
        # self.game_data.solitaire[1][1] = card.Card(13, 'H')
        self.generator.generate_image(game_data=self.game_data,
                                      stage=self.current_stage, talon=self.talon)
        self.game_loop()


def show_test(game_object=None, talon=None):
    """ Print the game """
    local_game = game_object
    print("Waste pile:", talon.waste)

    suit_piles = local_game.m_suit_pile.suit_piles
    print("H:", *suit_piles['H'])
    print("S:", *suit_piles['S'])
    print("D:", *suit_piles['D'])
    print("C:", *suit_piles['C'])

    print()
    for row in range(19):
        print()
        value = None
        for col in range(7):
            if local_game.solitaire[col, row] != 0:
                value = 1
                # Print back-side of card if it's flipped - else print the card
                if local_game.solitaire[col, row] is None or (local_game.solitaire[col, row] != 'Blank' and local_game.solitaire[col, row].is_facedown):
                    print("[ ]", end=" ")
                else:
                    print(local_game.solitaire[col, row], end=" ")
            else:
                print(" " * 4, end="")
        if not value:
            break
    print()

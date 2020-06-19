import Agent
import game_columns


class algorithm_action:
    def __init__(self, user_text: str, pc_action: str, from_card=None, to_card=None):
        self.user_text = user_text
        self.pc_action = pc_action
        self.from_card = from_card
        self.to_card = to_card


def decision(moves, current_card=None, card_destination=None):
    # Draw card if no moves available.
    if not moves:
        user_text = "Træk et kort"
        action = None
        return algorithm_action(user_text, action)

    # Check suit moves.
    for i in range(len(moves)):
        action = "to_suit"
        m_card = moves[i][0][0]

        if moves[i][1][1] == 7:
            user_text = "Ryk " + \
                str(moves[i][0][0].number) + \
                str(moves[i][0][0].suit) + " til første suit"
            return algorithm_action(user_text, action, from_card=m_card)
        elif moves[i][1][1] == 8:
            user_text = "Ryk " + \
                str(moves[i][0][0].number) + \
                str(moves[i][0][0].suit) + " til andet suit"
            return algorithm_action(user_text, action, from_card=m_card)
        elif moves[i][1][1] == 9:
            user_text = "Ryk " + \
                str(moves[i][0][0].number) + \
                str(moves[i][0][0].suit) + " til tredje suit"
            return algorithm_action(user_text, action, from_card=m_card)
        elif moves[i][1][1] == 10:
            user_text = "Ryk " + \
                str(moves[i][0][0].number) + \
                str(moves[i][0][0].suit) + " til fjerde suit"
            return algorithm_action(user_text, action, from_card=m_card)

    """
    Prioriteter:
    1. Bunker med flest kort med forsiden nedad.
    2. Hvis man rykker en kolonne så skal der prioriteres dem med konger.
    """
    print("her1")
    y_pos = 0
    current_card
    card_destination
    # Check regular moves.
    for i in range(len(moves)):
        if moves[i][0][2] > y_pos:
            y_pos = moves[i][0][2]
            current_card = moves[i][0][0]
            card_destination = moves[i][1][0]
    print(f"y er {y_pos}")
    # -1 for a card not placed in the columns
    # Goes here only if we look at the waste pile
    if moves[i][0][2] == -1:
        print("større end 11")
        # Move from waste pile
        for i in range(len(moves)):
            if moves[i][0][1] == 11:
                print("er herrrr")
                current_card = moves[i][0][0]
                card_destination = moves[i][1][0]
                user_text = "Ryk " + str(current_card) + \
                    " til " + str(card_destination)
                action = "from_waste_to_suit"
                return algorithm_action(user_text, action, current_card, card_destination)

    user_text = "Ryk " + str(current_card) + " til " + str(card_destination)
    action = "to_col"
    # Return new object of algorithm_action
    return algorithm_action(user_text, action, current_card, card_destination)

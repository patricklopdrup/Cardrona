import agent.action_moves as action_moves
import game.card as card

# Object to return


class algorithm_action:
    def __init__(self, user_text: str, pc_action: str, from_card=None, to_card=None):
        self.user_text = user_text
        self.pc_action = pc_action
        self.from_card = from_card
        self.to_card = to_card

    def __str__(self):
        return f"text: {self.user_text}, action: {self.pc_action}, from_card: {self.from_card}, to_card: {self.to_card}"


def decision(moves, current_card=None, card_destination=None):
    # Draw card if no moves available.
    if not moves:
        user_text = "Træk et kort"
        action = None
        return algorithm_action(user_text, action)

    # Check suit moves.
    for i in range(len(moves)):
        # Card to be moved
        m_card = moves[i][0][0]
        # Where to move m_card
        to_card = moves[i][1][1]

        # Check if the card is from the waste pile
        if m_card.x_pos == -1 and m_card.y_pos == -1:
            action = action_moves.waste_to_suit
        # Else if the card is from the columns
        else:
            action = action_moves.col_to_suit

        # If a card can be moved to a suit pile
        if to_card == 7:
            user_text = "Ryk " + \
                str(m_card.number) + \
                str(m_card.suit) + " til første suit"
            return algorithm_action(user_text, action, from_card=m_card, to_card=to_card)
        elif to_card == 8:
            user_text = "Ryk " + \
                str(m_card.number) + \
                str(m_card.suit) + " til andet suit"
            return algorithm_action(user_text, action, from_card=m_card, to_card=to_card)
        elif to_card == 9:
            user_text = "Ryk " + \
                str(m_card.number) + \
                str(m_card.suit) + " til tredje suit"
            return algorithm_action(user_text, action, from_card=m_card, to_card=to_card)
        elif to_card == 10:
            user_text = "Ryk " + \
                str(m_card.number) + \
                str(m_card.suit) + " til fjerde suit"
            return algorithm_action(user_text, action, from_card=m_card, to_card=to_card)

    """
    Prioriteter:
    1. Bunker med flest kort med forsiden nedad.
    2. Hvis man rykker en kolonne så skal der prioriteres dem med konger.
    """
    y_pos = 0
    # Check regular moves.
    for i in range(len(moves)):
        current_card = moves[i][0][0]
        card_destination = moves[i][1][0]
        if current_card.y_pos > y_pos:
            y_pos = current_card.y_pos
        # -1 for a card not placed in the columns
        # Goes here only if we look at the waste pile
        if current_card.y_pos == -1:
            # Move from waste pile
            for i in range(len(moves)):
                if moves[i][0][1] == 11:
                    current_card = moves[i][0][0]
                    card_destination = moves[i][1][0]
                    # If the destination column is empty
                    if card_destination:
                        user_text = "Ryk " + str(current_card) + \
                            " til " + str(card_destination)
                    else:
                        user_text = "Ryk " + \
                            str(current_card) + " til en tom plads"
                        # Create a placeholder card (we only use x and y pos NOT number or suit)
                        card_destination = card.Card(
                            1, 'H', x=moves[i][1][1], y=moves[i][1][2])
                    action = action_moves.waste_to_col
                    return algorithm_action(user_text, action, current_card, card_destination)

        if current_card.number == 13 and not card_destination:
            user_text = "Ryk " + \
                str(current_card) + " til en tom plads"
            card_destination = card.Card(
                1, 'H', x=moves[i][1][1], y=moves[i][1][2])
            action = action_moves.col_to_col
            return algorithm_action(user_text, action, current_card, card_destination)

    # Don't go into loop. Check for card above
    possible_count = 0
    for i in range(len(moves)):
        current_card = moves[i][0][0]
        card_destination = moves[i][1][0]
        if current_card.above and card_destination:
            if current_card.above.number == card_destination.number:
                user_text = "Træk et kort"
                action = None
                continue
        possible_count += 1
        action = action_moves.col_to_col
        user_text = "Ryk " + str(current_card) + \
            " til " + str(card_destination)
        return algorithm_action(user_text, action, current_card, card_destination)

    if possible_count < 1:
        return algorithm_action(user_text, action)

    user_text = "Ryk " + str(current_card) + " til " + str(card_destination)
    action = action_moves.col_to_col
    # Return new object of algorithm_action
    return algorithm_action(user_text, action, current_card, card_destination)

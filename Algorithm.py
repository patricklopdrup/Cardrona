import Agent
import game_columns

def decision(moves, current_card=None, card_destination=None):
    # Draw card if no moves available.
    if not moves:
        return "Træk et kort"

    # Check suit moves.
    for i in range(len(moves)):
        if moves[i][1][1] == 7:
            return "Ryk " + str(moves[i][0][0].number) + str(moves[i][0][0].suit) + " til første suit"
        elif moves[i][1][1] == 8:
            return "Ryk " + str(moves[i][0][0].number) + str(moves[i][0][0].suit) + " til andet suit"
        elif moves[i][1][1] == 9:
            return "Ryk " + str(moves[i][0][0].number) + str(moves[i][0][0].suit) + " til tredje suit"
        elif moves[i][1][1] == 10:
            return "Ryk " + str(moves[i][0][0].number) + str(moves[i][0][0].suit) + " til fjerde suit"
    """
    Prioriteter:
    1. Bunker med flest kort med forsiden nedad.
    2. Hvis man rykker en kolonne så skal der prioriteres dem med konger.
    """
    y_pos = 0
    current_card
    card_destination
    # Check regular moves.
    for i in range(len(moves)):
        if moves[i][0][2] > y_pos:
            y_pos = moves[i][0][2]
            current_card = moves[i][0][0]
            card_destination = moves[i][1][0]

    return "Ryk " + str(current_card.number) + str(current_card.suit) + " til " + str(card_destination.number) + str(card_destination.suit)

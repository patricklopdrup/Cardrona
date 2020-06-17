import Agent

"""
All return types need to be replaced by their equivalent method.
"""
def decision(moves):
    # Draw card if no moves available.
    if not moves:
        return "Træk et kort"

    # Check suit moves.
    for i in len(moves):
        if moves[i][0][1] == 7:
            return "Ryk kort til første suit"
        elif moves[i][0][1] == 8:
            return "Ryk kort til andet suit"
        elif moves[i][0][1] == 9:
            return "Ryk kort til tredje suit"
        elif moves[i][0][1] == 10:
            return "Ryk kort til fjerde suit"
    """
    Prioriteter:
    1. Bunker med flest kort med forsiden nedad.
    2. Hvis man rykker en kolonne så skal der prioriteres dem med konger.
    """
    # Check regular moves.
    for move in moves:
        # TODO: Prioritér kort?
        if move == "COLUMN":
            return "MOVE COLUMN"
        elif move == "ONE CARD":
            return "MOVE CARD"

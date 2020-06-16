import Agent

"""
All return types need to be replaced by their equivalent method.
"""
def decision(moves):
    # Draw card is no moves available.
    if not moves:
        return "DRAW CARD"

    # Check suit moves.
    for move in moves:
        if move.position == 8:
            return "MOVE TO FIRST SUIT"
        elif move.position == 9:
            return "MOVE TO SECOND SUIT"
        elif move.position == 10:
            return "MOVE TO THIRD SUIT"
        elif move.position == 11:
            return "MOVE TO FOURTH SUIT"

    # Check regular moves.
    for move in moves:
        # TODO: Prioritér kort?
        if move == "COLUMN":
            return "MOVE COLUMN"
        elif move == "ONE CARD":
            return "MOVE CARD"

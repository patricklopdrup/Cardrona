import solitaire as soli


# if card from middle of column is chosen. Checks if that's a legal move
def is_col_legal_move(col: int, row: int) -> bool:
    print(f"card: {soli.solitaire[col,row]}")
    is_legal = True
    # card we try to move (potentially from the middle of a column)
    start_card = soli.solitaire[col, row]
    if start_card == 0 or start_card.is_facedown:
        return False
    else:
        cur_color = start_card.color
        cur_num = start_card.number

    # all cards in the column (beginning from "start_card")
    cards = soli.solitaire[col]
    # we already saved current cards value so we start from the next card; col+1
    for card in cards[row+1:-1]:
        # if no card is represented
        if card == 0:
            break
        # if colors are the same or
        # the number is not 1 less than the card above we return False
        if (card.color == cur_color) or not (card.number == (cur_num-1)):
            return False
        # new values for current card
        cur_color = card.color
        cur_num = card.number
    return is_legal


def is_move_legal(from_index: list, to_index: list) -> bool:
    from_card = soli.solitaire[from_index[0], from_index[1]]
    to_card = soli.solitaire[to_index[0], to_index[1]]
    # kings can be moved to empty spaces
    if to_card == 0 and from_card.number == 13:
        return True
    # card can be placed on a card with with different color and +1 in number
    if to_card.color != from_card.color and to_card.number-1 == from_card.number:
        # check if the whole column is legal
        if is_col_legal_move(from_index[0], from_index[1]):
            return True

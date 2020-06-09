import solitaire as soli
import card


col_facedown: list = [0, 1, 2, 3, 4, 5, 6]


test_list = [
    [
        ['AH']
    ],
    [
        ['2H']
    ],
    [
        ['3H']
    ],
    [
        ['4H']
    ],
    [
        ['5H']
    ],
    [
        ['6H']
    ],
    [
        ['7H']
    ]
]


def parse_value(input: str) -> int:
    if len(input) > 2:
        return int(input[:2])
    name = input[0]
    if name == 'K':
        return 13
    elif name == 'Q':
        return 12
    elif name == 'J':
        return 11
    elif name == 'A':
        return 1
    else:
        return int(name)


def parse_suit(input: str) -> str:
    return input[-1]


def make_game_first_time(input_list: list):
    for row_index, row in enumerate(input_list):
        for col_index, col in enumerate(row):
            default_card = card.Card(2, 'H', True)
            # print(f"default kort num: {default_card.number}")
            # print(f"col: {col} og 0'te: {col[0]}")
            # print(f"val: {parse_value(col[0])} og suit: {parse_suit(col[0])}")
            my_card = card.Card(parse_value(col[0]), parse_suit(col[0]))
            if row_index == col_index:
                soli.solitaire[row_index, col_index] = my_card
            else:
                soli.solitaire[row_index, col_index] = default_card


def make_game_from_input(input_list: list):
    for row in input_list:
        for col in row:
            card = card.Card(parse_value(col[0]), parse_suit(col[0]))


def test():
    # hej = 'KH'
    # hej2 = "9S"
    # print(parse_value(hej2))
    # for i in test_list:
    #     for j in i:
    #         print(i[0])
    make_game_first_time(test_list)


test()

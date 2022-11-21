# A simple Tic Tac Toe program made by Pavel Umanskiy on 21.11.2022
def print_field(field):
    print('  0 1 2')
    print('0 %s %s %s' % (field[0][0], field[0][1], field[0][2]))
    print('1 %s %s %s' % (field[1][0], field[1][1], field[1][2]))
    print('2 %s %s %s' % (field[2][0], field[2][1], field[2][2]))

def players_turn(player, field):
    while True:
        coords = input(f"Player {player}'s turn: ")
        if len(coords) != 3:
            while True:
                print('Wrong input format! The input should be as follows: the first coordinate, space, the second coordinate. Please try again.')
                coords = input(f"Player {player}'s turn: ")
                if len(coords) == 3:
                    break
        coord1, coord2 = int(coords[0]), int((coords[2]))
        if coord1 not in [0, 1, 2] or coord2 not in [0, 1, 2]:
            while True:
                print("Coordinates out of field's range! Please try again! Each coordinate can be 0, 1 or 2")
                coords = input(f"Player {player}'s turn: ")
                if len(coords) != 3:
                    while True:
                        print('Wrong input format! The input should be as follows: the first coordinate, space, the second coordinate. Please try again.')
                        coords = input(f"Player {player}'s turn: ")
                        if len(coords) == 3:
                            break
                coord1, coord2 = int(coords[0]), int((coords[2]))
                if coord1 in [0, 1, 2] and coord2 in [0, 1, 2]:
                    break         
        if field[coord1][coord2] == '-':
            break
        else:
            print('This plase is already taken, choose another coordinates')
    field[coord1][coord2] = f'{player}'
    
def win_check(p, field):
    return (field[0][0] == f'{p}' and field[0][1] == f'{p}' and field[0][2] == f'{p}') or (
        field[1][0] == f'{p}' and field[1][1] == f'{p}' and field[1][2] == f'{p}') or (
        field[2][0] == f'{p}' and field[2][1] == f'{p}' and field[2][2] == f'{p}') or (
        field[0][0] == f'{p}' and field[1][0] == f'{p}' and field[2][0] == f'{p}') or (
        field[0][1] == f'{p}' and field[1][1] == f'{p}' and field[2][1] == f'{p}') or (
        field[0][2] == f'{p}' and field[1][2] == f'{p}' and field[2][2] == f'{p}') or (
        field[0][0] == f'{p}' and field[1][1] == f'{p}' and field[2][2] == f'{p}') or (
        field[0][2] == f'{p}' and field[1][1] == f'{p}' and field[2][0] == f'{p}')

def tie_check(field):
    rows_without_space = 0
    for row in field:
        if '-' not in row:
            rows_without_space += 1
    return True if rows_without_space == 3 else False

    
print("Hello and welcome to my little game of tic tac toe!\nThe rules are simple: on your turn enter the coorinates " +
      "(e.g. 1 2) and press Enter.\nDon't forget to put space between the coords! The rest is simple tick tack toe!\nHave fun!")
field = [['-' for _ in range(3)] for _ in range(3)]
print_field(field)
while True:
    players_turn('X', field)
    print_field(field)
    if win_check('X', field):
        print('Player X won!')
        break
    elif tie_check(field):
        print('Tie!')
        break
    players_turn('O', field)
    print_field(field)
    if win_check('O', field):
        print('Player O won!')
        break
    elif tie_check(field):
        print('Tie!')
        break
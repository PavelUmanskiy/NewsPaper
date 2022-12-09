# A battleship game made by Pavel Umanskiy on December, 9th 2022

from random import randrange, choice
from time import sleep
import os

class GameplayException(Exception):
    pass

class ShotException(GameplayException):
    pass

class OutException(ShotException):
    pass

class FiredAlreadyException(ShotException):
    pass

class AddShipException(GameplayException):
    pass

class LongInputException(GameplayException):
    pass

class CoordsOutOfRangeException(GameplayException):
    pass


class Dot():
    @property
    def coords(self) -> tuple:
        return self.xcoord, self.ycoord
    
    @coords.setter
    def coords(self, x=1, y=1) -> None:
        if isinstance(x, bool) or isinstance(y, bool):
            raise TypeError("Coords can't take bool type as argument")
            
        else:
            if (isinstance(x, int) and isinstance(y, int)) and (1 <= x <= 6 and 1 <= y <= 6):
                self.xcoord = x
                self.ycoord = y
            else:
                raise ValueError("Coord's values should be integers between 1 and 6")
    
    def __init__(self, x=1, y=1) -> None:
        if isinstance(x, bool) or isinstance(y, bool):
            raise TypeError("Coords can't take boolean values as an argument")
            
        else:
            if (isinstance(x, int) and isinstance(y, int)) and (1 <= x <= 6 and 1 <= y <= 6):
                self.xcoord = x
                self.ycoord = y
            else:
                raise ValueError("Coord's values should be integers between 1 and 6")
    
    def __eq__(self, other) -> bool:
        return self.xcoord == other.xcoord and self.ycoord == other.ycoord


class Ship():
    def __init__(self, bow_x=1, bow_y=1, size=1, direction='right') -> None:
        self.bow = Dot(bow_x, bow_y)
        if not isinstance(size, bool) and size in (1, 2, 3):
            self.size = size
            self.health = size
            
        else:
            raise ValueError("Ship's size shoul be an integer between 1 and 3")
        if direction.lower() in ('left', 'right', 'up', 'down'):
            self.direction = direction.lower()
        else:
            raise ValueError('Direction could be either "left", "right", "up" or "down" (case insensitive)')
    
    
    @property
    def dots(self) -> tuple:
        if self.size == 1:
            return self.bow.coords
        elif self.size == 2:
            if self.direction == 'left':
                return (self.bow.coords[0], self.bow.coords[1] - 1), self.bow.coords
            elif self.direction == 'right':
                return self.bow.coords, (self.bow.coords[0], self.bow.coords[1] + 1)
            elif self.direction == 'up':
                return self.bow.coords, (self.bow.coords[0] - 1, self.bow.coords[1])
            elif self.direction == 'down':
                return self.bow.coords, (self.bow.coords[0] + 1, self.bow.coords[1])
        elif self.size == 3:
            if self.direction == 'left':
                return (self.bow.coords[0], self.bow.coords[1] - 2), (self.bow.coords[0], self.bow.coords[1] - 1), self.bow.coords
            elif self.direction == 'right':
                return self.bow.coords, (self.bow.coords[0], self.bow.coords[1] + 1), (self.bow.coords[0], self.bow.coords[1] + 2)
            elif self.direction == 'up':
                return self.bow.coords, (self.bow.coords[0] - 1, self.bow.coords[1]), (self.bow.coords[0] - 2, self.bow.coords[1])
            elif self.direction == 'down':
                return self.bow.coords, (self.bow.coords[0] + 1, self.bow.coords[1]), (self.bow.coords[0] + 2, self.bow.coords[1])


class Board():
    def __init__(self) -> None:
        self.board_state = [
        [0,  1,   2,   3,   4,   5,   6 ],
        [1, 'O', 'O', 'O', 'O', 'O', 'O'],
        [2, 'O', 'O', 'O', 'O', 'O', 'O'],
        [3, 'O', 'O', 'O', 'O', 'O', 'O'],
        [4, 'O', 'O', 'O', 'O', 'O', 'O'],
        [5, 'O', 'O', 'O', 'O', 'O', 'O'],
        [6, 'O', 'O', 'O', 'O', 'O', 'O']]
        self.ship_list = []
        self.hidden = False
        self.ships_left = 0
    
    def clear_board(self):
        self.__init__
    
    
    def update_board(self, x, y, value) -> None:
        self.board_state[x][y] = value
    
    
    def print_board(self) -> None:
        if not self.hidden:
            for row in range(7):
                for column in range(7):
                    print(f'{self.board_state[row][column]}', end=' ')
                print('')
        else:
            for row in range(7):
                for column in range(7):
                    if self.board_state[row][column] == '■':
                        print('O', end=' ')
                    else:    
                        print(f'{self.board_state[row][column]}', end=' ')
                print('')
    
    
    def add_ship(self, ship) -> None:
        if ship.size == 1:
            if self.board_state[ship.dots[0]][ship.dots[1]] == 'O':
                for contour_part in self.contour(ship):
                    if self.board_state[contour_part[0]][contour_part[1]] == '■':
                        raise AddShipException("There's a ship in this ship's countour")
                else:
                    self.update_board(ship.dots[0], ship.dots[1], '■')
                    self.ship_list.append(ship)
                    self.ships_left += 1
            else:
                raise AddShipException("There's a ship in this ship's coordinates")

        else:
            try:
                for ship_part in ship.dots:
                    if self.board_state[ship_part[0]][ship_part[1]] == 'O':
                        for contour_part in self.contour(ship):
                            if self.board_state[contour_part[0]][contour_part[1]] == '■':
                                raise AddShipException("There's a ship in this ship's countour")
                    else:
                        raise AddShipException("There's a ship in this ship's coordinates")
                else:
                    for ship_part_checked in ship.dots:
                        self.update_board(ship_part_checked[0], ship_part_checked[1], '■')
                    else:
                        self.ship_list.append(ship)
                        self.ships_left += 1
            except IndexError:
                raise AddShipException("It seems that random ship goes out of bounds")
                
                            
    def contour(self, ship) -> tuple:
        contour_set = set()
        range_x = range(1, 7)
        range_y = range(1, 7)
        if ship.size == 1:
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    (new_x, new_y) = (ship.dots[0] + dx, ship.dots[1] + dy)
                    if (new_x in range_x) and (new_y in range_y) and (dx, dy) != (0, 0):
                        contour_set.add((new_x, new_y))
        else:
            for ship_part in ship.dots:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        (new_x, new_y) = (ship_part[0] + dx, ship_part[1] + dy)
                        if (new_x in range_x) and (new_y in range_y) and (dx, dy) != (0, 0):
                            contour_set.add((new_x, new_y))
        return tuple(contour_set)
    
    
    def out(self, dot) -> bool:
        return False if dot.coords[0] in range(1, 7) and dot.coords[1] in range(1, 7) else True
    
    
    def shot(self, dot) -> bool:
        if not self.out(dot):
            if self.board_state[dot.coords[0]][dot.coords[1]] == '■':
                self.update_board(dot.coords[0], dot.coords[1], 'X')
                for ship in self.ship_list:
                    hit = dot.coords
                    if ship.size == 1:
                        if hit == ship.bow.coords:
                            self.ship_list.remove(ship)

                    else:    
                        if hit in ship.dots:
                            ship.health -= 1
                            if not ship.health:
                                self.ship_list.remove(ship)
                return True
            
            elif self.board_state[dot.coords[0]][dot.coords[1]] == 'O':
                self.update_board(dot.coords[0], dot.coords[1], 'T')
                return False
            else:
                raise FiredAlreadyException("You alreay fired there.")
        else:
            raise OutException("Whoops! Out of board!")


class Player():
    mine_board = Board()
    opponents_board = Board()
    
    
    @property
    def self_board(self) -> Board:
        return self.mine_board
    
    
    @self_board.setter
    def self_board(self, new_board) -> None:
        self.mine_board = new_board
    
    
    @property
    def enemy_board(self) -> Board:
        return self.opponents_board
    
    
    @enemy_board.setter
    def enemy_board(self, opponent) -> None:
        self.opponents_board = opponent.self_board
    
    def ask(self):
        pass
    
    
    def move(self) -> bool:
        while True:
            point = self.ask()
            fire = Dot(point[0], point[1])
            try:
                shot_result = self.opponents_board.shot(fire)
            except OutException:
                print("Whoops! Out of board! Try again.")
                pass
            except FiredAlreadyException:
                print("You alreay fired there. Try again.")
                pass
            else:
                break
        return shot_result
        
class User(Player):
    def ask(self) -> tuple:
        while True:
            try:
                ans = input("Where would you like to fire? ")
                if len(ans) != 3 or not ans[1].isspace() or not ans[::2].isnumeric():
                    raise LongInputException()
                
                else:
                    if (not (int(ans[0]) in range(1, 7))) or (not (int(ans[2]) in range(1, 7))):
                        raise CoordsOutOfRangeException()
                    
            except LongInputException():
                print("Invalid format! Your answer should be formated like this: x y (coordinate 1, space, coordinate 2). Try again.")
            except CoordsOutOfRangeException():
                print("Invalid coorinates! x and y should both be between 1 and 6. Try again.")
            else:
                break
            
        return int(ans[0]), int(ans[2])


class BotPlayer(Player):
    proposals = []
    
    def ask(self):
        while True:
            proposal = (randrange(1, 7), randrange(1, 7))
            if proposal not in self.proposals:
                self.proposals.append(proposal)
                return proposal

        
class Game(): 
    def __init__(self, player, bot) -> None:
        self.human_player = player
        self.human_board = self.human_player.self_board.setter = self.random_board()
        self.human_board.hidden = False
        
        self.bot_player = bot
        self.bot_board = self.bot_player.self_board.setter = self.random_board()
        self.bot_board.hidden = True
        
        self.human_player.opponents_board = self.bot_board
        self.bot_player.opponents_board = self.human_board
        
    
     
    @staticmethod
    def greet() -> None:
        print("Good morning, Admiral! I'm your First mate and I will help you coordinate the battle.")
        print("Our previous commander has been sent to another mission by HQ, right before we engaged with an enemy fleet, so our ships are already in positions.")
        print("You will see positions of our ships and the map of the sector where the enemy is located.")
        print("If you would like to fire, simply tell me the coordinates of where you think enemy ship might be.")
        print('Remember that the coordinate of the "row" of the map comes befor the coordinate of the "column"')
        print("If you'll manage to hit an enemy ship, their admiral will be distracted, and you'll be able to fire once again!")
        print("But remember that the same works with us.")
        print('Your ships are marked with "■" sign, unknown or empty squares are marked with "O" sign and misses are marked witn"T" sign.')
        print("Keep in mind that ships can't be located on adlacent squares!")
        print("Good luck, Admiral!")
    
    
    def random_board(self) -> Board:        
        directions = ('up', 'down', 'left', 'right')
        
        while True:
            generated_board = Board()
            ship_count = [0, 0, 0]
            repeats = 0
            fubar = False
            for i in range(3):
                ships_needed = 4 if i == 2 else (i + 1)
                while ship_count[i] < ships_needed:
                    placed_smoothly = False
                    try:
                        rand_ship = Ship(randrange(1,7), randrange(1,7), (3 - i), choice(directions))
                        generated_board.add_ship(rand_ship)
                    except AddShipException:
                        pass
                    else:
                        placed_smoothly = True
                    repeats += 1
                    if placed_smoothly:
                        ship_count[i] += 1
                    if repeats >= 500:
                        fubar = True
                        break
                if fubar:
                    break
            if ship_count[2] == 4:
                self.generated_board = generated_board
                return generated_board
    
    
    def loop(self) -> bool:
        while True:
            repeat_turn = True
            turns_in_a_row = False
            
            while repeat_turn:
                
                if turns_in_a_row:
                    print("You've hit an enemy ship! Use that moment to strike again!")
                    turns_in_a_row = False
                
                print('Your board:')
                self.human_board.print_board()
                
                print("The bot's board:")
                self.bot_board.print_board()
                
                print("Your turn!")
                repeat_turn = self.human_player.move()
                
                
                if repeat_turn:
                    turns_in_a_row = True
                
                os.system('cls' if os.name == 'nt' else 'clear')
                
                if not self.bot_board.ship_list:
                    return True
            
            print("Bot's turn!")
            sleep(1.5)
            
            repeat_turn = True
            turns_in_a_row = False
            
            while repeat_turn:
                if turns_in_a_row:
                    print("They have hit our ship! They'll have the opportunity to strike again!")
                    turns_in_a_row = False
                
                repeat_turn = self.bot_player.move()
                
                if repeat_turn:
                    turns_in_a_row = True
                
                if not self.human_board.ship_list:
                    return False

    
    def start(self) -> None:
        self.greet()
        
        victory = self.loop()
        
        if victory:
            print("Congratulations, Admiral! You've destroyed all of the enemy ships!")
        else:
            print("I'm sorry, Admiral. It's semmes that this battle is theirs.")
            
                
if __name__ == '__main__':
    while True:
        bot = BotPlayer()
        player = User()
            
        new_game = Game(player=player, bot=bot)
        new_game.start()
        
        while True:
            continue_ = False
            ans = input("Off to the next battle? [y/n] ")
            
            if ans == 'y':
                continue_ = True
                break
            
            elif ans == 'n':
                break
        
        if  not continue_:
            print("Thank you for playing my game! I hope it was fun for you, goodbye!")
            break

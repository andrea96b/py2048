import numpy
import random
import os
from pynput import keyboard
from enum import Enum
 
class Moves(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

class Game2048:
    def __init__(self, row : int = 4, col : int = 4) -> None:
        self.row = row
        self.col = col
        self.mat = numpy.zeros((row, col), dtype=numpy.uint32)
        self.available_space = []
        for i in range(0, row):
            for j in range(0, col):
                self.available_space.append([i ,j])
        #start with two 2 in random position
        self.place_random_num(2)
        self.place_random_num(2)
        self.points = 0
    
    def move_to_right(self) -> bool:
        ret = []
        for i in range(self.row):
            ret.append(self.move_row_to_right(i))
        return any(ret)

    def move_to_left(self) -> bool:
        ret = []
        for i in range(self.row):
            ret.append(self.move_row_to_left(i))
        return any(ret)

    def move_to_up(self) -> bool:
        ret = []
        for i in range(self.col):
            ret.append(self.move_col_to_up(i))
        return any(ret)
    
    def move_to_down(self) -> bool:
        ret = []
        for i in range(self.col):
            ret.append(self.move_col_to_down(i))
        return any(ret)

    def move_row_to_right(self, row) -> bool:
        ret = False
        for col in range(self.col-1, -1, -1):
            j=col
            if col > 0:
                if (self.mat[row][col] > 0) and (self.mat[row][col-1] > 0) and (self.mat[row][col] == self.mat[row][col-1]):
                    self.mat[row][col] += self.mat[row][col-1]
                    self.points += self.mat[row][col]
                    self.mat[row][col-1] = 0
                    ret = True
                elif (self.mat[row][col] > 0) and (self.mat[row][col-1] == 0):
                    k = col-1
                    while((k > 0) and (self.mat[row][k] == 0)):
                        k -= 1
                        if self.mat[row][col] == self.mat[row][k]:
                            self.mat[row][col] += self.mat[row][k]
                            self.points += self.mat[row][col]
                            self.mat[row][k] = 0
                            ret = True
            while((j+1 < self.row) and (self.mat[row][j] > 0) and (self.mat[row][j+1] == 0)):
                self.mat[row][j+1] = self.mat[row][j]
                self.mat[row][j] = 0                
                j += 1
                ret = True
        return ret
    
    def move_row_to_left(self, row) -> bool:
        ret = False
        for col in range(0, self.col):
            j=col
            if col < self.row-1:
                if (self.mat[row][col] > 0) and (self.mat[row][col+1] > 0) and (self.mat[row][col] == self.mat[row][col+1]):
                    self.mat[row][col] += self.mat[row][col+1]
                    self.points += self.mat[row][col]
                    self.mat[row][col+1] = 0
                    ret = True
                elif (self.mat[row][col] > 0) and (self.mat[row][col+1] == 0):
                    k = col+1
                    while((k < self.col-1) and (self.mat[row][k] == 0)):
                        k += 1
                        if self.mat[row][col] == self.mat[row][k]:
                            self.mat[row][col] += self.mat[row][k]
                            self.points += self.mat[row][col]
                            self.mat[row][k] = 0
                            ret = True   
            while((j-1 > -1) and (self.mat[row][j] > 0) and (self.mat[row][j-1] == 0)):
                self.mat[row][j-1] = self.mat[row][j]
                self.mat[row][j] = 0                
                j -= 1
                ret = True
        return ret

    def move_col_to_up(self, col) -> bool:
        ret = False
        for row in range(0, self.row):
            j=row
            if row < self.col-1:
                if (self.mat[row][col] > 0) and (self.mat[row+1][col] > 0) and (self.mat[row][col] == self.mat[row+1][col]):
                    self.mat[row][col] += self.mat[row+1][col]
                    self.points += self.mat[row][col]
                    self.mat[row+1][col] = 0
                    ret = True
                elif (self.mat[row][col] > 0) and (self.mat[row+1][col] == 0):
                    k = row+1
                    while((k < self.row-1) and (self.mat[k][col] == 0)):
                        k += 1
                        if self.mat[row][col] == self.mat[k][col]:
                            self.mat[row][col] += self.mat[k][col]
                            self.points += self.mat[row][col]
                            self.mat[k][col] = 0
                            ret = True  
            while((j-1 > -1) and (self.mat[j][col] > 0) and (self.mat[j-1][col] == 0)):
                self.mat[j-1][col] = self.mat[j][col]
                self.mat[j][col] = 0                
                j -= 1
                ret = True
        return ret
    
    def move_col_to_down(self, col) -> bool:
        ret = False
        for row in range(self.row-1, -1, -1):
            j=row
            if row > 0:
                if (self.mat[row][col] > 0) and (self.mat[row-1][col] > 0) and (self.mat[row][col] == self.mat[row-1][col]):
                    self.mat[row][col] += self.mat[row-1][col]
                    self.points += self.mat[row][col]
                    self.mat[row-1][col] = 0
                    ret = True
                elif (self.mat[row][col] > 0) and (self.mat[row-1][col] == 0):
                    k = row-1
                    while((k > 0) and (self.mat[k][col] == 0)):
                        k -= 1
                        if self.mat[row][col] == self.mat[k][col]:
                            self.mat[row][col] += self.mat[k][col]
                            self.points += self.mat[row][col]
                            self.mat[k][col] = 0
                            ret = True 
            while((j+1 < self.col) and (self.mat[j][col] > 0) and (self.mat[j+1][col] == 0)):
                self.mat[j+1][col] = self.mat[j][col]
                self.mat[j][col] = 0                
                j += 1
                ret = True
        return ret


    def is_move_available_for_cell(self, row: int, col: int) -> bool:
        up = [row -1, col]
        down = [row+1, col]
        left = [row, col-1]
        right = [row, col+1]

        if up[0] > -1:
            if self.mat[up[0]][up[1]] == self.mat[row][col]:
                return True
        
        if down[0] < self.row:
            if self.mat[down[0]][down[1]] == self.mat[row][col]:
                return True
        
        if left[1] > -1:
            if self.mat[left[0]][left[1]] == self.mat[row][col]:
                return True
        
        if right[1] < self.col:
            if self.mat[right[0]][right[1]] == self.mat[row][col]:
                return True
        return False

    def is_move_available(self) -> bool:
        if len(self.available_space) > 0:
            return True
        else:
            for i in range(0, self.row):
                for j in range(0, self.col):
                    if self.is_move_available_for_cell(i, j):
                        return True
        return False
    
    def is_available_space(self) -> bool:
        return len(self.available_space) > 0
    
    def build_available_space(self) -> None:
        self.available_space.clear()
        for i in range(0, self.row):
            for j in range(0, self.col):
                if self.mat[i][j] == 0:
                    self.available_space.append([i ,j])

    def place_random_num(self, num : int = 0) -> None:
        numbers = [2, 4]
        num_to_place = numbers[random.randint(0, 1)] if num == 0 else num
        place = self.available_space.pop(random.randrange(0, len(self.available_space)))
        self.mat[place[0], place[1]] = num_to_place

    def show(self) -> None:
        os.system('clear')
        self.print_mat()

    def print_mat(self) -> None:
        for i in range(self.row):
            s = ''
            for j in range(self.col):
                s += f'{self.mat[i][j]} '
            print(s)
        print(' ')
        print(f'Points: {self.points}')

    def execute_move(self, move: Moves) -> bool:
        ret = True
        something_moved = False
        if move == Moves.RIGHT:
            something_moved = self.move_to_right()
        elif move == Moves.LEFT:
            something_moved = self.move_to_left()
        elif move == Moves.UP:
            something_moved = self.move_to_up()
        elif move == Moves.DOWN:
            something_moved = self.move_to_down()
        else:
            pass

        self.build_available_space()
        if self.is_move_available():
            if self.is_available_space() and something_moved:
                self.place_random_num()
        else:
            ret = False
        return ret

def on_key_release(key):
    global exit_game
    global game
    move = None
    if key == keyboard.Key.esc:
        exit_game = True
    elif key == keyboard.Key.right:
        move = Moves.RIGHT
    elif key == keyboard.Key.left:
        move = Moves.LEFT
    elif key == keyboard.Key.up:
        move = Moves.UP
    elif key == keyboard.Key.down:
        move = Moves.DOWN
    else:
        pass

    if move:
        exit_game = not game.execute_move(move)
    return False    

if __name__ == '__main__':
    game = Game2048()
    exit_game = False
    while not exit_game:
        # Collect events until released
        game.show()
        with keyboard.Listener(
                on_press=None,
                on_release=on_key_release) as listener:
            listener.join()
        game.show()

        

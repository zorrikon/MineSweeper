"""
Command line implementation of Minesweeper.
"""

import argparse
import itertools
import random

class MinesweeperGame:
    MINE = "*"
    HIDDEN = "H"
    EMPTY = "."
    FLAG = "F"

    def __init__(self, num_rows=10, num_cols=10, num_mines=10):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.num_mines = num_mines
        self.is_visible = set()
        self.flags = set()
        self.mine_hit = False
        self.__initialize_board()

    def print_board(self):
        first_row = "   " + "  ".join(str(c) for c in range(1, min(self.num_cols + 1, 10)))
        if self.num_cols >= 9:
            first_row += " " + " ".join(str(c) for c in range(10, self.num_cols + 1))
        rows = [first_row]
        for r in range(self.num_rows):
            start = str(r + 1) + " " * (3 - len(str(r + 1)))
            rows.append(start + "  ".join(self.__get_printable_char(r, c) for c in range(self.num_cols)))
        print("\n".join(rows))

    def do_move(self, row, col):
        if not self.is_visible:
            # First move of game, keep initializing board until row, col is an empty spot.
            while self.board[row][col] != self.EMPTY:
                self.__initialize_board()
        if self.board[row][col] == self.MINE:
            self.mine_hit = True
        # DFS on (row, col)'s neighbors to expand empty spots
        to_visit = [(row, col)]
        while to_visit:
            r, c = to_visit.pop()
            self.is_visible.add((r, c))
            if self.board[r][c] != self.EMPTY:
                continue
            for nr, nc in self.__neighbors(r, c):
                if (nr, nc) not in self.is_visible:
                    to_visit.append((nr, nc))
    
    def add_flag(self, row, col):
        self.flags.add((row, col))

    def is_done(self):
        return self.mine_hit or self.is_won()

    def is_won(self):
        return (len(self.is_visible) >= self.num_rows * self.num_cols - self.num_mines 
                and not self.mine_hit)

    def __get_printable_char(self, row, col):
        if (row, col) in self.is_visible:
            return self.board[row][col]
        if (row, col) in self.flags:
            return self.FLAG
        return self.HIDDEN

    def __initialize_board(self):
        self.board = self.__create_board(self.__create_mines())

    def __create_mines(self):
        mines = [i < self.num_mines for i in range(self.num_rows * self.num_cols)]
        random.shuffle(mines)
        return [[mines[r * self.num_cols + c] for c in range(self.num_cols)] for r in range(self.num_rows)]

    def __create_board(self, mines):
        board = [["" for _ in range(self.num_cols)] for _ in range(self.num_rows)]
        for r, row in enumerate(mines):
            for c, is_mine in enumerate(row):
                if is_mine:
                    board[r][c] = self.MINE
                else:
                    num_adj_mines = sum(mines[nr][nc] for nr, nc in self.__neighbors(r, c))
                    if num_adj_mines > 0:
                        board[r][c] = str(num_adj_mines)
                    else:
                        board[r][c] = self.EMPTY
        return board

    # Generator for all valid (r, c)'s adjacent to (row, col), including (row, col).
    def __neighbors(self, row, col):
        for dr, dc in itertools.product([-1, 0, 1], [-1, 0, 1]):
            new_row = dr + row
            new_col = dc + col
            if 0 <= new_row < self.num_rows and 0 <= new_col < self.num_cols:
                yield (new_row, new_col)
     

def main(num_rows, num_cols, num_mines):
    game = MinesweeperGame(num_rows, num_cols, num_mines)
    game.print_board()

    while not game.is_done():
        user_input = input("Enter 'row column' or '\"flag\" row column': ")
        user_input = user_input.split(" ")
        row = int(user_input[-2]) - 1
        col = int(user_input[-1]) - 1
        if len(user_input) == 2:
            game.do_move(row, col)
        else:
            game.add_flag(row, col)
        game.print_board()

    if game.is_won():
        print("Congratulations, you won!")
    else:
        print("Sorry, better luck next time :(.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("num_rows", type=int, default=10,
                        help="The number of rows in the board.")
    parser.add_argument("num_cols", type=int, default=10,
                        help="The number of columns in the board.")
    parser.add_argument("num_mines", type=int, default=10,
                        help="The number of mines in the board.")
    args = parser.parse_args()
    main(args.num_rows, args.num_cols, args.num_mines)
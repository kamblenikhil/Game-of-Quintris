# Simple quintris program! v0.2
# Prof. David Crandall, Sept 2021
#
# Author - Nikhil Kamble

from typing import final
from numpy.lib.utils import source
from AnimatedQuintris import *
from SimpleQuintris import *
from kbinput import *
import time, sys

import random
import numpy as np
import sys, time, random, threading #, thread

#david's code from QuintrisGame.py and SimpleQuintris.py starts here

class my_EndOfGame(Exception):
  def __init__(self,s) :
    self.str = s
  
  def __str__(self):
    return self.str

class my_QuintrisGame:

#   PIECES = [ [ " x ", "xxx", " x "], [ "xxxxx" ], [ "xxxx", "   x" ], [ "xxxx", "  x " ], [ "xxx", "x x"], [ "xxx ", "  xx" ] ]
  BOARD_HEIGHT = 25
  BOARD_WIDTH = 15

  # initialize empty board. State is a pair with the board in first element and score in the second.
  def __init__(self):
    # self.state = ([ " " * my_QuintrisGame.BOARD_WIDTH ] * my_QuintrisGame.BOARD_HEIGHT, 0)
    board = quintris.get_board()
    self.state = (board,0)
    self.piece, self.row, self.col = quintris.get_piece()
    # self.piece_dist = [ [i,] * random.randint(0, 10) for i in range(0, len(QuintrisGame.PIECES) ) ]
    # self.piece_dist = [ i for m in self.piece_dist for i in m ]
    # print(self.piece_dist)
    # self.next_piece = None
    # self.new_piece()
    
  # rotate a given piece by a given angle
  @staticmethod
  def rotate_piece(piece, rotation):
    rotated_90 = [ "".join([ str[i] for str in piece[::-1] ]) for i in range(0, len(piece[0])) ]
    return { 0: piece, 90: rotated_90, 180: [ str[::-1] for str in piece[::-1] ], 270: [ str[::-1] for str in rotated_90[::-1] ] }[rotation]

  @staticmethod
  def hflip_piece(piece):
    return [ str[::-1] for str in piece ]

  @staticmethod
  def vflip_piece(piece):
    return [ str for str in piece[::-1] ]
  
#   def random_piece(self):
#     return QuintrisGame.rotate_piece(QuintrisGame.PIECES[ random.choice(self.piece_dist) ], random.randrange(0, 360, 90) ) 

  # print out current state to the screen
  @staticmethod
  def print_state(board, score):
    # sboard = quintris.get_board()
    # print("\n dusra board - \n", *board, sep="\n")
    print("\n" * 3 + "Dusra Board \n" + "|\n".join(board) + "|\n" + "-" * my_QuintrisGame.BOARD_WIDTH)

  # return true if placing a piece at the given row and column would overwrite an existing piece
  @staticmethod
  def check_collision(board, score, piece, row, col):
      return col+len(piece[0]) > my_QuintrisGame.BOARD_WIDTH or row+len(piece) > my_QuintrisGame.BOARD_HEIGHT \
          or any( [ any( [ (c != " " and board[i_r+row][col+i_c] != " ") for (i_c, c) in enumerate(r) ] ) for (i_r, r) in enumerate(piece) ] )
    
  # take "union" of two strings, e.g. compare each character of two strings and return non-space one if it exists
  @staticmethod
  def combine(str1, str2):
      return "".join([ c if c != " " else str2[i] for (i, c) in enumerate(str1) ] )

  # place a piece on the board at the given row and column, and returns new (board, score) pair
  @staticmethod
  def place_piece(board, score, piece, row, col):
    return (board[0:row] + \
              [ (board[i+row][0:col] + my_QuintrisGame.combine(r, board[i+row][col:col+len(r)]) + board[i+row][col+len(r):] ) for (i, r) in enumerate(piece) ] + \
              board[row+len(piece):], score)

  # remove any "full" rows from board, and increase score accordingly
  @staticmethod
  def remove_complete_lines(board, score):
    complete = [ i for (i, s) in enumerate(board) if s.count(' ') == 0 ]
    return ( [(" " * my_QuintrisGame.BOARD_WIDTH),] * len(complete) + [ s for s in board if s.count(' ') > 0 ], score + len(complete) )

  # move piece left or right, if possible
  def move(self, col_offset, new_piece):
    new_col = max(0, min(my_QuintrisGame.BOARD_WIDTH - len(self.piece[0]), self.col + col_offset))
    # print("C-Move", new_col)
    (self.piece, self.col) = (new_piece, new_col) if not my_QuintrisGame.check_collision(*self.state, new_piece, self.row, new_col) else (self.piece, self.col)

  def finish(self):
      self.state = my_QuintrisGame.remove_complete_lines( *my_QuintrisGame.place_piece(*self.state, self.piece, self.row, self.col) )
    #   self.new_piece()

#   def new_piece(self, piece, row, col):
#       # generate a new random piece to fall at a random position
#       self.piece = piece
#     #   self.piece = self.next_piece if self.next_piece != None else self.random_piece()
#     #   self.next_piece = self.random_piece()
#       self.row = row
#       self.col = col

      # check if this immediately generates a collision, which means we lost!
    #   if(my_QuintrisGame.check_collision(*self.state, self.piece, self.row, self.col)):
    #     raise my_EndOfGame("ssssa Game over! Final score: " + str( self.state[1]))
        # print("something")

  def print_board(self, clear_screen, source_block, sb_row, sb_col):
    if clear_screen: print("\n"*80)
    # print("Next piece:\n" + "\n".join(self.next_piece))
    print("print board (row + col)", self.row, self.col)
    my_QuintrisGame.print_state(*my_QuintrisGame.place_piece(*self.state, source_block, self.row, self.col))

  ######
  # These are the "public methods" that your code might want to call!
 
  # move piece left, if possible, else do nothing
  def left(self):
    self.move(-1, self.piece)

  # move piece right, if possible, else do nothing
  def right(self):
    self.move(1, self.piece)

  # rotate piece one position if possible, else do nothing
  def rotate(self):
    self.move(0, my_QuintrisGame.rotate_piece(self.piece, 90))

  def hflip(self):
    self.move(0, my_QuintrisGame.hflip_piece(self.piece))

  def vflip(self):
    self.move(0, my_QuintrisGame.vflip_piece(self.piece))

  # make piece go all the way down until it hits a collision
  def down(self):
    while not my_QuintrisGame.check_collision(*self.state, self.piece, self.row+1, self.col):
      self.row += 1
    return self.row
    # self.finish()

  # return current state of board
  def get_board(self):
    return self.state[0]

  # return current score
  def get_score(self):
    return self.score

  # return currently-falling piece, and its current row and column on the board
  def get_piece(self):
    return (self.piece, self.row, self.col)

#   # return next piece 
#   def get_next_piece(self):
#     return self.next_piece

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

class my_SimpleQuintris(my_QuintrisGame):
  def __init__(self):
      my_QuintrisGame.__init__(self)

  arara = {}

  def start_game(self, player2, source_block, sb_row, sb_col, board, flag):
    COMMANDS = { "b": self.left, "n": self.rotate, "m": self.right, "h": self.hflip }
    # self.print_board(False, source_block, sb_row, sb_col, board)
    # row_width = []
    nos = 0
    # arara = []
    # flag = 0
    all_row_sum = 0

    # for i in range(0,15):
    moves = player2.give_me_moves(self, flag)
    row_width = []

    for c in moves:
        if c in COMMANDS:
            COMMANDS[c]()
        else:  
            raise "bad command!"
    r = self.down()

    # print("ROW", r)

    # self.print_board(False, source_block, sb_row, sb_col)
    r = r - len(source_block)

    # print("piece height - ", len(source_block))

    # row_width = [len(i) for i in board]
    for i in board:
        for x in i:
            if(x.isalpha()):
                nos = nos + 1
        row_width.append(nos)
        nos = 0
    #column height flag
    flag += 1
    #sum of the row where block fell
    all_row_sum = row_width[r]
    # print("ars", all_row_sum)
    # self.arara.append(all_row_sum)
    self.arara[moves] = all_row_sum
            
    # print("E - ", self.arara)

    fin_max = max(self.arara, key=self.arara.get)
    # print("Maximum value:",fin_max)

    if(flag == 15):
      # print("besttttt")
      moves = fin_max
    else:
      moves = ""

    return moves
    # return 0, moves

#david's code from QuintrisGame.py and SimpleQuintris.py ends here

#==============================================================================================================

class HumanPlayer:
    def get_moves(self, quintris):
        print("Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\n  h for horizontal flip\nThen press enter. E.g.: bbbnn\n")
        moves = input()
        return moves

    def control_game(self, quintris):
        while 1:
            c = get_char_keyboard()
            commands =  { "b": quintris.left, "h": quintris.hflip, "n": quintris.rotate, "m": quintris.right, " ": quintris.down }
            commands[c]()

class ComputerPlayer:
    # This function should generate a series of commands to move the piece into the "optimal"
    # position. The commands are a string of letters, where b and m represent left and right, respectively,
    # and n rotates. quintris is an object that lets you inspect the board, e.g.:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #
    # def get_moves(self, quintris):
    #     # super simple current algorithm: just randomly move left, right, and rotate a few times
    #     return random.choice("mnbh") * random.randint(1, 10)

    #6 blocks are used in the game with all the possible moves in this
    block_1 = [ [" x ", "xxx", " x "] ]
    block_2 = [ ["xxxxx"], ["x", "x", "x", "x", "x"] ]
    block_3 = [ ["xxxx", "   x"], ["xxxx", "x   "], ["x   ", "xxxx"], ["   x", "xxxx"], [" x", " x", " x", "xx"], ["x ", "x ", "x ", "xx"], ["xx", " x", " x", " x"], ["xx", "x ", "x ", "x "] ]
    block_4 = [ ["xxxx", "  x "], ["xxxx", " x  "], ["  x ", "xxxx"], [" x  ", "xxxx"], ["x ", "x ", "xx", "x "], [" x", " x", "xx", " x"], ["x ", "xx", "x ", "x "], ["x ", "xx", "x ", "x "] ]
    block_5 = [ ["xxx ", "  xx"], [" xxx", "xx  "], ["  xx", "xxx "], ["xx  ", " xxx"], [" x", " x", "xx", "x "], ["x ", "x ", "xx", " x"], [" x", "xx", "x ", "x "], ["x ", "xx", " x", " x"] ]
    block_6 = [ ["xxx", "x x"], ["x x", "xxx"], ["xx", " x", "xx"], ["xx", "x ", "xx"] ]

    #this will add all the possible combinations of rotation and hflip
    all_moves = ['n', 'h', 'nn', 'nh', 'nnn', 'nnh', 'nnnh']
  
    def give_me_moves(self, q, flag):

        # print("flag - ", flag)
        board = quintris.get_board()
        block, b_row, b_col = quintris.get_piece()
        test_m = ""
        left = "b"
        right = "m"
        # print(board)
        
        column_heights = [ min([ r for r in range(len(board)-1, 0, -1) if board[r][c] == "x"  ] + [25,] ) for c in range(0, len(board[0]) ) ]
        # print("col - ", column_heights)

        run_col = np.argmax(column_heights)
        # run_col = flag

        # print("max - ", run_col)
        
        # if(run_col!=0 or run_col!=15):
        #     run_col -= 1

        # print("r-col",run_col)
        # print("b-col",b_col)

        nos = abs(run_col-b_col)
        # print(nos)

        if(b_col > run_col):
            moves = test_m.ljust(nos+len(test_m),left)
        if(b_col < run_col):
            moves = test_m.ljust(nos+len(test_m),right)
        if(b_col == run_col):
            moves = ""

        # print("moves - ", str(moves))
        
        return str(moves)

    def give_best_move(self, source_block, sb_row, sb_col, list_block):
        
        board = quintris.get_board()
        # moves = []
        player2 = ComputerPlayer()
        q = my_SimpleQuintris()
        rand_block = random.choice(list_block)

        for i in range(0, 15):
          # moves = q.start_game(player2, source_block, sb_row, sb_col, board, i)
          moves1 = q.start_game(player2, source_block, sb_row, sb_col, board, i)
          # moves.append(xyz)
          # print("best moves", moves)

        # print("chai break")

        # for i in range(0, 15):
        #   # moves = q.start_game(player2, source_block, sb_row, sb_col, board, i)
        #   moves2 = q.start_game(player2, rand_block, sb_row, sb_col, board, i)
        #   # moves.append(xyz)
        #   # print("best moves", moves)

        # if(moves1 > moves2):
        #   final_block = source_block
        #   final_move = moves1
        # else:
        #   final_block = rand_block
        #   final_move = moves2

        # return final_block, 0, 0, final_move
        return source_block, 0, 0, moves1


    def succ_func(self, source_block, sb_row, sb_col, list_block):

        # print("S - ", source_block)
        # print("D - ", destination_block)
        # print(self.all_moves)
        temp_block = source_block
        # lr_stri = ""
        
        # destination_block = random.choice(list_block)
        destination_block, db_row, db_col, moves = self.give_best_move(temp_block, sb_row, sb_col, list_block)

        if(source_block == destination_block):
            return "" + moves

        for z in self.all_moves:
            
            if(source_block == destination_block):
                # print("stri", stri)
                # return stri + lr_stri
                return stri + moves
            temp_block = []
            stri = ""
            
            for charac in range(len(z)):
                
                if z[charac] == "n":
                    stri += "n"
                    source_block = QuintrisGame.rotate_piece(source_block, 90)
                    continue
                if z[charac] == "h":
                    stri += "h"
                    # print("hflip")
                    source_block = QuintrisGame.hflip_piece(source_block)

        return ""

    def block_list(self, curr_block, cb_row, cb_col):
        # print("mich toh - ", curr_block)
        # curr_block = ["xxxx", "   x"]
        the_block = []

        # to check the current_block in list_of_blocks (ie. 6 list of blocks) 
        while len(the_block) == 0:
            # print("while madhe ahey")

            #if the current_block lies in block1 list
            if(curr_block in self.block_1):
                the_block = self.block_1.copy()

            #if the current_block lies in block2 list
            if(curr_block in self.block_2):
                the_block = self.block_2.copy()
            
            #if the current_block lies in block3 list
            if(curr_block in self.block_3):
                the_block = self.block_3.copy()
            
            #if the current_block lies in block4 list
            if(curr_block in self.block_4):
                the_block = self.block_4.copy()
            
            #if the current_block lies in block5 list
            if(curr_block in self.block_5):
                the_block = self.block_5.copy()
            
            #if the current_block lies in block6 list
            if(curr_block in self.block_6):
                the_block = self.block_6.copy()
            
        # piece, p_row, p_col, way = self.succ_func(curr_block, cb_row, cb_col, the_block)
        way = self.succ_func(curr_block, cb_row, cb_col, the_block)
        # print("way - ", way)

        return way

    def get_moves(self, quintris):
        # super simple current algorithm: just randomly move left, right, and rotate a few times
        
        moves = ""
        block, b_row, b_col = quintris.get_piece()
        # piece, p_row, p_col, moves = self.move_move(block, b_row, b_col)
        moves += self.block_list(block, b_row, b_col)

        # print(piece, p_row, p_col, moves)
        # del QuintrisGame.piece

        # print(QuintrisGame.piece)

        # quintris.place_piece(board, 0, piece, b_row, b_col)

        return moves
#==========================================================================================================
    # This is the version that's used by the animted version. This is really similar to get_moves,
    # except that it runs as a separate thread and you should access various methods and data in
    # the "quintris" object to control the movement. In particular:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #
    def control_game(self, quintris):
        # another super simple algorithm: just move piece to the least-full column
        while(1):
            time.sleep(0.1)

            # board = quintris.get_board()
            # # print("bababa", board)
            # # time.sleep(100.0)
            # column_heights = [ min([ r for r in range(len(board)-1, 0, -1) if board[r][c] == "x"  ] + [100,] ) for c in range(0, len(board[0]) ) ]
            # index = column_heights.index(max(column_heights))

            # print(column_heights)
            # print(index)

            # if(index < quintris.col):
            #     quintris.left()
            # elif(index > quintris.col):
            #     quintris.right()
            # else:
            #     quintris.down()

            moves = ""
            block, b_row, b_col = quintris.get_piece()
            moves += self.block_list(block, b_row, b_col)

            # COMMANDS = { "b": self.left, "n": self.rotate, "m": self.right, "h": self.hflip }
            for i in moves:
              if(i == "b"):
                quintris.left()
              elif(i == "n"):
                quintris.rotate()
              elif(i == "m"):
                quintris.right()
              elif(i == "h"):
                quintris.hflip()
              
              quintris.down()
            # quintris.down()
              

###################
#### main program

(player_opt, interface_opt) = sys.argv[1:3]

try:
    if player_opt == "human":
        player = HumanPlayer()
    elif player_opt == "computer":
        player = ComputerPlayer()
    else:
        print("unknown player!")

    if interface_opt == "simple":
        quintris = SimpleQuintris()
    elif interface_opt == "animated":
        quintris = AnimatedQuintris()
    else:
        print("unknown interface!")

    quintris.start_game(player)

except EndOfGame as s:
    print("\n\n\n", s)




################################################################################
#                                                                              #
# David Fuller                                                                 #
#                                                                              #
# Sudoku class: Sudoku game class                                              #
#                                                                              #
# Created on 2017-4-29                                                         #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
#                              IMPORT STATEMENTS                               #
#                                                                              #
################################################################################

from   .processing import Processing   # Processing style package
from   .Constants  import *            # Constants file
from   .Block      import Block        # Block object
import pygame                          # For GUI
import random                          # For shuffling top row

################################################################################
#                                                                              #
#                                SUDOKU CLASS                                  #
#                                                                              #
################################################################################

class Sudoku(object):
    # Typehinting
    screenHint = "PyGame screen"

    ############################################################################
    #                                                                          #
    #                               CONSTRUCTOR                                #
    #                                                                          #
    ############################################################################
    
    def __init__(self, screen : screenHint) -> None:
        # Canvas / screen
        self.screen = screen

        # Processing object
        self.p5 = Processing(self.screen)

        # Blocks array
        self.blocks = []

        # Create blank board
        self.grid = [ZERO] * (SET_LENGTH * SET_LENGTH)
        self.createBoard()

    ############################################################################
    #                                                                          #
    #                                 METHODS                                  #
    #                                                                          #
    ############################################################################

    # Method creates grid of blocks
    def createBoard(self) -> None:
        # Grid of blocks
        x = ORIGIN[X]
        y = ORIGIN[Y]
        width = BLOCK_SIZE
        height = BLOCK_SIZE
        for i in range(SET_LENGTH):
            for j in range(SET_LENGTH):
                block = Block(self.screen, x, y, width, height)
                self.blocks.append(block)
                x = x + width
            x = ORIGIN[X]
            y = y + height

    # Method checks section for validity
    def checkGroup(self, group : list, index : int, num : int) -> bool:
        for i in range(SET_LENGTH):
            if int(num) == self.grid[group[i]] and \
               index != group[i]:
                return False
        return True

    # Method decides if move is valid or not
    def isValid(self, index : int, num : int) -> bool:
        # Off board => invalid
        if index < ZERO or index > 80:
            return False

        # Number greater than 9 => invalid
        if num > SET_LENGTH:
            return False

        # Assume valid
        valid = True

        # Check rows        
        tempindex = ZERO
        while index < ROW_INDEXES[tempindex]:
            tempindex = tempindex + ONE
        startingindex = ROW_INDEXES[tempindex]
        for i in range(SET_LENGTH):
            if int(num) == self.grid[i + startingindex] and \
               index != i + startingindex:
                valid = False
                break

        # Check cols
        if valid:
            startingindex = index % SET_LENGTH
            for i in range(SET_LENGTH):
                testindex = (i * SET_LENGTH) + startingindex
                if int(num) == self.grid[testindex] and \
                   index != testindex:
                    valid = False
                    break

        # Check groups
        if valid:
            if index in TOP_LEFT:
                valid = self.checkGroup(TOP_LEFT, index, num)
            elif index in TOP_CENTER:
                valid = self.checkGroup(TOP_CENTER, index, num)
            elif index in TOP_RIGHT:
                valid = self.checkGroup(TOP_RIGHT, index, num)
            elif index in MIDDLE_LEFT:
                valid = self.checkGroup(MIDDLE_LEFT, index, num)
            elif index in MIDDLE_CENTER:
                valid = self.checkGroup(MIDDLE_CENTER, index, num)
            elif index in MIDDLE_RIGHT:
                valid = self.checkGroup(MIDDLE_RIGHT, index, num)
            elif index in BOTTOM_LEFT:
                valid = self.checkGroup(BOTTOM_LEFT, index, num)
            elif index in BOTTOM_CENTER:
                valid = self.checkGroup(BOTTOM_CENTER, index, num)
            elif index in BOTTOM_RIGHT:
                valid = self.checkGroup(BOTTOM_RIGHT, index, num)

        # Return valid
        return valid

    # Method decides whether game has been solved or not
    def isSolved(self) -> bool:
        if ZERO in self.grid:
            return False
        return True

    # Method creates a new Sudoku game
    def newGame(self) -> None:
        # Top row
        toprow = []
        for i in range(SET_LENGTH):
            num = i + ONE
            toprow.append(str(num))
        random.shuffle(toprow)
        for i in range(SET_LENGTH):
            self.grid[i] = (int(toprow[i]))

        # Index 9 on
        index = SET_LENGTH
        while not self.isSolved():
            self.grid[index] = self.grid[index] + ONE
            while not self.isValid(index, self.grid[index]):
                self.grid[index] = self.grid[index] + ONE
                if self.grid[index] > SET_LENGTH:
                    self.grid[index] = ZERO
                    index = index - ONE
                    self.grid[index] = self.grid[index] + ONE
            index = index + ONE


        # Update blocks
        for i in range(SET_LENGTH * SET_LENGTH):
            self.blocks[i].update(str(self.grid[i]))

    # Method updates text of a block
    def update(self, index : int, text : str) -> None:
        self.blocks[index].update(text)

    # Method shows Sudoku game board
    def show(self) -> None:
        # Grid of blocks
        for block in self.blocks:
            block.show()

        # Bolder lines where appropriate
        self.p5.strokeWeight(TWO)
        x = ORIGIN[X]
        y = ORIGIN[Y]
        width = BLOCK_SIZE
        height = BLOCK_SIZE
        weight = self.p5.strokeweight / TWO
        maxsize = width * SET_LENGTH + weight * SET_LENGTH
        onethird = width * (SET_LENGTH * (ONE / THREE)) + x
        twothird = width * (SET_LENGTH * (TWO / THREE)) + x
        self.p5.line(x, y, maxsize, y)               # Top
        self.p5.line(x, y, x, maxsize)               # Left
        self.p5.line(x, maxsize, maxsize, maxsize)   # Bottom
        self.p5.line(maxsize, y, maxsize, maxsize)   # Right

        self.p5.line(x, onethird, maxsize, onethird)   # Horizontal 1
        self.p5.line(x, twothird, maxsize, twothird)   # Horizontal 1

        self.p5.line(onethird, y, onethird, maxsize)   # Vertical 1
        self.p5.line(twothird, y, twothird, maxsize)   # Vertical 1

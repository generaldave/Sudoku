################################################################################
#                                                                              #
# David Fuller                                                                 #
#                                                                              #
# Block class: Sudoku block class                                              #
#                                                                              #
# Created on 2017-4-29                                                         #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
#                              IMPORT STATEMENTS                               #
#                                                                              #
################################################################################

from   .Constants  import *            # Constants file
from   .processing import Processing   # Processing style package
import pygame                          # For GUI

################################################################################
#                                                                              #
#                                BLOCK CLASS                                   #
#                                                                              #
################################################################################

class Block(object):
    # Typehinting
    screenHint = "PyGame screen"

    ############################################################################
    #                                                                          #
    #                               CONSTRUCTOR                                #
    #                                                                          #
    ############################################################################
    
    def __init__(self, screen : screenHint, x : int, y : int, \
                 width : int, height : int) -> None:
        # Canvas / screen
        self.screen = screen

        # Processing object
        self.p5 = Processing(self.screen)

        # Block attributes
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.maxX = x + width
        self.maxY = y + height

        # Block sides
        self.left = (x, y, x, self.maxY)
        self.top = (x, y, self.maxX, y)
        self.right = (self.maxX, y, self.maxX, self.maxY)
        self.bottom = (x, self.maxY, self.maxX, self.maxY)

        # Block text
        pygame.font.init()
        self.font = pygame.font.SysFont("None", 42)
        self.text = "0"
        self.digit = self.font.render(self.text, False, BLACK)
        self.textX = self.x + self.width / TWO - \
                     self.digit.get_rect().width / TWO
        self.textY = self.y + self.height / TWO - \
                     self.digit.get_rect().height / TWO

    ############################################################################
    #                                                                          #
    #                                 METHODS                                  #
    #                                                                          #
    ############################################################################

    # Method updates text of block
    def update(self, text : str) -> None:
        self.text = text
        self.digit = self.font.render(self.text, False, BLACK)
        self.textX = self.x + self.width / TWO - self.digit.get_rect().width / TWO
        self.textY = self.y + self.height / TWO - self.digit.get_rect().height / TWO

    # Method shows block
    def show(self) -> None:
        self.p5.fill(WHITE)
        self.p5.stroke(BLACK)
        self.p5.strokeWeight(1)
        
        self.p5.rect(self.x, self.y, self.width, self.height)

        if self.text != "0":
            self.screen.blit(self.digit, (self.textX, self.textY))

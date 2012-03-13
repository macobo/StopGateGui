# -*- coding: cp1257 -*-
import pygame
from pygame.locals import *

class HumanPlayer(object):
    """A Human player for the StopGate Game."""
    lspos = None
    type = 'Human'
    def __init__(self, turn, board, name = None):
        if name == None:
            self.name = "Mängija %d" % (turn+1)
        else:
            self.name = name
        self.turn = turn
        self.board = board
        self.boardsize = self.board.boardsize
        self.halfsquare = self.board.squaresize/2

    def add_game(self, game):
        self.game = game
        
    def rename(self, newname):
        self.name = newname


    def get_input(self, message = None):
        """Processes all the clicks, reposting everything else besides
            legal moves.
            Returns square clicked on or none"""
        pygame.time.wait(30)
        clicks = []
        for event in pygame.event.get():      
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                spos = self.board.get_square(pos, self.turn)
                if self.game.legalmove(spos):
                    self.board.undraw_outline()
                    return spos
                if self.board.menubutton.hovering(pos):
                    clicks.append(event)
##                    pygame.event.post(event)
            else:
                clicks.append(event)
        for click in clicks: #repost clicks to eliminate lag/lost clicks    
            pygame.event.post(click)

            
        return None
    def output(self, message): pass
    def kill(self): pass
    def start(self): pass
    def __str__(self):
        return self.name

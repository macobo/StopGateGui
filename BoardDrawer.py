# -*- coding: cp1257 -*-
import pygame
from stopgatelocals import *
from ScrollingTextArea import ScrollingTextArea


class Board(object):
    orig_squaresize = 61
    orig_boardsize = orig_squaresize*12
    orig_buttonsize = 120
    last_outline = [(1,1),(1,1)] # for outline drawing
##    d = [11,0]
    
    def __init__(self, windowsize):
        self.windowsize = windowsize
        pygame.init()
        self.screen = pygame.display.set_mode(windowsize)
        pygame.display.set_caption('::StopGate::')
        self.set_size(windowsize)
        
    def set_size(self, new_windowsize = None):
        """ Resizes the default arguments, such as the board, buttons etc.
            zeropos is the position of the board on the game. """
        if new_windowsize != None:
            self.windowsize = new_windowsize
        import os
        self.fontsize = int(self.windowsize[1]*0.029)
        self.font = pygame.font.Font(os.path.join('Fonts','def.ttf'),
                                     self.fontsize)
        self.boardsize = self.windowsize[1]-self.fontsize
        self.zeropos = (self.fontsize, self.fontsize)
        
        ratio = 1.0*self.orig_boardsize/self.boardsize
        self.buttonsize = int(round(self.orig_buttonsize/ratio,0))
        self.halfsize = self.buttonsize / 2
        self.squaresize = int(self.orig_squaresize/ratio)
        self.loaded_buttons = False
        
    def load_buttons(self):
        """Reads the image files for tiles and buttons and resizes them.
            Also creates the menu button"""
        orig_squares = [pygame.image.load("Pics/WhiteSquare.png").convert_alpha(),
                    pygame.image.load("Pics/BlackSquare.png").convert_alpha()]
        orig_buttons = [pygame.image.load("Pics/white.png").convert_alpha(),
                        pygame.image.load("Pics/black.png").convert_alpha()]
        orig_outlines = [pygame.image.load("Pics/vertoutline.png").convert_alpha(),
                         pygame.image.load("Pics/horoutline.png").convert_alpha()]
##        orig_border = pygame.image.load("Pics/borderh.png").convert_alpha()
        self.squares = [pygame.transform.scale(orig_squares[x],(int(round(self.squaresize,0)), int(round(self.squaresize,0))))
                        for x in xrange(2)]
        self.buttons = [pygame.transform.scale(orig_buttons[0],(self.halfsize,self.buttonsize)),
                        pygame.transform.scale(orig_buttons[1],(self.buttonsize,self.halfsize))]
        self.outlines = [pygame.transform.scale(orig_outlines[0],(self.halfsize,self.buttonsize)),
                         pygame.transform.scale(orig_outlines[1],(self.buttonsize,self.halfsize))]
##        self.border = pygame.transform.scale(orig_border,(self.halfsize,self.buttonsize))
        from Hoverable import Hoverable
        default = self.font.render('Menüü', True, colors['white'])
        self.menuwidth = default.get_width()
        hovering = self.font.render('Menüü', True, colors['red'])
        x, y = self.windowsize
        x -= default.get_width()
        y -= default.get_height()
        self.menubutton = Hoverable((x, y), 4, default, hovering)
        self.loaded_buttons = True

        
    def draw_board(self):
        """Draws initial board. If buttons are not yet loaded, loads them"""
        if not self.loaded_buttons:
            self.load_buttons()
        self.screen.fill(colors['black'])
        #Draws boxes
        textx = (self.boardsize+self.fontsize)*1.0084
        h = self.font.size('ABCDEFGHIJKLMNOPQRSTU')[1]
        totlines = self.windowsize[1]/h
        rendered = self.font.render('Võimalikke käike:', True, colors['red'])
        self.screen.blit(rendered, (textx,5))
        self.scorebox = ScrollingTextArea(self.font, (textx,5+h),
                        (self.windowsize[0],5+h*3), color = colors['white'],
                        background = colors['black'])
        rendered = self.font.render('Mängu käik:', True, colors['red']) 
        self.screen.blit(rendered, (textx,5+h*3)) #4th line
        self.recordbox = ScrollingTextArea(self.font, (textx,5+h*4),
                        (self.windowsize[0],10+h*(totlines-6)), color = colors['white'],
                        background = colors['black'])
        rendered = self.font.render('Statistika:', True, colors['red']) 
        self.screen.blit(rendered, (textx,5+h*(totlines-6))) #4th line
        self.statisticsbox = ScrollingTextArea(self.font, (textx,5+h*(totlines-5)),
                        (self.windowsize[0],5+h*totlines), color = colors['white'],
                        background = colors['black'])
        for i in xrange(12):
            #labels
            rendered = self.font.render(str(i), True, colors['white'])
            w, h = rendered.get_size()
            x1, y1 = self.get_pixels((0,i))
            x2, y2 = self.get_pixels((i,0))
            self._draw(rendered, (x1-w,y1+(self.squaresize-h)/2))
            self._draw(rendered, (x2+(self.squaresize-w)/2,y2-h))
            for j in xrange(12):
                #tiles
                self.draw_square((i,j))

    def reset_boxes(self):
        """Resets the scoreboxes. Used at newgame"""
        self.scorebox.reset()
        self.recordbox.reset()
        self.statisticsbox.reset()
        
    def draw_square(self, square, surface = None):
        """Draws a board tile on the square provided
            if a surface is provided, draws on that instead of
            the screen.
            """
        i = (sum(square))%2
        self._draw(self.squares[i], self.get_pixels(square), surface)
        
    def draw_button(self, square, turn, surface = None):
        """Draws a button at the square provided.
            if turn == 0, draws a vertical button, else
            horizontal.
            if a surface is provided, draws on that instead of
            the screen.
            """
        dx = turn == 0
        self.undraw_outline()
        x, y = self.get_pixels(square)
        self._draw(self.buttons[turn], (x-dx, y), surface)
        self.last_outline = [(-2,-2),(-2,-2)]
    def undraw_outline(self):
        """Removes the last outline from the board"""
        self.draw_square(self.last_outline[0])
        self.draw_square(self.last_outline[1])
        self.last_outline = [(-2,-2),(-2,-2)]
    
    def draw_outline(self, pos, turn):
        """Draws an outline of specific turn on the square
            tuple given if the last drawn outline wasn't at
            that position.
            
            draw_outline((0,0), 0) would draw a vertical
            outline on squares (0,0) and (0,1)
            """
        turn = (turn) % 2
        if self.last_outline != pos:
            self.undraw_outline()
            dx, dy = turn, 1-turn
            x,y = self.get_square(pos, turn)
            self._draw(self.outlines[turn], self.get_pixels((x,y)))
            self.last_outline = [(x,y),(x+dx,y+dy)]

    def undraw_button(self, move, turn):
        """Deletes a button from screen"""
        dx = 1-turn
        dy = turn
        x, y = move
        self.draw_square((x,y))
        self.draw_square((x+dx,y+dy))
        
    def _draw(self, item, pos, surface = None):
        if surface == None:
            self.screen.blit(item, pos)
        else:
            surface.blit(item, pos)
        
    def get_square(self, pos, turn):
        """Returns the square from the pixel coordinate.
            So that the outline drawing would be better,
            tries to stick to the mouse, so
            if turn == 0: y-= squaresize/2
            else: x -= squaresize
            """
        x, y = pos
        #tries to "stick to the middle" of the mouse.
        if turn == 0:
            y -= self.squaresize/2
        else:
            x -= self.squaresize/2
        res = (int((x-self.zeropos[0])/self.squaresize),
                int((y-self.zeropos[1])/self.squaresize))
        return res
    def get_pixels(self, square):
        """Returns the pixel coordinate of the square provided"""
        x, y = square
        return (int(round((x)*self.squaresize,0))+self.zeropos[0],
                int(round((y)*self.squaresize,0))+self.zeropos[1])

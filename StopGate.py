#!/usr/bin/env python
# -*- coding: cp1257 -*-
import pygame
from pygame.locals import *
from stopgatelocals import *

import Game
import BoardDrawer
import Menu

import Human
import AI
import Log

import ConfigParser
from os import path

#read settings
parser = ConfigParser.SafeConfigParser()
parser.read('settings.ini')
w = parser.getint('Game', 'Screen_width')
h = parser.getint('Game', 'Screen_height')
size = (w,h)
ai_delay = parser.getint('Game','ai_delay')
AIS = sorted(parser.items('AIS'), key = lambda x:x[1].lower())

def write_config():
    """writes settings to settings.ini"""
    global parser
    parser.set('Game','Screen_width', str(size[0]))
    parser.set('Game','Screen_height', str(size[1]))
    parser.set('Game','ai_delay', str(ai_delay))
    parser.write(open('settings.ini', 'w'))
 

class StopGate(object):
    def __init__(self):
        self.board = BoardDrawer.Board(size)
        self.menu = Menu.Menu(size, AIS, ai_delay)
        self.keydown = False
        
    def new_game(self, players = [], gametype = CHOSENORMALGAME):
        """Decides which game type to start, gets input from menu"""
        global ai_delay, size
        if len(players) != 2 and gametype == CHOSENORMALGAME:
            # no info given, gets info from menu
            gametype, players = self.menu.show_menu(False)
        self.turncn = 1
        self.menu_hovering = False
        self.gametype = gametype
        
        if gametype == CHOSENORMALGAME:
            self.botgame, players = self._transformplayers(players)
            print 'Uus mäng: %s(V) vs %s(H)\n' % (players[0],players[1])
            self.game = Game.Game(*players)
            #breathe life into the bots.
            self.game.players[0].start()
            self.game.players[1].start()
            self.play_normalgame()
            
        elif gametype == CHOSELOGGAME:
            f = open(path.join('Logs',players)).read()
            self.game = Log.log_parser(f)
            self.play_loggame()
            
        elif gametype == CHANGEDSETTINGS:
            nsize, ndelay = players
            if ndelay != ai_delay:
                ai_delay = ndelay
            if nsize != size:
                size = nsize
                self.board = BoardDrawer.Board(nsize)
                self.menu = Menu.Menu(nsize, AIS, ai_delay)
    
    def play_normalgame(self):
        """Starts a normal game"""
        game = self.game
        
        self.board.draw_board()
        pygame.display.flip()
        
        self.menubutton = self.board.menubutton
        game.reset_boxes(self.board.scorebox, \
                        self.board.recordbox, \
                        self.board.statisticsbox)
        last_hovering = None
        game.set_time()
        move = game.players[0].get_input('start\n')
        clock = pygame.time.Clock()
        t = clock.tick()
        while game.movecn[game.turn] != 0:
            #loop while moves to be a move can be made
            if last_hovering != self.menu_hovering:
                #hovered over the menu button
                self.menubutton.draw(self.menu_hovering)
                last_hovering = self.menu_hovering
                pygame.display.flip()
            if self.event_handle() != None:
                #changed settings in the meantime
                break
            if self.botgame and t < ai_delay:
                #two bots are playing and need to pause
                #freezes game. Might look for a better solution
                pygame.time.wait(ai_delay-t)
                clock.tick()
            if move != None:
                #got a move from a player
                try:
                    legal = game.legalmove(move)
                except (UnboundLocalError, ValueError):
                    #no input got -> lost connection/invalid format?
                    #exception handling might slow things down
                    game.connection_lost()
                    print 'Viga:',[move]
                    break
                if legal:
                    self.board.draw_button(move, game.turn)
                    game.mark(move)
                else:
                    #illegal move, abort
                    game.invalid_move(move)
                    break
                #redraw button.
                self.menubutton.draw(self.menu_hovering)
                pygame.display.flip()
                #next move
                move = game.players[game.turn].get_input('%d %d\n' % move)
                t = clock.tick()
            else:
                #first move/human player
                move = game.players[game.turn].get_input()
                t = clock.tick()        
        else: #didn't restart game
            #game over
            self.game.win()
            self.game.players[game.turn].output('loss\n')
            self.game.players[1-game.turn].output('win\n')
        self.wait_keypress()
        
    def play_loggame(self):
        """Starts a log game

        draws the first move and waits for left/right
        keypress to move forward/back in the log

        """
        lastturncn = 0
        last_hovering = None
        game = self.game
        self.board.draw_board()
        self.menubutton = self.board.menubutton
        game.reset_boxes(self.board.scorebox, \
                        self.board.recordbox, \
                        self.board.statisticsbox)
        clock = pygame.time.Clock()
        while True:
            if last_hovering != self.menu_hovering:
                #hovered over the menu button
                self.menubutton.draw(self.menu_hovering)
                last_hovering = self.menu_hovering
                pygame.display.flip()
            if lastturncn != self.turncn:
                #next turn
                move = game.set_turn(self.turncn)
                if isinstance(move, tuple):
                    #fails if msg like ajalimiit vms
                    if lastturncn < self.turncn:
                        #next turn
                        self.board.draw_button(move, game.turn)
                    else:
                        #undid last turn
                        self.board.undraw_button(move, game.turn)
                lastturncn = self.turncn
                pygame.display.flip()
            if self.event_handle() != None:
                #changed settings in the meantime
                break
            pygame.time.wait(60)
##            py
            
    def wait_keypress(self):
        """Waits for a keypress/mosebuttonpress from user"""
        pygame.display.flip()
        self.quit_game()
        while pygame.event.wait().type not in (KEYDOWN, MOUSEBUTTONDOWN):
            pass
        
            
    def _transformplayers(self, players):
        """Transforms the players string tuple to Players a tuple (Human/AI)"""
        #Transforms from tuple to object
        result = []
        bots = 0
        for i, player in enumerate(players):
            if player == HUMANPLAYER:
                result.append(Human.HumanPlayer(i, self.board))
            else:
                fname, name = player
                ai = AI.ComputerPlayer(i, path = fname, name = name)
                bots += 1
                result.append(ai)
        return bots == 2, result
    
    def show_menu(self):
        """Show menu and act according to the input"""
        global ai_delay, size
        #show menu and get input from it
        gametype, players = self.menu.show_menu(True)
        if gametype == CHOSENORMALGAME or gametype == CHOSELOGGAME:
            #started a new game
            self.quit_game()
            self.new_game(players, gametype)
            return True #restarted game
        elif gametype == CHANGEDSETTINGS:
            #changed settings
            nsize, ndelay = players
            if ndelay != ai_delay:
                ai_delay = ndelay
            if nsize != size:
                size = nsize
                self.board = BoardDrawer.Board(nsize)
                self.menu = Menu.Menu(nsize, AIS, ai_delay)
                #quit and start anew
                self.quit_game()
                self.new_game()
                return True #restarted game

    def event_handle(self):
        clicks = []
        pygame.time.wait(50)
        for event in pygame.event.get():
            if event.type == QUIT:
                raise exited_game
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    #show meny
                    return self.show_menu()
                elif event.key == K_LEFT:
                    #backward in log_game
                    self.keydown = K_LEFT
                elif event.key == K_RIGHT:
                    #forward in log_game
                    self.keydown = K_RIGHT
            elif event.type == KEYUP and event.key in (K_LEFT, K_RIGHT):
                #paused going in log_game
                self.keydown = False
            elif event.type == MOUSEMOTION:
                #drawing outlines
                pos = pygame.mouse.get_pos()
                self.menu_hovering = self.menubutton.hovering(event.pos)
                if self.gametype == CHOSELOGGAME or self.botgame:
                    #no outlines for bot games/log games
                    continue
                spos = self.board.get_square(pos, self.game.turn)
                legal = self.game.legalmove(spos)
                if self.board.boardsize <= max(pos) \
                   <= self.board.boardsize+self.board.squaresize/2:
                    continue        
                elif legal:
                    self.board.draw_outline(pos, self.game.turn)
                    pygame.display.flip()
                elif not legal:
                    self.board.undraw_outline()
                    pygame.display.flip()
                
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.menubutton.hovering(pos):
                    return self.show_menu()
                clicks.append(event)
        for click in clicks:
            #repost clicks to eliminate lag/lost clicks for human players
            pygame.event.post(click)
        
        #in loggame, movement with left/right keys
        if self.keydown == K_RIGHT and self.turncn < self.game.totturns:
            self.turncn += 1
        elif self.keydown == K_LEFT and self.turncn > 1:
            self.turncn -= 1
            
    def quit_game(self):
        if self.gametype == CHOSENORMALGAME:
            try:
                self.game.players[0].kill()
                self.game.players[1].kill()
                del self.game
            except AttributeError: #already closed
                pass


if __name__ == "__main__":
    from sys import argv
    StopG_game = StopGate()
    try:
        if len(argv) == 3:
            #chose players from command line
            players = map(int, argv[1:])
            for j,i in enumerate(players):
                if i > len(AIS):
                    players[j] = HUMANPLAYER
                else:
                    players[j] = AIS[i]
            print players
            StopG_game.new_game(players, gametype = CHOSENORMALGAME)
        else:
            #normal game start
            while True: #play, play, play
                StopG_game.new_game()
    except exited_game: pass
    finally:
        #write the settings
        write_config()
        #close pygame
        pygame.quit()

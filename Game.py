# -*- coding: cp1257 -*-
import time
from stopgatelocals import colors
class Game(object):
    """A normal game object"""
    def __init__(self, player1, player2):        
        self.turn = 0 #0- vertikaalne 1-horisontaalne
        self.turncn = 1
        self.dx = self.turn
        self.dy = 1-self.turn
        self.players = [player1, player2]
        self.board = [[0]*12 for _ in xrange(12)]
        self.marked = [[0]*12 for _ in xrange(12)]
        self.movecn = [132,132] # 12*11
        player1.add_game(self)
        player2.add_game(self)
        self.score = 'V: %s: %d\nH: %s: %d' % (self.players[0],
                                                self.movecn[0],
                                                self.players[1],
                                                self.movecn[1]) #can be removed
        self.totaltime = [0.0,0.0]
        self.lasttime = [0.0,0.0]
        self.statistics = 'Eelmine käik\nV: %0.2fs\nH: %0.2fs\nKokku\nV: %0.2fs\nH: %0.2fs' %\
                        tuple(self.lasttime+self.totaltime)
    def reset_boxes(self, scorebox, recordbox, statisticsbox):
        """Resets boxes"""
        self.scorebox = scorebox
        self.recordbox = recordbox
        self.statisticsbox = statisticsbox
        self.update_boxes()
        
    def update_boxes(self, pos = None):
        """Updates the three boxes with the latest score"""
        self.scorebox.reset()
        self.scorebox.add_text(color = colors[0],
                               text = 'V: %s: %d' % (self.players[0],
                                                      self.movecn[0]))
        self.scorebox.add_text(color = colors[1],
                               text = 'H: %s: %d' % (self.players[1],
                                                      self.movecn[1]))
        if pos == None:
            self.recordbox.reset()
            self.recordbox.draw()
        else:
            pl = ['V','H']
            textargs = (self.turncn, pl[self.turn], str(pos))
            self.recordbox.add_text(color = colors[self.turn],
                                    text = '%d. %s: %s' % textargs)
        
        self.statisticsbox.set_text(self.statistics)
    def set_time(self):
        self.time = time.time()

    def is_free(self, x, y):
        return 0<=x<12 and 0<=y<12 and self.board[x][y] == 0

    def legalmove(self, pos, turn = None):
        """Returns if the move is a valid move (True/False)"""
        if pos == None: return False
        x, y = pos #may raise ValueError
        if turn!=None:
            dx = turn; dy = 1-turn
            return self.is_free(x, y) and self.is_free(x+dx, y+dy)
        return self.is_free(x, y) and self.is_free(x+self.dx, y+self.dy)


    def mark(self, pos):
        """Marks the move and updates boxes"""
        timetaken = time.time() - self.time
        self.time = time.time()
        self.lasttime[self.turn] = timetaken
        self.totaltime[self.turn] += timetaken
        def substract(x1,y1,x2,y2):
            """Substracts from movecount the
                number of moves lost"""
            f = ((0,1),(0,-1),(1,0),(-1,0))
            self.movecn[self.turn] -= 1
            for dx, dy in f:
                if self.is_free(x1+dx, y1+dy):
                    self.movecn[dx] -=1
                if self.is_free(x2+dx, y2+dy):
                    self.movecn[dx] -=1
         
        x, y = pos
        self.board[x][y] = 1
        self.board[x+self.dx][y+self.dy] = 1            
        self.marked[x][y] = self.turn + 1 #for redrawing, ha
        
        substract(x,y, x+self.dx, y+self.dy)
        pl = 'VH'
        self.statistics = 'Eelmine käik\nV: %0.2fs\nH: %0.2fs\nKokku\nV: %0.2fs\nH: %0.2fs' %\
                        tuple(self.lasttime+self.totaltime)
        print '%s: %s tegi käigu: %s Käike:%s Aega kulus:(%0.3fs)' % \
                                                (pl[self.turn],
                                                self.players[self.turn],
                                                pos,
                                                self.movecn,
                                                timetaken)
        self.update_boxes(pos)
        #next turn
        self.turn = 1-self.turn
        self.dx = self.turn 
        self.dy = 1-self.turn
        self.turncn += 1
    def win(self):
        """Announces the end of the game"""
        pl = 'VH'
        self.record = '%s: %s võitis. Hiireklõps jätkamiseks.' % \
                        (pl[1-self.turn], self.players[1-self.turn])
        self.statistics = 'Eelmine käik\nV: %0.2fs\nH: %0.2fs\nKokku\nV: %0.2fs\nH: %0.2fs' %\
                        tuple(self.lasttime+self.totaltime)
        self.recordbox.add_text(color = colors['yellow'],
                                text = self.record)
        print 
        print self.statistics
        print self.record
    def invalid_move(self, move):
        """Announces that an invalid move has been made"""
        record = '%s tegi vigase käigu: %s' % (self.players[self.turn], move)
        self.recordbox.add_text(color = colors['yellow'],
                                text = record)
        self.win()
    def connection_lost(self):
        record = "%s'iga kaotati ühendus." % (self.players[self.turn])
        self.recordbox.add_text(color = colors['yellow'],
                                text = record)
        self.win()        

# -*- coding: cp1257 -*-
import Human
import os, sys
from stopgatelocals import colors
startn = 'Vertikaalne (alustaja)'
endn = '\n</td>\n</tr>\n</table>'
class invalid_log(Exception):
    def __init__(self):
        pass
def html_parse(text):
    """Parses htm file taken from the server into the correct log form"""
    text = text[text.find(startn):]
    text = text[:text.find(endn)]
    text = text.replace('Ć¼','ü').replace('Ć¤','ä').replace('Ćµ','õ').replace('Ć–','ö')
    text = text.replace('\n</td>\n<td class="move">\n','\t ')
    text = text.replace('\n</td>\n<td class="contestant">\n','\t ')
    text = text.replace('\n</td>\n</tr>\n','')
    text = text.replace('\n<td class="move_no">','')
    text = text.replace('<tr class="even">','')
    text = text.replace('<tr class="odd">','')
    text = text.replace('<tr>','')
    text = text.replace('\n</td>\n<td class="header_right">\n','\t ')
    text = text.replace('\n<td class="header_left" colspan="2">','')
    text = text.replace('#','')
    return text
def log_parser(text):
    """Parses a log text, assuming it is in the correct form. raises
        invalid_log exception elsewise"""

    if text.find('<html>')!=-1:
        text = html_parse(text)
        
    start = text.find('Vertikaalne (alustaja)')
    if start == -1:
        raise invalid_log
    text = text[start:].splitlines()
    log = text[5:]
    vname = text[0].split('\t ')[1]
    hname = text[1].split('\t ')[1]
    info = '\n'.join(text[2:5]).replace('\t','\n  ')
    print info
    moves = []
    for i, line in enumerate(log):
        turnno, name, move = line.split('\t ')
        if '%d:' % (i+1) not in turnno:
            raise invalid_log
        try:
            move = tuple(map(int, move.split()))
        except ValueError:
            if 'Ajalimiit' not in move and 'Vigane' not in move:
                raise invalid_log
        moves.append(move)
    return LogGame(Logger(vname, hname, info, moves))

class Logger(object):
    def __init__(self, vname, hname, info, moves):
        self.name = (vname, hname)
        self.info = info
        self.moves = moves

class Marker(object):
    #dirty, I know
    def __init__(self):
        self.board = [[0]*12 for _ in xrange(12)]
        self.movecn = [132, 132]
        self.turn = 0
    def is_free(self, x, y):
        return 0<=x<12 and 0<=y<12 and self.board[x][y] == 0
    def mark(self, move):
        def substract(x1,y1,x2,y2):
            f = ((0,1),(0,-1),(1,0),(-1,0))
            self.movecn[self.turn] -= 1
            for dx, dy in f:
                if self.is_free(x1+dx, y1+dy):
                    self.movecn[dx] -=1
                if self.is_free(x2+dx, y2+dy):
                    self.movecn[dx] -=1
        if isinstance(move, tuple):
            x, y = move
            dx = self.turn
            dy = 1-self.turn
            self.board[x][y] = 1
            self.board[x+dx][y+dy] = 1
            substract(x,y,x+dx,y+dy)
            self.turn = 1-self.turn
        return tuple(self.movecn)
    
class LogGame(object):
    def __init__(self, log):
        self.players = [log.name[0], log.name[1]]
        self.info = log.info
        self.moves = log.moves
        self.records = []
        pl = ['V','H']
        marker = Marker()
        self.scores = []
        for i, move in enumerate(log.moves):
            self.scores.append(marker.mark(move))
            st = '%d. %s: %s' % (i+1, pl[i%2], move)
            self.records.append((colors[i%2],st))
        _, move = self.records[-1]
        self.turn = 0
        self.turncn = 0
        self.totturns = len(self.records)
        
    def reset_boxes(self, scorebox, recordbox, statisticsbox):
        self.scorebox = scorebox
        self.recordbox = recordbox
        self.lines = recordbox.maxlines
        self.statisticsbox = statisticsbox
        self.statisticsbox.set_text(self.info)

        self.update()
        
    def set_turn(self, turn):
        if 0 < turn <= self.totturns:
            self.turn = (turn-1) % 2
            if self.turncn > turn:
                ret = self.moves[self.turncn-1]
            else:
                ret = self.moves[turn-1]
            self.turncn = turn
            self.update()
            return ret
        
    def update(self):
        s = max(0, self.turncn - self.lines)
        e = self.turncn
        self.recordbox.text = self.records[s:e]
        self.scorebox.reset()
        self.scorebox.add_text(color = colors[0],
                               text = 'V: %s: %d' % (self.players[0],
                                                     self.scores[e-1][0]))
        self.scorebox.add_text(color = colors[1],
                               text = 'H: %s: %d' % (self.players[1],
                                                     self.scores[e-1][1]))
        print self.records[e-1][1], self.scores[e-1]
        self.recordbox.draw()

if __name__ == "__main__":
    fname = 'macobo-2 avo-1.htm'
    logtext = open(os.path.join('Logs',fname)).read()
    players = log_parser(logtext)
    


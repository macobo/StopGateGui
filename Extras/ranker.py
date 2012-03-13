# -*- coding: cp1257 -*-
"""Script, mis teeb samas kaustas olevate logide põhjal kasutajate järjestuse,
    mis sarnaneb lõppturniiri reeglitele, kasutades vaid viimast logi iga paari
    kohta.
    Lisaks saab iga koostatud profiili kohta rohkem infot uurida - näiteks
    kellele robot kaotanud on
    Võtab argumendiks käsurealt boti nime, kelle kohta täpsem statistika
    huvitab"""

import sys

class Profile(object):
    def __init__(self, name):
        self.name = name
        self.wins = []
        self.losses = []
    def addWin(self, opp_pos, opp):
        self.wins.append((opp,opp_pos))
    def addLoss(self, opp_pos, opp):
        self.losses.append((opp,opp_pos))
    def getWins(self):
        return len(self.wins)
    def getLosses(self):
        return len(self.losses)
    def statistics(self):
        print '\n%s:' % self.name
        l = ['-'.join(x) for x in sorted(self.wins)]
        i = ['-'.join(x) for x in sorted(self.losses)]
        print 'Wins: %d \t%s\n' % (self.getWins(), l)
        print 'Losses: %d \t%s' % (self.getLosses(), i)
    
def addWin(name, opp_pos, opp):
    if not profiles.has_key(name):
        profiles[name] = Profile(name)
    profiles[name].addWin(opp_pos, opp)
    
def addLoss(name, opp_pos, opp):
    if not profiles.has_key(name):
        profiles[name] = Profile(name)
    profiles[name].addLoss(opp_pos, opp)
    
def info_parser(f):
    text = open(f).readlines()
    v, h = [s.strip().split('\t ')[1] for s in text[:2]]
    winner = text[4].strip().split('\t ')[1]
    length = len(text)-5
    if winner == v:
        addWin(v, 'H', h)
        addLoss(h, 'V', v)
    elif winner == h:
        addWin(h, 'V', v)
        addLoss(v, 'H', h)
        
def new_ranking():
    import glob, time
    t = time.time()
    prev = None
    prevno = 0
    lis = glob.glob('*.txt')
    lis.sort(reverse = True)
    for filename in lis:
        firstpar = filename.split()[:-1]
        no = int(filename.split()[-1].split('.')[0])
        if firstpar != prev:
            info_parser(filename)
            prevno = 99999
        prev = firstpar
        assert prevno > no, '%d %d' % (prevno, no)
        prevno = no
##    print 'creating a new profile took %0.2fs\n' % (time.time()-t)
    
def list_ranking():
    global p
    p = profiles.items()
    p.sort(key = lambda x:x[1].getWins(), reverse = True)
    print 'Koht\t Bot\t\tVõite/Kaotusi\tSuhe\n'
    for rank, (name, bot) in enumerate(p):
        percent = 50.0*bot.getWins()/len(p)
        win = bot.getWins()
        allgames = bot.getLosses()+win
        namehalf = '%d:\t %s\t' % (rank+1, name)
        print namehalf,
        if len(name) < 7:
            print '\t',
        print '(%d/%d) \t\t%0.2f' % (win, allgames, percent)

profiles = {}
new_ranking()
list_ranking()
if len(sys.argv) > 1:
    #näitab statistikat boti kohta
    try:
        profiles[' '.join(sys.argv[1:])].statistics()
    except KeyError:
        print 'profiili nimega %s ei leitud!' % ' '.join(sys.argv[1:])

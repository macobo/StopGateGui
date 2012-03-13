# -*- coding: cp1257 -*-
from Exit import exited_game


HUMANPLAYER = 0
defaultsizes = [(1000, 742), (910, 680), (700, 507), (600,435)]
delays = [0, 200, 500, 1000, 2000]

__version__ = "0.3.4"
__author__ = "Karl Aksel Puulmann"
__year__ = 2011

colors = {
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'orange': (255, 100, 0),
    'purple': (255, 0, 255),
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'yellow': (255, 255, 0),
    'gray': (180, 180, 180),
    0: (144, 219, 98),
    1: (95, 175, 218)
    }

#events
CHOSE = 40
CHOSENORMALGAME = 42
CHOSELOGGAME = 43
CHANGEDSETTINGS = 41
BACK = 51
EXITMENU = 52
NEWGAME = EXITMENU #tmp


juhend ="""Stop-Gate'i m�ngitakse ruudukujulisel m�ngulaual m��tmetega 12x12. Nuppudena kasutatakse nuppe m��tmetega 2x1, st m�ngulauale asetatuna katavad nad �ra t�pselt kaks m�ngulaua ruutu.

�ksteise vastu m�ngivad kaks m�ngijat, kes sooritavad k�ike kordam��da, kusjuures k�igu sooritamiseks peab m�ngija asetama lauale �he nupu. Alustaja peab oma nupud paigutama vertikaalselt, tema vastasm�ngija horisontaalselt. Kaotab see, kes esimesena k�iku sooritada ei saa.

Nuppe on m�lemal m�ngijal piisavalt m�ngulaua t�itmiseks ja samal m�ngulaua ruudul ei tohi olla �le �he nupu. M�ngu alguses on laud t�hi.
"""
kasutajaliides = """Nupu asetamiseks kasuta hiire vasakut nuppu.
Kui �ks m�ngija on k�inud, l�heb k�imisj�rjekord �le teisele m�ngijale.
Logides navigeerimiseks kasutage paremat/vasakut nooleklahvi.

Men�� avamiseks v�ib kasutada paremal all serval olevat nuppu v�i vajutada nuppu ESC.
Men��des navigeerimiseks v�ib kasutada hiirt v�i klaviatuurinuppe.

K�surealt m�ngu k�ivitamiseks navigeerige kausta, kus StopGate.py on ja sisestage k�sk "python StopGate.py". Kui lisada argumentidena kaks numbrit, siis paneb arvuti m�ngima kaks boti v�i inimm�ngija. Nt "python StopGate.py 0 3" paneb m�ngima esimese ja neljanda boti (kui on alla 4 boti, siis selle asemel inimm�ngija).
"""

lisainfo = """
Autor: %s
Versioon: %s
Aasta: %d

Lisaks t�nud:
Neal Strobl logo eest
http://www.clker.com ikoonide eest
http://www.discoverfonts.com Dominican Small Caps Font'i eest

Bottide ja logide lisamine:
Readme failis on t�psemad juhised bottide ja logide lisamiseks.
""" % (__author__, __version__, __year__)
titles = ['Juhend', 'Kasutajaliides', 'Lisainfo']
instructions = [juhend, kasutajaliides, lisainfo]

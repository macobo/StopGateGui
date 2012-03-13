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


juhend ="""Stop-Gate'i mängitakse ruudukujulisel mängulaual mõõtmetega 12x12. Nuppudena kasutatakse nuppe mõõtmetega 2x1, st mängulauale asetatuna katavad nad ära täpselt kaks mängulaua ruutu.

Üksteise vastu mängivad kaks mängijat, kes sooritavad käike kordamööda, kusjuures käigu sooritamiseks peab mängija asetama lauale ühe nupu. Alustaja peab oma nupud paigutama vertikaalselt, tema vastasmängija horisontaalselt. Kaotab see, kes esimesena käiku sooritada ei saa.

Nuppe on mõlemal mängijal piisavalt mängulaua täitmiseks ja samal mängulaua ruudul ei tohi olla üle ühe nupu. Mängu alguses on laud tühi.
"""
kasutajaliides = """Nupu asetamiseks kasuta hiire vasakut nuppu.
Kui üks mängija on käinud, läheb käimisjärjekord üle teisele mängijale.
Logides navigeerimiseks kasutage paremat/vasakut nooleklahvi.

Menüü avamiseks võib kasutada paremal all serval olevat nuppu või vajutada nuppu ESC.
Menüüdes navigeerimiseks võib kasutada hiirt või klaviatuurinuppe.

Käsurealt mängu käivitamiseks navigeerige kausta, kus StopGate.py on ja sisestage käsk "python StopGate.py". Kui lisada argumentidena kaks numbrit, siis paneb arvuti mängima kaks boti või inimmängija. Nt "python StopGate.py 0 3" paneb mängima esimese ja neljanda boti (kui on alla 4 boti, siis selle asemel inimmängija).
"""

lisainfo = """
Autor: %s
Versioon: %s
Aasta: %d

Lisaks tänud:
Neal Strobl logo eest
http://www.clker.com ikoonide eest
http://www.discoverfonts.com Dominican Small Caps Font'i eest

Bottide ja logide lisamine:
Readme failis on täpsemad juhised bottide ja logide lisamiseks.
""" % (__author__, __version__, __year__)
titles = ['Juhend', 'Kasutajaliides', 'Lisainfo']
instructions = [juhend, kasutajaliides, lisainfo]

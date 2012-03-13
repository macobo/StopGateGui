# -*- coding: cp1257 -*-
import pygame
from pygame.locals import *
from Exit import exited_game
from ScrollingTextArea import ScrollingTextArea
from Hoverable import Hoverable
from stopgatelocals import *

HUMANPLAYER = 0

##Messy as hell with lots of copy-paste methods between classes.
##As this will never get reused (and I hope I won't regret this),
##I won't waste any more time trying to clean this up
##Sorry.
##-Karl

class Menu(object):
    quitwarning = 'Oled kindel, et soovid väljuda?'
    N = 6
    active = 2
    
    smallconst = 0.65
    largeconst = 0.85
    miniconst = 0.50
    
    def __init__(self, size, AI, aidelay):
        global AIS, ai_delay
        AIS = AI #bah, hack
        ai_delay = aidelay
        self.screensize = size
        
        self.perbut = 1.0*self.screensize[0] / self.N
        self.smallsize = int(self.smallconst*self.perbut)
        self.largesize = int(self.largeconst*self.perbut)
        self.minsize = int(self.perbut * self.miniconst)
        import os
        self.font = pygame.font.Font(os.path.join('Fonts','def.ttf'), self.screensize[0]/35)
        self.sfont = pygame.font.Font(os.path.join('Fonts','def.ttf'), self.screensize[0]/45)
        self.mfont = pygame.font.Font(os.path.join('Fonts','def.ttf'), self.screensize[0]/55)

        self.buttons = []
        t = 255/self.N
        names = ['Uus mäng', 'Naase mängu', 'Juhised', 'Logi vaataja', 'Valikud', 'Välju']
        filenames = ['newgame', 'return', 'instructions', 'logviewer', 'options', 'exit']
        for name, filename in zip(names, filenames):
            button = pygame.image.load("Pics/%s.png" % filename).convert_alpha()
            button = pygame.transform.smoothscale(button, (self.largesize,self.largesize))
            self.buttons.append((button,name))
            
        #generate sized and paired buttons and labels

        self.sized_buttons = []
        self.sized_fonts = [] # pairs 
        self.linked_buttons_sl = [] #small-large
        self.linked_buttons_ms = [] #min-small

        mx = (self.perbut - self.minsize)/2
        sx = (self.perbut - self.smallsize)/2
        my = (self.screensize[1] - self.minsize) * 0.95
        sy = (self.screensize[1] - self.smallsize) * 0.95
        syy = (self.screensize[1]-self.smallsize)/2
        for i, (button, name) in enumerate(self.buttons):
            l = self._transform_button(button, self.largesize)
            s = self._transform_button(button, self.smallsize)          
            m = self._transform_button(button, self.minsize)
            self.sized_buttons.append((l, s, m))
            lw = self.font.size(name)[0]
            sw = self.sfont.size(name)[0]
            mw = self.mfont.size(name)[0]
            
            ln = self.font.render(name, True, colors['white'])
            sn = self.sfont.render(name, True, colors['white'])
            mn = self.mfont.render(name, True, colors['white'])
            self.sized_fonts.append(((ln, lw), (sn, sw), (mn, mw)))
            x = i*self.perbut
            #small-large
            h1 = Hoverable((x+sx, syy), HAT_CENTERED, s, l)
            #min-small
            h2 = Hoverable((x+mx, my), HAT_DOWN, m, s)
            self.linked_buttons_sl.append(h1)
            self.linked_buttons_ms.append(h2)
        self.mini_menu = MiniMenu(self, self.linked_buttons_ms, self.sized_fonts)
        self.newgame_menu = NewGameMenu(self)
        self.instructions_menu = InstructionsMenu(self)
        self.confirmation_menu = ConfirmationMenu(self)
        self.log_menu = LogsMenu(self)
        self.options_menu = OptionsMenu(self)
        self.logo = pygame.image.load("Pics/logo.png").convert_alpha()
        x, y = size
        x -= self.logo.get_width()
        self.logopos = (x/2, y*0.05)
            
    def _transform_button(self, button, sqsize):
        return pygame.transform.smoothscale(button, (sqsize, sqsize))
    def get_screencopy(self):
        return self.screencopy

    def show_menu(self, playing):
        dimmer = Dimmer()
        self.screen = pygame.display.get_surface()
        dimmer.darken()
        self.screencopy = pygame.Surface(self.screensize)
        self.screencopy.blit(self.screen,(0,0))
        try:
            while True:
                self.screen.blit(self.screencopy,(0,0))
                level = self.handle(self.mainmenu_input())
                if isinstance(level,tuple) and len(level) == 2:
                    return level
                elif level != None and playing:
                    return level, None
##                else: #to-remove
##                    print level, type(level)
        finally:
            dimmer.restore()
            
    def mainmenu_input(self):
        lactive = None
        while True:
            if lactive != self.active: #moved the chosen
                self.screen.blit(self.screencopy,(0,0))
                self.screen.blit(self.logo,self.logopos)
                for i, button in enumerate(self.linked_buttons_sl):
                    boolean = i==self.active
                    button.draw(boolean)
                    rendered, width = self.sized_fonts[i][1-boolean]
                    tx, ty, bx, by = button.corners()
                    dx = (bx-tx-width)/2
                    self.screen.blit(rendered, (tx + dx, by))
                lactive = self.active
                pygame.display.flip()
            event, self.active = self.event_handle(self.active,
                                            self.linked_buttons_sl)
            if event == CHOSE:
                return self.active
            elif event == BACK:
                return BACK
            
    def handle(self, level):
        if level == BACK:
            return BACK
        elif level == 0:
            return self.newgame_menu.draw()
        elif level == 1:  #exited menu
            return BACK
        elif level == 2:
            return self.instructions_menu.draw()
        elif level == 3: #logid
            return self.log_menu.draw()
        elif level == 4: #valikud
            return self.options_menu.draw()
##            self.mini_menu.draw([level])
        elif level == 5:  #välju
            if self.confirmation_menu.confirm(self.quitwarning) == 0:
                raise exited_game
            
    def event_handle(self, active, hoverables, max_active = None):
##        pygame.time.wait(50)
        e = pygame.event.wait()
        pygame.event.post(e)
        if max_active == None:
            max_active = len(hoverables)
        for event in pygame.event.get():
            if event.type == QUIT :
                raise exited_game
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return BACK, active #return to game
                elif event.key == K_LEFT or event.key == K_UP:
                    active -= 1
                    if active == -1 or active >= max_active:
                        active = max_active-1
                elif event.key == K_RIGHT or event.key == K_DOWN:
                    active += 1
                    if active >= max_active:
                        active = 0
                elif event.key == K_RETURN:
                    return CHOSE, active #chose something
                
            elif event.type == MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                for i, hov in enumerate(hoverables):
                    if hov.hovering(pos):
                        active = i
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i, hov in enumerate(hoverables):
                    if hov.hovering(pos):
                        active = i
                        return CHOSE, active
        return None, active



class ConfirmationMenu(object):
    def __init__(self, parent):
        self.font = parent.font
        small_font = parent.sfont
##        self.screencopy = parent.screencopy
        self.event_handle = parent.event_handle
        self.handle = parent.handle
        self.get_screencopy = parent.get_screencopy

        w, h = pygame.display.get_surface().get_size()
        dyes_x, dyes_y = small_font.size('Jah')
        yy = (h - dyes_y)*0.55
        yes_orig = small_font.render('Jah', True, colors['white'])
        yes_active = self.font.render('Jah', True, colors['red'])
        dno_x, dno_y = small_font.size('Ei')
        yn = (h - dno_y)*0.55
        no_orig = small_font.render('Ei', True, colors['white'])
        no_active = self.font.render('Ei', True, colors['red'])
        
        self.hyes = Hoverable(((w - dno_x)*0.40, yy), HAT_CENTERED, yes_orig, yes_active)
        self.hno = Hoverable(((w - dyes_x)*0.60, yn), HAT_CENTERED, no_orig, no_active)
        
    def confirm(self, warning):
        rendered = self.font.render(warning, True, colors['white'])
        w, h = self.font.size(warning)
        screen = pygame.display.get_surface()
        x,y = screen.get_size()
        lactive = -1; active = 0
        while True:
            if lactive != active:
                screen.blit(self.get_screencopy(),(0,0))
                screen.blit(rendered,((x-w)*0.50, (y-h)*0.40))
                self.hyes.draw(active == 0)
                self.hno.draw(active == 1)
            pygame.display.flip()
            event, active = self.event_handle(active, [self.hyes, self.hno])
            if event == CHOSE:
                return active
            elif event == BACK:
                return BACK    
            

            
class MiniMenu(object):
    def __init__(self, parent, buttons, rendered_titles):
        self.perbut = parent.perbut
        self.buttons = buttons
        self.buttons_titles = zip(buttons, rendered_titles)
        self.N = parent.N
        
    def draw(self, active_buttons):
        for i, (button, title) in enumerate(self.buttons_titles):
            j = i * self.perbut
            boolean = i in active_buttons
            button.draw(boolean)
            rendered, width = title[2-boolean]
            tx, ty, bx, by = button.corners()
            dx = (bx-tx-width)/2
            pygame.display.get_surface().blit(rendered, (tx + dx, by)) 
class InstructionsMenu(object):
    main = 2
    chosen = 0
    def __init__(self, parent):
        self.mini_menu = parent.mini_menu
        self.event_handle = parent.event_handle
        self.handle = parent.handle
        self.get_screencopy = parent.get_screencopy
        self.N = parent.N
        
        font = parent.font
        small_font = parent.sfont
        sx, sy = parent.screensize
        minx = sx * 0.1
        miny = sy * 0.15
        maxx = sx * 0.9
        maxy = sy * 0.80
        
        self.text_area = ScrollingTextArea(small_font, (minx, miny),
                                                (maxx, maxy), None)
        y = miny-2*self.text_area.rowheight
        d = (maxx-minx)/3
        self.titles = []
        for i, title in enumerate(titles):
            orig = small_font.render(title, True, colors['white'])
            active = font.render(title, True, colors['yellow'])
            hov = Hoverable((minx+d*i,y), HAT_LEFTDOWN, orig, active)
            self.titles.append(hov)

    def draw(self):
        active_buttons = tuple([self.main])
        last = None
        choice = self.main
##        current_menu = 0
        while True:
            if  active_buttons != last:
                pygame.display.get_surface().blit(self.get_screencopy(),(0,0))
                self.mini_menu.draw(active_buttons)
                self.text_area.set_text(instructions[self.chosen], draw = False)
                for i, rendered in enumerate(self.titles):
                    rendered.draw(i == self.chosen)
                self.text_area.draw()
                pygame.display.flip()
                last = active_buttons
            event, choice = self.event_handle(choice, self.mini_menu.buttons +
                                self.titles, len(self.mini_menu.buttons))
            if event == CHOSE:
                if choice < self.N: #chose something from minimenu
                    return self.handle(choice)  
                else:
                    self.chosen = choice - self.N
                last = None
            elif event == BACK:
                return None
            active_buttons = (self.main, choice)
        
class NewGameMenu(object):
    main = 0
    def __init__(self, parent):
        def centerstr(name):
            namew, _ = font.size(name)
            spaces = int((diff - namew)/(2*spacesize))
            return ' '*spaces+name+' '*spaces
        self.mini_menu = parent.mini_menu
        self.handle = parent.handle
        self.get_screencopy = parent.get_screencopy
        
        self.bots = [0, 1]
        font = parent.sfont
        w, h = parent.screensize
        bots = [(HUMANPLAYER, 'Inimene')] + AIS
        self.lenbots = len(bots)*2
        row_1 = w * 0.25
        row_2 = w * 0.50
        maxbots = 12
        self.hoverable_bots = []
        y = h * 0.15
        afont = parent.font
        self.label = afont.render('Vali mängijad:', True, colors['yellow'])
##        print self.label.get_width()
        self.labelpos = (w * 0.5 - self.label.get_width()*0.5, h*0.07)
        per = font.size('ABCDEFGHIJKLMNOPQRSTU')[1]
        diff = w * 0.25
        spacesize, _ = font.size(' ')
        for i, (_, name) in enumerate(bots):
            if i == maxbots:
                row_1 = w*0.05
                row_2 = w*0.7
                y = h*0.15 + per
            y += per
            name = centerstr(name)
            not_chosen = font.render(name, True, colors['gray'])
            hovering = font.render(name, True, colors['red'])
            cur_choice = font.render(name, True, colors['white'])
            hov1 = Hoverable((row_1,y), HAT_LEFTDOWN, not_chosen, hovering, cur_choice)
            hov2 = Hoverable((row_2,y), HAT_LEFTDOWN, not_chosen, hovering, cur_choice)
            self.hoverable_bots.append(hov1)
            self.hoverable_bots.append(hov2)
        #startbutton
        alusta = 'Alusta mängu'
        hovering = parent.font.render(alusta, True, colors['red'])
        not_hovering = parent.font.render(alusta, True, colors['white'])
        x = w*0.5 - parent.font.size(alusta)[0]/2
        y = h*0.15 + (min(maxbots, len(bots))+1.5)*per
        self.startbutton = Hoverable((x, y), HAT_CENTERED, not_hovering, hovering)
        
    def draw(self):
        active_buttons = (self.main,)
        hovering = self.bots[0]
        last_buttons = None
        last_bots = None
        last_hovering = None
        while True:
            if  active_buttons != last_buttons or self.bots != last_bots \
                                        or hovering != last_hovering:
##                print active_buttons, last_buttons
                pygame.display.get_surface().blit(self.get_screencopy(),(0,0))
                self.mini_menu.draw(active_buttons) 
                left, right = self.bots
                pygame.display.get_surface().blit(self.label,self.labelpos)
                for i, hov in enumerate(self.hoverable_bots):
                    if i==left or i==right:
                        hov.draw(2)
                    elif i == hovering:
                        hov.draw(1)
                    elif i!=left and i!=right:
                        hov.draw(0)
                self.startbutton.draw(hovering == self.lenbots)   
                pygame.display.flip()
                last_buttons = active_buttons[:]
                last_bots = self.bots[:]
                last_hovering = hovering
                
            event, hovering = self.event_handle(hovering)
            if event == BACK:
                return None
            elif event == CHOSE:
                if hovering == self.lenbots: #start game button:
                    return CHOSENORMALGAME, \
                        [AIS[(x-2)/2] if x>1 else HUMANPLAYER for x in self.bots]
                elif hovering < self.lenbots:
                    self.bots[hovering%2] = hovering
                else: #minimenu
                    return self.handle(hovering - self.lenbots - 1)
            if hovering > self.lenbots:
                active_buttons = (self.main, hovering - self.lenbots - 1)
            else:
                active_buttons = (self.main,)

    def event_handle(self, active):
##        pygame.time.wait(50)
        e = pygame.event.wait()
        pygame.event.post(e)
        for event in pygame.event.get():
            if event.type == QUIT:
                raise exited_game
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return BACK, None
                elif event.key == K_RIGHT:
                    if active+1 <= self.lenbots + 6:
                        active += 1
                    else:
                        active = 0
                elif event.key == K_LEFT:
                    if active-1 >= 0:
                        active -= 1
                    else:
                        active = self.lenbots + 6
                elif event.key == K_UP:
                    if active > self.lenbots:
                        active -= 1
                    elif active-2 >= 0:
                        active -= 2
                    else:
                        active = self.lenbots + 6
                elif event.key == K_DOWN:
                    if active+2 <= self.lenbots:
                        active += 2
                    elif active <= self.lenbots + 6:
                        active += 1
                    else:
                        active = 0
                elif event.key == K_RETURN:
                    return CHOSE, active
            elif event.type == MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                for i, hov in enumerate(self.hoverable_bots):
                    if hov.hovering(pos):
                        return None, i # just hovering
                for i, hov in enumerate(self.mini_menu.buttons):
                    if hov.hovering(pos):
                        return None, i + self.lenbots + 1
                if self.startbutton.hovering(pos):
                    active = self.lenbots
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i, hov in enumerate(self.hoverable_bots):
                    if hov.hovering(pos):
                        return CHOSE, i #clicked bot
                for i, hov in enumerate(self.mini_menu.buttons):
                    if hov.hovering(pos):
                        return CHOSE, i + self.lenbots + 1#clicked menu
                if self.startbutton.hovering(pos):
                    return CHOSE, self.lenbots#clicked start      
        return None, active
class LogsMenu(object):
    chosen = 0
    main = 3
    def __init__(self, parent):
        self.mini_menu = parent.mini_menu
        self.handle = parent.handle
        self.get_screencopy = parent.get_screencopy
        self.screensize = parent.screensize
        self.bots = [0, 1]
        self.font = parent.sfont
        w, h = parent.screensize
        self.lfont = parent.font
        self.label = self.lfont.render('Vali logi:', True, colors['yellow'])
        self.labelpos = (w * 0.5 - self.label.get_width()*0.5, h*0.07)
        self.logs = []
        self.hoverables = []
        
    def create_buttons(self):
        def centerstr(name):
            namew, _ = self.font.size(name)
            spaces = int((diff - namew)/(2*spacesize))
            return ' '*spaces+name+' '*spaces
        import itertools
        per = self.font.size('ABCDEFGHIJKLMNOPQRSTU')[1]
        spacesize, _ = self.font.size(' ')
        w, h = self.screensize
        cols = itertools.cycle([(0.06*w,0.32*w),
                                (0.37*w,0.63*w),
                                (0.68*w,0.94*w)])
        diff = w*0.24
        y = 0.15*h - per
        for i, name in enumerate(self.logs):
            if i % 3 == 0:
                y += per
            sx, ex = cols.next()
            name = name.split('.')[0]
            name = centerstr(' '.join(name.split()[:-1])[:25])
            not_chosen = self.font.render(name[:25], True, colors['gray'])
            hovering = self.font.render(name[:25], True, colors['red'])
            cur_choice = self.font.render(name[:25], True, colors['white'])
            hov = Hoverable((sx,y), HAT_LEFTDOWN, not_chosen, hovering, cur_choice)
            self.hoverables.append(hov)
        alusta = 'Alusta mängu'
        hovering = self.lfont.render(alusta, True, colors['red'])
        not_hovering = self.lfont.render(alusta, True, colors['white'])
        x = w*0.5 - hovering.get_width()/2
        y += 1.5*per
        self.startbutton = Hoverable((x, y), HAT_CENTERED, not_hovering, hovering)        
        

    def draw(self):
        from os import listdir
        last_chosen = None
        last_buttons = None
        last_hovering = None
        hovering = self.chosen
        active_buttons = (self.main,)
        logs = listdir('Logs')
        if self.logs != logs: #the folder was updated
            self.logs = logs
            self.lenlogs = len(logs)
            self.hoverables = []
            self.create_buttons()
            
        while True:
            if  self.chosen != last_chosen or active_buttons != last_buttons or hovering != last_hovering:
                pygame.display.get_surface().blit(self.get_screencopy(),(0,0))
                self.mini_menu.draw(active_buttons) 
                pygame.display.get_surface().blit(self.label,self.labelpos)
                for i, hov in enumerate(self.hoverables):
                    if i == self.chosen:
                        hov.draw(2)
                    else:   
                        hov.draw(i == hovering)
                self.startbutton.draw(hovering == self.lenlogs)
                pygame.display.flip()
                last_chosen = self.chosen
                last_buttons = active_buttons
                last_hovering = hovering
            event, hovering = self.event_handle(hovering)
            if event == BACK:
                return None
            elif event == CHOSE:
                if hovering == self.lenlogs: #start game button:
                    return CHOSELOGGAME, self.logs[self.chosen]
                elif hovering < self.lenlogs:
                    self.chosen = hovering
                else: #minimenu
                    return self.handle(hovering - self.lenlogs - 1)
            if hovering > self.lenlogs:
                active_buttons = (self.main, hovering - self.lenlogs - 1)
            else:
                active_buttons = (self.main,)
            
    def event_handle(self, active):
        e = pygame.event.wait()
        pygame.event.post(e)
        for event in pygame.event.get():
            if event.type == QUIT:
                raise exited_game
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return BACK, None
                elif event.key == K_RIGHT:
                    if active+1 <= self.lenlogs + 6:
                        active += 1
                    else:
                        active = 0
                elif event.key == K_LEFT:
                    if active-1 >= 0:
                        active -= 1
                    else:
                        active = self.lenlogs + 6
                elif event.key == K_UP:
                    if active > self.lenlogs:
                        active -= 1
                    elif active-3 >= 0:
                        active -= 3
                    else:
                        active = self.lenlogs + 6
                elif event.key == K_DOWN:
                    if active+3 <= self.lenlogs:
                        active += 3
                    elif active <= self.lenlogs + 6:
                        active += 1
                    else:
                        active = 0
                elif event.key == K_RETURN:
                    return CHOSE, active
            elif event.type == MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                for i, hov in enumerate(self.hoverables):
                    if hov.hovering(pos):
                        return None, i # just hovering
                for i, hov in enumerate(self.mini_menu.buttons):
                    if hov.hovering(pos):
                        return None, i + self.lenlogs + 1
                if self.startbutton.hovering(pos):
                    return None, self.lenlogs
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i, hov in enumerate(self.hoverables):
                    if hov.hovering(pos):
                        return CHOSE, i #clicked bot
                for i, hov in enumerate(self.mini_menu.buttons):
                    if hov.hovering(pos):
                        return CHOSE, i + self.lenlogs + 1#clicked menu
                if self.startbutton.hovering(pos):
                    return CHOSE, self.lenlogs#clicked start      
        return None, active
    
class OptionsMenu(object):
    main = 4
    def __init__(self, parent):
        self.mini_menu = parent.mini_menu
        self.handle = parent.handle
        self.get_screencopy = parent.get_screencopy
        self.screensize = parent.screensize
        self.bots = [0, 1]
        self.font = parent.sfont
        w, h = parent.screensize
        self.lfont = parent.font
        self.label = self.lfont.render('Seaded', True, colors['yellow'])
        self.labelpos = (w * 0.5 - self.label.get_width()*0.5, h*0.07)

        self.logs = []
        self.hoverables = []
        self.create_buttons()
    def create_buttons(self):
        def centerstr(name):
            #centers string, expects spacesize and diff to be in local scope
            namew, _ = self.font.size(name)
            spaces = int((diff - namew)/(2*spacesize))
            return ' '*spaces+name+' '*spaces
        def createbutton(name):
            name = centerstr(name)
            not_chosen = self.font.render(name[:25], True, colors['gray'])
            hovering = self.font.render(name[:25], True, colors['red'])
            cur_choice = self.font.render(name[:25], True, colors['white'])
            return Hoverable((sx,y), HAT_LEFTDOWN, not_chosen, hovering, cur_choice)
        per = self.font.size('ABCDEFGHIJKLMNOPQRSTU')[1]
        spacesize, _ = self.font.size(' ')
        #local constants
        col1, col2, hstrt = 0.3, 0.7, 0.2
        w, h = self.screensize
        #creates resolution buttons, places them in the middle of the reslabel
        self.reslabel = self.font.render('Resolutsioon:', True, colors['yellow'])
        diff = self.reslabel.get_width()
        self.reslabelpos = (col1 * w  - diff/2, hstrt*h)
        y = hstrt*h
        sx = col1*w - diff/2
        for pos in defaultsizes:
            y += per
            st = '%d x %d' % pos
            self.hoverables.append(createbutton(st))
        #creates ai_delay buttons, places them in the middle of the delaylabel
        self.delaylabel = self.font.render('AI delay:', True, colors['yellow'])
        diff = self.delaylabel.get_width()
        self.delaylabelpos = (col2*w - diff/2, hstrt*h)
        y = hstrt*h
        sx = col2*w - diff/2
        for delay in delays:
            y += per
            self.hoverables.append(createbutton('%d ms' % delay))
        #start button
        alusta = 'Salvesta'
        hovering = self.lfont.render(alusta, True, colors['red'])
        not_hovering = self.lfont.render(alusta, True, colors['white'])
        x = w/2 - hovering.get_width()/2
##        y = 0.5*h
        y += 2*per
        self.startbutton = Hoverable((x, y), HAT_CENTERED, not_hovering, hovering)
    def draw(self):
        """Draws the OptionsMenu and loops over input until an error condition
            (enter being pressed/some other menu chosen) achieved through
            event_handle"""
        global ai_delay
        chosen1 = defaultsizes.index(self.screensize) if self.screensize in defaultsizes \
                                              else -1
        chosen2 = delays.index(ai_delay) + len(defaultsizes) if ai_delay in delays \
                                              else -1
        last_chosen1 = last_chosen2 = last_hovering = last_active = None
        active_buttons = (self.main,)
        hovering = -1
        ai = 0
        while True:
            if (last_chosen1, last_chosen2, last_hovering, last_active) != \
                (chosen1, chosen2, hovering, active_buttons):
                pygame.display.get_surface().blit(self.get_screencopy(),(0,0))
                self.mini_menu.draw(active_buttons)
                for i, hov in enumerate(self.hoverables):
                    if i in (chosen1, chosen2):
                        hov.draw(2)
                    else:   
                        hov.draw(i == hovering)
                self.startbutton.draw(hovering == len(self.hoverables))
                pygame.display.get_surface().blit(self.label,self.labelpos)
                pygame.display.get_surface().blit(self.reslabel,self.reslabelpos)
                pygame.display.get_surface().blit(self.delaylabel,self.delaylabelpos)
                last_chosen1 = chosen1
                last_chosen2 = chosen2
                last_hovering = hovering
                last_active = active_buttons
                pygame.display.flip()
            event, hovering = self.event_handle(hovering)
            if event == BACK:
                return None
            elif event == CHOSE:
                if hovering < len(defaultsizes):
                    #resolution
                    chosen1 = hovering
                elif hovering < len(self.hoverables):
                    #ai delay
                    chosen2 = hovering
                elif hovering == len(self.hoverables): #start game button:
                    ai_delay = delays[chosen2 - len(defaultsizes)]
                    return CHANGEDSETTINGS, (defaultsizes[chosen1],
                                             ai_delay)
                else: #minimenu
                    return self.handle(hovering - len(self.hoverables) - 1)
            if hovering > len(self.hoverables):
                active_buttons = (self.main, hovering - len(self.hoverables) - 1)
            else:
                active_buttons = (self.main,)
    def event_handle(self, active):
        e = pygame.event.wait()
        pygame.event.post(e)
        for event in pygame.event.get():
            if event.type == QUIT:
                raise exited_game
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return BACK, None
                #navigating by keyboard
                elif event.key == K_RIGHT or event.key == K_DOWN:
                    if active+1 <= len(self.hoverables) + 6:
                        active += 1
                    else:
                        active = 0
                elif event.key == K_LEFT or event.key == K_UP:
                    if active-1 >= 0:
                        active -= 1
                    else:
                        active = len(self.hoverables) + 6
                elif event.key == K_RETURN:
                    return CHOSE, active
            elif event.type == MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                for i, hov in enumerate(self.hoverables):
                    if hov.hovering(pos):
                        return None, i # just hovering
                for i, hov in enumerate(self.mini_menu.buttons):
                    if hov.hovering(pos):
                        return None, i + len(self.hoverables) + 1
                if self.startbutton.hovering(pos):
                    return None, len(self.hoverables)
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i, hov in enumerate(self.hoverables):
                    if hov.hovering(pos):
                        return CHOSE, i #clicked bot
                for i, hov in enumerate(self.mini_menu.buttons):
                    if hov.hovering(pos):
                        return CHOSE, i + len(self.hoverables) + 1#clicked menu
                if self.startbutton.hovering(pos):
                    return CHOSE, len(self.hoverables)#clicked start      
        return None, active
        
class Dimmer(object):
    darken_factor = 200
    filter = (0,0,0)
    def darken(self):
        screen = pygame.display.get_surface()
        screensize = screen.get_size()
        self.buffer = pygame.Surface(screensize)
        self.buffer.blit(screen, (0,0)) # to restore later
        darken=pygame.Surface(screensize)
        darken.fill(self.filter)
        darken.set_alpha(self.darken_factor)
        # safe old clipping rectangle...
        old_clip = screen.get_clip()
        # ..blit over entire screen...
        screen.blit(darken, (0,0))
        # ... and restore clipping
        screen.set_clip(old_clip)
##        pygame.display.flip()
        
    def restore(self):
        pygame.display.get_surface().blit(self.buffer,(0,0))
        pygame.display.flip()
        self.buffer = None
   

if __name__ == "__main__":
    pygame.init()
    size = (930, 700)
##    screen = pygame.display.set_mode((930, 700))
    screen = pygame.display.set_mode(size)
    white = (255,255,255)
    screen.fill(white)
    pygame.display.flip()
    menu = Menu(size,[('a','b')])
    try:
        print menu.show_menu(True)
    finally:
        print 'exiting'
        pygame.quit()

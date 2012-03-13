import pygame

class ScrollingTextArea(object):
    def __init__(self, font, zeropos, maxpos,
                 background = None, color = (255,255,255), spacing = 0.8):
        """font - used font, zeropos - start of the box, maxpos - end of the box,
            background - background color, color - default text color,
            spacing - how big space is between two lines"""
        self.font = font
        self.zeropos = zeropos
        self.maxpos = maxpos
        self.background = background
        self.color = color
        self.spacing = spacing
        self.text = []
        
        self.width = maxpos[0] - zeropos[0]
        self.height = maxpos[1] - zeropos[1]
        self.rowheight = self.font.size('ABCDEFGHIJKLMNOPQRSTUVWXYZ')[1] * self.spacing
        self.maxlines = int(self.height / self.rowheight)
    def reset(self):
        self.text = []
        
    def set_text(self, text, color = None, draw = True):
        if color == None: color = self.color
        self.text = []
        self.add_text(text, color, draw)
        
    def add_text(self, text, color = None, draw = True):
        if color == None: color = self.color
        for line in text.split('\n'):
            self.append_optimal_splitting(line.split(' '), color)
        if len(self.text) > self.maxlines:
            self.text = self.text[len(self.text)-self.maxlines:]
        if draw:
            self.draw()
        

    def append_optimal_splitting(self, spaced, color):
        #optimiseerida.
        if len(spaced) == 0: return
        nline = ' '.join(spaced)
        size = self.font.size(nline)[0]
        i = len(spaced)
        while size > self.width and i > 1:
            i -= 1
            nline = ' '.join(spaced[:i])
            size = self.font.size(nline)[0]
        self.text.append((color, nline))
        self.append_optimal_splitting(spaced[i:], color)

    def draw(self):
        screen = pygame.display.get_surface()
        if self.background != None:
            box = pygame.Surface((self.width, self.height))
            box.fill(self.background)
            pygame.display.get_surface().blit(box, self.zeropos)
        start = 0
        for color, line in self.text:
            rendered = self.font.render(line, True, color)
            screen.blit(rendered, (self.zeropos[0], self.zeropos[1]+start))
            start += self.rowheight
##        print text
##        
##        pygame.display.flip()
       

if __name__ == "__main__":
    import os
    from pygame.locals import *
    pygame.init()
    screen = pygame.display.set_mode((400,400))
##    screen.fill((255,255,255))
    pygame.display.flip()
    font = pygame.font.Font(os.path.join('Fonts','def.ttf'), 23)
    textarea = ScrollingTextArea(font, (30,30), (350,350), (0,0,0))
    textarea.add_text('ololololo 12 45 olenlahe eksju onju shalalalala')
##    textarea.draw()
    pygame.display.flip()
    p = True
    while p:
        for event in pygame.event.get():
            if event.type is KEYDOWN and event.key == K_RETURN:
                textarea.add_text('Mouseover at alala %s' % str(pygame.mouse.get_pos()),(255,0,0))
                pygame.display.flip()
                screen = pygame.display.set_mode((500,500))
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                p = False
                break
##    pygame.quit()

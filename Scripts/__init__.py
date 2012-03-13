import sys
err = sys.stderr

VERTICAL = 0; HORIZONTAL = 1
board = [[False]*12 for _ in xrange(12)]
turn = 0
dx = turn; dy = 1-turn
def fr(x, y):
    return 0 <= x < 12 and 0 <= y < 12 and not board[x][y]
def freeTurn(x, y, turn):
    return (fr(x,y), fr(x+turn,y+1-turn))
def makeMove(x, y):
    global turn, dx, dy
    dx = turn
    dy = 1-turn
    board[x][y] = board[x+dx][y+dy] = True
    turn = 1-turn

            
def getFirst():
    def place(a,b):
        kylg1 = all(freeTurn(a-dy,b-dx,turn))
        kylg2 = all(freeTurn(a+dy,b+dx,turn))
        tipp1 = fr(a-dx, b-dy)
        tipp2 = fr(a+2*dx, b+2*dy)
        up1, up2 = freeTurn(a-2*dy, b-2*dx, turn)
        down1, down2 = freeTurn(a+2*dy, b+2*dx, turn)
        if kylg1 and kylg2: #kyljed
            if not tipp1 and not tipp2: #m6lemad tipud kinni
                if not any((up1,up2,down1,down2)): #m6lemad kaugkyled kinni 
                    unos.append((a,b))
                    return
                elif not any((up1,up2)) or not any((down1,down2)): #yks kaugkylg kinni
                    tres.append((a,b))
                    return
            elif tipp1 or tipp2: #yks tipp kinni
                if not any((up1,up2,down1,down2)): #m6lemad kaugkyled kinni 
                    dos.append((a,b))
                    return
                elif not any((up1,up2)) or not any((down1,down2)): #yks kaugkylg kinni
                    quatro.append((a,b))
                    return
        elif kylg1 and (tipp1 or tipp2) and not any((up1,up2)):
            unos.append((a,b))
            return
        elif kylg2 and (tipp1 or tipp2) and not any((down1, down2)):
            unos.append((a,b))
            return            
        disrupts = ((0,0),(dx,dy),(-dy,-dx),(dx-dy,dy-dx))
        cn = reduce(lambda x,(dx,dy): x+int(all(freeTurn(a+dx,b+dy,1-turn))), disrupts,0)
        disrupt.append((cn, (a,b)))      
            
    global dx, dy
    dx = turn
    dy = 1-turn
    cero = []
    unos = []
    dos = []
    tres = []
    quatro = []
    disrupt = []
    for x in xrange(12):
        for y in xrange(12):
            if all(freeTurn(x,y,turn)):
                place(x,y)
    disrupt.sort(reverse = True, key = lambda x: x[0])
##    print disrupt
##    err.write('%s\n' % disrupt)
    if unos: return unos[0]
    if dos: return dos[0]
    if tres: return tres[0]
    if quatro: return quatro[0]
    
    return disrupt[0][1]
command = sys.stdin.readline().strip()
player = VERTICAL if command == 'start' else HORIZONTAL
opponent = 1-player

while command != 'win' and command != 'loss':
    if command != 'start':
        makeMove(*map(int, command.split()))
    move = getFirst()
    makeMove(*move)
    print '%d %d' % move
    sys.stdout.flush()
    command = sys.stdin.readline().strip()

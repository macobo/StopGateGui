import sys
err = sys.stderr

VERTICAL = 0; HORIZONTAL = 1
board = [[False]*12 for _ in xrange(12)]
turn = 0
dx = turn; dy = 1-turn
def fr(x, y):
    return 0 <= x < 12 and 0 <= y < 12 and not board[x][y]
def freeTurn(x, y, aturn):
    return (fr(x,y), fr(x+aturn,y+1-aturn))
def safeMove(a, b, aturn, outp = False):
    return all(freeTurn(a,b,aturn)) and \
           not any(freeTurn(a+1-aturn,b+turn, aturn)) and \
           not any(freeTurn(a-1+aturn,b-turn, aturn))

def grade():
    global board
    b = [x[:] for x in board]
    c0 = c1 = 0
    for x in xrange(12):
        for y in xrange(12):
            if safeMove(x, y, 0):
                board[x][y] = board[x][y+1] = True
                c0 += 1
            if safeMove(x, y, 1):
                board[x][y] = board[x+1][y] = True
                c1 += 1
    board = b
    return c0, c1



def trymove(a,b, outp = False):
    global turn
    dx = turn; dy = 1-turn
    disrupts = ((0,0),(dx,dy),(-dy,-dx),(dx-dy,dy-dx))
    v = l = 0
    v = reduce(lambda x,(adx,ady): x+int(all(freeTurn(a+adx,b+ady,1-turn))), disrupts, 0)
    l = 1 + int(all(freeTurn(a-dx,b-dy,turn))) + int(all(freeTurn(a+dx,b+dy,turn)))
    kyljed = ((-1,-1),(-1,1),(1,-1),(1,1),(-dy,-dx),(dy,dx))
    board[a][b] = board[a+dx][b+dy] = True
    cn = grade()
    board[a][b] = board[a+dx][b+dy] = False
##    if outp: err.write('==%d:Kaot:%d V-Kaot:%d Safe:%d WasSafe:%s\n' % (turn,l,v,s,safeMove(a,b,turn)))
    return v-l+cn[turn]-cn[1-turn]
def remove(a,b,aturn):
    try:
        del moves[aturn][a*12+b]
    except KeyError: pass
def makeMove(x, y):
    global turn, dx, dy
    trymove(x,y, True)
    dx = turn
    dy = 1-turn
    remove(x,y,turn)
    if all(freeTurn(x+dx,y+dy,turn)):
        remove(x+dx,y+dy,turn)
    if all(freeTurn(x-dx,y-dy,turn)):
        remove(x-dx,y-dy,turn)

    #vastast segavad
    disrupts = ((0,0),(dx,dy),(-dy,-dx),(dx-dy,dy-dx),(2*dx,2*dy),(-2*dx,-2*dy))
    for ax, ay  in disrupts:
        if all(freeTurn(x+ax,y+ay,dy)):
            remove(x+ax,y+ay,dy)
    board[x][y] = board[x+dx][y+dy] = True
    kyljed = ((-1,-1),(-1,1),(1,-1),(1,1),(-dy,-dx),(dy,dx))
    for adx, ady in kyljed:
        if safeMove(x+adx,y+ady,turn):
            remove(x+adx,y+ady,turn)
    
    turn = 1-turn            
def getFirst():
    global turn, moves
    if moves[turn]:
        m = -999
        best = None
        for move in moves[turn]:
            x, y = divmod(move, 12)
            if all(freeTurn(x,y,turn)):
                res = trymove(x,y)
                if res > m:
                    m = res
                    best = (x, y)
        if best:
            return best
    err.write('==Safemove?\n')
    for x in xrange(12):
        for y in xrange(12):
            if all(freeTurn(x,y,player)):
                return (x, y)
    
def makeMoves(player):
    global moves
    moves = [{},{}]
    for x in xrange(12):
        for y in xrange(12):
            if all(freeTurn(x,y,player)):
                moves[player][x*12+y] = True
            if all(freeTurn(x,y,1-player)):
                moves[player][x*12+y] = True

    
command = sys.stdin.readline().strip()
player = VERTICAL if command == 'start' else HORIZONTAL
opponent = 1-player
makeMoves(player)
while command != 'win' and command != 'loss':
    if command != 'start':
        makeMove(*map(int, command.split()))
    move = getFirst()
    makeMove(*move)
    print '%d %d' % move
    sys.stdout.flush()
    command = sys.stdin.readline().strip()

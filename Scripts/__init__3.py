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

def trymove(a,b, outp = False):
    global turn
    dx = turn; dy = 1-turn
    disrupts = ((0,0),(dx,dy),(-dy,-dx),(dx-dy,dy-dx))
    v = reduce(lambda x,(adx,ady): x+int(all(freeTurn(a+adx,b+ady,1-turn))), disrupts, 0)
    l = 1 + int(all(freeTurn(a-dx,b-dy,turn))) + int(all(freeTurn(a+dx,b+dy,turn)))
    kyljed = ((-1,-1),(-1,1),(1,-1),(1,1),(-dy,-dx),(dy,dx))
##    err.write('Me:')
    board[a][b] = board[a+dx][b+dy] = True
    s = reduce(lambda x,(dx,dy): x+int(safeMove(a+dx,b+dy,turn)), kyljed, 0)
    board[a][b] = board[a+dx][b+dy] = False
    if outp: err.write('==%d:Kaot:%d V-Kaot:%d Safe:%d WasSafe:%s\n' % (turn,l,v,s,safeMove(a,b,turn)))
    return v-l+s
def makeMove(x, y):
    global turn, dx, dy
    dx = turn
    dy = 1-turn
    board[x][y] = board[x+dx][y+dy] = True
    turn = 1-turn            
def getFirst():
    global turn
    m = -999
    for x in xrange(12):
        for y in xrange(12):
            if all(freeTurn(x,y,turn)):
                res = trymove(x,y)
                if res > m:
                    m = res
                    best = (x, y)
    return best
def makeMoves(player):
    global moves
    moves = {}
    for x in xrange(12):
        for y in xrange(12):
            if all(freeTurn(x,y,turn)):
                moves[x*12+y] = True

    
command = sys.stdin.readline().strip()
player = VERTICAL if command == 'start' else HORIZONTAL
opponent = 1-player

while command != 'win' and command != 'loss':
    if command != 'start':
        makeMove(*map(int, command.split()))
    try: move = getFirst()
    except: break
    makeMove(*move)
    print '%d %d' % move
    sys.stdout.flush()
    command = sys.stdin.readline().strip()

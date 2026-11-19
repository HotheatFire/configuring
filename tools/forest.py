import random,collections,json,sys
random.seed(31);W,H=56,40
g=[['.']*W for _ in range(H)]
inb=lambda x,y:0<=x<W and 0<=y<H
def setl(pts,ch):
    for (x0,y0),(x1,y1) in zip(pts,pts[1:]):
        x,y=x0,y0
        while True:
            g[y][x]=ch
            if (x,y)==(x1,y1):break
            if x!=x1:x+=1 if x1>x else -1
            elif y!=y1:y+=1 if y1>y else -1
# river & banks
for x in range(W):
    g[30][x]='s';g[31][x]='~';g[32][x]='~';g[33][x]='~';g[34][x]='s'
# hill: cliff ring + plateau
for y in range(16,28):
    for x in range(36,53):
        g[y][x]='C' if (y in(16,17,26,27) or x in(36,37,51,52)) else 'p'
for y in range(23,26):g[y][40]='~'
g[26][40]='W';g[27][40]='W'
for y in range(28,30):
    for x in range(39,42):g[y][x]='~'
g[30][40]='~'
g[22][36]='z';g[22][37]='z'
g[27][45]='V'
# trails
setl([(12,0),(12,12),(45,12),(45,0)],'-')
setl([(12,12),(12,20),(9,20)],'-')
setl([(30,12),(30,30)],'-');g[31][30]='j';g[32][30]='j'
setl([(30,22),(35,22)],'-')
setl([(30,29),(38,29)],'-');g[29][39]='b';g[29][40]='b';g[29][41]='b';setl([(42,29),(45,29),(45,28)],'-')
setl([(38,22),(41,22),(41,21)],'-')
setl([(30,20),(23,20)],'-')
# zones
meadow=lambda x,y:2<=x<=18 and 14<=y<=28
bamboo=lambda x,y:20<=x<=28 and 14<=y<=27
for y in range(H):
    for x in range(W):
        if g[y][x]!='.':continue
        if x in(0,W-1) or y in(0,H-1):g[y][x]='T';continue
        trailN=any(inb(x+a,y+c) and g[y+c][x+a] in '-zjb' for a,c in((1,0),(-1,0),(0,1),(0,-1)))
        r=random.random()
        if meadow(x,y):g[y][x]='T' if (r<.04 and (x<4 or x>16 or y>26)) else ('f' if r<.2 else '.')
        elif trailN:g[y][x]='f' if r<.25 else '.'
        else:g[y][x]='B' if bamboo(x,y) and r<.6 else ('T' if r<.5 else ('f' if r<.62 else '.'))
for y in range(17,26):
    for x in range(38,51):
        if g[y][x]=='p':g[y][x]='T' if random.random()<.12 and abs(x-43)>2 else ('f' if random.random()<.15 else '.')
g[0][12]='-';g[0][45]='-'
for x,y in [(14,6),(10,9),(33,15),(24,11),(47,8),(16,25),(27,29),(48,31-2)]:
    if g[y][x] in '.fTB':g[y][x]='l'
g[1][13]='S';g[1][44]='S';g[13][31]='S'
B=[{'id':'ruin','name':'ရှေးဟောင်း စေတီပျက်','x':42,'y':18,'w':2,'h':3,'style':'ruin'}]
for b in B:
    for j in range(b['y'],b['y']+b['h']):
        for i in range(b['x'],b['x']+b['w']):g[j][i]='H'
WALK=set('.-zjbsf p')
def reach():
    s={(12,0)};q=collections.deque([(12,0)])
    while q:
        x,y=q.popleft()
        for a,c in((1,0),(-1,0),(0,1),(0,-1)):
            X,Y=x+a,y+c
            if inb(X,Y) and (X,Y) not in s and g[Y][X] in WALK:s.add((X,Y));q.append((X,Y))
    return s
s=reach()
need={'village_exit':(45,0),'meadow':(10,20),'jetty':(30,32),'ruin':(43,21),'cave':(45,28),'bamboo':(24,20)}
for k,v in need.items():print(k,v in s)
for y,row in enumerate(g):print('%2d %s'%(y,''.join(row)))
json.dump({'grid':[''.join(r) for r in g],'B':B},open(sys.argv[1],'w'),ensure_ascii=False)

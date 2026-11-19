import sys,json,random,collections
d=json.load(open(sys.argv[1]));G=[list(r) for r in d['grid']];H=len(G);W=len(G[0])
random.seed(7)
inb=lambda x,y:0<=x<W and 0<=y<H
WALK=set('.-=bLrxkmf')
for y in range(H):
    for x in range(W):
        if G[y][x] in 'km':G[y][x]='k' if G[y][x]=='k' else '.'
        if G[y][x] in 'rxL':G[y][x]='.'
B=[]
def free(x,y,w,h):
    return all(inb(i,j) and G[j][i] in '.k' for j in range(y,y+h) for i in range(x,x+w))
def place(id,name,x,y,w,h,style,shop=None,force=False):
    if not force and not free(x,y,w,h):print('BLOCKED',id,x,y);return None
    for j in range(y,y+h):
        for i in range(x,x+w):G[j][i]='H'
    b=dict(id=id,name=name,x=x,y=y,w=w,h=h,style=style)
    if shop:b['shop']=shop
    B.append(b);return b
def findSpot(w,h,anc,fullFront=False,road=False):
    best=None
    for y in range(H-h):
        for x in range(W-w):
            if not free(x,y,w,h):continue
            fx,fy=x+w//2,y+h
            if not inb(fx,fy) or G[fy][fx] not in WALK:continue
            if road and G[fy][fx] not in '-=':continue
            if fullFront and not all(inb(i,fy) and G[fy][i] in WALK for i in range(x,x+w)):continue
            d=abs(x-anc[0])+abs(y-anc[1])
            if best is None or d<best[0]:best=(d,x,y)
    return best[1:] if best else None
def put(id,name,w,h,style,anc,shop=None,**k):
    s=findSpot(w,h,anc,**k);assert s,id;return place(id,name,s[0],s[1],w,h,style,shop)
place('mon','ဘုန်းကြီးကျောင်း',30,2,7,5,'monastery')
place('stupa','မြို့ဦးစေတီ',41,2,2,3,'stupa')
place('market','ရွာဈေး',0,45,8,2,'market','market')
for x in range(0,9):
    if G[20][x]=='.':G[20][x]='-'
put('tea','ဒေါ်စန်းစန်းရဲ့ လက်ဖက်ရည်ဆိုင်',6,3,'teashop',(27,39),'tea',fullFront=True,road=True)
put('store','ကိုဇော်ရဲ့ ကုန်စုံဆိုင်',5,3,'shop',(38,39),'store',road=True)
put('smith','ကိုထွန်းရဲ့ ပန်းပဲဖို',5,3,'smith',(47,39),'smith',road=True)
put('pharmacy','မခိုင်ရဲ့ ဆေးဆိုင်',4,3,'pharmacy',(20,39),'pharmacy',road=True)
put('school','အခြေခံပညာ မူလတန်းကျောင်း',5,3,'school',(14,34))
put('florist','မမြရဲ့ ပန်းနဲ့ မျိုးစေ့ဆိုင်',6,4,'florist',(10,28),'florist')
put('farmyard','ကိုမင်းရဲ့ ကြက်နွားခြံ',7,4,'ranch',(52,50),'livestock')
put('fisher','ဦးကျော်ရဲ့ ငါးဖမ်းအိမ်',5,3,'fisher',(46,12))
put('h4','သူကြီး ဦးလှမောင်ရဲ့ အိမ်',5,4,'headman',(34,30))
place('well','ရပ်ကွက် ရေတွင်း',40,13,1,1,'well') if free(40,13,1,1) else put('well','ရပ်ကွက် ရေတွင်း',1,1,'well',(40,13))
put('zayat','ရွာ့ ဇရပ်',4,2,'zayat',(37,45))
put('banyan','ညောင်ပင်ကြီးနဲ့ နတ်စင်',3,2,'banyan',(57,29))
# houses
styles=['thatch','bamboo','zinc','tile','thatch','bamboo']
n=0
for y in range(H):
    for x in range(W):
        if 25<=x<=53 and y<=10:continue
        if G[y][x]!='.':continue
        if random.random()>.9:continue
        for w in (4,3):
            h=3
            if not free(x,y,w,h):continue
            fx,fy=x+w//2,y+h
            if not inb(fx,fy) or G[fy][fx] not in WALK:continue
            if inb(x-1,y) and G[y][x-1]=='H':continue
            n+=1;place('r%d'%n,'',x,y,w,h,random.choice(styles));break
for b in list(B):
    if not b['id'].startswith('r'):continue
    for j in range(b['y'],b['y']+b['h']):
        for i in (b['x']-1,b['x']+b['w']):
            if inb(i,j) and G[j][i]=='.' and random.random()<.55:G[j][i]='F'
# reachability from west entry (0,20)
def walk(c):return c in WALK or c=='T'and False
seen={(0,20)};q=collections.deque([(0,20)])
while q:
    x,y=q.popleft()
    for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
        X,Y=x+dx,y+dy
        if inb(X,Y) and (X,Y) not in seen and G[Y][X] in WALK:seen.add((X,Y));q.append((X,Y))
print("seen",len(seen),G[20][:10]);bad=[b for b in B if (b['x']+b['w']//2,b['y']+b['h']) not in seen]
for b in bad:
    print('unreachable',b['id'])
    if b['id'].startswith('r'):
        B.remove(b)
        for j in range(b['y'],b['y']+b['h']):
            for i in range(b['x'],b['x']+b['w']):G[j][i]='.'
fronts={(b['x']+b['w']//2,b['y']+b['h']) for b in B}
near=lambda x,y:any(abs(x-a)+abs(y-c)<=1 for a,c in fronts)
for y in range(H):
    for x in range(W):
        if G[y][x]=='k':G[y][x]='T' if random.random()<.3 and not near(x,y) else ('f' if random.random()<.45 else '.')
        elif G[y][x]=='.' and not near(x,y):
            r=random.random()
            road=any(inb(x+a,y+c) and G[y+c][x+a] in '-=' for a,c in((1,0),(-1,0),(0,1),(0,-1)))
            house=any(inb(x+a,y+c) and G[y+c][x+a]=='H' for a,c in((1,0),(-1,0)))
            if house and r<.55:G[y][x]='f'
            elif r<.20:G[y][x]='T'
            elif r<(.45 if road else .32):G[y][x]='f'
def reach():
    s={(0,20)};q=collections.deque([(0,20)])
    while q:
        x,y=q.popleft()
        for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
            X,Y=x+dx,y+dy
            if inb(X,Y) and (X,Y) not in s and G[Y][X] in WALK:s.add((X,Y));q.append((X,Y))
    return s
cellB={(i,j):b for b in B for j in range(b['y'],b['y']+b['h']) for i in range(b['x'],b['x']+b['w'])}
for it in range(80):
    s=reach();bad=[f for f in fronts if f not in s]
    if not bad:break
    tx,ty=bad[0];prev={(0,20):None};q=collections.deque([(0,20)])
    while q:
        c=q.popleft()
        if c==(tx,ty):break
        for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
            X,Y=c[0]+dx,c[1]+dy
            own=cellB.get((X,Y))
            if inb(X,Y) and (X,Y) not in prev and (G[Y][X] in WALK or G[Y][X] in 'TF' or (own and own['id'][0]=='r' and own['id']!='farmyard')):prev[(X,Y)]=c;q.append((X,Y))
    c=(tx,ty)
    while c:
        if G[c[1]][c[0]] in 'TF':G[c[1]][c[0]]='.'
        own=cellB.get(c)
        if own and own in B and own['id'][0]=='r' and own['id']!='farmyard':
            B.remove(own)
            for j in range(own['y'],own['y']+own['h']):
                for i in range(own['x'],own['x']+own['w']):G[j][i]='.';cellB.pop((i,j),None)
        c=prev.get(c)
    fronts={(b['x']+b['w']//2,b['y']+b['h']) for b in B}
for sx,sy in((1,21),(1,19),(26,56),(24,56)):
    if G[sy][sx] in '.f' and not any(a for a in []):G[sy][sx]='S'
_r=reach();print('blocked fronts left',[(b['id'],b['x']+b['w']//2,b['y']+b['h']) for b in B if (b['x']+b['w']//2,b['y']+b['h']) not in _r])
print('houses',n,'buildings',len(B))
for i,row in enumerate(G):print('%2d %s'%(i,''.join(row)))
json.dump({'grid':[''.join(r) for r in G],'B':B},open(sys.argv[2],'w'),ensure_ascii=False)

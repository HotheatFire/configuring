import sys,json
d=json.load(open(sys.argv[1]));G=d['grid'];B=d['B'];fo=json.load(open(sys.argv[2]))
H=len(G);W=len(G[0])
WALK=set('.-=bf')
houses=[b for b in B if b['id'].startswith('r')]
front=lambda b:(b['x']+b['w']//2,b['y']+b['h'])
fam={'h1':((9,20),'ဒေါ်အေးရဲ့ အိမ်')}
used=set();HOMES={}
for fid,(anc,name) in fam.items():
    best=min((b for b in houses if b['id'] not in used),key=lambda b:abs(front(b)[0]-anc[0])+abs(front(b)[1]-anc[1]))
    used.add(best['id']);best['id']=fid;best['name']=name
    if fid=='h1':best['extra']='loom'
    f=front(best);HOMES[fid]=['village',f[0],f[1]]
for b in B:
    b['map']='village'
    if b['id'] in('tea','store','smith','mon','pharmacy','school','market','florist','farmyard','fisher','h4'):
        f=front(b);HOMES[b['id']]=['village',f[0],f[1]]
def ok(x,y):return 0<=x<W and 0<=y<H and G[y][x] in WALK
P={}
def add(k,cells,m='village'):
    good=[[m,x,y] for x,y in cells if ok(x,y)] if m=='village' else [[m,x,y] for x,y in cells]
    assert good,k;P[k]=good
fb=lambda id:next(b for b in B if b['id']==id)
def around(id):
    b=fb(id);fx,fy=front(b);return [(fx-2,fy),(fx+2,fy),(fx-1,fy),(fx+1,fy),(fx-3,fy+1),(fx+3,fy+1)]
for k in('market','tea','store','smith','pharmacy','school','mon','zayat','banyan','florist','farmyard','fisher','h4'):add(k,around(k))
tb=fb('tea');tf=front(tb);add('teaseat',[(x,tb['y']+tb['h']) for x in range(tb['x'],tb['x']+tb['w']) if x!=tf[0]])
add('stupa',[(40,5),(44,5),(41,5),(43,5)])
add('canal',[(28,11),(33,11),(38,11),(46,11),(50,11),(30,11)])
add('park',[(x,y) for y in range(49,55) for x in range(14,19)][::3])
add('square',[(41,44),(39,44),(43,47),(36,48),(45,48),(41,47)])
for k,v in {'farm':[(12,8)],'bin':[(9,7)],'farmhouse':[(6,7)],'stall':[(25,20),(23,20)],'yard':[(20,13)],'pond':[(25,6)]}.items():add(k,v,'farm')
FG=fo['grid']
fok=lambda x,y:FG[y][x] in '.-fjsz'
for k,v in {'meadow':[(8,20),(10,22),(14,24),(6,17),(16,18)],'river':[(24,30),(16,30),(36,30)],'jetty':[(30,32)],'ruin':[(42,22),(44,22)],'bamboo':[(24,20)],'cave':[(45,28)]}.items():
    for x,y in v:assert fok(x,y),(k,x,y,FG[y][x])
    add(k,v,'forest')
out=['const TOWN=%s;'%json.dumps(G),'const FOREST=%s;'%json.dumps(FG),
 'const BUILDINGS=%s.map(b=>({...b,name:b.name||"ရွာသား အိမ်"})).concat(%s.map(b=>({...b,map:"forest"})));'%(json.dumps(B,ensure_ascii=False),json.dumps(fo['B'],ensure_ascii=False)),
 'const HOMES=%s;'%json.dumps(HOMES),'const PLACES=%s;'%json.dumps(P)]
open(sys.argv[3],'w').write('\n'.join(out)+'\n')
print('ok',HOMES)

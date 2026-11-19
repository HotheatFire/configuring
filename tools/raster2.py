import sys,json,math,xml.etree.ElementTree as ET
r=ET.parse(sys.argv[1]).getroot()
W,H=int(sys.argv[3]),int(sys.argv[4]);S=float(sys.argv[5])
LAT0,LON0=float(sys.argv[6]),float(sys.argv[7]);ANG=math.radians(13.5)
ca,sa=math.cos(ANG),math.sin(ANG)
def tl(lat,lon):
    x=(lon-LON0)*106470;y=(lat-LAT0)*110600
    xr=x*ca+y*sa;yr=-x*sa+y*ca
    return (xr/S+W/2,-yr/S+H/2)
nodes={n.get('id'):(float(n.get('lat')),float(n.get('lon'))) for n in r.iter('node')}
ways=[]
for w in r.iter('way'):
    tags={t.get('k'):t.get('v') for t in w.iter('tag')}
    ways.append((tags,[tl(*nodes[nd.get('ref')]) for nd in w.iter('nd') if nd.get('ref') in nodes]))
pois=[]
for n in r.iter('node'):
    tags={t.get('k'):t.get('v') for t in n.iter('tag')}
    if tags:pois.append((tags,tl(float(n.get('lat')),float(n.get('lon')))))
g=[['.']*W for _ in range(H)]
inb=lambda x,y:0<=x<W and 0<=y<H
def snap(pts):
    out=[list(p) for p in pts]
    for i in range(len(out)-1):
        a,b=out[i],out[i+1];dx,dy=b[0]-a[0],b[1]-a[1]
        ang=abs(math.degrees(math.atan2(dy,dx)))%90
        if ang<14 or ang>76:
            if abs(dx)>abs(dy):m=(a[1]+b[1])/2;a[1]=b[1]=m
            else:m=(a[0]+b[0])/2;a[0]=b[0]=m
    return out
def line(pts,ch,wid=1,over=None):
    for (x0,y0),(x1,y1) in zip(pts,pts[1:]):
        n=int(max(abs(x1-x0),abs(y1-y0))*3)+1
        for i in range(n+1):
            x=x0+(x1-x0)*i/n;y=y0+(y1-y0)*i/n
            for dx in range(wid):
                for dy in range(wid):
                    X,Y=int(math.floor(x))+dx,int(math.floor(y))+dy
                    if inb(X,Y):
                        c=g[Y][X]
                        g[Y][X]=over.get(c,ch) if over else ch
def poly(pts,ch):
    if len(pts)<3:return
    ys=[p[1] for p in pts]
    for Y in range(max(0,int(min(ys))),min(H,int(max(ys))+1)):
        yc=Y+.5;xs=[]
        for (x0,y0),(x1,y1) in zip(pts,pts[1:]+pts[:1]):
            if (y0<=yc<y1) or (y1<=yc<y0):xs.append(x0+(yc-y0)*(x1-x0)/(y1-y0))
        xs.sort()
        for a,b in zip(xs[::2],xs[1::2]):
            for X in range(max(0,int(a+.5)),min(W,int(b+.5))):g[Y][X]=ch
for t,p in ways:
    if t.get('leisure')=='park':poly(p,'k')
    if t.get('amenity')=='marketplace':poly(p,'m')
for t,p in ways:
    if t.get('natural')=='water':poly(p,'~')
    if 'waterway' in t:line(snap(p),'~',2)
for t,p in ways:
    if t.get('railway')=='platform':poly(p,'L') if len(p)>3 else line(p,'L',2)
for t,p in ways:
    if t.get('railway')=='rail':line(p,'r')
keep=('tertiary','residential','unclassified')
for t,p in ways:
    hw=t.get('highway')
    if hw=='tertiary':line(snap(p),'=',2,over={'~':'b','r':'x','L':'L'})
    elif hw in ('residential','unclassified'):line(snap(p),'-',1,over={'~':'b','r':'x','L':'L','=':'='})
lm={}
for t,p in pois:
    k=None
    if t.get('railway')=='station':k='S'
    elif t.get('amenity')=='place_of_worship':k='P'
    elif t.get('shop')=='tea':k='T'
    elif t.get('amenity')=='school':k='E'
    elif t.get('shop')=='car_parts':k='A'
    elif t.get('shop')=='convenience':k='C'
    elif t.get('amenity')=='clinic':k='+'
    elif t.get('amenity')=='marketplace':k='M'
    elif t.get('amenity')=='townhall':k='H'
    if k:
        X,Y=int(p[0]),int(p[1])
        lm.setdefault(k,[]).append((X,Y))
blds=[]
for t,p in ways:
    if 'building' in t and len(p)>2:
        xs=[q[0] for q in p];ys=[q[1] for q in p];blds.append((min(xs),min(ys),max(xs),max(ys),t.get('building'),t.get('name')))
for t,p in ways:
    if t.get('amenity')=='place_of_worship':
        xs=[q[0] for q in p];ys=[q[1] for q in p];lm.setdefault('Pw',[]).append((sum(xs)/len(xs),sum(ys)/len(ys)))
show=[r[:] for r in g]
for k,v in lm.items():
    for X,Y in v:
        X,Y=int(X),int(Y)
        if inb(X,Y):show[Y][X]=k[0]
for i,row in enumerate(show):print('%2d %s'%(i,''.join(row)))
print({k:[(round(a,1),round(b,1)) for a,b in v if inb(int(a),int(b))] for k,v in lm.items()})
print('blds in view',sum(1 for b in blds if inb(int(b[0]),int(b[1]))))
json.dump({'grid':[''.join(r) for r in g],'lm':lm,'blds':blds,'rail':[p for t,p in ways if t.get('railway')=='rail']},open(sys.argv[2],'w'))

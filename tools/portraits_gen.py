import json,html
def shade(hexc,f):
    h=hexc.lstrip('#');r,g,b=[int(h[i:i+2],16) for i in (0,2,4)]
    c=lambda v:max(0,min(255,int(v*f)))
    return '#%02x%02x%02x'%(c(r),c(g),c(b))
L='#3a2418'
def eyes(p):
    out=''
    if p.get('closed'):
        for x in (98,142):out+=f'<path d="M{x-14} 142 Q{x} 152 {x+14} 142" fill="none" stroke="{L}" stroke-width="3" stroke-linecap="round"/>'
        return out
    iris=p.get('iris','#6a3a1e');fem=p.get('fem')
    for x in (98,142):
        out+=f'<ellipse cx="{x}" cy="142" rx="14" ry="12.5" fill="#fffaf2"/>'
        out+=f'<ellipse cx="{x}" cy="143" rx="9.5" ry="11.5" fill="{iris}"/><ellipse cx="{x}" cy="139" rx="9.5" ry="6" fill="{shade(iris,.6)}" opacity=".7"/>'
        out+=f'<ellipse cx="{x}" cy="144" rx="4.5" ry="6.5" fill="#1a0e08"/><ellipse cx="{x}" cy="150" rx="6" ry="3" fill="{shade(iris,1.5)}" opacity=".6"/>'
        out+=f'<circle cx="{x+4}" cy="137" r="3.4" fill="#fff"/><circle cx="{x-4}" cy="148" r="1.6" fill="#fff"/>'
        side=-1 if x<120 else 1
        out+=f'<path d="M{x-16} 140 Q{x} 124 {x+16} 139" fill="none" stroke="{L}" stroke-width="{4 if fem else 3.4}" stroke-linecap="round"/>'
        if fem:out+=f'<path d="M{x+16*side} 139 l{5*side} -4" stroke="{L}" stroke-width="3" stroke-linecap="round"/>'
        out+=f'<path d="M{x-10} 155 Q{x} 157 {x+10} 155" fill="none" stroke="{shade(L,1.4)}" stroke-width="1.4" opacity=".7"/>'
    if p.get('old'):
        for x in (98,142):
            s=-1 if x<120 else 1
            out+=f'<path d="M{x+18*s} 136 l{5*s} -2 M{x+18*s} 142 l{6*s} 0" stroke="{shade(p["skin"],.75)}" stroke-width="1.4" stroke-linecap="round"/>'
    return out
def brows(p):
    c=p.get('hc','#1e1612');o=''
    for x in (98,142):
        s=-1 if x<120 else 1
        if p.get('smug') and x>120:o+=f'<path d="M{x-12} 120 Q{x} 112 {x+13} 117" fill="none" stroke="{c}" stroke-width="3.4" stroke-linecap="round"/>'
        else:o+=f'<path d="M{x-12} {121 if s<0 else 119} Q{x} {113} {x+12} {119 if s<0 else 121}" fill="none" stroke="{c}" stroke-width="3.2" stroke-linecap="round"/>'
    return o
def mouth(p):
    if p.get('smug'):return f'<path d="M110 182 Q122 186 133 177" fill="none" stroke="{L}" stroke-width="2.4" stroke-linecap="round"/>'
    if p.get('open'):return f'<path d="M108 179 Q120 194 132 179 Z" fill="#a8423a" stroke="{L}" stroke-width="2"/><path d="M113 186 Q120 191 127 186" fill="#e88a7a"/>'
    return f'<path d="M110 180 Q120 188 130 180" fill="none" stroke="{L}" stroke-width="2.4" stroke-linecap="round"/>'
FACE="M70 128 C70 84 94 66 120 66 C146 66 170 84 170 128 C170 166 150 196 120 206 C90 196 70 166 70 128 Z"
def hair_back(p):
    c=p.get('hc','#1e1612');h=p.get('hair')
    if h=='bun':return f'<circle cx="{p.get("bunx",120)}" cy="{p.get("buny",50)}" r="25" fill="{c}" stroke="{L}" stroke-width="2"/><path d="M{p.get("bunx",120)-14} {p.get("buny",50)-8} q14 -10 26 2" fill="none" stroke="{shade(c,1.6)}" stroke-width="2.5" opacity=".6"/>'
    if h=='long':return f'<path d="M66 120 C60 190 74 236 92 246 L148 246 C166 236 180 190 174 120 Z" fill="{c}"/>'
    return ''
def hair_front(p):
    c=p.get('hc','#1e1612');h=p.get('hair');hi=shade(c,1.7)
    if h=='short':return f'<path d="M66 132 C58 72 94 48 122 50 C152 50 184 72 174 132 C170 108 162 96 154 90 C150 98 140 102 132 96 C126 104 112 104 104 96 C96 104 84 104 80 98 C74 108 69 118 66 132 Z" fill="{c}" stroke="{L}" stroke-width="2"/><path d="M96 62 Q120 54 146 62" fill="none" stroke="{hi}" stroke-width="3" opacity=".5"/>'
    if h=='slick':return f'<path d="M66 130 C58 72 94 50 124 50 C156 50 182 72 174 130 C168 106 160 92 150 86 C130 92 104 84 92 78 C80 92 70 108 66 130 Z" fill="{c}" stroke="{L}" stroke-width="2"/><path d="M92 78 Q118 70 150 86" fill="none" stroke="{hi}" stroke-width="2.5" opacity=".6"/><path d="M104 64 Q128 58 158 70" fill="none" stroke="{hi}" stroke-width="2" opacity=".45"/>'
    if h in('bun','long'):return f'<path d="M66 140 C56 76 92 50 120 50 C150 50 184 76 174 140 C172 116 164 100 152 92 C138 100 120 98 116 90 C108 100 92 102 82 96 C74 108 69 122 66 140 Z" fill="{c}" stroke="{L}" stroke-width="2"/><path d="M90 66 Q120 56 150 66" fill="none" stroke="{hi}" stroke-width="3" opacity=".5"/>'
    if h=='shaved':return f'<path d="M74 110 C76 78 98 64 120 64 C142 64 164 78 166 110 C150 96 90 96 74 110 Z" fill="{shade(p["skin"],.88)}" opacity=".7"/>'
    return ''
def headwear(p):
    w=p.get('head');o=''
    if w=='gaung':
        c=p['hw'];d=shade(c,.72);li=shade(c,1.25)
        o+=f'<path d="M64 112 C62 70 92 50 120 50 C150 50 178 70 176 112 C150 100 92 100 64 112 Z" fill="{c}" stroke="{L}" stroke-width="2"/>'
        for k in range(3):o+=f'<path d="M{70+k*4} {104-k*14} Q120 {88-k*16} {170-k*4} {104-k*14}" fill="none" stroke="{d}" stroke-width="2.2"/>'
        o+=f'<path d="M66 100 C44 92 38 72 52 62 C56 76 66 82 76 84 Z" fill="{li}" stroke="{L}" stroke-width="2"/><path d="M52 66 Q58 78 72 84" stroke="{d}" stroke-width="1.6" fill="none"/>'
    if w=='kamauk':
        o+=f'<path d="M24 112 L120 30 L216 112 Q120 124 24 112 Z" fill="#d8b46a" stroke="{L}" stroke-width="2.2"/>'
        for k in range(-4,5):o+=f'<path d="M120 32 L{120+k*22} {114 if abs(k)<4 else 112}" stroke="#a8843a" stroke-width="1.4"/>'
        o+=f'<path d="M24 112 Q120 124 216 112" fill="none" stroke="#8a6a2a" stroke-width="3"/><circle cx="120" cy="32" r="4" fill="#8a6a2a"/>'
    if w=='band':
        o+=f'<path d="M66 108 Q120 92 174 108 L174 118 Q120 102 66 118 Z" fill="{p["hw"]}" stroke="{L}" stroke-width="2"/><path d="M174 110 l18 -8 l-4 12 l10 2 l-22 2 Z" fill="{p["hw"]}" stroke="{L}" stroke-width="1.6"/>'
    if w=='nurse':
        o+=f'<path d="M84 74 Q120 52 156 74 L150 92 Q120 84 90 92 Z" fill="#fff" stroke="{L}" stroke-width="2"/><rect x="116" y="68" width="8" height="16" fill="#e2402f"/><rect x="112" y="72" width="16" height="8" fill="#e2402f"/>'
    if w=='scarf':
        c=p['hw'];o+=f'<path d="M62 132 C54 70 92 46 120 46 C150 46 186 70 178 132 C170 104 156 92 120 90 C84 92 70 104 62 132 Z" fill="{c}" stroke="{L}" stroke-width="2"/><path d="M80 70 Q120 56 160 70" fill="none" stroke="{shade(c,.8)}" stroke-width="2"/><path d="M164 56 q20 -6 22 10 q-12 -4 -20 2 Z" fill="{c}" stroke="{L}" stroke-width="1.6"/>'
    return o
def flowers(p):
    o='';bx,by=p.get('bunx',120),p.get('buny',50)
    if p.get('jasmine'):
        for k in range(9):
            import math;a=math.pi*(0.9+k*0.14);x=bx+27*math.cos(a);y=by+27*math.sin(a)*0.6+10
            o+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.6" fill="#fffdf4" stroke="#c8c0a0" stroke-width="1"/>'
    if p.get('flower'):
        fx,fy=bx+22,by+12;c=p['flower']
        for k in range(5):
            import math;a=k*2*math.pi/5;o+=f'<ellipse cx="{fx+7*math.cos(a):.1f}" cy="{fy+7*math.sin(a):.1f}" rx="5" ry="4" fill="{c}" stroke="{shade(c,.7)}" stroke-width="1" transform="rotate({k*72} {fx+7*math.cos(a):.1f} {fy+7*math.sin(a):.1f})"/>'
        o+=f'<circle cx="{fx}" cy="{fy}" r="3" fill="{shade(c,.6)}"/>'
    return o
def outfit(p):
    o=p['outfit'];c=p.get('oc','#f4f0e6');d=shade(c,.82);sk=p['skin']
    body="M14 300 C22 252 64 232 120 232 C176 232 218 252 226 300 Z"
    s=f'<path d="{body}" fill="{c}" stroke="{L}" stroke-width="2.4"/>'
    if o=='taikpon':s+=f'<path d="M104 232 L104 220 L136 220 L136 232" fill="{c}" stroke="{L}" stroke-width="2"/><path d="M120 236 Q150 250 168 300" fill="none" stroke="{d}" stroke-width="2.4"/>'+''.join(f'<circle cx="{126+k*9}" cy="{246+k*14}" r="3" fill="#e2c86a" stroke="{L}" stroke-width="1"/>' for k in range(4))+f'<path d="M30 300 C36 270 52 258 70 252" fill="none" stroke="{d}" stroke-width="2"/>'
    if o=='shirt':s+=f'<path d="M106 232 L106 222 L134 222 L134 232" fill="{c}" stroke="{L}" stroke-width="2"/><path d="M120 234 L120 300" stroke="{d}" stroke-width="2"/>'+''.join(f'<circle cx="120" cy="{246+k*16}" r="2.6" fill="#fff" stroke="{shade(c,.6)}" stroke-width="1"/>' for k in range(4))
    if o=='blouse':s+=f'<path d="M104 232 Q120 244 140 234" fill="none" stroke="{d}" stroke-width="2"/><path d="M120 240 Q132 258 150 300" fill="none" stroke="{d}" stroke-width="2.2"/>'+''.join(f'<circle cx="{124+k*7}" cy="{250+k*12}" r="2.4" fill="#f2c14e" stroke="{L}" stroke-width=".8"/>' for k in range(4))
    if p.get('shawl'):sh=p['shawl'];s+=f'<path d="M24 300 C34 262 60 244 84 238 C70 262 66 284 70 300 Z" fill="{sh}" stroke="{L}" stroke-width="2"/><path d="M216 300 C206 262 180 244 156 238 C170 262 174 284 170 300 Z" fill="{sh}" stroke="{L}" stroke-width="2"/>'
    if o=='robe':
        s=f'<path d="{body}" fill="{sk}" stroke="{L}" stroke-width="2.4"/><path d="M14 300 C22 252 64 232 112 232 C140 236 170 260 190 300 Z" fill="{c}" stroke="{L}" stroke-width="2.4"/><path d="M60 246 Q120 250 176 296" fill="none" stroke="{d}" stroke-width="2.4"/><path d="M40 270 Q90 266 150 300" fill="none" stroke="{d}" stroke-width="2"/>'
    if o=='suit':s+=f'<path d="M100 232 L120 300 L140 232 Z" fill="#fff" stroke="{L}" stroke-width="2"/><path d="M114 240 L126 240 L124 290 L120 298 L116 290 Z" fill="#b8302a" stroke="{L}" stroke-width="1.6"/><path d="M100 232 L120 290 M140 232 L120 290" stroke="{L}" stroke-width="2.2" fill="none"/>'
    if o=='tank':s=f'<path d="{body}" fill="{sk}" stroke="{L}" stroke-width="2.4"/><path d="M70 300 L76 240 Q120 260 164 240 L170 300 Z" fill="{c}" stroke="{L}" stroke-width="2.2"/><path d="M84 300 L88 262 Q120 272 152 262 L156 300 Z" fill="#8a5a30" stroke="{L}" stroke-width="2"/><circle cx="96" cy="266" r="2.4" fill="#d8c08a"/><circle cx="144" cy="266" r="2.4" fill="#d8c08a"/>'
    return s
def svg(p,gid='g'):
    sk=p['skin'];bg=p['bg'];o=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 300" width="240" height="300">'
    o+=f'<defs><radialGradient id="{gid}" cx="50%" cy="42%" r="70%"><stop offset="0" stop-color="{shade(bg,1.22)}"/><stop offset="1" stop-color="{bg}"/></radialGradient></defs><rect width="240" height="300" fill="url(#{gid})"/>'
    for k in range(5):o+=f'<path d="M{k*56-6} 300 a20 20 0 0 1 40 0" fill="none" stroke="#fff" stroke-opacity=".28" stroke-width="2.4"/><path d="M{k*56+6} 300 a8 8 0 0 0 16 0" fill="none" stroke="#fff" stroke-opacity=".28" stroke-width="2"/>'
    o+=f'<circle cx="120" cy="140" r="98" fill="#fff" opacity=".18"/>'
    o+=hair_back(p)
    o+=f'<rect x="105" y="190" width="30" height="40" fill="{shade(sk,.86)}" stroke="{L}" stroke-width="2"/>'
    o+='<g transform="translate(0,-10)">'+outfit(p)+'</g>'
    o+=f'<ellipse cx="68" cy="142" rx="8" ry="12" fill="{sk}" stroke="{L}" stroke-width="2"/><ellipse cx="172" cy="142" rx="8" ry="12" fill="{sk}" stroke="{L}" stroke-width="2"/>'
    if p.get('ear'):o+=f'<circle cx="68" cy="156" r="3.4" fill="#f2c14e" stroke="{L}" stroke-width="1"/><circle cx="172" cy="156" r="3.4" fill="#f2c14e" stroke="{L}" stroke-width="1"/>'
    o+=f'<path d="{FACE}" fill="{sk}" stroke="{L}" stroke-width="2.4"/>'
    o+=f'<path d="M78 174 C90 196 108 202 120 204 C108 196 92 188 78 174 Z" fill="{shade(sk,.9)}" opacity=".3"/>'
    if p.get('thanaka'):
        for x in (90,150):o+=f'<circle cx="{x}" cy="166" r="15" fill="#f2e2a8" opacity=".9"/>'+''.join(f'<path d="M{x-10+k*5} 156 l3 20" stroke="#e0c880" stroke-width="1.2" opacity=".8"/>' for k in range(5))
    o+=f'<ellipse cx="88" cy="170" rx="9" ry="5" fill="#f08a8a" opacity=".35"/><ellipse cx="152" cy="170" rx="9" ry="5" fill="#f08a8a" opacity=".35"/>'
    o+=eyes(p)+brows(p)
    o+=f'<path d="M121 158 Q124 166 118 168" fill="none" stroke="{shade(sk,.62)}" stroke-width="2" stroke-linecap="round"/>'
    o+=mouth(p)
    if p.get('old'):o+=f'<path d="M96 104 Q120 100 144 104" fill="none" stroke="{shade(sk,.78)}" stroke-width="1.4"/><path d="M102 176 q-4 6 -2 12 M138 176 q4 6 2 12" fill="none" stroke="{shade(sk,.75)}" stroke-width="1.4"/>'
    if p.get('beard'):o+=f'<path d="M104 176 Q120 168 136 176 Q128 172 120 175 Q112 172 104 176 Z" fill="{p["hc"]}" stroke="{L}" stroke-width="1.2"/><path d="M112 192 Q120 214 128 192 Q120 198 112 192 Z" fill="{p["hc"]}" stroke="{L}" stroke-width="1.2"/>'
    if p.get('stubble'):o+=''.join(f'<circle cx="{104+(k*7)%34}" cy="{190+(k*5)%12}" r=".9" fill="{shade(sk,.6)}"/>' for k in range(16))
    o+=hair_front(p)+headwear(p)+flowers(p)
    if p.get('glasses'):o+=f'<g fill="none" stroke="#3a3030" stroke-width="2.4"><circle cx="98" cy="142" r="17"/><circle cx="142" cy="142" r="17"/><path d="M115 140 Q120 136 125 140 M81 138 L70 134 M159 138 L170 134"/></g><path d="M86 132 l6 -5 M130 132 l6 -5" stroke="#fff" stroke-width="2" opacity=".7"/>'
    return o+'</svg>'
P={
 'me':dict(skin='#e8b48a',hair='short',hc='#1e1612',head='kamauk',outfit='shirt',oc='#f6f2e8',bg='#bfe0a0',open=1,iris='#5a3a1e'),
 'hla':dict(skin='#dca476',hair='short',hc='#8a8a8a',head='gaung',hw='#c86a7a',outfit='taikpon',oc='#fbf8f0',old=1,beard=1,bg='#a8c878'),
 'aye':dict(skin='#dca47a',hair='bun',hc='#a8a8a8',outfit='blouse',oc='#f0e4cc',shawl='#7a4a3a',old=1,thanaka=1,jasmine=1,glasses=1,ear=1,fem=1,bg='#e8d4b0'),
 'mya':dict(skin='#ecb890',hair='bun',hc='#1e1612',outfit='blouse',oc='#fbe2c6',shawl='#2f7a5a',thanaka=1,flower='#f6c829',jasmine=1,ear=1,fem=1,open=1,bg='#f2c878',bunx=128),
 'san':dict(skin='#dca070',hair='bun',hc='#2a1e16',outfit='blouse',oc='#f2c4c4',shawl='#8a2a3a',thanaka=1,flower='#e2402f',ear=1,fem=1,bg='#e8a888',bunx=126),
 'zaw':dict(skin='#d09a68',hair='short',hc='#1e1612',outfit='shirt',oc='#8ab04a',glasses=1,bg='#d8e8a8',open=1),
 'tun':dict(skin='#b8805a',hair='short',hc='#1e1612',head='band',hw='#d8433a',outfit='tank',oc='#5a5a5a',bg='#f0a868',stubble=1),
 'khine':dict(skin='#eab890',hair='bun',hc='#3a2418',head='nurse',outfit='blouse',oc='#ffffff',thanaka=1,ear=1,fem=1,bg='#c0e0e8',buny=56),
 'min':dict(skin='#c98e5c',hair='short',hc='#1e1612',head='kamauk',outfit='shirt',oc='#ece4cc',bg='#c8e080',open=1),
 'kyaw':dict(skin='#b8805a',hair='short',hc='#7a7a7a',head='kamauk',outfit='shirt',oc='#c8b890',old=1,stubble=1,bg='#98c4e0'),
 'monk':dict(skin='#d8a070',hair='shaved',outfit='robe',oc='#a8402a',closed=1,bg='#f0d088'),
 'rep':dict(skin='#e0a878',hair='slick',hc='#14100c',outfit='suit',oc='#34343c',glasses=1,smug=1,bg='#aab0c0'),
 'khin':dict(skin='#dca070',head='scarf',hw='#f0c64a',outfit='blouse',oc='#f0a8c0',thanaka=1,ear=1,fem=1,old=1,bg='#f4d0dc'),
}
json.dump({k:svg(v,'g_'+k) for k,v in P.items()},open('svgs.json','w'))
print('ok',len(P))

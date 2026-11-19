import re,html
s=open('/home/claude/configuring/shwe-pan-farm.html').read()
a=s.index('/* scenes */');b=s.index('function drawThingyan')
blk=s[a:b]
NAMES={'hla':'ဦးလှမောင်','aye':'ဒေါ်အေး','min':'ကိုမင်း','kyaw':'ဦးကျော်','zaw':'ကိုဇော်','tun':'ကိုထွန်း','rep':'ကိုဝင်းနိုင်','pc':'ကျွန်တော် (MC)','me':'ကိုယ့်အတွေး','nar':'ဇာတ်ကြောင်း'}
SC=[('introScene','၁။ ဦးလှမောင် စာအိတ်ပေး','နေ့ ၁ · ခြံ · ဂိမ်းစစချင်း'),
('dealerScene','၂။ ကိုဝင်းနိုင် ပထမဆုံး လာ','နေ့ ၅+ · ခြံ · မနက် ၈ – ညနေ ၅'),
('ayeScene','၃။ ဒေါ်အေးရဲ့ ပုံပြင်','ဒေါ်အေးနဲ့ စကားပြောရင် (အဘိုးအကြောင်း quest လုပ်နေစဉ်)'),
('GP','၄။ ကိုမင်း / ဦးကျော် ဆီက သဲလွန်စ','သူတို့နဲ့ စကားပြောရင်'),
('stoneScene','၅။ ညောင်ပင်ရင်းက ကျောက်တုံး','ညောင်ပင် အရှေ့ဘက်မှာ B နှိပ်'),
('ruinScene','၆။ စေတီပျက်','စေတီပျက်မှာ B နှိပ် → အခန်း ၁ ပြီး'),
('zawLanternScene','၇။ ကိုဇော့်ဆိုင် မီးအိမ်','မီးအိမ် ဝယ်ပြီးချိန်'),
('ch2Scene','၈။ အခန်း ၂ စ','နေ့ ၁၁+'),
('altarScene','၉။ ဂူထဲ ဆင်းတုတော်','ဂူအတွင်းဆုံး'),
('bridgeScene','၁၀။ တံတား ပြင်','ထင်း ၁၀ ချောင်းနဲ့ တံတားနားမှာ'),
('dealer2Scene','၁၁။ ကိုဝင်းနိုင် ပြန်လာ','နေ့ ၁၇+ · ခြံ · ညနေ')]
def fn(name):
  i=blk.index('function '+name+'(');j=blk.find('\nasync function',i+5);k=blk.find('\nconst ',i+5)
  ends=[x for x in (j,k) if x>0];return blk[i:min(ends) if ends else len(blk)]
pat=re.compile(r"(say|choose)\('(\w+)',\s*(`(?:[^`\\]|\\.)*`|'(?:[^'\\]|\\.)*')(?:,\s*(\[[^\]]*\]))?")
def regions(code):
  out=[]
  for key,lab in (('if(c===0){','A'),('if(c===1){','B'),('else{','B'),('else await','B')):
    i=code.find(key)
    while i>=0:
      if key=='else await':out.append((lab,i,code.find(';',code.find("')",i))+1))
      else:
        j=i+len(key);d=1
        while d and j<len(code):
          if code[j]=='{':d+=1
          elif code[j]=='}':d-=1
          j+=1
        out.append((lab,i,j))
      i=code.find(key,i+1)
  return out
def lines(code):
  out=[]
  for m in pat.finditer(code):
    kind,who,txt,opts=m.groups();t=txt[1:-1]
    t=re.sub(r"\$\{[^}]*\}","…",t)
    br=''
    for lab,a0,a1 in regions(code):
      if a0<=m.start()<a1:br=lab
    out.append((who,t,br))
    if kind=='choose' and opts:
      ops=re.findall(r"'((?:[^'\\]|\\.)*)'",opts)
      out.append(('CH',ops,''))
  return out
def row(who,t,br):
  if who=='CH':
    return '<div class="ch"><b>ရွေးချယ်ရန်</b>'+''.join(f'<div>{"AB"[i]}. {html.escape(o)}</div>' for i,o in enumerate(t))+'<small>(ရွေးတဲ့စာကြောင်းကို MC က ပြောတဲ့အနေနဲ့ ပြမယ်)</small></div>'
  tag=f'<span class="br">{br}</span>' if br else ''
  return f'<div class="l {who}">{tag}<b>{NAMES.get(who,who)}</b><p>{html.escape(t)}</p></div>'
body=''
for f,title,when in SC:
  if f=='GP':
    g=blk[blk.index('const GP_TALK'):blk.index('async function gpScene')]
    rows=''
    for who in ('min','kyaw'):
      arr=re.search(who+r":\[(.*?)\],\n",g,re.S).group(1);items=re.findall(r"'((?:[^'\\]|\\.)*)'",arr)
      _,ask,line,q,ans,think=items
      rows+=f'<h4>{NAMES[who]}</h4>'+''.join(row(w,t,'') for w,t in [('pc',ask),(who,line),('pc',q),(who,ans),('me',think),('pc','ကျေးဇူးပဲဗျာ။')])
  else:
    rows=''.join(row(*x) for x in lines(fn(f)))
    if f=='introScene':rows=rows.replace('<div class="l nar"><b>ဇာတ်ကြောင်း</b><p>စာအိတ်ထဲမှာ','<div class="letter">📜 အဘိုးရဲ့ စာ (၁) ပေါ်လာ</div><div class="l nar"><b>ဇာတ်ကြောင်း</b><p>စာအိတ်ထဲမှာ',1)
  body+=f'<section><h3>{title}</h3><div class="when">{when}</div>{rows}</section>'
page=f'''<!DOCTYPE html><html lang="my"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ရွှေပန်းရွာ · ဇာတ်ညွှန်း</title>
<style>body{{margin:0;background:#f6efe2;color:#2b2118;font:16px/1.75 "Padauk","Noto Sans Myanmar",system-ui,sans-serif}}main{{max-width:720px;margin:auto;padding:20px 14px 60px}}
h1{{font-size:22px;margin:0 0 4px}}.lead{{color:#6a5a48;font-size:14px}}.key{{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 18px;font-size:13px}}.key span{{padding:2px 8px;border-radius:6px}}
section{{background:#fffaf0;border:1px solid #e3d5bd;border-radius:12px;padding:12px 14px;margin:14px 0}}h3{{margin:0;font-size:18px}}h4{{margin:12px 0 4px;color:#6a5a48}}.when{{font-size:13px;color:#8a6d4a;margin-bottom:8px}}
.l{{padding:6px 10px;margin:5px 0;border-radius:8px;background:#f1e8d8}}.l b{{font-size:13px;color:#7a5230}}.l p{{margin:0}}
.l.pc{{background:#dcecf8;border-left:4px solid #3f7fb5}}.l.pc b{{color:#2d5f8a}}.l.me{{background:transparent;font-style:italic;color:#4a5a6a}}.l.nar{{background:transparent;color:#5d5040}}.l.nar b{{display:none}}
.br{{float:right;font-size:12px;background:#e8c070;border-radius:4px;padding:0 6px;color:#4a3410}}.ch{{border:1px dashed #c89a50;border-radius:8px;padding:6px 10px;margin:6px 0;background:#fff4dc}}.ch small{{color:#8a6d4a}}
.letter{{font-size:14px;color:#8a5a20;margin:6px 0}}</style></head><body><main>
<h1>ရွှေပန်းရွာ ခြံလေး · ဇာတ်ညွှန်း</h1><div class="lead">ဂိမ်းထဲက အရေးကြီး ဇာတ်ကွက် ၁၁ ခုရဲ့ စကားပြောတွေကို code ကနေ တိုက်ရိုက် ထုတ်ထားတာပါ။</div>
<div class="key"><span style="background:#dcecf8">အပြာ = MC ပြောတာ (အသစ်)</span><span style="background:#f1e8d8">NPC</span><span style="font-style:italic">စောင်း = ကိုယ့်အတွေး</span><span style="background:#e8c070">A/B = ရွေးချယ်မှုအလိုက်</span></div>
{body}</main></body></html>'''
open('/home/claude/work/script.html','w').write(page);print(len(page))

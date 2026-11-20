import re,html
s=open('/home/claude/configuring/shwe-pan-farm.html').read()
a=s.index('/* scenes */');b=s.index('function drawThingyan')
blk=s[a:b]
NAMES={'mya':'မမြ','san':'ဒေါ်စန်းစန်း','monk':'ဦးဇင်း ဦးပညာ','khine':'မခိုင်','hla':'ဦးလှမောင်','aye':'ဒေါ်အေး','min':'ကိုမင်း','kyaw':'ဦးကျော်','zaw':'ကိုဇော်','tun':'ကိုထွန်း','rep':'ကိုဝင်းနိုင်','pc':'ကျွန်တော် (MC)','me':'ကိုယ့်အတွေး','nar':'ဇာတ်ကြောင်း'}
SC=[('introScene','၁။ ဦးလှမောင် စာအိတ်ပေး','နေ့ ၁ · ခြံ · ဂိမ်းစစချင်း'),
('dealerScene','၂။ ကိုဝင်းနိုင် ပထမဆုံး လာ','နေ့ ၅+ · ခြံ · မနက် ၈ – ညနေ ၅'),
('ayeScene','၃။ ဒေါ်အေးရဲ့ ပုံပြင်','ဒေါ်အေး ♥3 ပြည့်မှ (မပြည့်ရင် "နောက်မှ လာထိုင်ပါ")'),
('GP','၄။ ကိုမင်း / ဦးကျော် ဆီက သဲလွန်စ','ကိုမင်း: ကြက်မွေးထားမှ (သို့) ♥3 · ဦးကျော်: မနက် ၁၀ နာရီမတိုင်ခင် ငါးမျှားနေတုန်း'),
('stoneScene','၅။ ညောင်ပင်ရင်းက ကျောက်တုံး','ဒေါ်အေးရဲ့ ပုံပြင် ကြားပြီးမှ · ညောင်ပင် အရှေ့ဘက် · နေထွက်ချိန် (မနက် ၅:၃၀–၈:၀၀)'),
('ruinScene','၆။ စေတီပျက်','ညဘက်မှသာ (၇ နာရီကျော်) လရောင်မှာ အထွင်း မြင်ရ → အခန်း ၁ ပြီး'),
('zawLanternScene','၇။ ကိုဇော့်ဆိုင် မီးအိမ်','မီးအိမ် ဝယ်ပြီးချိန်'),
('ch2Scene','၈။ အခန်း ၂ စ','နေ့ ၁၁+'),
('altarScene','၉။ ဂူထဲ ဆင်းတုတော်','ဂူအတွင်းဆုံး'),
('bridgeScene','၁၀။ တံတား ပြင်','ထင်း ၁၀ ချောင်းနဲ့ တံတားနားမှာ'),
('dealer2Scene','၁၁။ ကိုဝင်းနိုင် ပြန်လာ','နေ့ ၁၇+ · ခြံ · ညနေ'),
('fallScene','၁၂။ ရေကြီးနှစ်ရဲ့ ရေတံခွန်','ရေကြီးပြီး တံတားပြင်ပြီးမှ ဦးကျော်နဲ့ စကားပြော (ဒါမှမဟုတ် ကမ်းပါးက ရေတံခွန်ကို ကိုယ်တိုင် တွေ့)'),
('muralScene','၁၃။ ဂူနံရံ ရှေးစာ (mini game)','ဂူထဲ နံရံရုပ်ကြွကို ကြည့်ရင် · အမြစ်စာလုံး ဖော်ဖတ်'),
('ch3Scene','၁၄။ အခန်း ၃ စ','နေ့ ၂၁+'),
('hlaWellScene','၁၅။ ရေတွင်းဟောင်း','အခန်း ၃ · ဦးလှမောင်နဲ့ စကားပြော'),
('khineScene','၁၆။ ညဘက် တောဘက် သွားတဲ့သူ','အခန်း ၃ · မခိုင်နဲ့ စကားပြော'),
('monkScene','၁၇။ ဦးဇင်းနဲ့ စကားထာ','အခန်း ၃ · ဦးဇင်းနဲ့ စကားပြော'),
('dealer3Scene','၁၈။ ကိုဝင်းနိုင် နှုတ်ဆက်','နေ့ ၂၃+ · ခြံ'),
('zawCaveScene','၁၉။ ဂူထဲက ကိုဇော်','အခန်း ၃ · နေ့ ၂၂+ · ည ၉ နာရီကျော် ဂူထဲ'),
('zawLetterScene','၂၀။ အဘိုးရဲ့ စာနဲ့ ကိုဇော်','ဦးဇင်းဆီက စာ ရပြီးမှ ကိုဇော်ဆီ (ဂူထဲ ဒါမှမဟုတ် ဆိုင်မှာ)'),
('solvedScene','၂၁။ ပဟေဠိ ဖြေပြီး','မှတ်စု → ပဟေဠိ ဖြေမယ် (စေတီပျက် + ရေကြီးနှစ် ရေတံခွန်)'),
('slabScene','၂၂။ ရေတွင်းအောက်က ကျောက်ပြား','ပဟေဠိ ဖြေပြီး ခြံထဲ ရေတွင်းဟောင်း'),
('cowLoanScene','၂၃။ ကိုမင်းဆီ နွားငှား','ကျောက်ပြား တွေ့ပြီး ကိုမင်းနဲ့ စကားပြော (♥4 လို)'),
('balloonScene','၂၄။ မီးပုံးပျံ လွှတ်ပွဲ (mini game)','နေ့ ၂၈–၂၉ · ညနေ ၃ နာရီကျော် ဦးလှမောင်'),
('finaleScene','၂၅။ တန်ဆောင်မုန်း လပြည့်ည (ဇာတ်သိမ်း)','နေ့ ၂၉ · ည ၇ နာရီကျော် · ကြိုး + နွား · ရေတွင်းဟောင်း'),
('dogScene','၂၆။ ခွေးကလေး','နေ့ ၂ မနက် · ခြံ'),
('kasonScene','၂၇။ ကဆုန် ညောင်ရေသွန်း','နေ့ ၄ · ညောင်ပင်ကြီး · ရေပုံးထဲ ရေ ၅ ရှိရမယ်'),
('wasoScene','၂၈။ ဝါဆိုသင်္ကန်း','နေ့ ၁၂ · ဘုန်းကြီးကျောင်း'),
('kadawScene','၂၉။ သီတင်းကျွတ် ကန်တော့ပွဲ','နေ့ ၂၀ · ဒေါ်အေး၊ ဦးလှမောင်၊ ဦးဇင်း၊ ဦးကျော်၊ ဒေါ်စန်းစန်း'),
('htamaneScene','၃၀။ ထမနဲထိုးပွဲ (mini game)','နေ့ ၂၄ · ဇရပ်'),
('weaveScene','၃၁။ တန်ဆောင်တိုင် ယက်ကန်းပြိုင်ပွဲ','နေ့ ၂၈ · ဒေါ်အေး')]
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
    return '<div class="ch"><b>ရွေးချယ်ရန်</b>'+''.join(f'<div>{"ABCD"[i]}. {html.escape(o)}</div>' for i,o in enumerate(t))+'<small>(ရွေးတဲ့စာကြောင်းကို MC က ပြောတဲ့အနေနဲ့ ပြမယ်)</small></div>'
  tag=f'<span class="br">{br}</span>' if br else ''
  return f'<div class="l {who}">{tag}<b>{NAMES.get(who,who)}</b><p>{html.escape(t)}</p></div>'
body=''
g=s[s.index('const GREET={'):s.index('async function greetScene')]
rows=''
for who in ['aye','mya','kyaw','san','zaw','tun','monk','khine','min','hla']:
  m=re.search(r"\n  "+who+r":\[(.*?)\],\n",g,re.S)
  rows+=f'<h4>{NAMES[who]}</h4>'+''.join(row(w,t,'') for w,t in re.findall(r"\['(\w+)','((?:[^'\\]|\\.)*)'",m.group(1)))
body+=f'<section><h3>၀။ ပထမဆုံး တွေ့ချင်း နှုတ်ဆက်</h3><div class="when">ရွာသား တစ်ယောက်ချင်းနဲ့ ပထမဆုံး စကားပြောချိန် (အဘိုးအကြောင်း မေးတာက ဒုတိယအကြိမ်ကစ)</div>{rows}</section>'
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
ss=blk[blk.index('const SIDE_SCENES={'):blk.index('/* place-based')]
import re as _re
parts=_re.split(r"\n  (\w+):\{\n",ss)
SN={'aye_wind':'လေထဲ လွင့်သွားတဲ့ အဆင် (ဒေါ်အေး · နွေ · နေ့လယ်)','min_calf':'ပျောက်သွားတဲ့ နွားကလေး (ကိုမင်း · မိုး · မိုးရွာပြီး မနက်)','kyaw_fish':'ဦးကျော်ရဲ့ ငါးကြီး (မနက် ၆:၄၀–၈:၀၀)','well_mud':'ရေနောက်နေတဲ့ ရေတွင်း (ဦးလှမောင် · ရေကြီးပြီး · mini game)','monk_alms':'ဆောင်းမနက် ဆွမ်းလောင်း (ဦးဇင်း · ဆောင်း · မနက် ၆:၂၀–၇:၃၀)','smith_fire':'ငြိမ်းသွားတဲ့ ဖိုမီး (ကိုထွန်း · မိုးရွာနေ့)','khine_lost':'ပြန်မလာသေးတဲ့ မခိုင် (ဒေါ်စန်းစန်း · နေဝင်ချိန်)','tea_dealer':'မြို့သားရဲ့ မေးခွန်းတွေ (ဒေါ်စန်းစန်း · နေ့ ၆–၁၄)'}
srows=''
for i in range(1,len(parts),2):
  k=parts[i];code=parts[i+1]
  rows=''.join(row(*x) for x in lines(code))
  if rows:srows+=f'<h4>{SN.get(k,k)}</h4>'+rows
body+=f'<section><h3>ဘေး Quest များ</h3><div class="when">အချိန်နဲ့ နေရာ ကိုက်ရင် ရွာသားခေါင်းပေါ်မှာ "?" ပေါ်လာမယ်</div>{srows}</section>'
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
open(__import__('sys').argv[1] if len(__import__('sys').argv)>1 else 'script.html','w').write(page);print(len(page))

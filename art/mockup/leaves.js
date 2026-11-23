const OUT='#2a1a12';
function limb(x0,y0,x1,y1,w0,w1,bark){const L=Math.hypot(x1-x0,y1-y0);const nx=-(y1-y0)/L,ny=(x1-x0)/L;
  for(let i=0;i<=L*1.5;i++){const t=i/(L*1.5),cx=x0+(x1-x0)*t,cy=y0+(y1-y0)*t,w=w0+(w1-w0)*t;
    for(let k=-w/2-0.5;k<=w/2+0.5;k+=.5){const px=cx+nx*k,py=cy+ny*k;const e=Math.abs(k)>w/2-.2;const s=k/(w/2||1);P(px,py,e?OUT:s<-.3?bark[2]:s<.35?bark[1]:bark[0])}}}
// one small leaf: oval, 2-tone + dark edge + light tip pixel
function lf(x,y,a,len,w,shade,pal){const steps=Math.ceil(len*2.5);const pts=new Map();
  for(let i=0;i<=steps;i++){const t=i/steps,ww=w*Math.sin(Math.PI*Math.pow(t,.75));const cx=x+Math.cos(a)*len*t,cy=y+Math.sin(a)*len*t;
    for(let k=-ww;k<=ww;k+=.35){const px=Math.floor(cx-Math.sin(a)*k),py=Math.floor(cy+Math.cos(a)*k);const v=pts.get(px+','+py);if(v===undefined||Math.abs(k)<Math.abs(v))pts.set(px+','+py,k)}}
  const base=Math.max(1,Math.min(3,shade));
  // outline first (so neighbouring leaves stay separated)
  for(const [key] of pts){const [px,py]=key.split(',').map(Number);for(const [dx,dy] of [[1,0],[-1,0],[0,1],[0,-1]])if(!pts.has((px+dx)+','+(py+dy)))P(px+dx,py+dy,pal[0])}
  for(const [key,k] of pts){const [px,py]=key.split(',').map(Number);let s=base+(k<0?1:0);if(!pts.has(px+','+(py+1)))s-=1;P(px,py,pal[Math.max(1,Math.min(4,s))])}
  // midrib + glint
  const L=Math.floor(len);for(let i=1;i<L-1;i++)P(x+Math.cos(a)*i,y+Math.sin(a)*i,pal[Math.max(1,base-1)]);
  P(x+Math.cos(a)*len*.35-Math.sin(a)*w*.4,y+Math.sin(a)*len*.35+Math.cos(a)*w*.4-1,pal[Math.min(4,base+2)])
}
// light: from upper-left; depth 0 = back (dark) .. 1 = front (lit)
function shadeAt(x,y,cx,cy,rx,ry,depth){const dx=(x-cx)/rx,dy=(y-cy)/ry;const l=-(dx*.6+dy*.8);return Math.round(1+l*1.3+depth*1.1+(rnd()-.5)*.8)}

const page=location.hash.slice(1);
R(0,0,640,480,'#e8f2dc');grassField(0,380,640,100);
/* ===================== PADAUK ===================== */
function padauk(x,y){SH(x,y+4,170,18,.3);
  const B=['#5a4a3e','#7a6858','#a08a74'];
  const cx=x,cy=y-200,rx=200,ry=96;
  const LF=['#1e361c','#36602a','#4f8434','#74aa44','#a8d06a'];
  // back leaves first (behind limbs)
  const twigs=[];for(let i=0;i<620;i++){const a=rnd()*Math.PI*2,d=Math.sqrt(rnd());twigs.push([cx+Math.cos(a)*rx*d,cy+Math.sin(a)*ry*d*(Math.sin(a)>0?.75:1),rnd()])}
  twigs.sort((a,b)=>(a[2]-b[2])||(a[1]-b[1]));
  const drawTwig=([tx,ty,depth])=>{const ang=(tx<cx?Math.PI*0.72:Math.PI*0.28)+(rnd()-.5)*.9,n=4+(rnd()*3|0);let px=tx,py=ty;const sh=shadeAt(tx,ty,cx,cy,rx,ry,depth);
    for(let k=0;k<n;k++){px+=Math.cos(ang)*4.4;py+=Math.sin(ang)*3.4+1;P(px,py,LF[0]);lf(px,py,ang-1.15,6.5,2.4,sh,LF);lf(px,py,ang+1.15,6.5,2.4,sh,LF)}lf(px,py,ang,7,2.4,sh,LF)};
  twigs.filter(t=>t[2]<.45).forEach(drawTwig);
  // trunk + limbs
  limb(x,y,x,y-80,26,20,B);for(let i=0;i<300;i++){P(x-10+rnd()*20,y-80+rnd()*80,'#4a3c32');}
  limb(x-4,y-74,x-110,y-170,18,7,B);limb(x+4,y-74,x+118,y-178,18,7,B);limb(x,y-80,x-14,y-230,15,6,B);limb(x+3,y-120,x+56,y-246,9,4,B);limb(x-60,y-126,x-170,y-176,8,3,B);limb(x+66,y-132,x+176,y-160,8,3,B);
  twigs.filter(t=>t[2]>=.45).forEach(drawTwig);
  // golden flower panicles
  for(let i=0;i<620;i++){const a=rnd()*Math.PI*2,d=Math.sqrt(rnd());const fx=cx+Math.cos(a)*rx*.95*d,fy=cy+Math.sin(a)*ry*.95*d;
    const len=6+(rnd()*8|0);for(let k=0;k<len;k++){const px=fx+(k%2?1:0)+(rnd()-.5)*1.5,py=fy+k;P(px,py,k%3===0?'#d89a10':'#f8d020');if(rnd()<.7)P(px+1,py,'#ffe85a');if(rnd()<.35)P(px-1,py,'#fff4a0')}}
  for(let i=0;i<500;i++){const a=rnd()*6.28,d=Math.sqrt(rnd());P(x+Math.cos(a)*170*d,y+4+Math.sin(a)*18*d,rnd()<.6?'#f8d020':'#e0a010')}
}
/* ===================== BANYAN ===================== */
function banyan(x,y){SH(x,y+6,300,22,.34);
  const B=['#6a5a48','#8a7a64','#b0a088'];
  const cx=x,cy=y-250,rx=300,ry=110;
  const LF=['#10261a','#1e4428','#2e6232','#48843e','#82b85a'];
  const twigs=[];for(let i=0;i<1100;i++){const u=rnd()*2-1,v=rnd();twigs.push([cx+u*rx,cy-Math.sqrt(1-u*u)*ry*v+ry*.55*rnd(),rnd()])}
  twigs.sort((a,b)=>(a[2]-b[2])||(a[1]-b[1]));
  const drawTwig=([tx,ty,depth])=>{const sh=shadeAt(tx,ty,cx,cy,rx,ry,depth);const n=3+(rnd()*2|0);for(let k=0;k<n;k++){const a=-Math.PI/2+(k-(n-1)/2)*.9+(rnd()-.5)*.4;lf(tx,ty,a,14,5.4,sh,LF)}
    if(rnd()<.1){for(const [a,b] of [[0,0],[1,0],[0,1],[1,1]])P(tx+a,ty+2+b,(a+b)?'#a8281e':'#e8603a')}};
  twigs.filter(t=>t[2]<.4).forEach(drawTwig);
  // pillar roots, trunk, limbs, aerial roots
  for(const [dx,w] of [[-270,9],[-210,11],[-140,9],[140,9],[212,11],[272,9]])limb(x+dx,y+2,x+dx+(dx<0?5:-5),y-190,w,w-2,B);
  poly([[x-60,y+3],[x-42,y-150],[x+42,y-150],[x+62,y+3],[x+96,y+10],[x-96,y+10]],(px,py)=>{const f=((px-x+300)%9);return f===0||f===1?'#5a4a3a':px<x-12?'#a8987e':px>x+14?'#6a5a48':(h2(px>>1,py>>2)>.5?'#8a7a64':'#7e6e58')});
  polyOutline([[x-60,y+3],[x-42,y-150],[x+42,y-150],[x+62,y+3],[x+96,y+10],[x-96,y+10]],OUT);
  limb(x-30,y-140,x-280,y-200,30,12,B);limb(x+30,y-140,x+286,y-208,30,12,B);limb(x,y-148,x-26,y-260,24,10,B);limb(x+10,y-156,x+110,y-280,16,8,B);
  for(let i=0;i<220;i++){const dx=-290+rnd()*580,top=y-190+Math.abs(dx)*.03,len=30+rnd()*110;for(let k=0;k<len;k++){const px=x+dx+Math.sin(k*.15+i)*.8;P(px,top+k,k%5===0?'#5a4a3a':'#8a7a64');if(k%9===0)P(px+1,top+k,'#5a4a3a')}}
  twigs.filter(t=>t[2]>=.4).forEach(drawTwig);
}
if(page==='banyan'){banyan(320,452);label(8,458,'ညောင်ပင် — ရွက်ဘဲဥကြီးတွေ ကိုင်းဖျားမှာ အစုလိုက်၊ လေထဲက အမြစ်တွေ ပင်စည်ဖြစ်');}
else{padauk(320,440);label(8,452,'ပိတောက် — ရွက်ကလေးတွေ ကိုင်းပေါ် အစဉ်လိုက်တက်၊ ပွင့်ဝါခိုင်တွေ တွဲလောင်း');}

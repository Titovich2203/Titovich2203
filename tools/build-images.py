import base64,pathlib
exec(open("tools_build.py").read().split("SECTIONS=[")[0])

def dataimg(path,mime=None):
    p=pathlib.Path(path); mime=mime or ("image/jpeg" if p.suffix in(".jpg",".jpeg") else "image/png")
    return f"data:{mime};base64,"+base64.b64encode(p.read_bytes()).decode()
def imsize(path):
    from PIL import Image; return Image.open(path).size

BCSS="""
.flow{animation:flow 6s linear infinite}
.f2{animation-delay:-2s}.f3{animation-delay:-4s}.f4{animation-delay:-1s}
@keyframes flow{from{transform:translateX(0)}to{transform:translateX(1184px)}}
.spark{stroke-dasharray:460;stroke-dashoffset:460;animation:draw 2.6s cubic-bezier(.22,1,.36,1) .35s forwards}
@keyframes draw{to{stroke-dashoffset:0}}
.chip{opacity:0;animation:pop .55s ease-out forwards}.c1{animation-delay:1.1s}.c2{animation-delay:1.35s}
@keyframes pop{from{opacity:0}to{opacity:1}}
@media (prefers-reduced-motion:reduce){.flow,.spark,.chip{animation:none}.spark{stroke-dashoffset:0}.chip{opacity:1}}"""

def banner(p,tag):
    PX,PY,PS=48,58,168
    photo=dataimg(f"img/portrait-nat-{tag}.jpg")
    b=[f'<rect width="1280" height="330" fill="{p["bg"]}"/>']
    b.append(f'<defs><clipPath id="pc"><rect x="{PX}" y="{PY}" width="{PS}" height="{PS}" rx="16"/></clipPath></defs>')
    b.append(f'<image href="{photo}" x="{PX}" y="{PY}" width="{PS}" height="{PS}" clip-path="url(#pc)" preserveAspectRatio="xMidYMid slice"/>')
    b.append(f'<rect x="{PX}" y="{PY}" width="{PS}" height="{PS}" rx="16" fill="none" stroke="{p["stroke"]}"/>')
    b.append(f'<path d="M{PX} {PY+26} L{PX} {PY+10} Q{PX} {PY} {PX+10} {PY} L{PX+26} {PY}" fill="none" stroke="{p["acc"]}" stroke-width="3"/>')
    X=248
    b.append(f'<text class="xb" x="{X}" y="{PY+42}" font-size="44" letter-spacing="-1" fill="{p["ink"]}">Tito GBEDJEHA</text>')
    b.append(f'<rect x="{X}" y="{PY+60}" width="54" height="3" fill="{p["acc"]}"/>')
    b.append(f'<text class="md" x="{X}" y="{PY+96}" font-size="18" fill="{p["ink2"]}">Software engineer turned CEO.</text>')
    b.append(f'<text class="md" x="{X}" y="{PY+122}" font-size="18" fill="{p["acc"]}">I build and run regulated payment infrastructure in Africa.</text>')
    b.append(f'<rect x="{X}" y="{PY+140}" width="273" height="27" rx="13.5" fill="none" stroke="{p["stroke"]}"/>')
    b.append(f'<text class="sb" x="{X+16}" y="{PY+158}" font-size="11.5" letter-spacing="1" fill="{p["mut"]}">MD · LICENSED PSP · 5 COUNTRIES</text>')
    b.append(f'<rect x="{X+283}" y="{PY+140}" width="251" height="27" rx="13.5" fill="none" stroke="{p["stroke"]}"/>')
    b.append(f'<text class="sb" x="{X+299}" y="{PY+158}" font-size="11.5" letter-spacing="1" fill="{p["mut"]}">CO-FOUNDER &amp; CTO · WIICODE</text>')
    b.append(f'<text class="sb" x="1232" y="46" text-anchor="end" font-size="10.5" letter-spacing="1.9" fill="{p["dim"]}">PRODUCTION TELEMETRY</text>')
    b.append(f'<g class="sb" font-size="25" fill="{p["ink"]}" text-anchor="end"><text x="920" y="92">20M+</text><text x="1076" y="92">99.5%</text><text x="1232" y="92">100ms</text></g>')
    b.append(f'<g class="md" font-size="9.5" fill="{p["dim"]}" text-anchor="end" letter-spacing="1.3"><text x="920" y="110">TRANSACTIONS</text><text x="1076" y="110">UPTIME</text><text x="1232" y="110">P95 LATENCY</text></g>')
    b.append(f'<path class="spark" d="M820 178 L860 170 L900 180 L940 162 L980 168 L1020 152 L1060 160 L1100 144 L1140 152 L1180 136 L1232 142" fill="none" stroke="{p["acc"]}" stroke-width="1.8" stroke-linejoin="round"/>')
    b.append(f'<circle class="chip c1" cx="1232" cy="142" r="3" fill="{p["acc"]}"/>')
    b.append(f'<g class="chip c1"><rect x="820" y="196" width="151" height="27" rx="13.5" fill="{p["okbg"]}" stroke="{p["okbd"]}"/><circle cx="837" cy="209.5" r="3.5" fill="{p["acc"]}"/><text class="sb" x="849" y="214" font-size="11" letter-spacing=".9" fill="{p["okink"]}">ANTIC · PASSED</text></g>')
    b.append(f'<g class="chip c2"><rect x="983" y="196" width="171" height="27" rx="13.5" fill="{p["okbg"]}" stroke="{p["okbd"]}"/><circle cx="1000" cy="209.5" r="3.5" fill="{p["acc"]}"/><text class="sb" x="1012" y="214" font-size="11" letter-spacing=".9" fill="{p["okink"]}">BCEAO · LICENSED</text></g>')
    b.append(f'<line x1="48" y1="278" x2="1232" y2="278" stroke="{p["line"]}" stroke-width="1.5"/>')
    for cls,col,r in [("flow",p["acc"],2.6),("flow f2",p["acc"],2.6),("flow f3",p["acc2"],2.6),("flow f4",p["acc"],2)]:
        b.append(f'<g class="{cls}"><circle cx="-40" cy="278" r="{r}" fill="{col}" opacity=".8"/></g>')
    b.append(f'<g class="md" font-size="9.5" fill="{p["dim"]}" letter-spacing="1.5"><text x="48" y="302">INGEST</text><text x="640" y="302" text-anchor="middle">LEDGER</text><text x="1232" y="302" text-anchor="end">SETTLE</text></g>')
    return wrap("".join(b),1280,330,p,BCSS)

COMP=[("copay","Co-founder & CTO → Managing Director","2022 → now"),
 ("wiicode","Co-founder & CTO","2023 → now"),
 ("narrevo","Product design, architecture, build","2025 → now"),
 ("codify","Co-founder & Managing Director","2017 → 2023"),
 ("toosign","Project lead — e-signature","2022 → 2023"),
 ("faseya","Project manager — 25 people","2020 → 2024")]
def companies(p,tag):
    n=len(COMP);gap=14;tw=(1280-gap*(n-1))/n;H=118;b=[]
    for i,(slug,role,per) in enumerate(COMP):
        x=i*(tw+gap)
        b.append(f'<rect x="{x:.0f}" y="0" width="{tw:.0f}" height="{H}" rx="10" fill="{p["panel"]}" stroke="{p["stroke"]}"/>')
        f=f"img/logo-{slug}-{tag}.png";iw,ih=imsize(f)
        maxw,maxh=tw-52,34;sc=min(maxw/iw,maxh/ih);w,h=iw*sc,ih*sc
        b.append(f'<image href="{dataimg(f)}" x="{x+(tw-w)/2:.1f}" y="{40-h/2:.1f}" width="{w:.1f}" height="{h:.1f}"/>')
        b.append(f'<line x1="{x+24:.0f}" y1="70" x2="{x+tw-24:.0f}" y2="70" stroke="{p["line"]}"/>')
        b.append(f'<text class="md" x="{x+tw/2:.0f}" y="{88}" text-anchor="middle" font-size="10" fill="{p["ink2"]}">{esc(role)}</text>')
        b.append(f'<text class="sb" x="{x+tw/2:.0f}" y="{105}" text-anchor="middle" font-size="9.5" letter-spacing=".8" fill="{p["acc"] if i<3 else p["dim"]}">{esc(per)}</text>')
    return wrap("".join(b),1280,H,p)

def product(p,tag):
    b=[];H=92
    b.append(f'<rect x="0" y="0" width="1280" height="{H}" rx="10" fill="{p["panel"]}" stroke="{p["stroke"]}"/>')
    f=f"img/logo-narrevo-{tag}.png";iw,ih=imsize(f);sc=44/ih
    b.append(f'<image href="{dataimg(f)}" x="34" y="{(H-44)/2:.0f}" width="{iw*sc:.0f}" height="44"/>')
    xx=34+iw*sc+34
    b.append(f'<line x1="{xx-17:.0f}" y1="22" x2="{xx-17:.0f}" y2="{H-22}" stroke="{p["stroke"]}"/>')
    b.append(f'<text class="xb" x="{xx:.0f}" y="42" font-size="15" letter-spacing="-.1" fill="{p["ink"]}">Multi-tenant SaaS for AI-assisted video production</text>')
    b.append(f'<text class="md" x="{xx:.0f}" y="63" font-size="12" fill="{p["dim"]}">Product design, architecture and pipeline — in production, pilot phase</text>')
    b.append(f'<text class="sb" x="1246" y="{H/2+4:.0f}" text-anchor="end" font-size="12.5" letter-spacing=".4" fill="{p["acc"]}">narrevo.ai →</text>')
    return wrap("".join(b),1280,H,p)

out=pathlib.Path("assets")
for tag,p in [("dark",DARK),("light",LIGHT)]:
    (out/f"banner-{tag}.svg").write_text(banner(p,tag),encoding="utf-8")
    (out/f"companies-{tag}.svg").write_text(companies(p,tag),encoding="utf-8")
    (out/f"product-narrevo-{tag}.svg").write_text(product(p,tag),encoding="utf-8")

print("banner",(out/"banner-dark.svg").stat().st_size//1024,"KB | companies",(out/"companies-dark.svg").stat().st_size//1024,"KB")

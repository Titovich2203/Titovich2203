import base64, pathlib
def b64(p): return base64.b64encode(pathlib.Path(p).read_bytes()).decode()
FONTS = "".join(
f"""@font-face{{font-family:Syne;font-weight:{w};src:url(data:font/woff2;base64,{b64(f'sub/Syne-{n}.woff2')}) format('woff2')}}"""
for n,w in [("ExtraBold",800),("SemiBold",600),("Medium",500)])

DARK = dict(bg="#0d1117", grid="#161d26", ink="#e6edf3", ink2="#adbac7", mut="#7d8590",
            dim="#586069", line="#21262d", stroke="#30363d", acc="#2be8a0", acc2="#4c8dff",
            chipbg="#0f2e22", chipbd="#1c5c44", chipink="#5ce0b0", dot="#30363d")
LIGHT = dict(bg="#ffffff", grid="#eef1f5", ink="#1f2328", ink2="#59636e", mut="#59636e",
             dim="#8c959f", line="#e6eaef", stroke="#d8dee4", acc="#0f9d6e", acc2="#2563eb",
             chipbg="#e8f7f0", chipbd="#a9e0c8", chipink="#0b6b4c", dot="#d8dee4")

CSS = """
text{font-family:Syne,ui-sans-serif,system-ui,sans-serif}
.xb{font-weight:800}.sb{font-weight:600}.md{font-weight:500}
.flow{animation:flow 6s linear infinite}
.f2{animation-delay:-2s}.f3{animation-delay:-4s}.f4{animation-delay:-1s}.f5{animation-delay:-3.2s}.f6{animation-delay:-5.1s}
@keyframes flow{from{transform:translateX(0)}to{transform:translateX(1184px)}}
.spark{stroke-dasharray:560;stroke-dashoffset:560;animation:draw 2.6s cubic-bezier(.22,1,.36,1) .35s forwards}
@keyframes draw{to{stroke-dashoffset:0}}
.chip{opacity:0;animation:pop .55s ease-out forwards}
.c1{animation-delay:1.15s}.c2{animation-delay:1.4s}.c3{animation-delay:1.65s}
@keyframes pop{from{opacity:0;transform:translateY(3px)}to{opacity:1;transform:translateY(0)}}
.pulse{animation:pulse 2.6s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:.35}50%{opacity:1}}
.sweep{animation:sw 8s ease-in-out infinite}
@keyframes sw{0%{transform:translateX(-460px)}55%,100%{transform:translateX(1320px)}}
@media (prefers-reduced-motion:reduce){.flow,.spark,.chip,.pulse,.sweep{animation:none}.spark{stroke-dashoffset:0}.chip{opacity:1}}
"""

def chip(x,y,w,text,p):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="27" rx="13.5" fill="{p["chipbg"]}" stroke="{p["chipbd"]}"/>'
            f'<circle cx="{x+17}" cy="{y+13.5}" r="3.5" fill="{p["acc"]}"/>'
            f'<text class="sb" x="{x+29}" y="{y+18}" font-size="11" letter-spacing=".9" fill="{p["chipink"]}">{text}</text>')

def build(p, sid):
    g=f"g{sid}"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 300" width="1280" height="300" role="img" aria-label="Tito GBEDJEHA — software engineer turned CEO. Regulated payment infrastructure in Africa.">
<title>Tito GBEDJEHA</title>
<defs>
<pattern id="{g}" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{p['grid']}" stroke-width="1"/></pattern>
<linearGradient id="sw{sid}" x1="0" x2="1"><stop offset="0" stop-color="{p['acc']}" stop-opacity="0"/><stop offset=".5" stop-color="{p['acc']}" stop-opacity=".55"/><stop offset="1" stop-color="{p['acc']}" stop-opacity="0"/></linearGradient>
<clipPath id="rail{sid}"><rect x="48" y="246" width="1184" height="14"/></clipPath>
<style>{FONTS}{CSS}</style>
</defs>
<rect width="1280" height="300" fill="{p['bg']}"/>
<rect width="1280" height="300" fill="url(#{g})"/>
<rect x="0" y="0" width="340" height="300" fill="url(#sw{sid})" opacity=".08" class="sweep"/>

<text class="xb" x="48" y="88" font-size="50" letter-spacing="-1" fill="{p['ink']}">Tito GBEDJEHA</text>
<rect x="48" y="108" width="58" height="3" fill="{p['acc']}"/>
<text class="md" x="48" y="146" font-size="19" fill="{p['ink2']}">Software engineer turned CEO.</text>
<text class="md" x="48" y="174" font-size="19" fill="{p['acc']}">I build and run regulated payment infrastructure in Africa.</text>

<rect x="48" y="196" width="273" height="27" rx="13.5" fill="none" stroke="{p['stroke']}"/>
<text class="sb" x="64" y="214" font-size="11.5" letter-spacing="1" fill="{p['mut']}">MD · LICENSED PSP · 5 COUNTRIES</text>
<rect x="331" y="196" width="251" height="27" rx="13.5" fill="none" stroke="{p['stroke']}"/>
<text class="sb" x="347" y="214" font-size="11.5" letter-spacing="1" fill="{p['mut']}">CO-FOUNDER &amp; CTO · WIICODE</text>

<text class="sb" x="1232" y="50" text-anchor="end" font-size="10.5" letter-spacing="1.9" fill="{p['dim']}">PRODUCTION TELEMETRY</text>
<g class="sb" font-size="27" fill="{p['ink']}" text-anchor="end"><text x="880" y="94">20M+</text><text x="1056" y="94">99.5%</text><text x="1232" y="94">100ms</text></g>
<g class="md" font-size="10" fill="{p['dim']}" text-anchor="end" letter-spacing="1.4"><text x="880" y="113">TRANSACTIONS</text><text x="1056" y="113">UPTIME</text><text x="1232" y="113">P95 LATENCY</text></g>
<path class="spark" d="M760 180.2 L790 173.8 L820 183.4 L850 165 L880 171.4 L910 157.8 L940 166.6 L970 153.8 L1000 161.8 L1030 147.4 L1060 155.4 L1090 142.6 L1120 150.6 L1150 137.8 L1180 144.2 L1210 131.4 L1232 136.2" fill="none" stroke="{p['acc']}" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round" opacity=".9"/>
<circle class="chip c1" cx="1232" cy="136.2" r="3" fill="{p['acc']}"/>
<g class="chip c1">{chip(672,196,151,"ANTIC · PASSED",p)}</g>
<g class="chip c2">{chip(835,196,171,"BCEAO · LICENSED",p)}</g>
<g class="chip c3">{chip(1018,196,214,"BANK OF TANZANIA · PSP",p)}</g>

<line x1="48" y1="253" x2="1232" y2="253" stroke="{p['line']}" stroke-width="1.5"/>
<g clip-path="url(#rail{sid})">
<g class="flow"><circle cx="-40" cy="253" r="2.6" fill="{p['acc']}"/></g>
<g class="flow f2"><circle cx="-40" cy="253" r="2.6" fill="{p['acc']}" opacity=".6"/></g>
<g class="flow f3"><circle cx="-40" cy="253" r="2.6" fill="{p['acc2']}" opacity=".7"/></g>
<g class="flow f4"><circle cx="-40" cy="253" r="2" fill="{p['acc']}" opacity=".4"/></g>
<g class="flow f5"><circle cx="-40" cy="253" r="2.6" fill="{p['acc']}" opacity=".85"/></g>
<g class="flow f6"><circle cx="-40" cy="253" r="2" fill="{p['acc2']}" opacity=".5"/></g>
</g>
<g class="md" font-size="9.5" fill="{p['dim']}" letter-spacing="1.5">
<circle cx="48" cy="253" r="3" fill="{p['dot']}"/><text x="48" y="279">INGEST</text>
<circle cx="344" cy="253" r="3" fill="{p['dot']}"/><text x="344" y="279" text-anchor="middle">AGGREGATE</text>
<circle cx="640" cy="253" r="3" fill="{p['dot']}"/><text x="640" y="279" text-anchor="middle">LEDGER</text>
<circle cx="936" cy="253" r="3" fill="{p['dot']}"/><text x="936" y="279" text-anchor="middle">RECONCILE</text>
<circle cx="1232" cy="253" r="3.5" fill="{p['acc']}" class="pulse"/><text x="1232" y="279" text-anchor="end">SETTLE</text>
</g>
</svg>'''

pathlib.Path("assets").mkdir(exist_ok=True)
for name,p,sid in [("banner-dark",DARK,"d"),("banner-light",LIGHT,"l")]:
    s=build(p,sid); pathlib.Path(f"assets/{name}.svg").write_text(s,encoding="utf-8")
    print(name, len(s.encode())//1024, "KB")

d=base64.b64encode(pathlib.Path("assets/banner-dark.svg").read_bytes()).decode()
l=base64.b64encode(pathlib.Path("assets/banner-light.svg").read_bytes()).decode()
pathlib.Path("banner-preview.html").write_text(f"""<title>Syne — Control Plane</title>
<style>body{{background:#161b22;color:#e6edf3;font:15px/1.6 ui-sans-serif,system-ui,sans-serif;margin:0;padding:36px 32px 60px}}
.w{{max-width:1360px;margin:0 auto}} h1{{font-size:19px;margin:0 0 4px}} p.s{{color:#7d8590;font-size:13px;margin:0 0 30px}}
.l{{font:600 11px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.14em;color:#7d8590;text-transform:uppercase;margin:0 0 9px}}
.f{{border:1px solid #30363d;border-radius:10px;overflow:hidden;margin:0 0 34px}} img{{display:block;width:100%}}
.n{{color:#7d8590;font-size:13px;max-width:74ch}}</style>
<div class=w><h1>Control Plane — typographié en Syne</h1>
<p class=s>Les deux fichiers sont chargés ici en &lt;img&gt;, exactement comme GitHub les servira. Police embarquée dans le SVG.</p>
<p class=l>Dark</p><div class=f><img src="data:image/svg+xml;base64,{d}"></div>
<p class=l>Light</p><div class=f><img src="data:image/svg+xml;base64,{l}"></div>
<p class=n>Syne ExtraBold sur le nom, SemiBold sur les chiffres et les puces, Medium sur le reste.</p></div>""",encoding="utf-8")
print("preview", pathlib.Path("banner-preview.html").stat().st_size//1024,"KB")

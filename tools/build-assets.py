import base64, pathlib, re, subprocess, html
from fontTools.ttLib import TTFont

SRC="font/Syne/static/Syne-%s.ttf"
W={"xb":"ExtraBold","sb":"SemiBold","md":"Medium"}
FT={k:TTFont(SRC%v) for k,v in W.items()}
def mw(t,w,size,ls=0):
    f=FT[w];upm=f["head"].unitsPerEm;cm=f.getBestCmap();hm=f["hmtx"];tot=0
    for ch in t:
        g=cm.get(ord(ch))
        tot+=hm[g][0] if g else 0
    return tot/upm*size+ls*max(len(t)-1,0)

pathlib.Path("cache").mkdir(exist_ok=True)
def fontcss(text):
    chars="".join(sorted(set(text+"0123456789")))
    out=[]
    for k,v in W.items():
        key=pathlib.Path("cache")/f"{v}-{abs(hash(chars))}.woff2"
        if not key.exists():
            subprocess.run(["pyftsubset",SRC%v,f"--output-file={key}","--flavor=woff2",
                f"--text={chars}","--layout-features=kern,liga","--no-hinting","--desubroutinize"],check=True)
        b=base64.b64encode(key.read_bytes()).decode()
        wt={"xb":800,"sb":600,"md":500}[k]
        out.append(f"@font-face{{font-family:Syne;font-weight:{wt};src:url(data:font/woff2;base64,{b}) format('woff2')}}")
    return "".join(out)

BASECSS="""text{font-family:Syne,ui-sans-serif,system-ui,sans-serif}
.xb{font-weight:800}.sb{font-weight:600}.md{font-weight:500}"""

DARK=dict(bg="#0d1117",grid="#161d26",ink="#e6edf3",ink2="#adbac7",mut="#7d8590",dim="#586069",
 line="#21262d",stroke="#30363d",panel="#11161d",acc="#2be8a0",acc2="#4c8dff",warn="#f0a93b",
 okbg="#0f2e22",okbd="#1c5c44",okink="#5ce0b0",wnbg="#2e2412",wnbd="#5c4a1c",wnink="#e0b45c",dot="#30363d")
LIGHT=dict(bg="#ffffff",grid="#eef1f5",ink="#1f2328",ink2="#59636e",mut="#59636e",dim="#8c959f",
 line="#e6eaef",stroke="#d8dee4",panel="#f6f8fa",acc="#0f9d6e",acc2="#2563eb",warn="#bf7d0c",
 okbg="#e8f7f0",okbd="#a9e0c8",okink="#0b6b4c",wnbg="#fdf3e0",wnbd="#eecfa0",wnink="#8a5d0a",dot="#d8dee4")

def esc(s): return html.escape(s,quote=False)

def wrap(body,w,h,p,extra_css="",uid="x"):
    txt="".join(re.findall(r'>([^<>]*)</text>',body))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">'
            f'<defs><style>{fontcss(txt)}{BASECSS}{extra_css}</style></defs>'
            f'<rect width="{w}" height="{h}" fill="{p["bg"]}"/>{body}</svg>')

# ---------- section header ----------
def section(idx,title,sub,p):
    b=[]
    b.append(f'<text class="xb" x="0" y="30" font-size="13" letter-spacing="1.2" fill="{p["acc"]}">{idx}</text>')
    b.append(f'<line x1="30" y1="10" x2="30" y2="34" stroke="{p["stroke"]}"/>')
    tw=mw(title,"xb",27,-0.3)
    b.append(f'<text class="xb" x="46" y="31" font-size="27" letter-spacing="-.3" fill="{p["ink"]}">{esc(title)}</text>')
    x=46+tw+18
    sw=mw(sub,"md",12.5,.6)
    b.append(f'<text class="md" x="{x}" y="30" font-size="12.5" letter-spacing=".6" fill="{p["dim"]}">{esc(sub)}</text>')
    b.append(f'<line x1="{x+sw+18}" y1="24" x2="1280" y2="24" stroke="{p["line"]}"/>')
    return wrap("".join(b),1280,46,p)

# ---------- stat tiles ----------
STATS=[("20M+","TRANSACTIONS","2024–2025"),("27K","PER DAY","steady state"),
 ("50Bn+","FCFA PROCESSED","≈ €76M+"),("99.5%","UPTIME","since launch"),
 ("100ms","P95 LATENCY","end to end"),("3","REGULATORS CLEARED","CM · UEMOA · TZ")]
def stats(p):
    b=[];W_=1280;n=len(STATS);cw=W_/n
    for i,(v,l,s) in enumerate(STATS):
        x=i*cw
        if i: b.append(f'<line x1="{x:.0f}" y1="22" x2="{x:.0f}" y2="122" stroke="{p["line"]}"/>')
        cx=x+26
        b.append(f'<text class="xb" x="{cx:.0f}" y="66" font-size="34" letter-spacing="-.5" fill="{p["ink"]}">{esc(v)}</text>')
        b.append(f'<text class="sb" x="{cx:.0f}" y="88" font-size="10" letter-spacing="1.5" fill="{p["acc"]}">{esc(l)}</text>')
        b.append(f'<text class="md" x="{cx:.0f}" y="107" font-size="10.5" letter-spacing=".3" fill="{p["dim"]}">{esc(s)}</text>')
    return wrap("".join(b),1280,144,p)

# ---------- regulatory board ----------
REG=[("ANTIC","Cameroon","ISO 27001-type security audit of the information system","PASSED",1),
 ("BCEAO","UEMOA","Licensed PSP compliance framework · NE / TG / ML coverage","LICENSED",1),
 ("BANK OF TANZANIA","Tanzania","PSP licence · e-money, TIPS / TISS / TACH interoperability","GRANTED",1),
 ("PCI-DSS","COPAY group","Certification programme under my direction","IN PROGRESS · 2026",0),
 ("ISO/IEC 27001","Lead Auditor","Personal certification","IN PROGRESS · 2026",0)]
def regulatory(p):
    b=[];y=8;rh=52
    b.append(f'<text class="sb" x="0" y="14" font-size="10" letter-spacing="1.6" fill="{p["dim"]}">AUTHORITY</text>')
    b.append(f'<text class="sb" x="1280" y="14" text-anchor="end" font-size="10" letter-spacing="1.6" fill="{p["dim"]}">OUTCOME</text>')
    y=26
    for name,zone,scope,status,ok in REG:
        b.append(f'<line x1="0" y1="{y}" x2="1280" y2="{y}" stroke="{p["line"]}"/>')
        b.append(f'<text class="xb" x="0" y="{y+26}" font-size="16" letter-spacing="-.2" fill="{p["ink"]}">{esc(name)}</text>')
        nw=mw(name,"xb",16,-0.2)
        b.append(f'<text class="md" x="{nw+12:.0f}" y="{y+26}" font-size="11" letter-spacing=".4" fill="{p["dim"]}">{esc(zone)}</text>')
        b.append(f'<text class="md" x="0" y="{y+43}" font-size="12.5" fill="{p["ink2"]}">{esc(scope)}</text>')
        bg,bd,ik=(p["okbg"],p["okbd"],p["okink"]) if ok else (p["wnbg"],p["wnbd"],p["wnink"])
        sw=mw(status,"sb",11,.9)+46
        b.append(f'<rect x="{1280-sw:.0f}" y="{y+16}" width="{sw:.0f}" height="27" rx="13.5" fill="{bg}" stroke="{bd}"/>')
        b.append(f'<circle cx="{1280-sw+17:.0f}" cy="{y+29.5}" r="3.5" fill="{p["acc"] if ok else p["warn"]}"/>')
        b.append(f'<text class="sb" x="{1280-sw+29:.0f}" y="{y+34}" font-size="11" letter-spacing=".9" fill="{ik}">{esc(status)}</text>')
        y+=rh+8
    b.append(f'<line x1="0" y1="{y}" x2="1280" y2="{y}" stroke="{p["line"]}"/>')
    return wrap("".join(b),1280,y+10,p)

# ---------- stack grid ----------
STACK=[("LANGUAGES",["TypeScript","Python","Java","C#","PHP"]),
 ("BACKEND",["NestJS","Node.js","Symfony","Laravel","REST","GraphQL","SOAP"]),
 ("FRONTEND & MOBILE",["Next.js","React","Angular","Flutter"]),
 ("DATA",["PostgreSQL","pgvector / HNSW","MySQL","SQL Server","Oracle","MongoDB","Redis"]),
 ("EVENT-DRIVEN",["Apache Kafka","async high-volume processing"]),
 ("AI IN PRODUCTION",["LLM & agent orchestration","Whisper ASR","ONNX vision","RAG","anomaly detection / AML"]),
 ("CLOUD & DEVOPS",["AWS","Kubernetes","Terraform","Docker","GitHub Actions","GitLab CI","Jenkins","Prometheus","Grafana"]),
 ("SECURITY",["Zero Trust","MFA","WAF","IDS/IPS","key management","network segmentation"])]
def stack(p):
    b=[];y=6;LX=0;CX=196;RIGHT=1280
    for label,items in STACK:
        b.append(f'<text class="sb" x="{LX}" y="{y+21}" font-size="10" letter-spacing="1.5" fill="{p["acc"]}">{esc(label)}</text>')
        x=CX;rows=1
        for it in items:
            w=mw(it,"md",12,.2)+28
            if x+w>RIGHT: x=CX;y+=32;rows+=1
            b.append(f'<rect x="{x:.0f}" y="{y+2}" width="{w:.0f}" height="26" rx="6" fill="{p["panel"]}" stroke="{p["stroke"]}"/>')
            b.append(f'<text class="md" x="{x+14:.0f}" y="{y+19}" font-size="12" letter-spacing=".2" fill="{p["ink2"]}">{esc(it)}</text>')
            x+=w+8
        y+=44
    return wrap("".join(b),1280,y,p)

# ---------- pipeline ----------
PIPE=[("01","TRANSCRIBE","Whisper · Groq","speech to text"),
 ("02","DIRECT","Claude LLM","cuts, pacing, creative calls"),
 ("03","PLACE","Vision model · ONNX","adaptive overlay placement"),
 ("04","GENERATE","Higgsfield","image → video, deterministic cache"),
 ("05","RENDER","async workers","multi-tenant isolation")]
PIPECSS="""
.pkt{animation:pk 7s linear infinite}
@keyframes pk{0%{transform:translateX(0);opacity:0}4%{opacity:1}96%{opacity:1}100%{transform:translateX(1140px);opacity:0}}
.gl{animation:gl 7s ease-in-out infinite}
@keyframes gl{0%,100%{opacity:.25}50%{opacity:.7}}
@media (prefers-reduced-motion:reduce){.pkt,.gl{animation:none}}"""
def pipeline(p):
    b=[];bw=232;gap=30;x0=0;top=52;bh=104
    b.append(f'<text class="sb" x="0" y="18" font-size="10" letter-spacing="1.6" fill="{p["dim"]}">MEDIA IN</text>')
    b.append(f'<text class="sb" x="1280" y="18" text-anchor="end" font-size="10" letter-spacing="1.6" fill="{p["dim"]}">PUBLISHED VIDEO OUT</text>')
    b.append(f'<line x1="0" y1="30" x2="1280" y2="30" stroke="{p["line"]}"/>')
    b.append(f'<g class="pkt"><circle cx="4" cy="30" r="3.5" fill="{p["acc"]}"/></g>')
    for i,(n,t,tech,desc) in enumerate(PIPE):
        x=x0+i*(bw+gap)
        b.append(f'<rect x="{x}" y="{top}" width="{bw}" height="{bh}" rx="8" fill="{p["panel"]}" stroke="{p["stroke"]}"/>')
        b.append(f'<text class="sb" x="{x+18}" y="{top+24}" font-size="10" letter-spacing="1.4" fill="{p["acc"]}">{n}</text>')
        b.append(f'<text class="xb" x="{x+18}" y="{top+50}" font-size="17" letter-spacing="-.2" fill="{p["ink"]}">{esc(t)}</text>')
        b.append(f'<text class="sb" x="{x+18}" y="{top+70}" font-size="11.5" fill="{p["acc2"]}">{esc(tech)}</text>')
        b.append(f'<text class="md" x="{x+18}" y="{top+88}" font-size="10.5" fill="{p["dim"]}">{esc(desc)}</text>')
        if i<len(PIPE)-1:
            cx=x+bw+gap/2
            b.append(f'<path d="M{x+bw+7} {top+bh/2} L{x+bw+gap-7} {top+bh/2}" stroke="{p["stroke"]}" stroke-width="1.5"/>')
            b.append(f'<path d="M{x+bw+gap-11} {top+bh/2-4} l4 4 l-4 4" fill="none" stroke="{p["stroke"]}" stroke-width="1.5"/>')
    ry=top+bh+34
    b.append(f'<rect x="262" y="{ry}" width="756" height="44" rx="8" fill="none" stroke="{p["stroke"]}" stroke-dasharray="3 4"/>')
    b.append(f'<text class="sb" x="282" y="{ry+27}" font-size="11" letter-spacing="1.2" fill="{p["acc"]}">RETRIEVAL LAYER</text>')
    b.append(f'<text class="md" x="420" y="{ry+27}" font-size="12" fill="{p["ink2"]}">PostgreSQL · pgvector · HNSW index — grounds every step above</text>')
    b.append(f'<path d="M378 {top+bh} L378 {ry}" stroke="{p["acc"]}" stroke-width="1.2" stroke-dasharray="3 4" class="gl"/>')
    b.append(f'<path d="M640 {top+bh} L640 {ry}" stroke="{p["acc"]}" stroke-width="1.2" stroke-dasharray="3 4" class="gl"/>')
    b.append(f'<path d="M902 {top+bh} L902 {ry}" stroke="{p["acc"]}" stroke-width="1.2" stroke-dasharray="3 4" class="gl"/>')
    return wrap("".join(b),1280,ry+58,p,PIPECSS)


TIMELINE=[("2022 → now","COPAY SA","Co-founder & CTO → COO → Managing Director","Built the aggregator, then the team, then the company. Group leadership across five countries."),
 ("2024 → now","COPAY Tanzania","Chief Operating Officer","PSP licence, domestic interoperability, AML/CFT framework — granted."),
 ("2023 → now","WIICODE","Co-founder & CTO","Product portfolio and engineering standards; designed and shipped narrevo.ai."),
 ("2024","Transport operator · SN + TG","Engagement director","Full technical audit, then restructuring. Dispatch engine rebuilt; five-person in-house team created."),
 ("2022 → 2023","TOOSIGN · Côte d'Ivoire","IT consultant, project lead","First electronic signature platform in Africa."),
 ("2021 → 2022","TRANCH MONEY · Côte d'Ivoire","IT consultant","Digitalisation of financial services; web and mobile delivery."),
 ("2020 → 2024","FASEYA · France","Consultant → Project manager","Yatouze platform — 25 people across six countries; application security review."),
 ("2017 → 2023","CODIFY","Co-founder & Managing Director","Ticketing, real estate, insurance, travel, delivery marketplace; advisory to West African fintechs.")]
def timeline(p):
    b=[];RX=152;CX=186;y=14;rh=68
    b.append(f'<line x1="{RX}" y1="8" x2="{RX}" y2="{14+rh*len(TIMELINE)-24}" stroke="{p["line"]}" stroke-width="1.5"/>')
    for i,(per,ent,role,desc) in enumerate(TIMELINE):
        cy=y+16
        b.append(f'<text class="sb" x="128" y="{cy+5}" text-anchor="end" font-size="11.5" letter-spacing=".5" fill="{p["acc"] if i<3 else p["dim"]}">{esc(per)}</text>')
        b.append(f'<circle cx="{RX}" cy="{cy}" r="4.5" fill="{p["bg"]}" stroke="{p["acc"] if i<3 else p["stroke"]}" stroke-width="2"/>')
        ew=mw(ent,"xb",17,-.2)
        b.append(f'<text class="xb" x="{CX}" y="{cy+6}" font-size="17" letter-spacing="-.2" fill="{p["ink"]}">{esc(ent)}</text>')
        b.append(f'<text class="md" x="{CX+ew+14:.0f}" y="{cy+6}" font-size="11.5" letter-spacing=".3" fill="{p["dim"]}">{esc(role)}</text>')
        b.append(f'<text class="md" x="{CX}" y="{cy+27}" font-size="12.5" fill="{p["ink2"]}">{esc(desc)}</text>')
        y+=rh
    return wrap("".join(b),1280,y-6,p)

SECTIONS=[("01","AT SCALE","what the platform actually does in production"),
 ("02","WHAT I RUN","two roles, in parallel"),
 ("03","REGULATORY CLEARANCE","three authorities, three frameworks"),
 ("04","FEATURED BUILD","narrevo.ai — AI video pipeline"),
 ("05","STACK","what is running, not what I once tried"),
 ("06","TRACK RECORD","nine years, nine countries"),
 ("07","HOW I WORK","teams, method, and AI in engineering practice"),
 ("08","ELSEWHERE","where to find the rest")]

out=pathlib.Path("assets");out.mkdir(exist_ok=True)
for tag,p in [("dark",DARK),("light",LIGHT)]:
    for idx,t,s in SECTIONS:
        (out/f"sec-{idx}-{tag}.svg").write_text(section(idx,t,s,p),encoding="utf-8")
    (out/f"stats-{tag}.svg").write_text(stats(p),encoding="utf-8")
    (out/f"regulatory-{tag}.svg").write_text(regulatory(p),encoding="utf-8")
    (out/f"stack-{tag}.svg").write_text(stack(p),encoding="utf-8")
    (out/f"pipeline-{tag}.svg").write_text(pipeline(p),encoding="utf-8")
    (out/f"timeline-{tag}.svg").write_text(timeline(p),encoding="utf-8")
print(sum(f.stat().st_size for f in out.glob("*.svg"))//1024,"KB total,",len(list(out.glob("*.svg"))),"files")

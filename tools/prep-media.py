from PIL import Image, ImageOps, ImageEnhance
import numpy as np, pathlib
U="/mnt/user-data/uploads/readme-titovich2203"

# ---------- PORTRAIT ----------
src=Image.open(f"{U}/photo.png").convert("RGB")
# square crop on the face (scaled from the jpg reference)
x0,y0,s=180,177,480
sq=src.crop((x0,y0,x0+s,y0+s)).resize((672,672),Image.LANCZOS)
sq.save("img/portrait-raw.jpg",quality=92)

def duotone(im,dark,light,gamma=1.0):
    g=ImageOps.grayscale(im)
    g=ImageEnhance.Contrast(g).enhance(1.12)
    a=np.asarray(g).astype(np.float32)/255.0
    a=np.power(a,gamma)
    d=np.array(dark,dtype=np.float32); l=np.array(light,dtype=np.float32)
    out=d[None,None,:]+(l-d)[None,None,:]*a[:,:,None]
    return Image.fromarray(out.clip(0,255).astype(np.uint8))

def neutral(im,tint=(0.98,1.0,1.0),sat=.45):
    e=ImageEnhance.Color(im).enhance(sat)
    e=ImageEnhance.Contrast(e).enhance(1.08)
    a=np.asarray(e).astype(np.float32)*np.array(tint,dtype=np.float32)[None,None,:]
    return Image.fromarray(a.clip(0,255).astype(np.uint8))

sm=sq.resize((336,336),Image.LANCZOS)
duotone(sm,(8,18,14),(228,246,238),0.95).save("img/portrait-duo-dark.jpg",quality=86)
duotone(sm,(16,32,26),(255,255,255),1.05).save("img/portrait-duo-light.jpg",quality=86)
neutral(sm).save("img/portrait-nat-dark.jpg",quality=86)
neutral(sm,(1.0,1.0,.99),.55).save("img/portrait-nat-light.jpg",quality=86)

# ---------- LOGOS ----------
def trim(im):
    a=np.asarray(im); al=a[:,:,3]
    ys,xs=np.where(al>8)
    return im.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))

def recolor_flat(im,rgb):
    a=np.asarray(im).astype(np.uint8).copy()
    a[:,:,0],a[:,:,1],a[:,:,2]=rgb
    return Image.fromarray(a)

def swap_neutrals(im,to_rgb,lum_gt=150):
    a=np.asarray(im).astype(np.int16).copy()
    r,g,b=a[:,:,0],a[:,:,1],a[:,:,2]
    mx=a[:,:,:3].max(axis=2); mn=a[:,:,:3].min(axis=2)
    lum=(0.299*r+0.587*g+0.114*b)
    m=((mx-mn)<40)&(lum>lum_gt)&(a[:,:,3]>10)
    for i,v in enumerate(to_rgb): a[:,:,i]=np.where(m,v,a[:,:,i])
    return Image.fromarray(a.astype(np.uint8))

def norm(im,h=104):
    im=trim(im); w=int(im.size[0]*h/im.size[1])
    return im.resize((w,h),Image.LANCZOS)

L=lambda n: Image.open(f"{U}/logos/{n}").convert("RGBA")
INK_L=(31,35,40)
out={}
out["copay-dark"]=norm(L("copay 5.png"));           out["copay-light"]=norm(L("copay 1.png"))
out["wiicode-dark"]=norm(L("logo wiicode white.png")); out["wiicode-light"]=norm(L("logo wiicode.png"))
out["toosign-dark"]=norm(recolor_flat(L("logo_blue toosign.png"),(120,190,235))); out["toosign-light"]=norm(L("logo_blue toosign.png"))
out["codify-dark"]=norm(recolor_flat(L("codify.png"),(230,237,243)));  out["codify-light"]=norm(L("codify.png"))
out["faseya-dark"]=norm(recolor_flat(L("logo faseya.png"),(230,237,243))); out["faseya-light"]=norm(L("logo faseya.png"))
nv=L("narrevo logo.png")
out["narrevo-dark"]=norm(nv); out["narrevo-light"]=norm(swap_neutrals(nv,INK_L,110))
for k,v in out.items():
    v.save(f"img/logo-{k}.png",optimize=True)
    print(f"{k:16} {v.size} {pathlib.Path(f'img/logo-{k}.png').stat().st_size//1024}KB")

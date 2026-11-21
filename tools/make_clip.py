import sys, math, random, subprocess, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H,FPS=1080,1920,30
HERE=os.path.dirname(os.path.abspath(__file__))
B=os.path.join(HERE,'assets','Poppins-Bold.ttf')
M=os.path.join(HERE,'assets','Poppins-Medium.ttf')
LOGO=os.path.join(HERE,'assets','logo.png')
GOLD=(232,185,92); CREAM=(250,240,220); NAVY=(14,20,38)
def F(p,s): return ImageFont.truetype(p,s)
def grad(w,h,top,bot):
    im=Image.new('RGB',(w,h)); d=ImageDraw.Draw(im)
    for y in range(h):
        t=y/(h-1); d.line([(0,y),(w,y)],fill=tuple(int(top[i]+(bot[i]-top[i])*t) for i in range(3)))
    return im
def mountains(im,base,amp,col,seed):
    random.seed(seed); d=ImageDraw.Draw(im); w,h=im.size; pts=[(0,h)]; x=0
    while x<=w+50:
        pts.append((x,base-random.random()*amp)); x+=w/random.randint(7,11)
    pts+=[(w,h)]; d.polygon(pts,fill=col)
def background():
    bw,bh=int(W*1.15),int(H*1.15)
    im=grad(bw,bh,(16,20,50),(150,78,64)); d=ImageDraw.Draw(im); random.seed(4)
    for _ in range(500):
        x,y=random.randrange(bw),random.randrange(int(bh*.6)); r=random.choice([1,2,2,3]); a=random.randint(120,255)
        d.ellipse([x-r,y-r,x+r,y+r],fill=(a,a,min(255,a+20)))
    mx,my,mr=bw*.78,bh*.16,95
    g=Image.new('RGBA',(bw,bh),(0,0,0,0)); ImageDraw.Draw(g).ellipse([mx-mr*2.4,my-mr*2.4,mx+mr*2.4,my+mr*2.4],fill=(255,210,150,70))
    im=Image.alpha_composite(im.convert('RGBA'),g.filter(ImageFilter.GaussianBlur(90))).convert('RGB')
    ImageDraw.Draw(im).ellipse([mx-mr,my-mr,mx+mr,my+mr],fill=(250,226,190))
    mountains(im,bh*.74,bh*.12,(58,40,62),1); mountains(im,bh*.84,bh*.10,(32,26,46),2); mountains(im,bh*.94,bh*.07,NAVY,5)
    # darken for text legibility
    ov=Image.new('RGBA',(bw,bh),(8,10,24,95)); im=Image.alpha_composite(im.convert('RGBA'),ov)
    return im
def text_layer(lines):
    """lines: list of (text, font, color, y_center, start_s, max_width) -> list of (RGBA image, x, y, start)"""
    out=[]
    for t,f,c,yc,st in lines:
        d=ImageDraw.Draw(Image.new('RGB',(1,1))); bb=d.textbbox((0,0),t,font=f,anchor='lt')
        w,h=bb[2]-bb[0]+24,bb[3]-bb[1]+24
        L=Image.new('RGBA',(w,h),(0,0,0,0)); ld=ImageDraw.Draw(L)
        sh=Image.new('RGBA',(w,h),(0,0,0,0)); ImageDraw.Draw(sh).text((12-bb[0],14-bb[1]),t,font=f,fill=(0,0,0,200),anchor='lt')
        L=Image.alpha_composite(L,sh.filter(ImageFilter.GaussianBlur(4)))
        ImageDraw.Draw(L).text((12-bb[0],12-bb[1]),t,font=f,fill=c,anchor='lt')
        out.append((L,(W-w)//2,int(yc-h/2),st))
    return out
def card_layer(text,sub,yc,st):
    w,h=900,190; L=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(L)
    d.rounded_rectangle([0,0,w-1,h-1],radius=36,fill=(14,18,40,215),outline=GOLD,width=4)
    d.text((w//2,72),text,font=fit(text,B,64,840),fill=CREAM,anchor='mm'); d.text((w//2,140),sub,font=fit(sub,M,40,840),fill=GOLD,anchor='mm')
    return (L,(W-w)//2,int(yc-h/2),st)
def ease(t): t=max(0,min(1,t)); return 1-(1-t)**3
def render(out,layers,dur):
    bg=background(); logo=Image.open(LOGO).resize((190,190),Image.LANCZOS)
    wm=text_layer([("Forever Field Notes",F(B,40),CREAM,0,0)])[0][0]
    path=out
    p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
        '-f','lavfi','-i','anullsrc=r=44100:cl=stereo','-shortest','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',
        '-c:a','aac','-b:a','128k','-movflags','+faststart',path],stdin=subprocess.PIPE)
    n=int(dur*FPS)
    for i in range(n):
        s=i/FPS; z=1+0.06*s/dur
        cw,ch=int(W*1.15/z),int(H*1.15/z); bw,bh=bg.size
        fr=bg.crop(((bw-cw)//2,(bh-ch)//2,(bw-cw)//2+cw,(bh-ch)//2+ch)).resize((W,H),Image.BILINEAR)
        fr.alpha_composite(logo,((W-190)//2,150))
        fr.alpha_composite(wm,((W-wm.width)//2,355))
        for L,x,y,st in layers:
            a=ease((s-st)/0.45)
            if a<=0: continue
            l=L if a>=1 else L.copy()
            if a<1:
                al=l.getchannel('A').point(lambda v:int(v*a)); l.putalpha(al)
            fr.alpha_composite(l,(x,y+int((1-a)*60)))
        # fade out last 0.4s
        if s>dur-0.4:
            k=(dur-s)/0.4; fr=Image.blend(Image.new('RGBA',(W,H),(0,0,0,255)),fr,k)
        p.stdin.write(fr.convert('RGB').tobytes())
    p.stdin.close(); p.wait(); print(path)

def fit(text,path,size,maxw):
    while size>30 and ImageDraw.Draw(Image.new('RGB',(1,1))).textlength(text,font=F(path,size))>maxw: size-=4
    return F(path,size)

def build(spec,out):
    """spec: {"title":[line1,line2], "cards":[[title,sub],...(max 3)], "footer":[line,cta], "dur":12}"""
    t=spec["title"]; cards=spec.get("cards",[]); foot=spec.get("footer",["",""])
    L=text_layer([(t[0],fit(t[0],B,104,980),CREAM,610,0.2),(t[1],fit(t[1],B,124,980),GOLD,740,0.6)])
    step=max(1.0,(spec.get("dur",12)-6)/max(1,len(cards)))
    for k,(a,b) in enumerate(cards[:3]):
        L.append(card_layer(a,b,980+230*k,1.6+step*k*0.8))
    y=980+230*len(cards[:3])-20
    if foot[0]: L+=text_layer([(foot[0],fit(foot[0],M,46,980),CREAM,y+40,1.6+step*len(cards)*0.8)])
    if len(foot)>1 and foot[1]: L+=text_layer([(foot[1],fit(foot[1],B,52,980),GOLD,y+130,2.4+step*len(cards)*0.8)])
    render(out,L,spec.get("dur",12))

if __name__=="__main__":
    # usage: python3 make_clip.py spec.json out.mp4
    import json
    build(json.load(open(sys.argv[1])),sys.argv[2])

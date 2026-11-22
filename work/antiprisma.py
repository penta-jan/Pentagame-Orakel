import numpy as np
from scipy.spatial import ConvexHull
from collections import defaultdict
phi=(1+5**0.5)/2; d=5**0.5            # Kugeldurchmesser sqrt5, Luecken 1 (Fuenfeck) und 3 (Wechselstrecke)
a=d+1; Lw=d+3                           # Mittelpunktsabstaende: 2phi und 2phi^2
R=a/(2*np.sin(np.radians(36)))
h=np.sqrt(Lw**2-(2*R*np.sin(np.radians(18)))**2)
rb=d/2
SC=0.56
e=np.radians(19); az=np.radians(10)
cols={'Holz':'my_green','Feuer':'my_red','Erde':'my_yellow','Metall':'my_white','Wasser':'my_blue'}
names=['Holz','Feuer','Erde','Metall','Wasser']
V=[];lab=[]
for k,n in enumerate(names):
    a=np.radians(90-72*k); V.append((R*np.cos(a),R*np.sin(a),h)); lab.append(('E',n))
for k,n in enumerate(names):
    a=np.radians(90-72*k+180); V.append((R*np.cos(a),R*np.sin(a),0)); lab.append(('K',n))
V=np.array(V); ca,sa=np.cos(az),np.sin(az)
V=np.array([(x*ca-y*sa,x*sa+y*ca,z) for x,y,z in V])
view=np.array([0,-np.cos(e),np.sin(e)])
P=lambda p:(p[0], p[2]*np.cos(e)+p[1]*np.sin(e))
depth=lambda p: p[1]*np.cos(e)-p[2]*np.sin(e)
hull=ConvexHull(V); ed=defaultdict(list)
for simp,eq in zip(hull.simplices,hull.equations):
    for i in range(3):
        a,b=sorted((simp[i],simp[(i+1)%3])); ed[(a,b)].append(eq[:3])
L=lambda a,b,s: r"\draw[%s, shorten <=%.3fcm, shorten >=%.3fcm] (%.3f,%.3f) -- (%.3f,%.3f);"%(s,rb*SC*0.92,rb*SC*0.92,*P(V[a]),*P(V[b]))
def ball(i):
    x,y=P(V[i]); c=cols[lab[i][1]]
    s=r"\shade[ball color=%s] (%.3f,%.3f) circle (%.3f);"%(c+("!88!black" if c=='my_white' else ""),x,y,rb)
    if c=='my_white': s+=r"\draw[black!35, line width=0.3pt] (%.3f,%.3f) circle (%.3f);"%(x,y,rb)
    return s
poly=lambda idx: " -- ".join("(%.3f,%.3f)"%P(V[i]) for i in idx)+" -- cycle"
hidden=[];vislat=[]
for (a,b),ns in ed.items():
    if len(ns)==2 and np.allclose(ns[0],ns[1]): continue
    vis=any(np.dot(n,view)>1e-9 for n in ns)
    lat=lab[a][0]!=lab[b][0]
    if not vis: hidden.append(L(a,b,"black!50, dashed, line width=0.8pt"))
    elif lat: vislat.append(L(a,b,"black!80, line width=1.3pt"))
out=[r"\begin{tikzpicture}[scale=0.56]"]
out+=hidden
out.append(r"\fill[black!8, fill opacity=0.8] %s;"%poly(range(5,10)))
out.append(r"\draw[black!60, line width=1.1pt] %s;"%poly(range(5,10)))
out+=[ball(i) for i in sorted(range(5,10),key=lambda i:-depth(V[i]))]
out+=vislat
out.append(r"\fill[black!6, fill opacity=0.55] %s;"%poly(range(5)))
out.append(r"\draw[black!70, line width=1.1pt] %s;"%poly(range(5)))
out+=[ball(i) for i in sorted(range(5),key=lambda i:-depth(V[i]))]
xr=max(P(V[i])[0] for i in range(10))+rb+0.6
yt=np.mean([P(V[i])[1] for i in range(5)]); yb=np.mean([P(V[i])[1] for i in range(5,10)])
out.append(r"\node[font=\footnotesize\itshape, anchor=west, align=left, overlay] at (%.3f,%.3f) {oben:\\Ring mit Ecken};"%(xr,yt))
out.append(r"\node[font=\footnotesize\itshape, anchor=west, align=left, overlay] at (%.3f,%.3f) {unten:\\Pentagon mit\\Kreuzungen};"%(xr,yb))
ytop=max(P(V[i])[1] for i in range(5))
out.append(r"\draw[-{Stealth[scale=1.1]}, black!60, line width=0.8pt] (0,%.3f) -- (0,%.3f) node[pos=0, above, font=\footnotesize\itshape] {Blick von oben};"%(ytop+rb+1.9,ytop+rb+0.3))
out.append(r"\end{tikzpicture}")
open('/home/claude/work/antiprisma.tex','w').write("\n".join(out)+"\n")
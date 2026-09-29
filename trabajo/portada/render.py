import cadquery as cq, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import sys; sys.path.insert(0,"../cad")
from ensamblaje import conjunto   # piezas colocadas (lista de (nombre, shape))
def tris(shape):
    v,t=shape.tessellate(0.6,0.4); v=np.array([[p.x,p.y,p.z] for p in v]); return v[np.array(t)]
COL={"plataforma":"#2b2d31","peldano":"#2b2d31"}
def dibujar(ax,plegado,dx):
    L=conjunto(plegado)
    zmin=0
    if plegado:
        zmin=min((sh.val() if hasattr(sh,"val") else sh).rotate(cq.Vector(0,0,0),cq.Vector(1,0,0),-15).BoundingBox().ymin for _,sh in L)
    luz=np.array([-0.45,0.8,0.55]); luz/=np.linalg.norm(luz)
    for nom,sh in L:
        sh=sh.val() if hasattr(sh,"val") else sh
        if plegado: sh=sh.rotate(cq.Vector(0,0,0),cq.Vector(1,0,0),-15)
        T=tris(sh); T=T[:,:,[0,2,1]]*np.array([1,-1,1])  # (x, -z, y): y arriba
        T[:,:,0]+=dx
        if plegado: T[:,:,2]-=zmin; T[:,:,1]+=350
        n=np.cross(T[:,1]-T[:,0],T[:,2]-T[:,0]); n/=np.linalg.norm(n,axis=1)[:,None]+1e-12
        base=np.array(matplotlib.colors.to_rgb(COL.get(nom,"#9aa4b1")))
        k=0.45+0.55*np.abs(n@luz)
        c=np.clip(base[None,:]*k[:,None]+0.08*(1-k[:,None]),0,1)
        pc=Poly3DCollection(T,facecolors=c,edgecolors=c,linewidths=0.25); ax.add_collection3d(pc)
        # sombra en el suelo
        S=T.copy(); S[:,:,2]=0.5; S[:,:,1]-=0; 
        ax.add_collection3d(Poly3DCollection(S,facecolors=(0,0,0,0.035),edgecolors="none"))

from PIL import Image
def uno(pleg,fn):
    fig=plt.figure(figsize=(6,6),dpi=500); ax=fig.add_axes([0,0,1,1],projection="3d")
    dibujar(ax,pleg,0)
    ax.set_xlim(-500,500); ax.set_ylim(-500,500); ax.set_zlim(0,1000); ax.set_box_aspect((1,1,1))
    ax.view_init(elev=14,azim=-32 if not pleg else -25); ax.set_proj_type("persp",focal_length=0.35); ax.axis("off")
    fig.savefig(fn,transparent=True); plt.close(fig)
    im=Image.open(fn); return im.crop(im.getbbox())
a=uno(False,"_a.png"); b=uno(True,"_b.png")
# misma escala: la altura en pixeles es proporcional a la altura real (786 vs 861 mm aprox.)
H=max(a.height,b.height); gap=int(0.12*a.width)
M=Image.new("RGBA",(b.width+gap+a.width,H),(0,0,0,0))
M.paste(b,(0,H-b.height),b); M.paste(a,(b.width+gap,H-a.height),a)
M.save("render_portada.png"); print(M.size)

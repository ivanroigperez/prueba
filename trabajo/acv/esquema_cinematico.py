import numpy as np, math, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, sys
sys.path.insert(0,"../cad")
from cinematica import A,S,P,d,rh,uP,qP,cP,eS,qS,cS,Lr,sweep
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":8.5})
def rot2(pt,c,phi):
    phi=math.radians(phi); v=pt-c; return c+np.array([v[0]*math.cos(phi)-v[1]*math.sin(phi),v[0]*math.sin(phi)+v[1]*math.cos(phi)])
angP=sweep(A,uP,qP,cP); angS=sweep(S,eS,qS,cS)
fig,axs=plt.subplots(1,3,figsize=(12,5.6),dpi=220)
for ax,t,tit in zip(axs,(0,20,40),("Abierto (uso)","Posición intermedia","Plegado")):
    th=-41*t/40
    F0=np.array([0,0]); Ft=810*d
    Ptop=P-30*rh; Pbot=P+Lr*rh
    Ptop,Pbot=rot2(Ptop,P,th),rot2(Pbot,P,th)
    ph=math.radians(75 if t==40 else angP[t]); ps=math.radians(75 if t==40 else angS[t])
    def bandeja(G,L,front,phi):
        u=np.array([math.cos(phi),math.sin(phi)]); return G-front*u, G+(L-front)*u, G
    p0,p1,_=bandeja(A,300,20,ph); s0,s1,_=bandeja(S,230,20,ps)
    U=A+uP*np.array([math.cos(ph),math.sin(ph)]); T=S+eS*np.array([math.cos(ps),math.sin(ps)])
    Q=rot2(P+qP*rh,P,th); R=rot2(P+qS*rh,P,th)
    ax.plot([0,0],[0,0]); ax.axhline(0,color="#999",lw=0.8)
    ax.plot(*zip(F0,Ft),color="#1f6fb2",lw=6,solid_capstyle="butt",label="Larguero delantero")
    ax.plot(*zip(Ptop,Pbot),color="#c0392b",lw=6,solid_capstyle="butt",alpha=0.9,label="Pata trasera")
    ax.plot(*zip(p0,p1),color="#333",lw=5,label="Plataforma"); ax.plot(*zip(s0,s1),color="#666",lw=5,label="Peldaño")
    ax.plot(*zip(U,Q),color="#d68910",lw=2.2,label="Biela plataforma"); ax.plot(*zip(T,R),color="#3c8d2f",lw=2.2,label="Tirante peldaño")
    for p in (A,S,P,U,T,Q,R): ax.plot(*p,"o",ms=4.5,mfc="white",mec="k",zorder=5)
    if t==0:
        for p,n in ((A,"A"),(S,"S"),(P,"P")): ax.annotate(n,p,xytext=(p[0]-45,p[1]+8),fontsize=9,fontweight="bold")
        ax.annotate("",xy=(-60,480),xytext=(-60,0),arrowprops=dict(arrowstyle="<->")); ax.text(-95,230,"480",rotation=90)
        ax.annotate("",xy=(-25,240),xytext=(-25,0),arrowprops=dict(arrowstyle="<->")); ax.text(-58,100,"240",rotation=90)
        ax.annotate("",xy=(0,-30),xytext=(496,-30),arrowprops=dict(arrowstyle="<->")); ax.text(200,-60,"496",)
        ax.text(P[0]+15,P[1]+15,"pivote a 657 mm",fontsize=7.5)
    ax.set_aspect("equal"); ax.set_xlim(-120,560); ax.set_ylim(-90,860); ax.axis("off"); ax.set_title(tit,fontsize=10.5,fontweight="bold")
h,l=axs[0].get_legend_handles_labels(); fig.legend(h,l,loc="lower center",ncol=6,fontsize=8,frameon=False,bbox_to_anchor=(0.5,0.04))
fig.suptitle("Esquema cinemático definitivo del mecanismo de plegado (cotas en mm)",fontsize=11.5,fontweight="bold",x=0.01,ha="left")
fig.text(0.01,0.01,"Dos cuadriláteros articulados comparten la pata trasera: al cerrarla, las bielas giran la plataforma y el peldaño hasta quedar paralelos al larguero. Elaboración propia.",fontsize=7,color="#555")
plt.tight_layout(rect=(0,0.08,1,0.95)); plt.savefig("figura_esquema_cinematico.png"); print("ok")

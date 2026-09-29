import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle, FancyBboxPatch
import numpy as np
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":9})
INK="#2b2b2b"; WOOD="#e9dcc6"; WOOD2="#d8c6a6"; RED="#c0392b"; BLUE="#1f6fb2"; GREY="#8a8a8a"

def limb(ax,p,q,w,c,z=5):
    p,q=np.array(p),np.array(q); d=q-p; n=np.array([-d[1],d[0]])/np.linalg.norm(d)*w/2
    ax.add_patch(Polygon([p+n,q+n,q-n,p-n],closed=True,fc=c,ec="none",zorder=z))
    for r in (p,q): ax.add_patch(Circle(r,w/2,fc=c,ec="none",zorder=z))

def persona(ax,x,H,R,c):
    """Silueta de perfil frontal con brazo derecho levantado hasta R"""
    hip=0.53*H; sh=0.815*H
    limb(ax,(x-0.045*H,hip),(x-0.06*H,0.02),0.075*H,c)      # piernas
    limb(ax,(x+0.045*H,hip),(x+0.06*H,0.02),0.075*H,c)
    ax.add_patch(Polygon([(x-0.10*H,hip),(x+0.10*H,hip),(x+0.125*H,sh),(x-0.125*H,sh)],fc=c,ec="none",zorder=5))
    limb(ax,(x-0.11*H,sh-0.01*H),(x-0.15*H,hip-0.03*H),0.05*H,c)   # brazo bajado
    limb(ax,(x+0.11*H,sh-0.01*H),(x+0.13*H,R-0.03),0.05*H,c)       # brazo levantado
    ax.add_patch(Circle((x,0.93*H),0.065*H,fc=c,ec="none",zorder=5))
    limb(ax,(x,0.84*H),(x,0.88*H),0.05*H,c)

def cota(ax,x,y0,y1,txt,c=INK,side="r"):
    ax.annotate("",xy=(x,y0),xytext=(x,y1),arrowprops=dict(arrowstyle="<|-|>",color=c,lw=0.8,mutation_scale=7),zorder=6)
    ax.text(x+(0.04 if side=="r" else -0.04),(y0+y1)/2,txt,rotation=90,va="center",ha="left" if side=="r" else "right",fontsize=7.5,color=c)

# ---------------- FIGURA 1 ----------------
fig,ax=plt.subplots(figsize=(10,6.4),dpi=220)
ax.set_aspect("equal"); ax.set_xlim(-0.45,4.6); ax.set_ylim(-0.32,2.78); ax.axis("off")
# suelo y techo
ax.add_patch(Rectangle((-0.35,-0.12),4.95,0.12,fc="#ececec",ec="none"))
ax.plot([-0.35,4.6],[0,0],color=INK,lw=1.2)
ax.plot([-0.35,4.6],[2.60,2.60],color=GREY,lw=0.8); ax.text(4.58,2.62,"Techo 2,60 m",ha="right",va="bottom",fontsize=7,color=GREY)
# banda fuera de alcance
ax.add_patch(Rectangle((-0.35,1.85),4.95,0.75,fc=RED,alpha=0.07,ec="none",zorder=0))
# mueble bajo con encimera
ax.add_patch(Rectangle((0,0),1.8,0.10,fc="#555",ec="none"))
for i in range(3):
    ax.add_patch(Rectangle((i*0.6+0.01,0.10),0.58,0.76,fc=WOOD,ec=WOOD2,lw=1))
    ax.add_patch(Rectangle((i*0.6+0.25,0.78),0.10,0.018,fc=GREY,ec="none"))
ax.add_patch(Rectangle((-0.02,0.86),1.84,0.04,fc="#9c9c9c",ec="none"))
# muebles altos
for i in range(3):
    ax.add_patch(Rectangle((i*0.6+0.01,1.45),0.58,0.75,fc=WOOD,ec=WOOD2,lw=1))
    ax.add_patch(Rectangle((i*0.6+0.25,1.48),0.10,0.018,fc=GREY,ec="none"))
    for y in (1.70,1.95): ax.plot([i*0.6+0.04,i*0.6+0.56],[y,y],color=WOOD2,lw=0.6,ls=":")
    ax.add_patch(Rectangle((i*0.6+0.01,2.22),0.58,0.36,fc="#f4ecdf",ec=WOOD2,lw=1))
    ax.add_patch(Rectangle((i*0.6+0.25,2.25),0.10,0.018,fc=GREY,ec="none"))
# objetos en baldas
ax.add_patch(Rectangle((0.12,1.955),0.10,0.17,fc="#7fa7c9",ec="none")); ax.add_patch(Rectangle((0.28,1.955),0.14,0.12,fc="#c9a27f",ec="none"))
ax.add_patch(Rectangle((0.75,1.955),0.16,0.20,fc="#9cc98f",ec="none"))
ax.add_patch(Rectangle((1.40,2.30),0.25,0.18,fc="#bda5d6",ec="none"))
# cotas de mobiliario
cota(ax,-0.07,0,0.90,"0,90 m","#555","l")
cota(ax,-0.19,0,1.45,"1,45 m","#555","l")
cota(ax,-0.31,0,2.20,"2,20 m","#555","l")
ax.text(0.9,1.62,"Mueble alto",ha="center",fontsize=8,color="#6b5a3e")
ax.text(0.9,2.40,"Altillo",ha="center",fontsize=8,color="#6b5a3e")
ax.text(0.9,0.45,"Mueble bajo",ha="center",fontsize=8,color="#6b5a3e")
# personas
persona(ax,2.55,1.50,1.85,RED)
persona(ax,3.55,1.74,2.15,BLUE)
for x,y,c in [(2.55+0.13*1.5,1.85,RED),(3.55+0.13*1.74,2.15,BLUE)]:
    ax.plot([-0.05,4.35],[y,y],color=c,lw=1.1,ls=(0,(5,3)),zorder=4)
ax.text(4.36,1.85,"1,85 m",color=RED,fontsize=8.5,va="center",fontweight="bold")
ax.text(4.36,2.15,"2,15 m",color=BLUE,fontsize=8.5,va="center",fontweight="bold")
cota(ax,2.25,0,1.50,"1,50 m",RED,"l"); cota(ax,3.25,0,1.74,"1,74 m",BLUE,"l")
ax.text(2.55,-0.07,"Mujer P5",ha="center",va="top",fontsize=8,color=RED,fontweight="bold")
ax.text(3.55,-0.07,"Hombre P50",ha="center",va="top",fontsize=8,color=BLUE,fontweight="bold")
ax.text(2.0,2.52,"Zona fuera de alcance sin ayuda",color=RED,fontsize=9,fontweight="bold",va="center")
ax.text(2.0,2.43,"(por encima de 1,85 m para una usuaria de percentil 5)",color=RED,fontsize=7.5,va="center")
ax.set_title("Alturas habituales del mobiliario de cocina frente al alcance vertical del usuario",fontsize=11,fontweight="bold",loc="left",pad=8)
ax.text(-0.45,-0.28,"Estaturas y alcances aproximados (alcance ≈ 1,24 × estatura; ver NTP 1050, INSST). Elaboración propia.",fontsize=7,color="#666")
plt.savefig("figura1_alcance_mobiliario.png",bbox_inches="tight"); plt.close()

# ---------------- FIGURA 2 ----------------
fig,ax=plt.subplots(figsize=(8,3.6),dpi=220)
cats=["Caídas","Golpes y choques","Cortes y aplastamientos","Otros"]; vals=[51.1,16.6,14.2,18.1]
cols=[RED,"#b9b9b9","#b9b9b9","#d9d9d9"]
y=np.arange(len(cats))[::-1]
ax.barh(y,vals,color=cols,height=0.62)
for yi,v in zip(y,vals): ax.text(v+0.8,yi,f"{v:.1f} %".replace(".",","),va="center",fontsize=10,fontweight="bold" if v>50 else "normal",color=RED if v>50 else INK)
ax.set_yticks(y,cats,fontsize=10); ax.set_xlim(0,60); ax.set_xticks([])
for s in ["top","right","bottom"]: ax.spines[s].set_visible(False)
ax.tick_params(axis="y",length=0)
fig.text(0.01,0.95,"Accidentes domésticos y de ocio en España según su tipo",fontsize=11.5,fontweight="bold")
ax.text(0,-0.95,"Más de la mitad de los accidentes se deben a caídas; el 54,5 % ocurre en el interior de la vivienda.",fontsize=8.5,color="#444",transform=ax.get_yaxis_transform())
fig.text(0.01,0.01,"Fuente: Ministerio de Sanidad / Instituto Nacional del Consumo, informe DADO 2011. Elaboración propia.",fontsize=7,color="#666")
plt.tight_layout(rect=(0,0.04,1,0.92)); plt.savefig("figura2_accidentes_DADO.png"); plt.close()

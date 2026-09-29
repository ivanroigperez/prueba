import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":9})
INK="#2b2b2b"; RED="#c0392b"; BLUE="#1f6fb2"; GREEN="#3c8d2f"; GREY="#8a8a8a"; ORANGE="#d68910"; BROWN="#8d6e4a"

# ---- FIG 5: precios de la competencia ----
prod=[("IKEA BOLMEN\n(PP, 1 peldaño)",1.50,"Plástico"),("Altipesa aluminio\n2 peldaños",19.27,"Aluminio"),
("IKEA BEKVÄM\n(haya, no plegable)",24.99,"Madera"),("Hailo Safety\n4312-001 (acero)",52.39,"Acero"),
("Hailo K20\n4396-901 (acero)",58.87,"Acero"),("Hailo L90\n4442-701 (aluminio)",86.03,"Aluminio")]
col={"Plástico":"#9b59b6","Aluminio":"#7f8c8d","Madera":BROWN,"Acero":BLUE}
fig,ax=plt.subplots(figsize=(9,4.6),dpi=220)
x=np.arange(len(prod))
ax.bar(x,[p[1] for p in prod],color=[col[p[2]] for p in prod],width=0.62)
for xi,p in zip(x,prod): ax.text(xi,p[1]+1.5,f"{p[1]:.2f} €".replace(".",","),ha="center",fontsize=8.5,fontweight="bold")
ax.axhspan(0,45,xmin=0,xmax=1,color=GREEN,alpha=0.06)
ax.axhline(45,color=GREEN,lw=1.6,ls="--"); ax.text(0.7,46.5,"Precio objetivo ≤ 45 €",color=GREEN,ha="left",fontweight="bold",fontsize=9)
ax.axhline(54.1,color=RED,lw=1,ls=":"); ax.text(-0.35,56,"Media plegables 150 kg ≈ 54 €",color=RED,fontsize=8)
ax.set_xticks(x,[p[0] for p in prod],fontsize=7.8); ax.set_ylabel("Precio de venta (€, IVA incl.)"); ax.set_ylim(0,97)
for s in ["top","right"]: ax.spines[s].set_visible(False)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=c,label=k) for k,c in col.items()],frameon=False,loc="upper left",fontsize=8,ncol=4)
ax.set_title("Precio de venta de taburetes-escalera del mercado español",fontsize=11,fontweight="bold",loc="left")
fig.text(0.01,0.01,"Fuentes: IKEA, Obramat, ManoMano, comercialpazos.com, tuandco.com (consultado sept. 2026). Elaboración propia.",fontsize=6.8,color="#666")
plt.tight_layout(rect=(0,0.03,1,1)); plt.savefig("figura5_precios_mercado.png"); plt.close()

# ---- FIG 6: rueda estratégica de ecodiseño (LiDS) ----
cats=["Materiales de\nbajo impacto","Reducción de\nmaterial","Producción\nlimpia","Distribución\neficiente","Impacto\nen el uso","Vida útil","Fin de vida"]
actual=[2,2,3,2,5,4,2]; objetivo=[4,4,3,4,5,5,4]
ang=np.linspace(0,2*np.pi,len(cats),endpoint=False).tolist(); ang+=ang[:1]
fig=plt.figure(figsize=(7,6.2),dpi=220); ax=plt.subplot(111,polar=True)
for v,c,l in [(actual,GREY,"Taburete de acero típico del mercado"),(objetivo,GREEN,"Objetivo del nuevo diseño")]:
    vv=v+v[:1]; ax.plot(ang,vv,color=c,lw=2,label=l); ax.fill(ang,vv,color=c,alpha=0.15)
ax.set_xticks(ang[:-1],cats,fontsize=8.5); ax.set_yticks([1,2,3,4,5],["1","2","3","4","5"],fontsize=7,color="#777"); ax.set_ylim(0,5)
ax.set_theta_offset(np.pi/2); ax.set_theta_direction(-1); ax.tick_params(axis="x",pad=14)
ax.legend(loc="lower center",bbox_to_anchor=(0.5,-0.2),frameon=False,fontsize=8.5,ncol=1)
ax.set_title("Rueda estratégica de ecodiseño (valoración cualitativa, 1 = malo, 5 = muy bueno)",fontsize=10,fontweight="bold",pad=22)
plt.tight_layout(); plt.savefig("figura6_rueda_ecodiseno.png"); plt.close()

# ---- FIG 7: mapa mental ----
fig,ax=plt.subplots(figsize=(12,7.4),dpi=220); ax.set_xlim(-7.2,7.2); ax.set_ylim(-4.6,4.6); ax.axis("off")
ramas=[("USUARIO",["Mujer P5 → alcance 1,85 m","Personas mayores","Uso breve y frecuente","Manejo con una mano"],RED,(0,2.6),"arriba"),
("SEGURIDAD",["Carga 150 kg","Bloqueo automático","Antideslizante","UNE-EN 14183"],"#b03a2e",(3.3,1.9),"der"),
("ALMACENAJE",["Plegado plano ≤ 50 mm","Colgar en la pared","Detrás de una puerta","Asa integrada"],BLUE,(3.8,0),"der"),
("MATERIALES",["Acero","Aluminio","Madera / contrachapado","PP reforzado, TPE"],"#7f8c8d",(3.3,-1.9),"der"),
("FABRICACIÓN",["Tubo curvado","Extrusión","Inyección","Remaches / pasadores"],ORANGE,(0,-2.6),"abajo"),
("ESTÉTICA",["Líneas limpias","Colores neutros","Transmitir solidez","Cocina / salón"],"#8e44ad",(-3.3,-1.9),"izq"),
("MEDIO AMBIENTE",["Reciclable","Monomaterial por pieza","Desmontable","Embalaje de cartón"],GREEN,(-3.8,0),"izq"),
("COSTE",["PVP ≤ 45 €","Series largas","Pocas piezas","Montaje rápido"],BROWN,(-3.3,1.9),"izq")]
ax.add_patch(FancyBboxPatch((-1.7,-0.7),3.4,1.4,boxstyle="round,pad=0.02,rounding_size=0.6",fc=RED,ec="none"))
ax.text(0,0,"TABURETE-ESCALERA\nPLEGABLE",ha="center",va="center",color="white",fontweight="bold",fontsize=11)
for t,items,c,(cx,cy),lado in ramas:
    ax.plot([0,cx],[0,cy],color=c,lw=3.5,solid_capstyle="round",zorder=0)
    ax.add_patch(FancyBboxPatch((cx-0.95,cy-0.25),1.9,0.5,boxstyle="round,pad=0.02,rounding_size=0.2",fc=c,ec="none",zorder=2))
    ax.text(cx,cy,t,ha="center",va="center",color="white",fontweight="bold",fontsize=8.5,zorder=3)
    for k,it in enumerate(items):
        if lado=="der":   ex,ey,ha=cx+1.45,cy+0.66-k*0.44,"left"
        elif lado=="izq": ex,ey,ha=cx-1.45,cy+0.66-k*0.44,"right"
        elif lado=="arriba": ex,ey,ha=-4.5+k*3.0,cy+1.25,"center"
        else: ex,ey,ha=-4.5+k*3.0,cy-1.25,"center"
        sx=cx+(0.95 if lado=="der" else -0.95 if lado=="izq" else 0); sy=cy+(0.25 if lado=="arriba" else -0.25 if lado=="abajo" else 0)
        ax.plot([sx,ex],[sy,ey],color=c,lw=1,alpha=0.7,zorder=0)
        ax.text(ex,ey,it,fontsize=8,ha=ha,va="center",color=INK,zorder=3,bbox=dict(fc="white",ec=c,lw=0.9,boxstyle="round,pad=0.3"))
ax.set_title("Mapa mental del taburete-escalera",fontsize=12,fontweight="bold",loc="left")
plt.savefig("figura7_mapa_mental.png",bbox_inches="tight"); plt.close()

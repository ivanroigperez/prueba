import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":9})
INK="#2b2b2b"; GREY="#8a8a8a"

# ---------------- árbol de estructura del producto ----------------
fig,ax=plt.subplots(figsize=(10,5.9),dpi=220); ax.set_xlim(0,10); ax.set_ylim(0,5.9); ax.axis("off")
def caja(x,y,w,h,t,fc,ec,fs=8.5,bold=False,tc=INK,ls="-"):
    ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.10",fc=fc,ec=ec,lw=1.2,ls=ls))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,fontweight="bold" if bold else "normal",color=tc)
caja(5,5.35,6.2,0.62,"CONJUNTO: TABURETE-ESCALERA PLEGABLE","#c0392b","#8e2a1f",9.5,True,"white")
subs=[("Bastidor\ndelantero",["Larguero delantero (1) ×2","Travesaño-asidero (3) ×1"],["Soportar el peso","Ofrecer agarre","Transportarlo"],"#fbe9e7","#c0392b"),
      ("Bastidor\ntrasero",["Pata trasera (2) ×2","Travesaño trasero (4) ×1"],["Soportar el peso","Dar estabilidad"],"#fdf2e3","#d68910"),
      ("Superficies\nde apoyo",["Plataforma (5) ×1","Peldaño (6) ×1"],["Apoyar el pie","Transportarlo\n(hueco-asa)"],"#e8f1fa","#1f6fb2"),
      ("Mecanismo de\nplegado y bloqueo",["Biela (7) ×2","Tirante (8) ×2","Pasador (9) ×10","Pestillo* ×1"],["Plegar y desplegar","Bloquear en uso"],"#efe9f6","#6c3fa0"),
      ("Apoyos\nal suelo",["Taco (10) ×4"],["No deslizar","No marcar el suelo"],"#eef6ea","#3c8d2f")]
xs=[1.0,3.0,5.0,7.0,9.0]
ax.plot([xs[0],xs[-1]],[4.72,4.72],color=GREY,lw=1); ax.plot([5,5],[5.04,4.72],color=GREY,lw=1)
for x,(t,piezas,funcs,fc,ec) in zip(xs,subs):
    ax.plot([x,x],[4.72,4.52],color=GREY,lw=1)
    caja(x,4.18,1.86,0.66,t,ec,ec,8.6,True,"white")
    y=3.55
    for p in piezas:
        ax.plot([x,x],[y+0.27,y+0.2],color=ec,lw=1)
        caja(x,y,1.86,0.4,p,fc,ec,7.6); y-=0.5
    ax.text(x,1.42,"Funciones",ha="center",fontsize=7.4,color=ec,fontweight="bold")
    yy=1.18
    for f in funcs:
        ax.text(x,yy,"• "+f,ha="center",va="top",fontsize=7.2,color="#444"); yy-=0.27+0.2*f.count("\n")
ax.plot([0.1,9.9],[1.62,1.62],color="#ddd",lw=0.8)
ax.text(5,0.08,"(n) = marca en la lista de piezas del plano de conjunto.   * Pestillo dimensionado en el apartado 3.5, pendiente de diseño de detalle.\n"
        "Todas las uniones son articulaciones con pasadores desmontables, lo que facilita la reparación y la separación de materiales (R15 y R21).",
        ha="center",va="bottom",fontsize=7,color="#555")
ax.set_title("Árbol de estructura del taburete-escalera",fontsize=11,fontweight="bold",loc="left")
plt.savefig("figura_estructura.png",bbox_inches="tight"); plt.close(); print("ok")

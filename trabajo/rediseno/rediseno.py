import numpy as np, json, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":8})
# ===================== QFD =====================
ques=[("Que sea seguro y estable",5),("Que permita llegar alto",5),("Que sea ligero de llevar",4),("Que ocupe poco guardado",4),
      ("Que sea cómodo al subir",4),("Que se abra y cierre fácil",4),("Que sea barato",3),("Que respete el medio ambiente",3),("Que sea bonito",2)]
comos=[("Carga máx. (kg)","↑","150"),("Altura plataf. (mm)","◎","480"),("Peso total (kg)","↓","≤ 3,5"),("Espesor plegado (mm)","↓","≤ 50"),
       ("Prof. peldaño (mm)","↑","≥ 200"),("Tiempo apertura (s)","↓","≤ 3"),("Coste fabric. (€)","↓","≤ 17,3"),("Huella CO₂ (kg)","↓","mínima"),("Nº piezas distintas","↓","≤ 10")]
R=np.array([  # 9 fuerte, 3 media, 1 débil, 0 nada
 [9,3,1,0,3,3,0,0,1],   # seguro
 [1,9,0,0,1,0,0,0,0],   # llegar alto
 [3,1,9,3,1,0,1,3,3],   # ligero
 [0,1,3,9,1,1,0,1,3],   # poco guardado
 [3,3,0,1,9,0,0,0,0],   # comodo
 [1,0,3,3,0,9,0,0,3],   # abrir/cerrar
 [3,1,3,1,1,1,9,1,9],   # barato
 [1,0,9,3,0,0,3,9,3],   # medio ambiente
 [0,0,1,3,1,0,3,1,1]])  # bonito
imp=np.array([q[1] for q in ques]); score=imp@R; rel=100*score/score.sum()
comp={"Hailo K20 (acero)":[5,5,2,5,5,4,2,4,2,3,3],"Altipesa (aluminio)":[3,4,5,5,2,4,5,3,2],"Nuestro diseño (alt. 2)":[5,5,5,5,5,4,4,2,4]}
comp={k:v[:9] for k,v in comp.items()}
fig,ax=plt.subplots(figsize=(13,8.3),dpi=200); ax.set_xlim(0,130); ax.set_ylim(0,122); ax.axis("off")
x0,y0,cw,rh=38,18,6.2,4.6; n=len(comos); m=len(ques)
# cuerpo
for i,(q,w) in enumerate(ques):
    y=y0+(m-1-i)*rh
    ax.add_patch(Rectangle((2,y),30,rh,fill=False,lw=0.5)); ax.text(3,y+rh/2,q,va="center",fontsize=7.5)
    ax.add_patch(Rectangle((32,y),6,rh,fill=False,lw=0.5)); ax.text(35,y+rh/2,str(w),ha="center",va="center",fontsize=8,fontweight="bold")
    for j in range(n):
        ax.add_patch(Rectangle((x0+j*cw,y),cw,rh,fill=False,lw=0.5))
        v=R[i,j]; sym={9:"●",3:"○",1:"△",0:""}[v]; ax.text(x0+j*cw+cw/2,y+rh/2,sym,ha="center",va="center",fontsize=9)
    # evaluación competitiva
    for k,(nm,vals) in enumerate(comp.items()):
        xc=x0+n*cw+6+vals[i]*6; ax.plot(xc,y+rh/2,["s","^","o"][k],color=["#7f8c8d","#d68910","#c0392b"][k],ms=4.5)
for k in range(1,6): ax.text(x0+n*cw+6+k*6,y0+m*rh+1,str(k),ha="center",fontsize=7)
for k,(nm,vals) in enumerate(comp.items()):
    xs=[x0+n*cw+6+v*6 for v in vals]; ys=[y0+(m-1-i)*rh+rh/2 for i in range(m)]
    ax.plot(xs,ys,color=["#7f8c8d","#d68910","#c0392b"][k],lw=0.9,marker=["s","^","o"][k],ms=4,label=nm)
ax.legend(loc="upper right",bbox_to_anchor=(1.0,0.72),fontsize=7.5,frameon=False)
ax.text(x0+n*cw+6+18,y0+m*rh+5,"Evaluación del cliente (1-5)",ha="center",fontsize=7.5,fontweight="bold")
# cabecera cómos (vertical)
for j,(c,d,t) in enumerate(comos):
    x=x0+j*cw; yt=y0+m*rh
    ax.add_patch(Rectangle((x,yt),cw,4,fill=False,lw=0.5)); ax.text(x+cw/2,yt+2,d,ha="center",va="center",fontsize=9)
    ax.add_patch(Rectangle((x,yt+4),cw,20,fill=False,lw=0.5)); ax.text(x+cw/2,yt+14,c,rotation=90,ha="center",va="center",fontsize=6.5)
    # tejado
    pass
# tejado (correlaciones)
top=y0+m*rh+24
roof=[(0,2,"−"),(2,3,"+"),(2,7,"++"),(0,3,"−"),(3,4,"−"),(2,6,"+"),(6,8,"+"),(5,8,"+")]
for j in range(n):
    for k in range(j+1,n):
        cx=x0+(j+k+1)*cw/2; cy=top+(k-j)*cw/2
        ax.add_patch(Polygon([(cx,cy-cw/2),(cx+cw/2,cy),(cx,cy+cw/2),(cx-cw/2,cy)],fill=False,lw=0.3,ec="#999"))
for j,k,s in roof:
    cx=x0+(j+k+1)*cw/2; cy=top+(k-j)*cw/2; ax.text(cx,cy,s,ha="center",va="center",fontsize=7.5,fontweight="bold",color="#c0392b" if "−" in s else "#1e8449")
# filas inferiores
for r,(lab,vals) in enumerate((("Importancia absoluta",[f"{v:.0f}" for v in score]),("Importancia relativa (%)",[f"{v:.1f}".replace(".",",") for v in rel]),("Valor objetivo",[c[2] for c in comos]))):
    y=y0-(r+1)*4.5
    ax.add_patch(Rectangle((2,y),36,4.5,fill=False,lw=0.5)); ax.text(3,y+2.25,lab,va="center",fontsize=7.5,fontweight="bold")
    for j,v in enumerate(vals):
        ax.add_patch(Rectangle((x0+j*cw,y),cw,4.5,fill=False,lw=0.5)); ax.text(x0+j*cw+cw/2,y+2.25,v,ha="center",va="center",fontsize=6.8)
ax.text(2,118,"Casa de la calidad (QFD) del taburete-escalera",fontsize=11,fontweight="bold")
ax.text(2,114,"Relación: ● fuerte (9)  ○ media (3)  △ débil (1)   ·   Dirección: ↑ maximizar  ↓ minimizar  ◎ valor nominal   ·   Tejado: + sinergia, − conflicto",fontsize=7)
plt.savefig("figura_qfd.png",bbox_inches="tight"); plt.close()
json.dump({"comos":[c[0] for c in comos],"abs":score.tolist(),"rel":rel.tolist()},open("qfd.json","w"),ensure_ascii=False)
print("QFD:",[(c[0],round(r,1)) for c,r in zip(comos,rel)])

# ===================== ANÁLISIS DEL VALOR =====================
F=["Soportar la carga","Dar estabilidad","Apoyar el pie","Ofrecer agarre","Plegar y desplegar","Bloquear en uso","Transportar y guardar","Estética","Antideslizante / no marcar"]
valor=np.array([20,18,14,6,10,12,8,4,8.])
coste_comp={"Largueros":3.88,"Patas traseras":3.66,"Trav. asidero":0.71,"Trav. trasero":0.65,"Plataforma":1.53,"Peldaño":1.30,"Bielas":0.63,"Tirantes":0.60,"Pasadores":0.30,"Tacos":0.20}
reparto={"Largueros":[40,25,0,15,10,0,0,10,0],"Patas traseras":[40,40,0,0,15,0,0,5,0],"Trav. asidero":[0,20,0,60,0,0,0,20,0],"Trav. trasero":[30,70,0,0,0,0,0,0,0],
 "Plataforma":[25,0,50,0,0,0,15,10,0],"Peldaño":[30,0,60,0,0,0,0,10,0],"Bielas":[30,0,0,0,50,20,0,0,0],"Tirantes":[30,0,0,0,50,20,0,0,0],"Pasadores":[40,0,0,0,60,0,0,0,0],"Tacos":[0,0,0,0,0,0,0,0,100]}
cf=np.zeros(len(F))
for c,e in coste_comp.items(): cf+=e*np.array(reparto[c])/100
cpct=100*cf/cf.sum()
fig,ax=plt.subplots(figsize=(10,4.8),dpi=200); x=np.arange(len(F))
ax.bar(x-0.2,valor,0.4,color="#1e8449",label="Valor para el cliente (%)"); ax.bar(x+0.2,cpct,0.4,color="#c0392b",label="Coste de la función (%)")
for i in range(len(F)):
    ax.text(x[i]-0.2,valor[i]+0.4,f"{valor[i]:.0f}",ha="center",fontsize=7); ax.text(x[i]+0.2,cpct[i]+0.4,f"{cpct[i]:.1f}".replace(".",","),ha="center",fontsize=7)
ax2=ax.twinx(); ax2.plot(x,np.cumsum(valor),color="#1e8449",marker="o",lw=1.2); ax2.plot(x,np.cumsum(cpct),color="#c0392b",marker="s",lw=1.2); ax2.set_ylim(0,110); ax2.set_ylabel("Acumulado (%)")
ax.set_xticks(x,F,rotation=25,ha="right",fontsize=7.5); ax.set_ylabel("%"); ax.set_ylim(0,max(cpct.max(),valor.max())*1.25)
ax.legend(loc="upper left",frameon=False,fontsize=8); ax.set_title("Análisis del valor: valor para el cliente frente a coste de cada función",fontsize=10.5,fontweight="bold",loc="left")
for s in["top"]: ax.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig("figura_analisis_valor.png"); plt.close()
json.dump({"F":F,"valor":valor.tolist(),"coste_eur":cf.tolist(),"coste_pct":cpct.tolist(),"coste_comp":coste_comp},open("av.json","w"),ensure_ascii=False)
print("AV:",[(f,v,round(c,1)) for f,v,c in zip(F,valor,cpct)])

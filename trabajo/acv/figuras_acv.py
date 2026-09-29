import json, numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys; sys.path.insert(0,"../cad")
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":9})
R=json.load(open("resultados_acv.json"))
alts=["ALT1_ACERO","ALT2_ALUMINIO","ALT3_MADERA"]; lab=["Alternativa 1\nAcero","Alternativa 2\nAluminio + PP","Alternativa 3\nMadera"]
fases=[("produccion","Producción","#1f6fb2"),("transporte","Transporte","#d68910"),("uso","Uso","#8e44ad"),("fin_de_vida","Fin de vida","#7f8c8d")]
# ---- Fig A: por fases ----
fig,ax=plt.subplots(figsize=(8.5,4.8),dpi=220); x=np.arange(3); b=np.zeros(3)
for k,n,c in fases:
    v=np.array([R[a][k] for a in alts]); ax.bar(x,v,0.55,bottom=b,color=c,label=n); b+=v
for i,a in enumerate(alts):
    ax.text(i,b[i]+0.6,f"{R[a]['total_A_C']:.1f}".replace(".",","),ha="center",fontweight="bold",fontsize=10)
    ax.bar(i+0.33,R[a]["modulo_D"],0.12,color="#3c8d2f",alpha=0.8,label="Beneficio del reciclaje (módulo D)" if i==0 else None)
    ax.text(i+0.33,R[a]["modulo_D"]-1.3,f"{R[a]['modulo_D']:.1f}".replace(".",","),ha="center",fontsize=8,color="#3c8d2f")
ax.axhline(0,color="k",lw=0.8); ax.set_xticks(x,lab); ax.set_ylabel("kg CO₂-eq por taburete"); ax.set_ylim(-17,31)
for s in["top","right"]: ax.spines[s].set_visible(False)
ax.legend(frameon=False,fontsize=8,loc="upper left")
ax.set_title("Huella de carbono de las tres alternativas por fase del ciclo de vida",fontsize=11,fontweight="bold",loc="left")
fig.text(0.01,0.01,"Factores: ICE v2.0 (Univ. Bath), DEFRA 2024 (transporte), MITECO 2024 (electricidad). Masas: modelo SolidWorks. Elaboración propia.",fontsize=6.5,color="#666")
plt.tight_layout(rect=(0,0.03,1,1)); plt.savefig("figura_acv_fases.png"); plt.close()
# ---- Fig B: producción por componente ----
nom={"Larguero_delantero":"Largueros del.","Pata_trasera":"Patas traseras","Travesano_asidero":"Trav. asidero","Travesano_trasero":"Trav. trasero","Plataforma":"Plataforma","Peldano":"Peldaño","Biela_plataforma":"Bielas plat.","Tirante_peldano":"Tirantes peld.","Pasador":"Pasadores","Taco":"Tacos"}
fig,axs=plt.subplots(1,3,figsize=(12,4.3),dpi=220,sharey=True)
cols=["#1f6fb2","#7f8c8d","#8d6e4a"]
for ax,a,l,c in zip(axs,alts,lab,cols):
    d=R[a]["prod_componentes"]; ks=list(nom); v=[d[k] for k in ks]
    ax.barh(range(len(ks)),v,color=c); ax.set_yticks(range(len(ks)),[nom[k] for k in ks]); ax.invert_yaxis()
    for j,vv in enumerate(v): ax.text(vv+max(v)*0.02,j,f"{vv:.2f}".replace(".",","),va="center",fontsize=7.5)
    ax.set_title(l.replace("\n"," – ")+f"\n(total producción {R[a]['produccion']:.1f} kg CO₂-eq)".replace(".",","),fontsize=9.5)
    ax.set_xlim(0,max(v)*1.22)
    for s in["top","right"]: ax.spines[s].set_visible(False)
axs[1].set_xlabel("kg CO₂-eq (fase de producción)")
fig.suptitle("Huella de carbono de la fase de producción por componente",fontsize=11,fontweight="bold",x=0.01,ha="left")
plt.tight_layout(); plt.savefig("figura_acv_componentes.png"); plt.close()
print("ok")

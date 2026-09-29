import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
with plt.xkcd(scale=0.6,length=120,randomness=2):
    plt.rcParams["font.family"]="DejaVu Sans"
    fig,axs=plt.subplots(1,3,figsize=(13,6),dpi=200,gridspec_kw=dict(width_ratios=[1.35,0.55,1.1]))
    # --- vista lateral abierta (mm) ---
    ax=axs[0]; ax.set_aspect("equal"); ax.set_xlim(-120,840); ax.set_ylim(-110,820); ax.axis("off")
    ax.plot([-100,820],[0,0],"k",lw=1.2)
    F0=np.array([60,0]); F1=np.array([190,480])        # larguero delantero
    R0=np.array([560,0]); R1=np.array([430,480])       # pata trasera
    ax.plot(*zip(F0,F1),color="#1f6fb2",lw=5); ax.plot(*zip(R0,R1),color="#c0392b",lw=5)
    ax.plot([150,470],[480,480],color="#333",lw=7)       # plataforma
    ax.plot([60+130*0.5,60+130*0.5+220],[240,240],color="#333",lw=6)  # peldano 1
    ax.plot([60+130*0.5+220,560-130*0.5],[240,240],color="#c0392b",lw=1.8,ls="--")  # tirante
    ax.plot([150,150],[480,760],color="#555",lw=3); ax.plot([150,300],[760,760],color="#555",lw=3)  # asidero
    for p in [F1,R1,(60+130*0.5+220,240)]: ax.plot(*p,"o",ms=8,mfc="white",mec="k")
    ax.annotate("asidero\n(opcional, R11)",xy=(230,760),xytext=(330,700),arrowprops=dict(arrowstyle="->"),fontsize=9)
    ax.annotate("plataforma\nprofunda ~300 mm",xy=(400,485),xytext=(470,600),arrowprops=dict(arrowstyle="->"),fontsize=9)
    ax.annotate("peldaño abatible\n(~200 mm)",xy=(200,245),xytext=(-110,360),arrowprops=dict(arrowstyle="->"),fontsize=9)
    ax.annotate("tirante\nde bloqueo",xy=(420,240),xytext=(585,95),arrowprops=dict(arrowstyle="->"),fontsize=9)
    ax.annotate("articulación",xy=R1,xytext=(540,400),arrowprops=dict(arrowstyle="->"),fontsize=9)
    ax.annotate("",xy=(790,480),xytext=(790,0),arrowprops=dict(arrowstyle="<->")); ax.text(802,200,"480",rotation=90,fontsize=10)
    ax.annotate("",xy=(0,240),xytext=(0,0),arrowprops=dict(arrowstyle="<->")); ax.text(-45,90,"240",rotation=90,fontsize=9)
    ax.annotate("",xy=(60,-40),xytext=(560,-40),arrowprops=dict(arrowstyle="<->")); ax.text(230,-62,"~500 (huella)",fontsize=9,va="top")
    ax.set_title("A. Vista lateral, abierto",fontsize=12)
    # --- plegado ---
    ax=axs[1]; ax.set_aspect("equal"); ax.set_xlim(-60,200); ax.set_ylim(-60,820); ax.axis("off")
    ax.plot([-50,190],[0,0],"k",lw=1.2)
    ax.plot([40,40],[0,620],color="#1f6fb2",lw=5); ax.plot([80,80],[0,620],color="#c0392b",lw=5)
    ax.plot([60,60],[40,580],color="#333",lw=4)
    ax.plot([40,40],[620,760],color="#555",lw=3)
    ax.annotate("",xy=(30,-35),xytext=(90,-35),arrowprops=dict(arrowstyle="<->")); ax.text(20,-45,"≤ 50",fontsize=9,va="top")
    ax.text(100,300,"todo queda\nen un plano",fontsize=9)
    ax.set_title("B. Plegado",fontsize=12)
    # --- detalle bloqueo y notas ---
    ax=axs[2]; ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis("off")
    ax.set_title("C. Ideas y notas",fontsize=12)
    notas=["- Peldaños y plataforma giran con el larguero:\n  al cerrar quedan verticales (TRIZ 15, dinamicidad)",
    "- Bloqueo por el propio peso del usuario:\n  el tirante queda 'pasado de punto muerto'",
    "- Pestillo de seguridad con 2 gestos para\n  plegar (evita cierres accidentales)",
    "- Hueco-asa en la plataforma para llevarlo\n  con una mano y colgarlo en la pared",
    "- Tacos de TPE sin marcar el suelo",
    "- Piezas de un solo material y unidas con\n  pasadores/remaches → fácil de separar",
    "- ALTERNATIVAS de material (etapa 4):\n  1) acero  2) aluminio  3) madera + acero"]
    for i,t in enumerate(notas): ax.text(0.1,9.3-i*1.35,t,fontsize=9.2,va="top")
    fig.suptitle("Boceto inicial del concepto (cotas en mm, orientativas)",fontsize=13,x=0.02,ha="left")
    plt.savefig("figura8_boceto_inicial.png",bbox_inches="tight"); plt.close()

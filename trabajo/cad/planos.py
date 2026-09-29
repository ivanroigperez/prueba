import cadquery as cq, numpy as np, math, json, csv, datetime
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from OCP.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape
from OCP.HLRAlgo import HLRAlgo_Projector
from OCP.gp import gp_Ax2, gp_Pnt, gp_Dir
from modelo import piezas
from ensamblaje import conjunto
from cinematica import uP,eS,cP,cS,qP,qS
PZ=piezas("aluminio")
VIEWS={"alzado":((-1,0,0),(0,0,1)),"perfil":((0,0,-1),(-1,0,0)),"planta":((0,1,0),(0,0,1)),
       "alzado_pieza":((0,0,1),(1,0,0)),"lateral_pieza":((1,0,0),(0,0,-1)),"planta_pieza":((0,1,0),(1,0,0)),
       "sup_z":((0,0,1),(1,0,0)),"frente_y":((0,-1,0),(1,0,0)),"lat_x":((1,0,0),(0,1,0)),"iso":((-1,1,-1),(-1,0,1))}
def proyectar(shape,vista,ocultas=False):
    N,X=VIEWS[vista]; algo=HLRBRep_Algo(); algo.Add(shape.wrapped)
    algo.Projector(HLRAlgo_Projector(gp_Ax2(gp_Pnt(0,0,0),gp_Dir(*N),gp_Dir(*X)))); algo.Update(); algo.Hide()
    h=HLRBRep_HLRToShape(algo); out={"v":[],"h":[]}
    for key,comp in (("v",h.VCompound()),("v",h.OutLineVCompound()),("h",h.HCompound() if ocultas else None)):
        if comp is None or comp.IsNull(): continue
        for e in cq.Shape.cast(comp).Edges():
            n=max(2,min(200,int(e.Length()/1.5)+2)); pts=[e.positionAt(t) for t in np.linspace(0,1,n)]
            out[key].append(np.array([[p.x,p.y] for p in pts]))
    return out
class Hoja:
    def __init__(s,titulo,num,escala):
        s.fig=plt.figure(figsize=(420/25.4,297/25.4)); s.ax=s.fig.add_axes([0,0,1,1]); s.ax.set_xlim(0,420); s.ax.set_ylim(0,297); s.ax.axis("off")
        a=s.ax; a.add_patch(plt.Rectangle((20,10),390,277,fill=False,lw=1.4))
        # cajetín
        x0,y0,w,h=230,10,180,40
        a.add_patch(plt.Rectangle((x0,y0),w,h,fill=False,lw=1.2))
        for yy in (y0+10,y0+20,y0+30): a.plot([x0,x0+w],[yy,yy],lw=0.6,color="k")
        a.plot([x0+60,x0+60],[y0,y0+30],lw=0.6,color="k"); a.plot([x0+120,x0+120],[y0,y0+30],lw=0.6,color="k")
        a.text(x0+w/2,y0+35,"UNIVERSIDAD DE LA RIOJA · Grado en Ingeniería Mecánica · Ingeniería Simultánea",ha="center",va="center",fontsize=7)
        a.text(x0+w/2,y0+25,titulo,ha="center",va="center",fontsize=10.5,fontweight="bold")
        for (xx,lab,val) in ((x0,"Escala",escala),(x0+60,"Plano nº",str(num)),(x0+120,"Fecha",datetime.date.today().strftime("%d/%m/%Y"))):
            a.text(xx+3,y0+17.5,lab,fontsize=6,va="center",color="#444"); a.text(xx+30,y0+13,val,fontsize=9,ha="center",va="center",fontweight="bold")
        a.text(x0+3,y0+7,"Dibujado:",fontsize=6,va="center",color="#444"); a.text(x0+17,y0+7,"Iván Roig Pérez",fontsize=6.5,va="center",fontweight="bold"); a.text(x0+63,y0+7,"Sistema europeo (ISO-E)  ⊖⊙",fontsize=6.5,va="center")
        a.text(x0+123,y0+7,"Cotas en mm",fontsize=6.5,va="center")
        s.a=a
    def dibujar(s,proy,ox,oy,esc,lw=0.7,flipx=False):
        for key,style in (("h",dict(lw=0.35,ls=(0,(3,1.5)),color="#333")),("v",dict(lw=lw,color="k"))):
            for pl in proy[key]:
                x=pl[:,0]/esc; y=pl[:,1]/esc
                s.a.plot(ox+x,oy+y,solid_capstyle="round",**style)
    def cota(s,p1,p2,off,txt,vertical=False,fs=7):
        a=s.a; p1=np.array(p1,float); p2=np.array(p2,float)
        if vertical:
            x=p1[0]+off; a.plot([p1[0],x+np.sign(off)*1.5],[p1[1],p1[1]],lw=0.35,color="k"); a.plot([p2[0],x+np.sign(off)*1.5],[p2[1],p2[1]],lw=0.35,color="k")
            a.annotate("",xy=(x,p1[1]),xytext=(x,p2[1]),arrowprops=dict(arrowstyle="<|-|>",lw=0.45,mutation_scale=6,color="k"))
            a.text(x-1.2,(p1[1]+p2[1])/2,txt,rotation=90,ha="center",va="bottom" if True else "top",fontsize=fs)
        else:
            y=p1[1]+off; a.plot([p1[0],p1[0]],[p1[1],y+np.sign(off)*1.5],lw=0.35,color="k"); a.plot([p2[0],p2[0]],[p2[1],y+np.sign(off)*1.5],lw=0.35,color="k")
            a.annotate("",xy=(p1[0],y),xytext=(p2[0],y),arrowprops=dict(arrowstyle="<|-|>",lw=0.45,mutation_scale=6,color="k"))
            a.text((p1[0]+p2[0])/2,y+0.8,txt,ha="center",va="bottom",fontsize=fs)
    def rot(s,x,y,t,fs=8,**k): s.a.text(x,y,t,fontsize=fs,**k)
    def tabla(s,x0,y1,cab,filas,anchos,fs=6.5,alto=5.2):
        a=s.a; y=y1
        for fila,bold in [(cab,True)]+[(f,False) for f in filas]:
            xx=x0
            for v,w in zip(fila,anchos):
                a.add_patch(plt.Rectangle((xx,y-alto),w,alto,fill=bold,fc="#e6e6e6" if bold else "none",ec="k",lw=0.5))
                a.text(xx+1.2,y-alto/2,str(v),fontsize=fs,va="center",fontweight="bold" if bold else "normal"); xx+=w
            y-=alto
    def cerrar(s,pdf,png): s.fig.savefig(png,dpi=160); pdf.savefig(s.fig); plt.close(s.fig)

pdf=PdfPages("../Anexo_Planos.pdf")
# ================= PLANO 1: conjunto abierto =================
comp=cq.Compound.makeCompound([sh.val() for n,sh in conjunto(False)])
H=Hoja("TABURETE-ESCALERA PLEGABLE · CONJUNTO ABIERTO",1,"1:5"); E=5
# alzado (lateral): x=Z, y=Y ; planta: x=Z, y=X ; perfil: x=-X, y=Y
alz=proyectar(comp,"alzado"); pla=proyectar(comp,"planta"); per=proyectar(comp,"perfil")
OXa,OYa=60,100
H.dibujar(alz,OXa,OYa,E)
OXf=215
H.dibujar(per,OXf,OYa,E)
iso=proyectar(comp,"iso"); H.dibujar(iso,352,120,10,lw=0.5)
H.cota((OXa+0,OYa),(OXa+496/E,OYa),-8,"496")
H.cota((OXa-3,OYa),(OXa-3,OYa+480/E),-8,"480",vertical=True)
H.cota((OXa-3,OYa),(OXa-3,OYa+240/E),-3,"240",vertical=True)
H.cota((OXf+225/E,OYa),(OXf+225/E,OYa+786/E),10,"786",vertical=True)
H.cota((OXf-225/E,OYa),(OXf+225/E,OYa),-8,"450")
H.rot(OXa+50,OYa+170,"ALZADO (vista lateral) · E 1:5",fs=7.5,fontweight="bold",ha="center")
H.rot(OXf,OYa+170,"PERFIL (vista frontal) · E 1:5",fs=7.5,fontweight="bold",ha="center")
H.rot(318,102,"VISTA ISOMÉTRICA (E 1:10)",fs=7.5,fontweight="bold")
# lista de piezas
M={r[0]:r for r in csv.reader(open("masas_solidworks.csv"),delimiter=";") if r[0] and r[0]!="Pieza"}
den=[("1","Larguero delantero","Larguero_delantero","Al 6063-T5, tubo 40×20×2"),("2","Pata trasera","Pata_trasera","Al 6063-T5, tubo 40×20×2"),
     ("3","Travesaño asidero","Travesano_asidero","Al 6063-T5, tubo 20×20×2"),("4","Travesaño trasero","Travesano_trasero","Al 6063-T5, tubo 20×20×2"),
     ("5","Plataforma","Plataforma","PP inyectado, e = 3"),("6","Peldaño","Peldano","PP inyectado, e = 3"),
     ("7","Biela plataforma","Biela_plataforma","Al 6063-T5, pletina 20×4"),("8","Tirante peldaño","Tirante_peldano","Al 6063-T5, pletina 20×4"),
     ("9","Pasador Ø8 × 45","Pasador","Acero"),("10","Taco","Taco","Caucho (TPE)")]
filas=[(m,d_,M[k][1],mat,M[k][3]) for m,d_,k,mat in den]
H.tabla(282,285,["Marca","Denominación","Cant.","Material (alternativa 2)","Masa (g)"],filas[::-1],[10,30,10,48,18])
H.rot(282,285-5.2*11-4,"Masa total alternativa 2: 3,17 kg (modelo SolidWorks)",fs=6.5)
# globos
glob=[(1,(60,300),(-14,4)),(2,(430,200),(8,6)),(3,(200,763),(6,4)),(4,(496-60,30),(6,-6)),(5,(250,480),(6,5)),(6,(150,240),(-10,-7)),(7,(300,520),(8,8)),(8,(290,300),(8,-8))]
for n_,(z,y),(dx,dy) in glob:
    px,py=OXa+z/E,OYa+y/E; H.a.plot([px,px+dx],[py,py+dy],lw=0.4,color="k"); H.a.plot(px,py,"o",ms=1.5,color="k")
    H.a.add_patch(plt.Circle((px+dx+np.sign(dx)*3,py+dy),3,fill=False,lw=0.6)); H.a.text(px+dx+np.sign(dx)*3,py+dy,str(n_),fontsize=6,ha="center",va="center")
H.cerrar(pdf,"plano1_conjunto_abierto.png")

# ================= PLANO 2: conjunto plegado =================
comp=cq.Compound.makeCompound([sh.val() for n,sh in conjunto(True)])
H=Hoja("TABURETE-ESCALERA PLEGABLE · CONJUNTO PLEGADO",2,"1:5")
alz=proyectar(comp,"alzado"); per=proyectar(comp,"perfil")
H.dibujar(alz,70,70,E); H.dibujar(per,210,70,E)
bb=comp.BoundingBox()
H.cota((210-225/E,70+bb.ymin/E),(210+225/E,70+bb.ymin/E),-9,"450")
H.cota((210+225/E,70+bb.ymin/E),(210+225/E,70+bb.ymax/E),10,f"{bb.ylen:.0f}",vertical=True)
H.rot(70+15,70+175,"ALZADO (vista lateral)",fs=7.5,fontweight="bold",ha="center"); H.rot(210,70+175,"PERFIL (vista frontal)",fs=7.5,fontweight="bold",ha="center")
H.rot(40,40,"Espesor plegado medido perpendicular a los largueros: 40 mm.\nVolumen plegado: 861 × 450 × 40 mm.",fs=8)
H.cerrar(pdf,"plano2_conjunto_plegado.png")

# ================= PLANO 3: larguero y pata trasera =================
H=Hoja("LARGUERO DELANTERO (1) Y PATA TRASERA (2)",3,"1:5 / 1:1")
for i,(k,L,ang,ag,y0,tit) in enumerate((("larguero_delantero",810,15,[233,481,680],200,"1 · LARGUERO DELANTERO (2 uds.)"),("pata_trasera",761,26,[331,611,731],110,"2 · PATA TRASERA (2 uds.)"))):
    sh=PZ[k].rotate((0,0,0),(0,0,1),-90).val()   # eje de la pieza horizontal (+X)
    pr=proyectar(sh,"planta_pieza",ocultas=True)
    ox=40; H.dibujar(pr,ox,y0,E)
    H.cota((ox,y0-5),(ox+L/E,y0-5),-8,str(L))
    xs=[ox]+[ox+a/E for a in ag]
    for a in ag: H.cota((ox,y0+5),(ox+a/E,y0+5),6+ag.index(a)*6,str(a))
    H.rot(ox+L/E+4,y0,f"Corte extremos a {90-ang}° (paralelo al suelo)\n3 taladros Ø8,5 pasantes",fs=6.5,va="center")
    H.rot(ox,y0+30,tit,fs=8,fontweight="bold")
# sección 1:1
sx,sy=300,160; H.a.add_patch(plt.Rectangle((sx,sy),20,40,fill=False,lw=0.9)); H.a.add_patch(plt.Rectangle((sx+2,sy+2),16,36,fill=False,lw=0.9))
import matplotlib.patches as mp
H.a.add_patch(mp.Rectangle((sx,sy),20,40,fill=False,hatch="////",lw=0)); H.a.add_patch(mp.Rectangle((sx+2,sy+2),16,36,fc="white",ec="k",lw=0.9))
H.cota((sx,sy),(sx+20,sy),-6,"20"); H.cota((sx+20,sy),(sx+20,sy+40),6,"40",vertical=True); H.rot(sx+23,sy+41,"e = 2",fs=7)
H.rot(sx-5,sy+48,"SECCIÓN DEL PERFIL (1:1)\nAl 6063-T5, tubo 40×20×2",fs=7.5,fontweight="bold")
H.cerrar(pdf,"plano3_larguero_pata.png")

# ================= PLANO 4: plataforma y peldaño =================
H=Hoja("PLATAFORMA (5) Y PELDAÑO (6)",4,"1:5")
E4=5
for k,D,dB,ox,oyf,tit,asa in (("plataforma",300,uP,40,250,"5 · PLATAFORMA (1 ud.)",True),("peldano",230,eS,40,140,"6 · PELDAÑO (1 ud.)",False)):
    sh=PZ[k].val()   # X ancho 350, Y fondo (frente en -Y), Z alto
    cx=ox+350/2/E4
    fr=proyectar(sh,"frente_y",ocultas=True); H.dibujar(fr,cx,oyf,E4)                  # alzado
    pl=proyectar(sh,"sup_z",ocultas=True); H.dibujar(pl,cx,oyf-15-D/2/E4-12,E4)       # planta (debajo)
    la=proyectar(sh,"lat_x",ocultas=True); lx=ox+350/E4+25+D/2/E4; H.dibujar(la,lx,oyf,E4)  # perfil izq. (a la derecha)
    top=oyf+15/E4; bot=oyf-15/E4
    H.cota((ox,top),(ox+350/E4,top),5,"350")
    H.cota((ox,bot),(ox,top),-5,"30",vertical=True)
    x0=lx-D/2/E4
    H.cota((x0,top),(x0+D/E4,top),5,str(D))
    for j,dd in enumerate((20,20+dB)):
        H.cota((x0,bot),(x0+dd/E4,bot),-5-j*6,(f"{dd:.1f}".rstrip("0").rstrip(".")).replace(".",","))
    H.cota((x0+D/E4,top-15/E4),(x0+D/E4,top),5,"15",vertical=True)
    H.rot(ox,top+13,tit+" · E 1:5",fs=8,fontweight="bold")
    H.rot(lx+D/2/E4+8,oyf,"2 taladros Ø8,5\npasantes en ambos laterales\nPared de 3 mm",fs=6.5,va="center")
    if asa:
        ycen=oyf-15-D/2/E4-12+(D/2-45)/E4
        H.rot(cx+350/2/E4+6,ycen,"Hueco-asa 120 × 30\ncentrado a 45 mm\ndel borde trasero",fs=6.5,va="center")
H.cerrar(pdf,"plano4_plataforma_peldano.png")

# ================= PLANO 5: piezas varias =================
H=Hoja("TRAVESAÑOS (3, 4), BIELA (7), TIRANTE (8), PASADOR (9) Y TACO (10)",5,"1:2 / 1:1")
y=235
for k,L,tit in (("travesano_asidero",410,"3 · TRAVESAÑO ASIDERO (1 ud.) · tubo 20×20×2 · E 1:2"),("travesano_trasero",360,"4 · TRAVESAÑO TRASERO (1 ud.) · tubo 20×20×2 · E 1:2")):
    pr=proyectar(PZ[k].val(),"alzado_pieza",ocultas=True); H.dibujar(pr,40+L/4,y,2)
    H.cota((40,y-5),(40+L/2,y-5),-6,str(L)); H.rot(40,y+9,tit,fs=7.5,fontweight="bold"); y-=45
for k,c,tit in (("biela_plataforma",cP,"7 · BIELA PLATAFORMA (2 uds.) · pletina 20×4 · E 1:1"),("tirante_peldano",cS,"8 · TIRANTE PELDAÑO (2 uds.) · pletina 20×4 · E 1:1")):
    pr=proyectar(PZ[k].val(),"sup_z",ocultas=False)
    ox=40+(c+20)/2; H.dibujar(pr,ox,y,1)
    H.cota((ox-c/2,y-11),(ox+c/2,y-11),-5,f"{c:.1f}".replace(".",",")); H.rot(40,y+14,tit,fs=7.5,fontweight="bold"); H.rot(ox+c/2+16,y,"2 taladros Ø8,5",fs=6.5,va="center"); y-=45
H.rot(260,235,"9 · PASADOR (10 uds.) · Ø8 × 45 · acero",fs=7.5,fontweight="bold")
H.a.add_patch(plt.Rectangle((262,215),45,8,fill=False,lw=0.8)); H.cota((262,215),(307,215),-6,"45"); H.cota((307,215),(307,223),5,"Ø8",vertical=True)
H.rot(260,185,"10 · TACO (4 uds.) · caucho/TPE",fs=7.5,fontweight="bold")
H.a.add_patch(plt.Rectangle((262,150),24,25,fill=False,lw=0.8)); H.a.plot([264,264,284,284],[150,170,170,150],lw=0.4,ls=(0,(3,1.5)),color="k")
H.cota((262,150),(286,150),-6,"24"); H.cota((286,150),(286,175),5,"25",vertical=True); H.rot(292,160,"Alojamiento 20 × 40 × 20\n(ancho exterior 24 × 44)",fs=6.5,va="center")
H.cerrar(pdf,"plano5_piezas_varias.png")
pdf.close(); print("ok")

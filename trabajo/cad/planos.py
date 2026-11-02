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
        a.plot([x0+60,x0+60],[y0,y0+20],lw=0.6,color="k"); a.plot([x0+120,x0+120],[y0,y0+20],lw=0.6,color="k")
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
     ("5","Plataforma","Plataforma","PP + 30 % FV, e = 3, 3 nervios"),("6","Peldaño","Peldano","PP + 30 % FV, e = 3, 3 nervios"),
     ("7","Biela plataforma","Biela_plataforma","Al 6063-T5, pletina 20×4"),("8","Tirante peldaño","Tirante_peldano","Al 6063-T5, pletina 20×4"),
     ("9","Pasador Ø8 × 45","Pasador","Acero"),("10","Taco","Taco","Caucho (TPE)")]
filas=[(m,d_,M[k][1],mat,M[k][3]) for m,d_,k,mat in den]
H.tabla(282,285,["Marca","Denominación","Cant.","Material (alternativa 2)","Masa (g)"],filas[::-1],[10,30,10,48,18])
H.rot(282,285-5.2*11-4,"Masas del modelo SolidWorks (total 3,17 kg). Con PP reforzado, nervios y casquillos (apartado 3.5): ≈ 3,46 kg.\nAluminio con alto contenido reciclado. FV: fibra de vidrio.",fs=6.2,va="top")
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

# ================= PLANO 3: plano de fabricación del larguero delantero =================
import matplotlib.patches as mp
H=Hoja("LARGUERO DELANTERO · PLANO DE FABRICACIÓN",3,"1:5 / 1:1")
L,ang,ag,a_,b_,t_=810,15,[233,481,680],40,20,2
sh=PZ["larguero_delantero"].rotate((0,0,0),(0,0,1),-90).val()   # eje de la pieza horizontal (+X)
ox,y0=40,215
pr=proyectar(sh,"planta_pieza",ocultas=True); H.dibujar(pr,ox,y0,E)
H.rot(ox,y0+37,"ALZADO · E 1:5",fs=7.5,fontweight="bold")
# cotas de posición de los taladros (desde el vértice inferior) y longitud total
for k,a in enumerate(ag): H.cota((ox,y0+a_/2/E),(ox+a/E,y0+a_/2/E),7+k*6.5,f"{a} ±0,2")
H.cota((ox,y0-a_/2/E),(ox+L/E,y0-a_/2/E),-14,"810 ±0,5")
H.cota((ox+L/E,y0-a_/2/E),(ox+L/E,y0+a_/2/E),7,"40",vertical=True)
xh=ox+ag[-1]/E; H.a.annotate("3 taladros Ø8,5 H12\npasantes (ambas caras)",xy=(xh,y0),xytext=(xh+39,y0-19),fontsize=6.8,
    arrowprops=dict(arrowstyle="-",lw=0.45,color="k"),va="center")
# vista superior (primer diedro: debajo del alzado)
y1=150
pr2=proyectar(sh,"sup_z",ocultas=True); H.dibujar(pr2,ox,y1,E)
H.rot(ox,y1+12,"VISTA SUPERIOR · E 1:5",fs=7.5,fontweight="bold")
H.cota((ox+L/E,y1-b_/2/E),(ox+L/E,y1+b_/2/E),7,"20",vertical=True)
# indicación del detalle C y de la sección A-A
H.a.add_patch(plt.Circle((ox+4,y0),8.5,fill=False,lw=0.5,ls=(0,(4,2))))
H.rot(ox-8,y0+9,"C",fs=8,fontweight="bold")
xa=ox+560/E
for yy,dy in ((y0+a_/2/E+2.5,5),(y0-a_/2/E-2.5,-5)):
    H.a.plot([xa,xa],[yy,yy+dy],lw=1.2,color="k"); H.a.annotate("",xy=(xa+5,yy+dy),xytext=(xa,yy+dy),arrowprops=dict(arrowstyle="-|>",lw=0.8,color="k",mutation_scale=7))
    H.rot(xa+6.5,yy+dy,"A",fs=8,fontweight="bold",va="center")
# DETALLE C (1:1): extremo inferior con el corte a 15°
cx,cy=268,205; h=a_*np.tan(np.radians(ang))
H.a.plot([cx,cx+h],[cy-a_/2,cy+a_/2],lw=0.9,color="k")
H.a.plot([cx,cx+75],[cy-a_/2,cy-a_/2],lw=0.9,color="k"); H.a.plot([cx+h,cx+75],[cy+a_/2,cy+a_/2],lw=0.9,color="k")
hi=(a_/2-t_)*2*np.tan(np.radians(ang))
H.a.plot([cx+t_*np.tan(np.radians(ang)),cx+75],[cy-a_/2+t_,cy-a_/2+t_],lw=0.4,ls=(0,(3,1.5)),color="k")
H.a.plot([cx+h-t_*np.tan(np.radians(ang)),cx+75],[cy+a_/2-t_,cy+a_/2-t_],lw=0.4,ls=(0,(3,1.5)),color="k")
zx=np.array([0,1.5,-1.5,0]); H.a.plot(cx+75+zx[[0,1,2,3]]*[1,1,1,1],[cy-a_/2-2,cy-5,cy+5,cy+a_/2+2],lw=0.5,color="k")
H.a.plot([cx,cx],[cy-a_/2,cy+a_/2+12],lw=0.4,ls=(0,(6,2,1,2)),color="k")
H.a.add_patch(mp.Arc((cx,cy-a_/2),2*(a_+8),2*(a_+8),theta1=90-ang,theta2=90,lw=0.5))
H.rot(cx+5.5,cy+a_/2+10,"15°",fs=7.5)
H.cota((cx,cy-a_/2),(cx+h,cy-a_/2),-6,"10,7",fs=6.5)
H.rot(cx-5,cy+a_/2+20,"DETALLE C · E 1:1",fs=7.5,fontweight="bold")
H.rot(cx,cy-a_/2-17,"Corte a 15° de la normal al eje en los dos extremos\n(caras paralelas; quedan horizontales al montar).",fs=6.5)
# SECCIÓN A-A (1:1)
sx,sy=362,185
H.a.add_patch(mp.Rectangle((sx,sy),b_,a_,fill=False,hatch="////",lw=0)); H.a.add_patch(mp.Rectangle((sx,sy),b_,a_,fill=False,lw=0.9))
H.a.add_patch(mp.Rectangle((sx+t_,sy+t_),b_-2*t_,a_-2*t_,fc="white",ec="k",lw=0.9))
H.cota((sx,sy),(sx+b_,sy),-6,"20"); H.cota((sx+b_,sy),(sx+b_,sy+a_),6,"40",vertical=True); H.rot(sx+23,sy+a_+1,"e = 2",fs=7)
H.rot(sx-6,sy+a_+12,"SECCIÓN A-A · E 1:1",fs=7.5,fontweight="bold")
# notas de fabricación
notas=["NOTAS DE FABRICACIÓN",
"1. Material: aluminio EN AW-6063 T5 (UNE-EN 573-3), tubo rectangular extruido",
"    40 × 20 × 2 mm (UNE-EN 755-2), con alto contenido de aluminio reciclado.",
"2. Cantidad: 2 piezas iguales por taburete. Masa: 482 g/ud. (modelo SolidWorks).",
"3. Tolerancias generales no indicadas: ISO 2768-mK.",
"4. Cotas de los taladros medidas desde el vértice inferior del perfil.",
"5. Taladros Ø8,5 H12 para pasador Ø8; eliminar rebabas.",
"6. Aristas vivas matadas 0,3 × 45°.",
"7. Acabado: anodizado natural, 15 µm (UNE-EN ISO 7599).",
"8. Proceso: corte con sierra a 15°, taladrado, desbarbado y anodizado."]
for k,tn in enumerate(notas): H.rot(28,112-k*6.2,tn,fs=7 if k else 7.6,fontweight="bold" if k==0 else "normal")
H.a.add_patch(mp.Rectangle((24,112-len(notas)*6.2+2),190,len(notas)*6.2+4.5,fill=False,lw=0.6))
H.cerrar(pdf,"plano3_larguero_fabricacion.png")
pdf.close(); print("ok")

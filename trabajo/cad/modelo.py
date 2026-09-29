import cadquery as cq, math, json
from cinematica import uP,qP,cP,eS,qS,cS,Lr
T=2.0  # espesor tubo (se cambia por alternativa)
def tubo(L,a,b,t,ang_inf,ang_sup):
    """tubo rectangular a(prof, Z) x b(lat, X), eje Y, extremos cortados a ang (grados desde horizontal-perp)"""
    s=cq.Workplane("XZ").rect(b,a).extrude(-L)            # eje +Y
    if t: s=s.cut(cq.Workplane("XZ").rect(b-2*t,a-2*t).extrude(-L))
    h1=a*math.tan(math.radians(ang_inf)); h2=a*math.tan(math.radians(ang_sup))
    cut1=cq.Workplane("YZ").polyline([(0,-a/2),(0,a/2),(h1,a/2)]).close().extrude(b,both=True)
    cut2=cq.Workplane("YZ").polyline([(L,-a/2),(L-h2,-a/2),(L,a/2)]).close().extrude(b,both=True)
    return s.cut(cut1).cut(cut2)
def taladros(s,ys,dia=8.5):
    for y in ys: s=s.cut(cq.Workplane("YZ").center(y,0).circle(dia/2).extrude(100,both=True))
    return s
def piezas(alt):
    P={}
    if alt=="madera":
        tf=tubo(810,40,20,0,15,15); tr=tubo(761,40,20,0,26,26); tb=lambda L: cq.Workplane("XY").box(L,20,20)
    else:
        t=2.0
        tf=tubo(810,40,20,t,15,15); tr=tubo(761,40,20,t,26,26)
        tb=lambda L: cq.Workplane("XY").box(L,20,20).cut(cq.Workplane("XY").box(L,20-2*t,20-2*t))
    P["larguero_delantero"]=taladros(tf,[233,481,680])
    P["pata_trasera"]=taladros(tr,[731,731-qP,731-qS])            # P a 30 mm del extremo superior
    P["travesano_asidero"]=tb(410); P["travesano_trasero"]=tb(360)
    def bandeja(Wd,D,H,holes):
        if alt=="acero": b=cq.Workplane("XY").box(Wd,D,H).faces("<Z").shell(-1.2)
        elif alt=="aluminio": b=cq.Workplane("XY").box(Wd,D,H).faces("<Z").shell(-3.0)
        else:
            b=cq.Workplane("XY").box(Wd,D,15).translate((0,0,H/2-7.5)).union(cq.Workplane("XY").box(15,D,H).translate((Wd/2-7.5,0,0))).union(cq.Workplane("XY").box(15,D,H).translate((-Wd/2+7.5,0,0)))
        for yy in holes: b=b.cut(cq.Workplane("YZ").center(-D/2+yy,H/2-15).circle(4.25).extrude(Wd,both=True))
        return b
    pl=bandeja(350,300,30,[20,20+uP]).cut(cq.Workplane("XY").center(0,300/2-45).slot2D(120,30).extrude(50,both=True))
    P["plataforma"]=pl
    P["peldano"]=bandeja(350,230,30,[20,20+eS])
    pl_=lambda c: cq.Workplane("XY").slot2D(c+20,20).extrude(4).cut(cq.Workplane("XY").pushPoints([(-c/2,0),(c/2,0)]).circle(4.25).extrude(4))
    P["biela_plataforma"]=pl_(cP); P["tirante_peldano"]=pl_(cS)
    P["pasador"]=cq.Workplane("XY").circle(4).extrude(45)
    P["taco"]=cq.Workplane("XY").box(24,44,25).translate((0,0,12.5)).cut(cq.Workplane("XY").box(20,40,20).translate((0,0,15)))
    return P
cant={"larguero_delantero":2,"pata_trasera":2,"travesano_asidero":1,"travesano_trasero":1,"plataforma":1,"peldano":1,"biela_plataforma":2,"tirante_peldano":2,"pasador":10,"taco":4}
dens={"acero":{"est":7.85,"band":7.85},"aluminio":{"est":2.70,"band":1.12},"madera":{"est":0.72,"band":0.68}}
mat={"acero":("Acero S235","Acero S235 (chapa 1,2 mm)"),"aluminio":("Aluminio 6063-T5","PP + 30 % fibra de vidrio"),"madera":("Haya maciza","Contrachapado de haya/abedul")}
res={}
for alt in ("acero","aluminio","madera"):
    P=piezas(alt); res[alt]={}
    for k,s in P.items():
        v=s.val().Volume()/1000  # cm3
        if k in("plataforma","peldano"): rho=dens[alt]["band"]; m=mat[alt][1]
        elif k in("biela_plataforma","tirante_peldano") and alt=="aluminio": rho=2.70; m="Aluminio 6063-T5"
        elif k in("biela_plataforma","tirante_peldano","pasador"): rho=7.85; m="Acero"
        elif k=="taco": rho=1.10; m="TPE"
        else: rho=dens[alt]["est"]; m=mat[alt][0]
        res[alt][k]={"cant":cant[k],"material":m,"masa_g":round(v*rho,1),"total_g":round(v*rho*cant[k],1)}
    res[alt]["TOTAL_kg"]=round(sum(r["total_g"] for r in res[alt].values())/1000,2)
    if alt=="aluminio":
        import os; os.makedirs("step",exist_ok=True)
        for k,s in P.items(): cq.exporters.export(s,f"step/{k}.step"); cq.exporters.export(s,f"step/{k}.stl")
json.dump(res,open("masas.json","w"),indent=1,ensure_ascii=False)
for alt in res: print(alt,res[alt]["TOTAL_kg"],"kg")

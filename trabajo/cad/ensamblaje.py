import cadquery as cq, numpy as np, math
from cinematica import A,S,P,d,rh,uP,qP,cP,eS,qS,cS
from modelo import piezas
PZ=piezas("aluminio")
def V(zy,x=0): return cq.Vector(x,zy[1],zy[0])
def rotX(s,deg,about=(0,0,0)):
    return s.rotate(cq.Vector(about),cq.Vector(about)+cq.Vector(1,0,0),deg)
def conjunto(plegado):
    parts=[]
    al,be=15,26
    th_rear=41.0 if plegado else 0
    for sx in (-1,1):
        f=rotX(PZ["larguero_delantero"],al).translate((sx*215,0,0)); parts.append(("larguero",f))
        r=rotX(PZ["pata_trasera"],-be)
        # llevar agujero P (local y=731) al punto P
        loc=np.array([0,731*math.cos(math.radians(be)),-731*math.sin(math.radians(be))])
        r=r.translate((sx*190,P[1]-loc[1],P[0]-loc[2]))
        if plegado: r=rotX(r,th_rear,(0,P[1],P[0]))
        parts.append(("pata",r))
    parts.append(("asidero",PZ["travesano_asidero"].translate(V(790*d))))
    Pr=P+650*rh
    tt=PZ["travesano_trasero"].translate(V(Pr))
    if plegado: tt=rotX(tt,th_rear,(0,P[1],P[0]))
    parts.append(("trav_trasero",tt))
    def bandeja(key,D,H,G,ang):
        b=PZ[key].rotate((0,0,0),(1,0,0),-90).rotate((0,0,0),(0,1,0),180)
        piv=cq.Vector(0,H/2-15,-(D/2-20)) # tras rotaciones
        b=b.translate(V(G)-piv)
        return rotX(b,ang,(0,G[1],G[0]))
    parts.append(("plataforma",bandeja("plataforma",300,30,A,-75 if plegado else 0)))
    parts.append(("peldano",bandeja("peldano",230,30,S,-75 if plegado else 0)))
    def link(key,p1,p2,x):
        c=np.linalg.norm(p2-p1); l=PZ[key].translate((0,0,-2)).rotate((0,0,0),(0,1,0),90)  # eje en Z, espesor en X
        ang=math.degrees(math.atan2(p2[1]-p1[1],p2[0]-p1[0]))
        l=rotX(l,-ang); m=(p1+p2)/2
        return l.translate((x,m[1],m[0]))
    def rot2(pt,c,phi):
        phi=math.radians(phi); v=pt-c; return c+np.array([v[0]*math.cos(phi)-v[1]*math.sin(phi),v[0]*math.sin(phi)+v[1]*math.cos(phi)])
    xh=np.array([1.0,0])
    U=A+uP*xh; T=S+eS*xh; Q=P+qP*rh; R=P+qS*rh
    if plegado: U=A+uP*d; T=S+eS*d; Q=rot2(Q,P,-41); R=rot2(R,P,-41)
    for sx in (-1,1):
        parts.append(("biela",link("biela_plataforma",U,Q,sx*177.5)))
        parts.append(("tirante",link("tirante_peldano",T,R,sx*177.5)))
    return parts
if __name__=="__main__":
    for nombre,pleg in (("abierto",False),("plegado",True)):
        ps=conjunto(pleg); asm=cq.Assembly()
        for i,(n,s) in enumerate(ps): asm.add(s,name=f"{n}_{i}")
        comp=cq.Compound.makeCompound([s.val() for n,s in ps])
        bb=comp.BoundingBox(); print(nombre,"ancho X=%.0f alto Y=%.0f fondo Z=%.0f (min Y %.0f)"%(bb.xlen,bb.ylen,bb.zlen,bb.ymin))
        cq.exporters.export(cq.Workplane().add(comp),f"conjunto_{nombre}.stl",tolerance=0.3)
        cq.exporters.export(cq.Workplane().add(comp),f"conjunto_{nombre}.step")
    # interferencias en abierto y plegado
    for pleg in (False,True):
        ps=conjunto(pleg); bad=[]
        for i in range(len(ps)):
            for j in range(i+1,len(ps)):
                try:
                    v=ps[i][1].val().intersect(ps[j][1].val()).Volume()
                    if v>50: bad.append((ps[i][0],ps[j][0],round(v)))
                except Exception as e: pass
        print("plegado" if pleg else "abierto","interferencias >50 mm3:",bad)

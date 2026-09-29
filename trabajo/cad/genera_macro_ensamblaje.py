import numpy as np, math
from cinematica import A,S,P,d,rh,uP,qP,cP,eS,qS,cS
def RX(g):
    c,s=math.cos(math.radians(g)),math.sin(math.radians(g)); return np.array([[1,0,0],[0,c,-s],[0,s,c]])
RY180=np.diag([-1,1,-1.0])
def W(zy,x=0): return np.array([x,zy[1],zy[0]])      # (z,y) plano lateral -> (x,y,z)
Aw,Sw,Pw=W(A),W(S),W(P)
def about(Rrot,piv,R,t): return Rrot@R, piv+Rrot@(t-piv)
def rot2(pt,c,phi):
    phi=math.radians(phi); v=pt-c; return c+np.array([v[0]*math.cos(phi)-v[1]*math.sin(phi),v[0]*math.sin(phi)+v[1]*math.cos(phi)])
def comps(pleg):
    L=[]
    for sx in (-1,1):
        L.append(("Larguero_delantero",RX(15)@RY180,np.array([sx*215.,0,0])))
        R0=RX(-26); Pl=Pw.copy(); Pl[0]=sx*190; t0=Pl-R0@np.array([0,731.,0])
        R,t=(about(RX(41),Pl,R0,t0) if pleg else (R0,t0)); L.append(("Pata_trasera",R,t))
    L.append(("Travesano_asidero",np.eye(3),W(790*d)))
    R,t=np.eye(3),W(P+650*rh)
    if pleg: R,t=about(RX(41),Pw,R,t)
    L.append(("Travesano_trasero",R,t))
    for nom,G,D in (("Plataforma",Aw,300),("Peldano",Sw,230)):
        R0=RY180; t0=G-R0@np.array([0,30-15.,D/2-20])
        R,t=(about(RX(-75),G,R0,t0) if pleg else (R0,t0)); L.append((nom,R,t))
    xh=np.array([1.0,0]); U=A+uP*xh; T=S+eS*xh; Q=P+qP*rh; Rr=P+qS*rh
    if pleg: U=A+uP*d; T=S+eS*d; Q=rot2(Q,P,-41); Rr=rot2(Rr,P,-41)
    for nom,p1,p2 in (("Biela_plataforma",U,Q),("Tirante_peldano",T,Rr)):
        for sx in (-1,1):
            u=W(p2)-W(p1); u/=np.linalg.norm(u); z=np.array([1.,0,0]); y=np.cross(z,u)
            R=np.column_stack([u,y,z]); m=(W(p1)+W(p2))/2; m[0]=sx*177.5-2
            L.append((nom,R,m))
    return L
def vba_list(pleg):
    out=[]
    for nom,R,t in comps(pleg):
        arr=list(R[:,0])+list(R[:,1])+list(R[:,2])+list(t/1000)
        out.append('    Poner "%s", Array(%s)'%(nom,", ".join("%.6f"%v for v in arr)))
    return "\n".join(out)
plantilla=open("plantilla_ensamblaje.vba",encoding="utf8").read()
vba=plantilla.replace("'@@ABIERTO@@",vba_list(False)).replace("'@@PLEGADO@@",vba_list(True))
vba=vba.replace("\r\n","\n").replace("\n","\r\n")
open("Ensamblaje_macro_para_copiar.txt","w",encoding="utf8",newline="").write(vba)
print(vba_list(False).splitlines()[0]); print(len(comps(False)),"componentes")

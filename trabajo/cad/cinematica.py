import numpy as np
deg=np.pi/180; a=15*deg; d=np.array([np.sin(a),np.cos(a)]); x=np.array([1.0,0])
sA,sS,sP,beta=481.0,233.0,680.0,26*deg
A,S,P=sA*d,sS*d,sP*d; rh=np.array([np.sin(beta),-np.cos(beta)]); Lr=P[1]/np.cos(beta)
from scipy.optimize import brentq
def solve(sG,q,lo,hi):
    G=sG*d;Q=P+q*rh; return brentq(lambda u: np.linalg.norm(G+u*x-Q)-abs(sG+u-(sP-q)),lo,hi)
qP=120; uP=solve(sA,qP,150,300); qS=400; eS=solve(sS,qS,120,200)
cP=np.linalg.norm(A+uP*x-(P+qP*rh)); cS=np.linalg.norm(S+eS*x-(P+qS*rh))
def sweep(G,L,q,c):
    ang0=np.arctan2(rh[1],rh[0]); ang1=np.arctan2(-d[1],-d[0]); res=[]; prev=0.0
    ph=np.linspace(-np.pi,np.pi,72001)
    for t in np.linspace(0,1,41):
        th=ang0+(ang1-ang0)*t; Q=P+q*np.array([np.cos(th),np.sin(th)])
        pts=G[:,None]+L*np.vstack([np.cos(ph),np.sin(ph)]); err=np.abs(np.linalg.norm(pts-Q[:,None],axis=0)-c)
        cand=ph[err<0.5]
        if len(cand)==0: res.append(None); continue
        k=np.argmin(np.abs(np.angle(np.exp(1j*(cand-prev))))); prev=cand[k]; res.append(round(prev/deg,1))
    return res
if __name__=="__main__":
    print(f"A={A.round(1)} S={S.round(1)} P={P.round(1)} pie_trasero={(P+Lr*rh).round(0)} Lr={Lr:.0f}")
    print(f"PLATAFORMA: punto en plataforma a {uP:.1f} mm de A; punto en pata a {qP} mm de P; biela {cP:.1f} mm")
    print(f"PELDAÑO:    punto en peldaño a {eS:.1f} mm de S; punto en pata a {qS} mm de P; tirante {cS:.1f} mm")
    print("plegado objetivo:",round(np.arctan2(d[1],d[0])/deg,1),"°")
    print("plataforma:",sweep(A,uP,qP,cP)[::4]); print("peldaño:   ",sweep(S,eS,qS,cS)[::4])

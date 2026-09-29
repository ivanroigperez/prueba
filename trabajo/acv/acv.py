import csv, json
# masas (g por unidad) medidas en SolidWorks
M={}
for r in csv.reader(open("../cad/masas_solidworks.csv"),delimiter=";"):
    if r[0]=="Pieza" or not r[0]: continue
    M[r[0]]=(int(r[1]),[float(x.replace(",",".")) for x in r[2:5]])
# factores de emisión, kg CO2-eq / kg (ICE v2.0, Univ. Bath, 2011)
F={"acero_tubo":1.45,"acero_chapa":1.38,"acero_barra":1.40,"alu_extr":9.08,"pp":4.98,"haya":0.24,"contrachapado":0.45,"caucho":3.61}
E_INY=1.47*0.283        # inyección: 1,47 kWh/kg x 0,283 kg CO2-eq/kWh (MITECO 2024, sin GdO)
CAMION=0.0672            # kg CO2-eq / t·km (DEFRA 2024, articulado >33 t, carga media)
KM_DIST, KM_FIN = 600, 50
CRED={"acero":2.89-0.47,"alu":12.50-2.12}   # (virgen - reciclado), ICE v2.0
CONT={"acero":0.59,"alu":0.33}              # contenido reciclado de partida (ICE v2.0)
TASA_REC=0.90; INCIN=3.14                   # plásticos/caucho a incineración (C3H6 -> 3 CO2)
mat={
 "ALT1_ACERO":   {"Larguero_delantero":"acero_tubo","Pata_trasera":"acero_tubo","Travesano_asidero":"acero_tubo","Travesano_trasero":"acero_tubo","Plataforma":"acero_chapa","Peldano":"acero_chapa","Biela_plataforma":"acero_barra","Tirante_peldano":"acero_barra","Pasador":"acero_barra","Taco":"caucho"},
 "ALT2_ALUMINIO":{"Larguero_delantero":"alu_extr","Pata_trasera":"alu_extr","Travesano_asidero":"alu_extr","Travesano_trasero":"alu_extr","Plataforma":"pp","Peldano":"pp","Biela_plataforma":"alu_extr","Tirante_peldano":"alu_extr","Pasador":"acero_barra","Taco":"caucho"},
 "ALT3_MADERA":  {"Larguero_delantero":"haya","Pata_trasera":"haya","Travesano_asidero":"haya","Travesano_trasero":"haya","Plataforma":"contrachapado","Peldano":"contrachapado","Biela_plataforma":"acero_barra","Tirante_peldano":"acero_barra","Pasador":"acero_barra","Taco":"caucho"}}
res={}
for i,alt in enumerate(mat):
    prod={}; fin={}; D={}; masa=0
    for p,(n,ms) in M.items():
        kg=n*ms[i]/1000; masa+=kg; m=mat[alt][p]
        e=kg*F[m]+(kg*E_INY if m=="pp" else 0); prod[p]=e
        if m.startswith("acero"): D[p]=-kg*(TASA_REC-CONT["acero"])*CRED["acero"]; fin[p]=0.0
        elif m.startswith("alu"): D[p]=-kg*(TASA_REC-CONT["alu"])*CRED["alu"]; fin[p]=0.0
        elif m in("pp","caucho"): fin[p]=kg*INCIN
        else: fin[p]=0.0                      # madera: CO2 biogénico, neutro
    trans=masa/1000*KM_DIST*CAMION
    uso=M["Taco"][0]*M["Taco"][1][i]/1000*F["caucho"]      # sustitución de los tacos una vez
    fin_tr=masa/1000*KM_FIN*CAMION
    res[alt]={"masa_kg":round(masa,3),"produccion":round(sum(prod.values()),3),"transporte":round(trans,4),
              "uso":round(uso,3),"fin_de_vida":round(sum(fin.values())+fin_tr,3),
              "prod_componentes":{k:round(v,3) for k,v in prod.items()},"fin_componentes":{k:round(v,3) for k,v in fin.items()}}
    r=res[alt]; r["modulo_D"]=round(sum(D.values()),3); r["D_componentes"]={k:round(v,3) for k,v in D.items()}
    r["total_A_C"]=round(r["produccion"]+r["transporte"]+r["uso"]+r["fin_de_vida"],3)
    r["total_con_D"]=round(r["total_A_C"]+r["modulo_D"],3)
json.dump(res,open("resultados_acv.json","w"),indent=1,ensure_ascii=False)
for a,r in res.items(): print(f"{a:14s} masa {r['masa_kg']:.2f} kg | prod {r['produccion']:.2f} | transp {r['transporte']:.3f} | uso {r['uso']:.3f} | fin {r['fin_de_vida']:.3f} | A-C {r['total_A_C']:.2f} | D {r['modulo_D']:.2f} | A-D {r['total_con_D']:.2f}")

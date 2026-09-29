import json, copy
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
d=Document("Trabajo_Taburete.docx")
R=json.load(open("acv/resultados_acv.json"))
def n(v,dec=2): return f"{v:.{dec}f}".replace(".",",")
anchor=[p for p in d.paragraphs if p.text.startswith("[Pendiente: modelado en SolidWorks")][0]
def ins(text="",style=None,bold=False,italic=False,size=None,center=False,before=None):
    b=before or anchor
    p=b.insert_paragraph_before("",style=style) if style else b.insert_paragraph_before("")
    if text:
        r=p.add_run(text); r.bold=bold; r.italic=italic
        if size: r.font.size=Pt(size)
    if center: p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    return p
def fig(path,cap,w,before=None):
    p=ins(center=True,before=before); p.add_run().add_picture(path,width=Cm(w)); ins(cap,italic=True,size=9,center=True,before=before)
def shade(c,col):
    tcPr=c._tc.get_or_add_tcPr(); s=OxmlElement("w:shd"); s.set(qn("w:val"),"clear"); s.set(qn("w:color"),"auto"); s.set(qn("w:fill"),col); tcPr.append(s)
def tabla(cab,filas,ws,cap,before=None,fs=8.5):
    t=d.add_table(rows=1,cols=len(cab)); t.style="Table Grid"
    for i,c in enumerate(cab):
        cl=t.rows[0].cells[i]; cl.text=""; r=cl.paragraphs[0].add_run(c); r.bold=True; r.font.size=Pt(fs+0.5); r.font.color.rgb=RGBColor(255,255,255); shade(cl,"C0392B")
    for f in filas:
        cells=t.add_row().cells
        for i,v in enumerate(f):
            cells[i].text=""; r=cells[i].paragraphs[0].add_run(str(v)); r.font.size=Pt(fs)
            if str(f[0]).startswith("TOTAL"): r.bold=True
    tblPr=t._tbl.tblPr; lay=OxmlElement("w:tblLayout"); lay.set(qn("w:type"),"fixed"); tblPr.append(lay)
    for gc,w in zip(t._tbl.tblGrid.findall(qn("w:gridCol")),ws): gc.set(qn("w:w"),str(int(w/2.54*1440)))
    for row in t.rows:
        for c,w in zip(row.cells,ws): c.width=Cm(w)
    (before or anchor)._p.addprevious(t._tbl)
    ins(cap,italic=True,size=9,center=True,before=before)
B=lambda t,before=None: ins(t,style="List Bullet",before=before)

# ======================= 3.3: nota y alternativas ======================
for p in d.paragraphs:
    if p.text.startswith("Alternativa 2: largueros de perfil extruido"):
        p.runs[0].text="Alternativa 2: largueros, travesaños y bielas de perfil extruido de aluminio 6063-T5, y plataforma y peldaño de polipropileno inyectado."
    if p.text.startswith("Alternativa 3: largueros y peldaños de contrachapado"):
        p.runs[0].text="Alternativa 3: largueros y travesaños de haya maciza, plataforma y peldaño de contrachapado, y bielas y tirantes de acero."
    if p.text.startswith("Alternativa 1: largueros de tubo rectangular"):
        p.runs[0].text="Alternativa 1: largueros y travesaños de tubo rectangular de acero, plataforma y peldaño de chapa de acero de 1,2 mm, y bielas y tirantes de acero."

# ======================= 3.4 ======================
ins("Una vez definido el concepto, se ha modelado el producto en SolidWorks. Antes de modelar las piezas definitivas se comprobó el funcionamiento del mecanismo de plegado mediante un estudio cinemático en el plano lateral, y esta comprobación obligó a modificar el boceto inicial, lo que es un buen ejemplo de cómo en la ingeniería simultánea el diseño de detalle retroalimenta a las etapas anteriores.")
ins("Rediseño del mecanismo de plegado",style="Heading 3")
ins("En el boceto inicial la pata trasera giraba bajo la plataforma y un único tirante unía el peldaño con ella. Al estudiar el movimiento se vio que, con esa disposición, la plataforma quedaba en voladizo detrás de su articulación y el conjunto no podía llegar a plegarse en un plano. La solución adoptada (Ilustración 13) consiste en:")
B("Llevar el pivote de las patas traseras (P) por encima de la plataforma, a 657 mm de altura, prolongando los largueros delanteros hasta unos 780 mm. Esta prolongación forma además un asidero, con lo que se cumple el requisito deseable R11.")
B("Articular la plataforma (A) y el peldaño (S) en los largueros delanteros y unirlos a la pata trasera mediante una biela (154 mm) y un tirante (133 mm). Se forman así dos cuadriláteros articulados que comparten la pata trasera.")
B("Al cerrar la pata trasera (un giro de 41°), las bielas obligan a la plataforma y al peldaño a girar 75° hasta quedar paralelos a los largueros. Con los puntos de unión calculados, la plataforma y el peldaño quedan exactamente alineados con el larguero en la posición plegada.")
fig("acv/figura_esquema_cinematico.png","Ilustración 13. Esquema cinemático definitivo: posiciones abierta, intermedia y plegada. Elaboración propia.",16.5)
ins("Modelo en SolidWorks",style="Heading 3")
ins("El producto se ha modelado en SolidWorks 2026 como diez piezas (larguero delantero, pata trasera, travesaño del asidero, travesaño trasero, plataforma, peldaño, biela de la plataforma, tirante del peldaño, pasador y taco) y dos ensamblajes, uno en posición abierta y otro plegado. Cada pieza tiene tres configuraciones, una por alternativa de material (ALT1_ACERO, ALT2_ALUMINIO y ALT3_MADERA), en las que cambian el material asignado y, cuando es necesario, la geometría: en la alternativa de madera se suprime el hueco de los perfiles (piezas macizas) y el espesor del vaciado de la plataforma y el peldaño pasa a 15 mm, mientras que en acero es de 1,2 mm y en polipropileno de 3 mm.")
fig("capturas/sw_lateral_abierto.png","Ilustración 14. Ensamblaje abierto, vista lateral (SolidWorks).",10.5)
fig("capturas/sw_frontal_abierto.png","Ilustración 15. Ensamblaje abierto, vista frontal (SolidWorks).",8.5)
fig("capturas/sw_iso_plegado.png","Ilustración 16. Ensamblaje plegado, vista isométrica (SolidWorks).",9)
ins("Con el modelo se han comprobado las principales propiedades fijadas en la etapa inicial: plataforma a 480 mm y peldaño a 240 mm del suelo, huella de 496 × 450 mm, espesor plegado de 40 mm (P6 exigía 50 mm como máximo) y ausencia de interferencias entre piezas tanto abierto como plegado. En la posición plegada las patas traseras sobresalen unos 4 cm por debajo de los largueros, lo cual no supone ningún problema porque el taburete plegado se guarda apoyado en la pared o colgado por el asa. Las masas de cada pieza, obtenidas con la herramienta de propiedades físicas, se recogen en la Tabla 10.")
M={}
import csv
for r in csv.reader(open("cad/masas_solidworks.csv"),delimiter=";"):
    if r[0] and r[0]!="Pieza": M[r[0]]=(int(r[1]),[float(x.replace(",",".")) for x in r[2:5]])
nom={"Larguero_delantero":"Larguero delantero","Pata_trasera":"Pata trasera","Travesano_asidero":"Travesaño asidero","Travesano_trasero":"Travesaño trasero","Plataforma":"Plataforma","Peldano":"Peldaño","Biela_plataforma":"Biela plataforma","Tirante_peldano":"Tirante peldaño","Pasador":"Pasador","Taco":"Taco"}
filas=[(nom[k],v[0],n(v[1][0],1),n(v[1][1],1),n(v[1][2],1)) for k,v in M.items()]
tot=[sum(v[0]*v[1][i] for v in M.values())/1000 for i in range(3)]
filas.append(("TOTAL (kg)","",n(tot[0]),n(tot[1]),n(tot[2])))
tabla(["Pieza","Cant.","Acero (g/ud.)","Aluminio + PP (g/ud.)","Madera (g/ud.)"],filas,[4.5,1.3,3.3,3.6,3.3],"Tabla 10. Masa de cada pieza por alternativa, obtenida del modelo de SolidWorks.")
ins("Solo la alternativa de aluminio cumple la propiedad P5 (peso máximo de 3,5 kg). La de madera se queda cerca (3,96 kg) y la de acero la supera ampliamente (9,20 kg). Hay que señalar que en la alternativa de aluminio la plataforma y el peldaño se han modelado con polipropileno sin reforzar, porque la biblioteca de materiales de SolidWorks no incluye el polipropileno con fibra de vidrio; con este material (1,12 g/cm³ frente a 0,89 g/cm³) el peso aumentaría unos 170 g, hasta unos 3,34 kg, y seguiría cumpliendo.")
anchor._p.getparent().remove(anchor._p)

# ======================= 4. EVALUACIÓN ======================
anchor=[p for p in d.paragraphs if p.text=="Bibliografía"][0]
ins("4. ETAPA DE EVALUACIÓN",style="Heading 1")
ins("En esta etapa se evalúan las tres alternativas de material mediante un análisis de ciclo de vida (ACV) simplificado, calculando su huella de carbono en kg de CO₂ equivalente. Después se comparan también con el resto de criterios del EDP para elegir la alternativa más adecuada.")
ins("4.1. METODOLOGÍA Y DATOS DEL ANÁLISIS",style="Heading 2")
ins("El análisis sigue el enfoque «de la cuna a la tumba» de las normas UNE-EN ISO 14040 y 14044. La unidad funcional es un taburete-escalera que permite a un usuario de hasta 150 kg alcanzar 2,30 m de altura durante 10 años de uso doméstico. Se han considerado las siguientes fases:")
B("Producción: extracción y transformación de los materiales de cada pieza, a partir de las masas del modelo de SolidWorks (Tabla 10). En las piezas de polipropileno se suma la energía de inyección (1,47 kWh/kg).")
B("Transporte: distribución del producto desde la fábrica hasta el punto de venta, 600 km en camión articulado.")
B("Uso: el producto no consume energía; solo se considera la sustitución de los cuatro tacos una vez durante su vida útil.")
B("Fin de vida: transporte de 50 km al punto limpio; reciclaje del 90 % de los metales, incineración de los plásticos y del caucho, y valorización energética de la madera (CO₂ de origen biogénico, que no se contabiliza).")
B("Beneficio del reciclaje (módulo D, según UNE-EN 15804): emisiones evitadas por el material reciclado neto, es decir, la diferencia entre el porcentaje que se recicla al final de la vida (90 %) y el que ya contenía el material de partida (59 % en el acero y 33 % en el aluminio). Se presenta por separado para no contarlo dos veces.")
tabla(["Material o proceso","Factor","Fuente"],[
("Acero, tubo (59 % reciclado)","1,45 kg CO₂-eq/kg","ICE v2.0, Univ. de Bath"),
("Acero, chapa","1,38 kg CO₂-eq/kg","ICE v2.0"),
("Acero, barra (bielas, pasadores)","1,40 kg CO₂-eq/kg","ICE v2.0"),
("Aluminio extruido (33 % reciclado)","9,08 kg CO₂-eq/kg","ICE v2.0"),
("Polipropileno","4,98 kg CO₂/kg","ICE v2.0"),
("Madera de frondosa (haya), fósil","0,24 kg CO₂-eq/kg","ICE v2.0"),
("Contrachapado, fósil","0,45 kg CO₂-eq/kg","ICE v2.0"),
("Caucho","3,61 kg CO₂/kg","ICE v2.0"),
("Electricidad (inyección)","0,283 kg CO₂-eq/kWh","MITECO 2024, sin garantía de origen"),
("Camión articulado > 33 t, carga media","0,0672 kg CO₂-eq/t·km","DEFRA 2024"),
("Incineración de plásticos","3,14 kg CO₂/kg","Estequiometría del polipropileno"),
("Acero virgen / reciclado","2,89 / 0,47 kg CO₂-eq/kg","ICE v2.0 (para el módulo D)"),
("Aluminio virgen / reciclado","12,50 / 2,12 kg CO₂-eq/kg","ICE v2.0 (para el módulo D)")],
[6,4.5,5.5],"Tabla 11. Factores de emisión utilizados en el análisis de ciclo de vida.")
ins("Se trata de un ACV simplificado: no incluye el embalaje, la pintura o el anodizado, ni las mermas de fabricación, y los factores de emisión son valores medios de bases de datos, por lo que los resultados deben interpretarse de forma comparativa entre alternativas y no como valores absolutos.")
alts=[("ALT1_ACERO","4.2. ALTERNATIVA 1: ACERO"),("ALT2_ALUMINIO","4.3. ALTERNATIVA 2: ALUMINIO Y POLIPROPILENO"),("ALT3_MADERA","4.4. ALTERNATIVA 3: MADERA")]
txt={"ALT1_ACERO":"En la alternativa de acero la fase de producción supone el {pp} % del total. Los componentes que más contribuyen son los largueros delanteros y las patas traseras, que por su longitud concentran la mayor parte de la masa, seguidos de la plataforma y el peldaño de chapa. El peso elevado (9,20 kg) también hace que su transporte sea el que más emite, aunque en valor absoluto sigue siendo pequeño. Al final de su vida el acero se recicla con facilidad, lo que da un beneficio de {D} kg CO₂-eq.",
"ALT2_ALUMINIO":"La alternativa de aluminio es la de mayor huella de carbono, a pesar de ser la más ligera. El motivo es el alto factor de emisión del aluminio extruido (9,08 kg CO₂-eq/kg), que hace que los largueros y las patas traseras supongan por sí solos más de 16 kg CO₂-eq. La plataforma y el peldaño de polipropileno añaden unos 3,6 kg CO₂-eq en producción y otros 2 kg en su incineración al final de su vida. En cambio, es la alternativa con mayor beneficio de reciclaje ({D} kg CO₂-eq), porque el aluminio reciclado evita mucha energía respecto al primario.",
"ALT3_MADERA":"La alternativa de madera es claramente la de menor huella de carbono. La madera tiene un factor de emisión fósil muy bajo y el CO₂ que se libera en su valorización al final de su vida es de origen biogénico. En esta alternativa las piezas que más emiten son, curiosamente, las de acero (bielas, tirantes y pasadores), que suponen más de un tercio de la producción."}
for a,tit in alts:
    r=R[a]; ins(tit,style="Heading 2")
    pp=round(100*r["produccion"]/r["total_A_C"])
    ins(txt[a].format(pp=pp,D=n(r["modulo_D"],1)))
    tabla(["Fase","kg CO₂-eq"],[("Producción",n(r["produccion"])),("Transporte",n(r["transporte"])),("Uso",n(r["uso"])),("Fin de vida",n(r["fin_de_vida"])),("TOTAL ciclo de vida (A–C)",n(r["total_A_C"])),("Beneficio del reciclaje (módulo D)",n(r["modulo_D"]))],[8,4],f"Tabla {12+[x[0] for x in alts].index(a)}. Huella de carbono de la {tit.split('. ')[1].lower().capitalize()}.")
ins("4.5. COMPARATIVA Y CONCLUSIONES",style="Heading 2")
fig("acv/figura_acv_fases.png","Ilustración 17. Huella de carbono de las tres alternativas por fase del ciclo de vida. Elaboración propia.",15.5)
fig("acv/figura_acv_componentes.png","Ilustración 18. Huella de carbono de la fase de producción por componente. Elaboración propia.",16.5)
ins("Desde el punto de vista ambiental, la alternativa de madera es la mejor con mucha diferencia (2,6 kg CO₂-eq), seguida de la de acero (13,9) y la de aluminio (27,3), que emite unas diez veces más que la de madera. En las tres alternativas la fase de producción es la dominante, mientras que el transporte y el uso son prácticamente despreciables, algo lógico en un producto que no consume energía. Por tanto, las decisiones de diseño con más efecto sobre el medio ambiente son la elección del material y la cantidad de material empleado.")
ins("Sin embargo, la huella de carbono no es el único criterio del EDP. Para tomar la decisión se ha elaborado una matriz de decisión ponderada con los criterios más importantes, puntuados de 1 (peor) a 5 (mejor):")
tabla(["Criterio","Peso","Acero","Aluminio + PP","Madera"],[
("Huella de carbono (ACV)","30 %","3","1","5"),
("Peso (requisito ≤ 3,5 kg)","25 %","1","5","4"),
("Coste estimado","20 %","5","3","3"),
("Durabilidad y resistencia a la humedad","15 %","3","5","2"),
("Estética y percepción de calidad","10 %","3","4","5"),
("TOTAL ponderado","100 %","2,90","3,30","3,90")],[6,1.8,2.5,3,2.5],"Tabla 15. Matriz de decisión ponderada. Las puntuaciones de coste, durabilidad y estética son valoraciones cualitativas propias.")
ins("Conclusiones:",bold=True)
B("La alternativa mejor valorada es la de madera, por su muy baja huella de carbono y su buena estética. Para que sea la solución definitiva debe rediseñarse para cumplir el peso máximo: reduciendo el espesor de la plataforma y el peldaño de 15 a 12 mm se ahorrarían del orden de 0,35 kg, y es necesario tratarla con un barniz resistente a la humedad para su uso en baños y cocinas.")
B("La alternativa de aluminio es la única que cumple ahora mismo todas las propiedades del EDP, pero tiene la mayor huella de carbono. Si se fabricara con aluminio reciclado (unos 2,1 kg CO₂-eq/kg en lugar de 9,08), su huella bajaría de 27,3 a unos 11,3 kg CO₂-eq, por debajo de la de acero.")
B("La alternativa de acero es la más barata y robusta, pero su peso (9,20 kg) es incompatible con el requisito de transporte con una mano, por lo que se descarta.")
ins("Por todo ello, se propone continuar el desarrollo con la alternativa de madera, aplicando las mejoras indicadas, y mantener la de aluminio reciclado como alternativa en caso de que las pruebas de humedad o de resistencia de la madera no fueran satisfactorias.")

# bibliografía extra
bib=[p for p in d.paragraphs if p.text[:4].strip().rstrip(".").isdigit()]
last=bib[-1]; k=int(last.text.split(".")[0])
from docx.text.paragraph import Paragraph
for t in ["Hammond, G. y Jones, C. (2011). Inventory of Carbon & Energy (ICE) Version 2.0. University of Bath.",
"UK Government (DEFRA/DESNZ). Greenhouse gas reporting: conversion factors 2024.",
"MITECO. Factores de emisión. Registro de huella de carbono, compensación y proyectos de absorción, 2024.",
"UNE-EN ISO 14040:2006 y UNE-EN ISO 14044:2006. Gestión ambiental. Análisis del ciclo de vida.",
"UNE-EN 15804:2012+A2:2020. Sostenibilidad en la construcción. Declaraciones ambientales de producto."]:
    k+=1; np_=copy.deepcopy(last._p); last._p.addnext(np_); last=Paragraph(np_,last._parent)
    for r in last.runs[1:]: r._r.getparent().remove(r._r)
    last.runs[0].text=f"{k}. {t}"
d.save("Trabajo_Taburete.docx")
print("ok")

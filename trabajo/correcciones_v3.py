import hashlib, copy
from docx import Document
from docx.shared import Cm, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX
S="/tmp/claude-0/-home-user-prueba/1e15d777-fea3-54a9-ae9b-0a6049279c2c/scratchpad/"
d=Document("Trabajo_Taburete.docx")

# ---------- 1. sustituir imagen de la figura 1 ----------
old=hashlib.md5(open(S+"fig1_old.png","rb").read()).hexdigest()
new=open("figura1_alcance_mobiliario.png","rb").read()
n=0
for rel in d.part.rels.values():
    if "image" in rel.reltype:
        p=rel.target_part
        if hashlib.md5(p.blob).hexdigest()==old: p._blob=new; n+=1
print("figura 1 sustituida:",n)

# ---------- 2. texto de 1.1 ----------
for p in d.paragraphs:
    if p.text.startswith("El problema es que estas alturas"):
        p.text=("El problema es que estas alturas no están al alcance de todo el mundo. Si tomamos como referencia el percentil 5 "
        "de la población femenina española, con una estatura de 1,49 m según los datos antropométricos del INSHT, y teniendo en "
        "cuenta que el alcance vertical máximo de pie es aproximadamente 1,24 veces la estatura, este alcance ronda los 1,85 m. "
        "Por tanto, la balda superior de un mueble alto y todo el altillo quedan fuera de su alcance (Ilustración 1). Incluso un "
        "hombre de estatura media (1,70 m, con un alcance de unos 2,11 m) no puede llegar al altillo sin ayuda.")

# ---------- utilidades de inserción ----------
def ins(before, text="", style=None, bold=False, italic=False, size=None, center=False):
    p=before.insert_paragraph_before("", style=style) if style else before.insert_paragraph_before("")
    if text:
        r=p.add_run(text); r.bold=bold; r.italic=italic
        if size: r.font.size=Pt(size)
    if center: p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    return p
def ins_img(before,path,cap,w):
    p=ins(before,center=True); p.add_run().add_picture(path,width=Cm(w))
    ins(before,cap,italic=True,size=9,center=True)
def remove_between(start_txt, end_txt, include_start=True):
    ps=d.paragraphs; i=[k for k,p in enumerate(ps) if p.text.startswith(start_txt)][0]
    j=[k for k,p in enumerate(ps) if k>i and p.text.startswith(end_txt)][0]
    for p in ps[(i if include_start else i+1):j]: p._p.getparent().remove(p._p)
    return d.paragraphs[[k for k,p in enumerate(d.paragraphs) if p.text.startswith(end_txt)][0]]

# ---------- 3. patentes (2.5.1 a 2.5.4) ----------
anchor=remove_between("2.5.1. PATENTE PRIMERA","Otras patentes consultadas")
ilu=[9]
def patente(tit,datos,resumen,rei_tit,rei,afecta,img,cap,w):
    ins(anchor,tit,style="Heading 3")
    for t in datos: ins(anchor,t,style="List Bullet")
    ins(anchor,"Resumen:",bold=True); ins(anchor,resumen)
    ins(anchor,rei_tit,bold=True); ins(anchor,rei,italic=True)
    ins_img(anchor,img,cap,w)
    ins(anchor,"¿Afecta a nuestro producto?",bold=True); ins(anchor,afecta)
patente("2.5.1. PATENTE PRIMERA: ES 1 070 877 U — Dispositivo de enclavamiento para taburetes plegables y similares",
 ["Tipo: modelo de utilidad español (clasificación A47C 7/00).","Solicitante: Gesco, S.L. (Casarrubios del Monte, Toledo). Inventor: Jorge Pajares Calvo.",
  "Nº de solicitud: U 200901059. Fecha de presentación: 26/06/2009. Publicación: 12/11/2009.",
  "Situación: caducado (la protección máxima de un modelo de utilidad es de 10 años, por lo que terminó como muy tarde en 2019)."],
 "Dispositivo que mantiene desplegado un taburete plegable. En una de las patas, junto a la articulación con la plataforma superior, hay un vástago que atraviesa la pata y que un muelle mantiene sobresaliendo. La pared lateral de la plataforma tiene un orificio enfrentado al vástago y, antes de él, una zona abombada hacia fuera. Al desplegar el taburete, esa zona empuja el vástago hacia dentro; cuando el vástago llega al orificio, el muelle lo vuelve a sacar y queda encajado, bloqueando el taburete abierto.",
 "Reivindicación 1 (texto literal):",
 "«Dispositivo de enclavamiento para taburetes plegables y similares, destinado a mantener el taburete en la condición de desplegado con plenas garantías de eficacia y seguridad para el usuario, caracterizado porque comprende en relación con al menos una de las patas (1) del taburete, en las proximidades del punto de articulación (4) entre la pata (1) y la pared lateral (3a) de la plataforma o peldaño (3) superior del taburete, la provisión de un elemento de vástago (8) escamoteable, retraíble contra la acción de un resorte (11), cuyo vástago (8) se extiende a través del espesor total de la pata (1) mencionada y presenta una porción que sobresale desde el plano superficial de dicha pata en una extensión considerable predeterminada, mientras que la citada pared (3a) lateral de dicha plataforma (3) superior del taburete presenta un orificio (9) en posición correspondientemente enfrentada a dicho vástago (8) escamoteable, dimensionado para recibir y retener a este último, desde cuyo orificio y en dirección hacia el borde libre de la pared existe una porción (10) deformada, expandida hacia fuera, que durante el despliegue del taburete alcanza y actúa sobre el extremo libre semiesférico de dicho vástago (8) para empujarlo en contra de la acción del resorte (11) y permitir el alojamiento de éste en el interior del orificio (9) cuando se alcanza el enfrentamiento mutuo de ambos, merced a la recuperación de dicho resorte (11).»",
 "No. Es el documento más parecido a nuestro producto, porque se trata precisamente de un taburete de dos peldaños con bloqueo automático al abrirlo. Sin embargo, el modelo de utilidad está caducado, así que su solución es de dominio público y se puede usar libremente. De hecho, es una buena referencia para el bloqueo automático que se busca (principio TRIZ 10, acción previa).",
 "patente1_ES1070877U.png","Ilustración 9. Figura 1 del modelo de utilidad ES 1 070 877 U, con el detalle D del vástago de bloqueo. Fuente: OEPM / Google Patents.",9)
patente("2.5.2. PATENTE SEGUNDA: US 6 454 050 B2 — Foldable step stool with leg lock and handle",
 ["Tipo: patente de Estados Unidos.","Titular original: Cosco Management, Inc. (actualmente Dorel Home Furnishings). Inventores: William B. Gibson y otros.",
  "Fecha de solicitud: 17/04/2001, con prioridad de 11/08/2000. Concesión: 24/09/2002.","Situación: expirada."],
 "Taburete-escalera plegable con un bastidor formado por una pata delantera y una pata trasera que se mueven una respecto a la otra, y un asa de transporte que gira sobre una de las patas. Una pieza de retención unida al asa gira con ella y bloquea la pata delantera con la trasera cuando el taburete está plegado, de modo que no se abre al transportarlo.",
 "Reivindicación 1 (traducción propia):",
 "«Taburete-escalera que comprende un bastidor con una pata delantera y una pata trasera acoplada a la delantera para moverse respecto a ella, un asa, un soporte de pivote configurado para que el asa gire sobre la pata delantera alrededor de un eje, y un elemento de retención unido al asa, que gira con ella y está dispuesto para atrapar una parte de la pata trasera entre el soporte de pivote y el propio elemento de retención cuando el asa se lleva a una posición determinada respecto a la pata trasera, bloqueando la pata delantera con la trasera cuando ambas están juntas en posición plegada.»",
 "No. Es una patente estadounidense, sin efectos en España, y además ha expirado. Aporta una idea interesante: usar la propia asa de transporte para mantener el taburete cerrado mientras se lleva, algo que también es útil en nuestro producto para que no se abra al colgarlo en la pared.",
 "patente2_US6454050.png","Ilustración 10. Figuras 1 y 2 de la patente US 6 454 050 B2. Fuente: USPTO / Google Patents.",9)
patente("2.5.3. PATENTE TERCERA: US 6 966 404 B2 — Folding step stool",
 ["Tipo: patente de Estados Unidos.","Titular original: Cosco Management, Inc. (actualmente Dorel Home Furnishings). Inventor: Paul K. Meeker.",
  "Fecha de solicitud: 19/05/2003. Concesión: 22/11/2005.","Situación: expirada por impago de tasas."],
 "Taburete de un escalón con dos patas que giran respecto al escalón. Cada pata tiene un soporte de bloqueo que la mantiene fija en posición de uso y, al accionarlo, permite plegar las patas paralelas al escalón para guardarlo. El escalón tiene unas aberturas que sirven de asa y una ventana por la que se ve el soporte de bloqueo cuando está bien cerrado.",
 "Reivindicación 1 (traducción propia):",
 "«Taburete-escalera que comprende un escalón con una superficie superior y una cara inferior; una primera y una segunda pata, cada una unida de forma pivotante al escalón, dispuestas extremo con extremo y paralelas al escalón en la posición cerrada de almacenaje, y separadas y no paralelas en la posición abierta de uso; y un conjunto de bloqueo para cada pata, con un soporte de bloqueo cuyo extremo inferior está unido a la cara interior de la pata y cuyo extremo superior está unido a la cara inferior del escalón, que mantiene cada pata fija respecto al escalón en la posición abierta; donde la superficie superior tiene una abertura con una plataforma rebajada y una abertura indicadora visual que deja ver una parte del soporte de bloqueo cuando este está en posición bloqueada.»",
 "No. Es una patente estadounidense, sin efectos en España, y ha expirado. Aporta dos ideas útiles: el asa formada por aberturas en la plataforma y, sobre todo, el indicador visual de bloqueo, que responde a la función comunicativa «mostrar cómo se abre y cuándo está bloqueado» del apartado 1.4.",
 "patente3_US6966404.png","Ilustración 11. Figuras 1 y 2 de la patente US 6 966 404 B2. Fuente: USPTO / Google Patents.",9)
patente("2.5.4. PATENTE CUARTA: US 12 419 421 B2 — Foldable locking step stool",
 ["Tipo: patente de Estados Unidos (clasificación A47C 4/10).","Titular: Jool Products, LLC (Lakewood, Nueva Jersey). Inventores: Judah Bergman, Yishak Sultan y Jiaxuan Ma.",
  "Nº de solicitud: 17/743,098. Fecha de solicitud: 12/05/2022. Publicación de la solicitud: US 2023/0363538 A1 (16/11/2023). Concesión: 23/09/2025.",
  "Situación: en vigor en Estados Unidos."],
 "Taburete plegable cuya plataforma se divide en dos mitades unidas por una bisagra. Tiene un mecanismo de bloqueo a prueba de niños formado por dos deslizadores, uno en cada lado de la plataforma, que hay que accionar a la vez para liberar dos pestillos con muelle y poder plegarlo. Así se evita que un niño lo cierre y se pille los dedos. Incluye agarres antideslizantes sobremoldeados y un asa integrada que queda oculta cuando el taburete está en uso.",
 "Reivindicación 1 (traducción propia):",
 "«Taburete plegable con bloqueo que comprende: una plataforma configurada para plegarse mediante bisagra en un primer y un segundo miembro; patas unidas mediante bisagra a la plataforma; y un mecanismo de bloqueo a prueba de niños; con una posición abierta, en la que ambos miembros de la plataforma quedan bloqueados en un mismo plano y el taburete está listo para usarse, y una posición cerrada, en la que quedan desbloqueados y plegados para moverlo o guardarlo; donde el mecanismo comprende un primer y un segundo deslizador situados en bordes laterales opuestos de la plataforma, cada uno accionable manualmente solo hacia fuera y conectado a un pestillo con muelle que encaja en un hueco de los miembros de la plataforma, estando los pestillos enlazados de forma que es necesario desplazar ambos deslizadores a la vez para liberar los dos pestillos.»",
 "No. La patente solo protege el invento en Estados Unidos: en su portada no figura ninguna solicitud internacional (PCT) ni prioridad extranjera, y en la búsqueda realizada no se ha encontrado ninguna solicitud europea de la misma familia. Además, nuestro diseño no divide la plataforma en dos mitades ni usa dos deslizadores simultáneos, que son elementos esenciales de la reivindicación. Si en el futuro se quisiera vender el producto en Estados Unidos, habría que evitar ese mecanismo concreto.",
 "patente4_US12419421.png","Ilustración 12. Figuras 1 y 3 de la patente US 12 419 421 B2. Fuente: USPTO.",14)

# ---------- 4. TRIZ ----------
for p in d.paragraphs:
    if p.text.startswith("Este tipo de contradicción se resuelve con los principios de separación"):
        extra=ins(d.paragraphs[[k for k,q in enumerate(d.paragraphs) if q is p][0]+1] if False else p, "")  # placeholder
        extra._p.getparent().remove(extra._p)
        np_=copy.deepcopy(p._p); p._p.addnext(np_)
        from docx.text.paragraph import Paragraph
        q=Paragraph(np_,p._parent); q.text=("Si el mismo conflicto se plantea como contradicción técnica (mejorar 13 – Estabilidad del objeto, empeora 7 – Volumen del objeto móvil), "
          "la matriz propone los principios 28, 10, 1 y 39. De ellos resulta útil el 10 (acción previa): dejar el taburete preparado para que, "
          "al abrirlo, quede automáticamente en su posición estable, y el 1 (segmentación), ya aplicado en la contradicción primera.")
        break
anchor=remove_between("Principios propuestos por la matriz: [consultar","3.3. BOCETO INICIAL")
ins(anchor,"Principios propuestos por la matriz (celda 33 / 27): 17 (otra dimensión), 27 (objetos baratos de vida corta), 8 (contrapeso) y 40 (materiales compuestos).",style="List Bullet")
ins(anchor,"Aplicación de los principios al producto:")
for t in ["Principio 8, contrapeso: aprovechar el peso del propio usuario para mantener el bloqueo. El tirante que une el peldaño con la pata trasera se diseña para quedar ligeramente pasado de su punto muerto, de forma que, al cargar el taburete, la fuerza tiende a abrirlo más en lugar de cerrarlo. Cuanto más peso, más bloqueado está.",
"Principio 17, otra dimensión: que el pestillo de seguridad se accione en una dirección perpendicular al movimiento de plegado (por ejemplo, un deslizador lateral), de modo que un golpe o una carga en el sentido de cierre no pueda soltarlo.",
"Principio 40, materiales compuestos: ya se aplica en los peldaños de polipropileno reforzado con fibra de vidrio (contradicción primera).",
"Principio 27, objetos baratos de vida corta: se descarta, porque va en contra del requisito de larga vida útil (R20).",
"Como complemento se aplica también el principio 10 (acción previa): el bloqueo se activa solo al abrir el taburete, sin que el usuario tenga que hacer nada, como en el modelo de utilidad ES 1 070 877 U."]:
    ins(anchor,t,style="List Bullet")

# ---------- 5. costes: quitar resaltado (son hipótesis declaradas) ----------
for t in d.tables:
    for row in t.rows:
        for c in row.cells:
            for par in c.paragraphs:
                for r in par.runs:
                    if r.font.highlight_color: r.font.highlight_color=None
# legislación: completar
tl=[t for t in d.tables if t.rows[0].cells[0].text=="Documento"][0]
for row in tl.rows:
    if row.cells[0].text.startswith("Reglamento (UE) 2025/40"):
        row.cells[0].paragraphs[0].runs[0].text="Reglamento (UE) 2025/40, de envases y residuos de envases"
        row.cells[1].paragraphs[0].runs[0].text="Publicado el 22/01/2025 y aplicable con carácter general desde el 12/08/2026; deroga la Directiva 94/62/CE. Reducción de envases, contenido reciclable y etiquetado de los materiales del embalaje."
        row.cells[2].paragraphs[0].runs[0].text="Obligatorio"
    if row.cells[0].text.startswith("Reglamento (CE) 1907/2006"):
        row.cells[1].paragraphs[0].runs[0].text="Restringe sustancias peligrosas en los artículos. Según la entrada 50 del anexo XVII (modificada por el Reglamento (UE) 1272/2013), las partes de caucho o plástico en contacto directo y prolongado con la piel, como los tacos y los recubrimientos antideslizantes, no pueden contener más de 1 mg/kg de cada hidrocarburo aromático policíclico (HAP)."
# nueva fila RD 1468/1988
new=copy.deepcopy(tl.rows[2]._tr); tl.rows[2]._tr.addnext(new)
from docx.table import _Row
r=_Row(new,tl)
vals=["Real Decreto 1468/1988, Reglamento de etiquetado, presentación y publicidad de los productos industriales","Información mínima obligatoria en el producto o su embalaje para la venta al consumidor: nombre del producto, fabricante o importador, características, instrucciones de uso y advertencias.","Obligatorio"]
for c,v in zip(r.cells,vals): c.paragraphs[0].runs[0].text=v

# ---------- 6. bibliografía ----------
for p in d.paragraphs:
    if "NTP 1050" in p.text:
        p.runs[0].text=p.runs[0].text.split(". ",1)[0]+". Carmona Benjumea, A. (2003). Aspectos antropométricos de la población laboral española aplicados al diseño industrial. INSHT, Madrid."
last=[p for p in d.paragraphs if p.text[:3].strip().rstrip(".").isdigit()][-1]
k=int(last.text.split(".")[0])
extra=["Pheasant, S. y Haslegrave, C. M. (2006). Bodyspace: Anthropometry, Ergonomics and the Design of Work. 3.ª ed. CRC Press.",
"Reglamento (UE) n.º 1272/2013 de la Comisión, por el que se modifica el anexo XVII de REACH en relación con los HAP. https://www.boe.es/buscar/doc.php?id=DOUE-L-2013-82738",
"Reglamento (UE) 2025/40, sobre los envases y residuos de envases. https://www.boe.es/buscar/doc.php?id=DOUE-L-2025-80087",
"Real Decreto 1468/1988, de 2 de diciembre. https://www.boe.es/buscar/act.php?id=BOE-A-1988-28089",
"USPTO. US 12,419,421 B2, Foldable locking step stool (2025). https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12419421",
"OEPM. ES 1 070 877 U, Dispositivo de enclavamiento para taburetes plegables y similares (2009)."]
cur=last
for t in extra:
    k+=1; np_=copy.deepcopy(cur._p); cur._p.addnext(np_)
    from docx.text.paragraph import Paragraph
    cur=Paragraph(np_,cur._parent); 
    for r in cur.runs[1:]: r._r.getparent().remove(r._r)
    cur.runs[0].text=f"{k}. {t}"

d.save("Trabajo_Taburete.docx")
# informe de resaltados restantes
d=Document("Trabajo_Taburete.docx")
for p in d.paragraphs:
    for r in p.runs:
        if r.font.highlight_color: print("RESALTADO:",r.text[:90])

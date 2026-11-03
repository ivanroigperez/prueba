# Deja el ACV de Eco-it solo para la alternativa 2 (decisión de Iván, 3/11/2026) y reordena el capítulo 4:
# 4.1 selección frente al EDP, 4.2 metodología y datos del ACV, 4.3 resultados y 4.4 conclusiones.
import copy, re
from docx import Document
from docx.enum.text import WD_COLOR_INDEX
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph
from docx.text.run import Run

F = "Trabajo_Taburete_v2.docx"
d = Document(F)

def paras():
    return [p for p in d.paragraphs if p._p.find(".//" + qn("w:tab")) is None]
def buscar(ini):
    r = [p for p in paras() if p.text.startswith(ini)]
    assert len(r) == 1, (ini, len(r)); return r[0]
def tabla(cond):
    r = [t for t in d.tables if cond(t)]
    assert len(r) == 1, len(r); return r[0]
def poner(p, t):
    runs = p.runs
    base = copy.deepcopy(next((r for r in runs if r.font.highlight_color is None), runs[0])._r)
    for r in runs: r._r.getparent().remove(r._r)
    for seg in re.split(r"(⟦.*?⟧)", t):
        if not seg: continue
        r = copy.deepcopy(base); p._p.append(r)
        for e in r.findall(qn("w:t")) + r.findall(qn("w:drawing")) + r.findall(qn("w:br")): r.remove(e)
        run = Run(r, p)
        if seg.startswith("⟦"):
            run.text = seg[1:-1]; run.font.highlight_color = WD_COLOR_INDEX.YELLOW
        else:
            run.text = seg; run.font.highlight_color = None
def celda(c, t):
    p = c.paragraphs[0]
    for r in p.runs[1:]: r._r.getparent().remove(r._r)
    r = p.runs[0]; r.text = t; r.font.highlight_color = None
def borrar_entre(a, b):
    el = a
    while el is not b:
        sig = el.getnext(); el.getparent().remove(el); el = sig

# ---- localizar ----
intro = buscar("En esta etapa se evalúan las tres alternativas")
nota = buscar("[NOTA, BORRAR ANTES DE ENTREGAR")
h41 = buscar("4.1. METODOLOGÍA Y DATOS DEL ANÁLISIS")
elim = buscar("Eliminación: reciclaje del 90 % de los metales")
datos = buscar("Los datos introducidos en Eco-it para cada alternativa")
t12 = tabla(lambda t: t.rows[0].cells[0].text == "Elemento")
pie12 = buscar("Tabla 12. Datos introducidos en Eco-it")
excl = buscar("El análisis no incluye el embalaje")
h42 = buscar("4.2. ALTERNATIVA 1: ACERO")
h43 = buscar("4.3. ALTERNATIVA 2: ALUMINIO Y POLIPROPILENO")
p43 = buscar("La alternativa de aluminio es la más ligera")
h44 = buscar("4.4. ALTERNATIVA 3: MADERA")
h45 = buscar("4.5. COMPARATIVA Y CONCLUSIONES")
comp = buscar("En las tres alternativas domina")
filtro = buscar("El impacto ambiental no es el único criterio")
t16 = tabla(lambda t: t.rows[0].cells[0].text == "Criterio")
pie16 = buscar("Tabla 16. Comprobación de las alternativas")
c1 = buscar("Solo la alternativa de aluminio y polipropileno cumple todas")
c2 = buscar("Su punto débil es el impacto del aluminio primario")
c3 = buscar("La madera es la alternativa de menor impacto ambiental")
etiq = c1._p.getprevious()
assert Paragraph(etiq, c1._parent).text == "Conclusiones:"
assert filtro._p.getnext() is t16._tbl and t16._tbl.getnext() is pie16._p

# ---- borrar lo de las alternativas 1 y 3, la comparativa y la nota ----
borrar_entre(h42._p, h43._p)               # 4.2 completo: texto, Tabla 13 y hueco de la Ilustración 18
borrar_entre(h44._p.getnext(), h45._p)     # contenido del 4.4: texto, Tabla 15 y hueco de la Ilustración 23
borrar_entre(comp._p, filtro._p)           # texto de la comparativa y hueco de la Ilustración 24
for el in (nota._p, etiq): el.getparent().remove(el)

# ---- 4.1: la selección frente al EDP pasa al principio ----
intro._p.addnext(h45._p); h45._p.addnext(filtro._p); filtro._p.addnext(t16._tbl); t16._tbl.addnext(pie16._p)
for row in t16.rows:
    if row.cells[0].text.startswith("Impacto del ciclo de vida"):
        row._tr.getparent().remove(row._tr)

# ---- títulos ----
poner(h45, "4.1. SELECCIÓN DE LA ALTERNATIVA")
poner(h41, "4.2. METODOLOGÍA Y DATOS DEL ACV")
poner(h43, "4.3. RESULTADOS DEL ACV")
poner(h44, "4.4. CONCLUSIONES")

# ---- textos ----
poner(intro, "En esta etapa se elige una de las tres alternativas de material del apartado 3.3 y se analiza su impacto ambiental con un pequeño análisis de ciclo de vida (ACV) hecho con Eco-it, el programa de las prácticas de la asignatura.")
poner(filtro, "Para elegir, se ha comprobado qué alternativas cumplen las propiedades imprescindibles del EDP, ya que un requisito imprescindible no se compensa con una buena nota en otros criterios (Tabla 16). El ACV se ha hecho solo con la alternativa que las cumple todas.")
poner(elim, "Eliminación: reciclaje del 90 % de los metales (el 10 % restante va a vertedero) e incineración del polipropileno y del caucho.")
poner(datos, "Los datos de la alternativa 2 introducidos en Eco-it están en la Tabla 12. Se ha calculado una variante con aluminio reciclado en lugar de primario para valorar la mejora propuesta en las conclusiones.")
poner(pie12, "Tabla 12. Datos de la alternativa 2 introducidos en Eco-it (masas del modelo de SolidWorks). Elaboración propia.")
poner(excl, "El análisis no incluye el embalaje, el anodizado ni las mermas de fabricación, y las bases de datos de Eco-it recogen valores medios.")
poner(p43, "La alternativa de aluminio es la más ligera, pero el aluminio primario tiene un impacto por kilo muy alto. Los datos se han introducido en Eco-it pieza a pieza (Ilustraciones 19 y 20). La producción es la fase de mayor impacto, con 33 kg CO₂-eq de un total de 35 kg CO₂-eq (Tabla 14 e Ilustración 21). Solo el aluminio primario, 2,29 kg a 12,2 kg CO₂-eq/kg, aporta unos 28 kg CO₂-eq, y 1,86 kg de ese aluminio están en los largueros y las patas traseras. La fase de uso es nula en un producto que no consume energía. La eliminación suma 1,9 kg CO₂-eq por la incineración del polipropileno y del caucho, y el reciclaje de los metales prácticamente no cuenta en esta base de datos.")

# ---- Tabla 12: solo la columna de la alternativa 2 ----
tbl = t12._tbl; anchos = (3969, 4536)
grid = tbl.find(qn("w:tblGrid")); gcs = grid.findall(qn("w:gridCol")); assert len(gcs) == 4
for i in (3, 1): grid.remove(gcs[i])
for gc, w in zip(grid.findall(qn("w:gridCol")), anchos): gc.set(qn("w:w"), str(w))
for tr in tbl.findall(qn("w:tr")):
    tcs = tr.findall(qn("w:tc")); assert len(tcs) == 4 and not tr.findall(".//" + qn("w:gridSpan"))
    for i in (3, 1): tr.remove(tcs[i])
    for tc, w in zip(tr.findall(qn("w:tc")), anchos):
        tcW = tc.find(qn("w:tcPr") + "/" + qn("w:tcW"))
        if tcW is not None: tcW.set(qn("w:w"), str(w)); tcW.set(qn("w:type"), "dxa")
tblW = tbl.find(qn("w:tblPr") + "/" + qn("w:tblW"))
print("tblW:", None if tblW is None else (tblW.get(qn("w:w")), tblW.get(qn("w:type"))))
if tblW is not None and tblW.get(qn("w:type")) == "dxa": tblW.set(qn("w:w"), str(sum(anchos)))
celda(t12.rows[0].cells[1], "Material y cantidad")

# ---- conclusiones: madera tras la selección, después el ACV y el aluminio reciclado ----
poner(c3, "La alternativa de madera se queda cerca del peso máximo, pero su modelo está simplificado. Los listones son macizos y tienen la misma sección que los perfiles metálicos (40 × 20 mm), que habría que aumentar para soportar 150 kg, y el vaciado de la plataforma no se puede fabricar en contrachapado. Queda como línea de trabajo futura si se consigue un diseño en madera verificado por debajo de 3,5 kg.")
nuevo = copy.deepcopy(c1._p)
c1._p.addnext(c3._p); c3._p.addnext(nuevo)
poner(Paragraph(nuevo, c1._parent), "En el ACV de la alternativa 2 la producción concentra casi todo el impacto, 33 de los 35 kg CO₂-eq. Las decisiones de diseño con más efecto ambiental son la elección del material y la cantidad empleada.")
poner(c2, "El punto débil de la alternativa 2 es el aluminio primario, y por eso se especifica aluminio con alto contenido reciclado. Si todo el aluminio es reciclado, el impacto del ciclo de vida baja de 35 a 10,5 kg CO₂-eq, un 70 % menos.")

# ---- renumeración de ilustraciones y tablas (pies y referencias) ----
RXCAP = re.compile(r"^(Ilustración|Tabla) (\d+|§\w+§)\. ")
mapa = {"Ilustración": {}, "Tabla": {}}; cont = {"Ilustración": 0, "Tabla": 0}
for p in paras():
    m = RXCAP.match(p.text)
    if m:
        tipo, tok = m.group(1), m.group(2); cont[tipo] += 1; mapa[tipo][tok] = cont[tipo]
        if tok != str(cont[tipo]):
            poner(p, f"{tipo} {cont[tipo]}. " + p.text[m.end():])
RXREF = re.compile(r"\b(Ilustraci(?:ón|ones)|Tablas?)(\s+)((?:\d+|§\w+§)(?:\s*(?:,|y|a|e|–|-)\s*(?:\d+|§\w+§))*)")
cambios = []
def renum(p):
    if p._p.find(".//" + qn("w:tab")) is not None or RXCAP.match(p.text): return
    for r in p.runs:
        def f(m):
            tipo = "Ilustración" if m.group(1).startswith("Ilustraci") else "Tabla"
            def g(t):
                v = mapa[tipo].get(t.group())
                if v is None: cambios.append(("SIN MAPA", t.group(), p.text[:50])); return t.group()
                if str(v) != t.group(): cambios.append((tipo, t.group(), v))
                return str(v)
            return m.group(1) + m.group(2) + re.sub(r"\d+|§\w+§", g, m.group(3))
        n = RXREF.sub(f, r.text)
        if n != r.text: r.text = n
for p in d.paragraphs: renum(p)
for tb in d.tables:
    for row in tb.rows:
        for c in row.cells:
            for p in c.paragraphs: renum(p)
print("ilustraciones:", cont["Ilustración"], "tablas:", cont["Tabla"])
for c in cambios: print("  ", c)
amarillo = [p.text[:60] for p in d.paragraphs if any(r.font.highlight_color is not None for r in p.runs)]
amarillo += [c.text[:60] for t in d.tables for row in t.rows for c in row.cells for p in c.paragraphs if any(r.font.highlight_color is not None for r in p.runs)]
print("texto en amarillo que queda:", amarillo)
d.save(F); print("guardado")

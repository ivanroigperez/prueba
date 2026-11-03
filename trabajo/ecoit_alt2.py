# Inserta en Trabajo_Taburete_v2.docx los resultados de Eco-it de la alternativa 2 (práctica del 3/11/2026):
# capturas de producción, eliminación y gráfico, y los valores 33 / 0 / 1,9 / 35 kg CO2-eq.
import copy, re
from docx import Document
from docx.shared import Cm, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph
from docx.text.run import Run

F = "Trabajo_Taburete_v2.docx"
d = Document(F)
body = d.element.body
X = "⟦[      ]⟧"

def paras():
    return [p for p in d.paragraphs if p._p.find(".//" + qn("w:tab")) is None]
def buscar(ini):
    r = [p for p in paras() if p.text.startswith(ini)]
    assert len(r) == 1, (ini, len(r)); return r[0]
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

# ---- 4.1: base de datos y tacos de repuesto ----
p = buscar("Eco-it es una herramienta de ACV simplificado")
poner(p, "Eco-it es una herramienta de ACV simplificado pensada para diseñadores. El análisis sigue el enfoque “de la cuna a la tumba” de las normas UNE-EN ISO 14040 y 14044, usa la base de datos Ecoindicadores_IHOBE y expresa los resultados como huella de carbono, en kg de CO₂ equivalente. La unidad funcional es un taburete-escalera que permite a un usuario de hasta 150 kg alcanzar 2,30 m de altura durante 10 años de uso doméstico. Eco-it divide el ciclo de vida en tres fases:")
poner(buscar("Uso: el producto no consume energía"), "Uso: el producto no consume energía. Eco-it no admite materiales en la fase de uso, y los cuatro tacos de repuesto que se cambian una vez en su vida útil se han incluido en la producción.")
t12 = [t for t in d.tables if t.rows[0].cells[0].text == "Elemento"][0]
for row in t12.rows:
    if row.cells[0].text.startswith("Uso: tacos de repuesto"):
        celda(row.cells[0], "Tacos de repuesto (en producción)")

# ---- 4.3: texto de la alternativa 2 ----
p43 = buscar("La alternativa de aluminio es la más ligera")
poner(p43, f"La alternativa de aluminio es la más ligera, pero el aluminio primario tiene un impacto por kilo muy alto. Los datos se han introducido en Eco-it pieza a pieza (Ilustraciones §a2prod§ y §a2elim§). La producción vuelve a dominar, con 33 kg CO₂-eq de un total de 35 kg CO₂-eq (Tabla 14 e Ilustración §a2res§). Solo el aluminio primario, 2,29 kg a 12,2 kg CO₂-eq/kg, aporta unos 28 kg CO₂-eq, y 1,86 kg de ese aluminio están en los largueros y las patas traseras. La eliminación suma 1,9 kg CO₂-eq por la incineración del polipropileno y del caucho, y el reciclaje de los metales prácticamente no cuenta en esta base de datos. Con aluminio reciclado el total baja a {X} kg CO₂-eq.")

# ---- capturas de producción y eliminación (antes de la Tabla 14) ----
t14 = [t for t in d.tables if [c.text for c in t.rows[0].cells] == ["Fase", "Aluminio primario", "Aluminio reciclado"]][0]
modelo_pie = buscar("Ilustración 18. Resultados de Eco-it")._p
def figura(png, ancho, pie, antes_de):
    p = d.add_paragraph(); antes_de.addprevious(p._p)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(png, width=Cm(ancho))
    c = copy.deepcopy(modelo_pie); antes_de.addprevious(c); poner(Paragraph(c, p._parent), pie)
figura("ecoit/alt2_produccion.png", 13, "Ilustración §a2prod§. Fase de producción de la alternativa 2 en Eco-it. Elaboración propia.", t14._tbl)
figura("ecoit/alt2_eliminacion.png", 13, "Ilustración §a2elim§. Fase de eliminación de la alternativa 2 en Eco-it. Elaboración propia.", t14._tbl)

# ---- Tabla 14: columna de aluminio primario ----
for row, v in zip(t14.rows[1:], ("33", "0", "1,9", "35")):
    celda(row.cells[1], v)

# ---- gráfico de resultados en el hueco de la alternativa 2 ----
hueco = buscar("[Pegar la captura de los resultados de Eco-it de la alternativa 2]")
for r in hueco.runs: r._r.getparent().remove(r._r)
hueco.paragraph_format.space_before = None; hueco.paragraph_format.space_after = None
hueco.add_run().add_picture("ecoit/alt2_resultados.png", width=Cm(10))
poner(buscar("Ilustración 19. Resultados de Eco-it de la alternativa 2"), "Ilustración §a2res§. Resultados de Eco-it de la alternativa 2: aluminio y polipropileno. Elaboración propia.")

# ---- Tabla 16 y conclusión ----
t16 = [t for t in d.tables if t.rows[0].cells[0].text == "Criterio"][0]
for row in t16.rows:
    if row.cells[0].text.startswith("Impacto del ciclo de vida"):
        celda(row.cells[2], "35")
poner(buscar("Su punto débil es el impacto del aluminio primario"), f"Su punto débil es el impacto del aluminio primario, y por eso se especifica aluminio con alto contenido reciclado. Con este material Eco-it da {X} kg CO₂-eq en lugar de 35, un {X} % menos.")

# ---- renumeración de ilustraciones (pies y referencias) ----
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
for t in d.tables:
    for row in t.rows:
        for c in row.cells:
            for p in c.paragraphs: renum(p)
print("ilustraciones:", cont["Ilustración"], "tablas:", cont["Tabla"])
for c in cambios: print("  ", c)
print("marcas sin resolver:", [p.text[:60] for p in d.paragraphs if "§" in p.text])
d.save(F); print("guardado")

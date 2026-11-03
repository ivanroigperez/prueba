# Inserta en Trabajo_Taburete_v2.docx los resultados de Eco-it de la variante de la alternativa 2 con aluminio
# reciclado (práctica del 3/11/2026): producción 8,6, uso 0, eliminación 1,9 kg CO2-eq. La suma de fases es 10,5;
# el gráfico de Eco-it la redondea a 11.
import copy, re
from docx import Document
from docx.shared import Cm
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

# ---- 4.3: la frase de la variante sale del párrafo principal ----
p43 = buscar("La alternativa de aluminio es la más ligera")
t = p43.text; fin = "Con aluminio reciclado el total baja a"
assert fin in t
poner(p43, t[:t.index(fin)].rstrip())

# ---- Tabla 14: columna de aluminio reciclado ----
t14 = [t for t in d.tables if [c.text for c in t.rows[0].cells] == ["Fase", "Aluminio primario", "Aluminio reciclado"]][0]
for row, v in zip(t14.rows[1:], ("8,6", "0", "1,9", "10,5")):
    celda(row.cells[2], v)

# ---- párrafo y gráfico de la variante, después de la Ilustración 21 ----
pie21 = buscar("Ilustración 21. Resultados de Eco-it de la alternativa 2")
img21 = pie21._p.getprevious()
assert img21.find(".//" + qn("w:drawing")) is not None
txt = copy.deepcopy(p43._p); pie21._p.addnext(txt)
poner(Paragraph(txt, p43._parent),
      "En la variante con aluminio reciclado, las cuatro piezas de aluminio pasan a ser de “Aluminio secundario, a partir de chatarra vieja” y el resto del modelo no cambia. "
      "La producción baja de 33 a 8,6 kg CO₂-eq y el total, de 35 a 10,5 kg CO₂-eq, un 70 % menos (Tabla 14 e Ilustración §a2rec§). "
      "El gráfico de Eco-it muestra este total redondeado a 11 kg CO₂-eq.")
img = copy.deepcopy(img21)
for r in img.findall(qn("w:r")): img.remove(r)
txt.addnext(img)
pimg = Paragraph(img, p43._parent); pimg.paragraph_format.keep_with_next = True
pimg.add_run().add_picture("ecoit/alt2_reciclado_resultados.png", width=Cm(10))
pie = copy.deepcopy(pie21._p); img.addnext(pie)
poner(Paragraph(pie, p43._parent), "Ilustración §a2rec§. Resultados de Eco-it de la alternativa 2 con aluminio reciclado. Elaboración propia.")

# ---- conclusión ----
poner(buscar("Su punto débil es el impacto del aluminio primario"),
      "Su punto débil es el impacto del aluminio primario, y por eso se especifica aluminio con alto contenido reciclado. "
      "Si todo el aluminio es reciclado, el impacto del ciclo de vida baja de 35 a 10,5 kg CO₂-eq, un 70 % menos.")

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
for tb in d.tables:
    for row in tb.rows:
        for c in row.cells:
            for p in c.paragraphs: renum(p)
print("ilustraciones:", cont["Ilustración"], "tablas:", cont["Tabla"])
for c in cambios: print("  ", c)
print("marcas sin resolver:", [p.text[:60] for p in d.paragraphs if "§" in p.text])
d.save(F); print("guardado")

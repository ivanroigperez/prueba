# Correcciones tras las comprobaciones del 3/11/2026: precio del IKEA BOLMEN (4,99 € en ikea.es), celda TRIZ 13/7
# (28, 10, 19, 39 en la matriz clásica) y frase del 4.2 sobre las masas usadas en el ACV.
import copy, re
from docx import Document
from docx.enum.text import WD_COLOR_INDEX
from docx.oxml.ns import qn
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
    r = copy.deepcopy(base); p._p.append(r)
    for e in r.findall(qn("w:t")) + r.findall(qn("w:drawing")) + r.findall(qn("w:br")): r.remove(e)
    run = Run(r, p); run.text = t; run.font.highlight_color = None
def celda(c, t):
    p = c.paragraphs[0]
    for r in p.runs[1:]: r._r.getparent().remove(r._r)
    p.runs[0].text = t

# ---- Tabla 4 e Ilustración 6: precio del BOLMEN ----
t4 = [t for t in d.tables if t.rows[0].cells[0].text == "Producto" and t.rows[0].cells[-1].text == "Precio"]
assert len(t4) == 1
fila = [r for r in t4[0].rows if r.cells[0].text == "IKEA BOLMEN"]; assert len(fila) == 1
assert fila[0].cells[-1].text == "1,50 €"; celda(fila[0].cells[-1], "4,99 €")
pie4 = buscar("Tabla 4. Taburetes-escalera del mercado español")
r = [r for r in pie4.runs if "septiembre de 2026" in r.text]; assert len(r) == 1
r[0].text = r[0].text.replace("septiembre de 2026", "septiembre y noviembre de 2026")
pie6 = buscar("Ilustración 6. Precio de venta")
blip = pie6._p.getprevious().find(".//" + qn("a:blip"))
parte = d.part.related_parts[blip.get(qn("r:embed"))]
parte._blob = open("figura5_precios_mercado.png", "rb").read()

# ---- 3.2: celda 13/7 de la matriz ----
poner(buscar("Planteado como contradicción técnica (mejorar el parámetro 13"),
      "Planteado como contradicción técnica (mejorar el parámetro 13, estabilidad del objeto, empeora el 7, volumen del objeto móvil), "
      "la matriz propone los principios 28, 10, 19 y 39. El más útil es el 10 (acción previa), que consiste en dejar el taburete preparado "
      "para que al abrirlo quede solo en su posición estable. El 28 (sustitución de sistemas mecánicos), el 19 (acción periódica) y el 39 "
      "(atmósfera inerte) no tienen una aplicación clara en este producto.")

# ---- 4.2: masas del ACV frente al diseño final ----
poner(buscar("El análisis no incluye el embalaje, el anodizado"),
      "El ACV usa las masas del modelo de SolidWorks (3,17 kg), sin la fibra de vidrio, los nervios y los casquillos del apartado 3.5, "
      "que llevan la masa a unos 3,46 kg. El análisis no incluye el embalaje, el anodizado ni las mermas de fabricación, y las bases de datos "
      "de Eco-it recogen valores medios.")
d.save(F); print("guardado")

# ---- Después: celdas de tabla sin tamaño propio (salían a 11 pt) al tamaño mayoritario del cuerpo de su tabla ----
from collections import Counter
from docx.shared import Pt
d = Document(F)
for ti, t in enumerate(d.tables):
    if ti < 2: continue  # tablas de la portada
    cnt = Counter(); nulos = []
    for r in t.rows[1:]:
        for c in r.cells:
            for p in c.paragraphs:
                for run in p.runs:
                    if run.text.strip():
                        if run.font.size: cnt[run.font.size.pt] += 1
                        else: nulos.append(run)
    if nulos and cnt:
        for run in nulos: run.font.size = Pt(cnt.most_common(1)[0][0])
d.save(F)

# Genera Guion_presentacion.docx a partir de las notas de las diapositivas (copia local del deck en el scratchpad).
import json, re
from docx import Document
from docx.shared import Pt, Cm, RGBColor

D = "/tmp/claude-0/-home-user-prueba/1e15d777-fea3-54a9-ae9b-0a6049279c2c/scratchpad/deck/project"
deck = json.load(open(f"{D}/deck.json", encoding="utf-8"))
doc = Document()
s = doc.sections[0]; s.page_width = Cm(21); s.page_height = Cm(29.7)
for m in ("left_margin", "right_margin", "top_margin", "bottom_margin"): setattr(s, m, Cm(2.2))
st = doc.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(11)
for h, sz in (("Heading 1", 15), ("Heading 2", 12)):
    doc.styles[h].font.name = "Calibri"; doc.styles[h].font.size = Pt(sz); doc.styles[h].font.color.rgb = RGBColor(0x2F, 0x55, 0x97)
doc.add_heading("Guion de la presentación (8 minutos)", level=1)
p = doc.add_paragraph("Documento para ensayar, no se entrega. El mismo texto está en las notas de cada diapositiva. "
                      "No hace falta decirlo palabra por palabra: léelo en voz alta con cronómetro y cambia las frases que no dirías tú.")
p.runs[0].italic = True
total = 0
for n, sid in enumerate(deck["order"], 1):
    h = open(f"{D}/slides/{sid}.html", encoding="utf-8").read()
    titulo = re.search(r"<h[12][^>]*>(.*?)</h[12]>", h, re.S).group(1)
    nota = re.search(r"<aside>(.*?)</aside>", h, re.S).group(1).strip()
    m = re.match(r"\[(\d+:\d+) - (\d+:\d+)\]\s*(.*)", nota, re.S)
    doc.add_heading(f"{n}. {titulo}  ({m.group(1)} a {m.group(2)})", level=2)
    doc.add_paragraph(m.group(3))
    total += len(m.group(3).split())
doc.add_heading("Si vas justo de tiempo", level=2)
doc.add_paragraph("Acorta las diapositivas 5 (patentes) y 8 (comprobaciones): basta con decir la conclusión de cada una.")
doc.add_heading("Preguntas probables", level=2)
for q, a in [
    ("¿Por qué no el acero o la madera?", "Porque no cumplen el peso máximo, que es imprescindible para llevarlo con una mano: 9,20 y 3,96 kg frente a 3,5 kg."),
    ("¿Por qué el ACV solo de la alternativa 2?", "El profesor pidió el ACV del producto, y las otras dos ya quedan descartadas antes por el peso."),
    ("¿Por qué el gráfico de Eco-it dice 11 y la tabla 10,5?", "Eco-it redondea a dos cifras. Las fases suman 8,6 + 0 + 1,9 = 10,5."),
    ("¿El ACV tiene en cuenta la fibra de vidrio y los nervios?", "No. Usa las masas del modelo (3,17 kg) con polipropileno normal, porque la base de datos no tiene PP con fibra. Está dicho en el apartado 4.2."),
    ("¿Está diseñado el pestillo?", "Está dimensionado (522 N·m, 710 N por pasador) pero no modelado. Es el siguiente paso, junto con un prototipo para los ensayos de la norma."),
    ("¿Bastan las comprobaciones a mano?", "Son cálculos sencillos con coeficiente de seguridad 2. El paso siguiente sería una simulación en SolidWorks y los ensayos de la UNE-EN 14183."),
]:
    p = doc.add_paragraph(style="List Bullet"); r = p.add_run(q + " "); r.bold = True; p.add_run(a)
doc.save("/home/user/prueba/presentacion/Guion_presentacion.docx")
print("palabras del guion:", total, "(unos", round(total / 135, 1), "min a ritmo tranquilo)")

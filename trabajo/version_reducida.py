# Versión reducida del trabajo (unas 25 páginas), pedida por Iván el 7/11/2026. Parte de Trabajo_Taburete_v2.docx
# y deja solo lo que pide el profesor: etapa inicial, información (mercado y costes, EDP, patentes y legislación),
# técnico-creativa (mapa mental y TRIZ), evaluación con el ACV de Eco-it y realización (planos).
import copy, re, shutil
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph
from docx.text.run import Run

SRC, F = "Trabajo_Taburete_v2.docx", "Trabajo_Taburete_reducido.docx"
shutil.copy(SRC, F)
d = Document(F)

def paras():
    return [p for p in d.paragraphs if p._p.find(".//" + qn("w:tab")) is None]
def buscar(ini):
    r = [p for p in paras() if p.text.startswith(ini)]
    assert len(r) == 1, (ini, len(r)); return r[0]
def poner(p, t):
    runs = p.runs
    base = copy.deepcopy(runs[0]._r)
    for r in runs: r._r.getparent().remove(r._r)
    r = copy.deepcopy(base); p._p.append(r)
    for e in r.findall(qn("w:t")) + r.findall(qn("w:drawing")) + r.findall(qn("w:br")): r.remove(e)
    Run(r, p).text = t
def cambiar(ini, viejo, nuevo):
    p = buscar(ini); t = p.text
    assert t.count(viejo) == 1, (ini, viejo); poner(p, t.replace(viejo, nuevo))
def nivel(el):
    if el.tag != qn("w:p"): return None
    s = Paragraph(el, d).style.name
    return int(s[-1]) if s.startswith("Heading ") and s[-1].isdigit() else None
def borrar_seccion(titulo):
    h = buscar(titulo); n = nivel(h._p); el = h._p
    while el is not None and el.tag != qn("w:sectPr"):
        sig = el.getnext(); el.getparent().remove(el); el = sig
        if el is not None and nivel(el) is not None and nivel(el) <= n: break
def borrar_pie_y_objeto(pie):
    p = buscar(pie); obj = p._p.getprevious()
    assert obj.tag == qn("w:tbl") or obj.find(".//" + qn("w:drawing")) is not None, pie
    obj.getparent().remove(obj); p._p.getparent().remove(p._p)

# ---- 1. apartados que no pide el profesor ----
for t in ("2.4. TECNOLOGÍAS EXISTENTES", "2.7. NORMAS INTERESANTES", "2.8. AFECCIÓN AL ENTORNO",
          "2.9. ALMACENAJE", "2.10. EMBALAJE", "2.11. MONTAJE", "5. ETAPA DE REDISEÑO"):
    borrar_seccion(t)

# ---- 2. TRIZ: la tabla de los 39 parámetros y 40 principios ----
borrar_pie_y_objeto("Tabla 9. Los 39 parámetros técnicos")
cambiar("TRIZ (Teoría para Resolver Problemas de Inventiva)", "40 principios inventivos (Tabla 9), relacionados", "40 principios inventivos, relacionados")

# ---- 3. patentes: sin el texto completo de las reivindicaciones ----
for p in [p for p in paras() if p.text.startswith("Reivindicación 1 (")]:
    cita = p._p.getnext(); assert Paragraph(cita, p._parent).text.startswith("“")
    cita.getparent().remove(cita); p._p.getparent().remove(p._p)

# ---- 4. frases que citaban lo eliminado ----
cambiar("El coste industrial se ha repartido", " El reparto por componente se ha revisado en el análisis del valor (apartado 5.3) con las masas del modelo de SolidWorks.", "")
cambiar("El modelo todavía no incluye el pestillo", "Su diseño de detalle queda como acción correctora del AMFEC (apartado 5.2).", "Su diseño de detalle queda pendiente.")
cambiar("La etapa de información reúne", "costes, competencia, patentes, normativa, tecnologías y condiciones de almacenaje, embalaje y montaje", "costes, competencia, patentes y normativa")
cambiar("Diseño, ciclo de vida y rediseño", "Diseño, ciclo de vida y rediseño", "Diseño y ciclo de vida")

# ---- 4b. patentes en formato corto: datos en un párrafo, sin rótulos y con figura solo en la primera y la cuarta ----
DATOS = {
 "2.5.1.": "Modelo de utilidad español (A47C 7/00) de Gesco, S.L., con Jorge Pajares Calvo como inventor. Se presentó el 26/06/2009 con el número U 200901059 y está caducado, ya que un modelo de utilidad protege como máximo 10 años (hasta 2019 en este caso).",
 "2.5.2.": "Patente de Estados Unidos de Cosco Management, Inc. (hoy Dorel Home Furnishings), con William B. Gibson y otros como inventores. Se solicitó el 17/04/2001, con prioridad de 11/08/2000, se concedió el 24/09/2002 y ha expirado.",
 "2.5.3.": "Patente de Estados Unidos de Cosco Management, Inc. (hoy Dorel Home Furnishings), con Paul K. Meeker como inventor. Se solicitó el 19/05/2003, se concedió el 22/11/2005 y ha expirado por impago de tasas.",
 "2.5.4.": "Patente de Estados Unidos (A47C 4/10) de Jool Products, LLC (Lakewood, Nueva Jersey), con Judah Bergman, Yishak Sultan y Jiaxuan Ma como inventores. Se solicitó el 12/05/2022 (17/743,098), se publicó como US 2023/0363538 A1 el 16/11/2023 y se concedió el 23/09/2025. Está en vigor en Estados Unidos.",
}
for clave, texto in DATOS.items():
    h = buscar(clave); el = h._p.getnext(); vinetas = []
    while Paragraph(el, h._parent).style.name == "List Bullet":
        vinetas.append(el); el = el.getnext()
    assert len(vinetas) == 4 and Paragraph(el, h._parent).text == "Resumen:", clave
    rotulo, resumen = el, el.getnext()
    nuevo = copy.deepcopy(resumen); vinetas[0].addprevious(nuevo); poner(Paragraph(nuevo, h._parent), texto)
    for e in vinetas + [rotulo]: e.getparent().remove(e)
for pie in ("Ilustración 8. Figuras 1 y 2 de la patente US 6 454 050", "Ilustración 9. Figuras 1 y 2 de la patente US 6 966 404"):
    borrar_pie_y_objeto(pie)
for p in [p for p in paras() if p.text in ("¿Afecta al producto?", "¿Es patentable el producto?")]:
    sig = Paragraph(p._p.getnext(), p._parent)
    if p.text.startswith("¿Afecta"):
        assert sig.text.startswith("No. "); poner(sig, "No afecta al producto. " + sig.text[4:])
    p._p.getparent().remove(p._p)

# ---- 4c. figuras que repiten información ----
borrar_pie_y_objeto("Ilustración 2. Accidentes domésticos")
cambiar("Las caídas son el accidente doméstico", " (Ilustración 2)", "")
borrar_pie_y_objeto("Ilustración 6. Precio de venta")
cambiar("Se han analizado los taburetes-escalera", "Sus características principales están en la Tabla 4 y sus precios en la Ilustración 6.", "Sus características y precios están en la Tabla 4.")
borrar_pie_y_objeto("Ilustración 16. Ensamblaje abierto, vista frontal")
cambiar("El modelo de SolidWorks 2026 tiene diez piezas", "(Ilustraciones 15 a 17)", "(Ilustraciones 15 y 17)")
borrar_pie_y_objeto("Ilustración 19. Fase de eliminación")
cambiar("La alternativa de aluminio es la más ligera", "(Ilustraciones 18 y 19)", "(Ilustración 18)")
h35 = buscar("3.5. COMPROBACIONES DE RESISTENCIA")
for e in h35._p.pPr.findall(qn("w:pageBreakBefore")): h35._p.pPr.remove(e)

# ---- 4d. más recortes de lo que repite información (los capítulos siguen empezando en página nueva) ----
borrar_pie_y_objeto("Ilustración 1. Alturas habituales del mobiliario")
cambiar("Estas alturas no están al alcance", " (Ilustración 1)", "")
borrar_pie_y_objeto("Ilustración 4. Árbol de funciones")
cambiar("Las funciones del producto se han clasificado", " (Ilustración 4)", "")
borrar_pie_y_objeto("Ilustración 10. Figuras 1 y 3 de la patente US 12 419 421")
rot = buscar("Análisis de las soluciones existentes:"); el = rot._p.getnext()
while Paragraph(el, rot._parent).style.name == "List Bullet":
    sig = el.getnext(); el.getparent().remove(el); el = sig
rot._p.getparent().remove(rot._p)
p = buscar("Solo la alternativa de aluminio cumple la propiedad P5"); p._p.getparent().remove(p._p)
borrar_pie_y_objeto("Tabla 10. Masa de cada pieza por alternativa")
cambiar("El modelo confirma las propiedades principales", "Las masas de cada pieza, calculadas con la herramienta de propiedades físicas, están en la Tabla 10.", "Las masas de cada pieza se han calculado con la herramienta de propiedades físicas.")
cambiar("Producción: materiales y procesos de fabricación", " (Tabla 10)", "")
borrar_pie_y_objeto("Tabla 13. Datos de la alternativa 2 introducidos en Eco-it")
cambiar("Los datos de la alternativa 2 introducidos en Eco-it están en la Tabla 13.", "Los datos de la alternativa 2 introducidos en Eco-it están en la Tabla 13. ", "")
p = buscar("La alternativa de madera se queda cerca del peso máximo"); p._p.getparent().remove(p._p)

# ---- 4e. ajuste de huecos: la figura de la patente, un poco menor para que quepa en su página, y dos frases repetidas ----
WP = "{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
img = buscar("Ilustración 7. Figura 1 del modelo de utilidad")._p.getprevious()
ext = next(img.iter(WP + "extent")); cx, cy = int(ext.get("cx")), int(ext.get("cy")); f = 8.5 / (cy / 360000)
for e in list(img.iter(WP + "extent")) + list(img.iter(A + "ext")):
    if e.get("cx") is not None: e.set("cx", str(round(int(e.get("cx")) * f))); e.set("cy", str(round(int(e.get("cy")) * f)))
cambiar("Las funciones del producto se han clasificado", " Las demás son secundarias y hacen posible o mejoran la principal.", "")
cambiar("Las propiedades traducen los requisitos", " Los valores de peso y de espesor plegado se endurecieron tras el estudio de mercado del apartado 2.2, al quedar los iniciales por debajo de lo que ya ofrece la competencia.", "")

# ---- 4f. etapa inicial en cinco páginas: el árbol de estructura al ancho de la Ilustración 3 (15 cm) y una frase que ya muestra el árbol ----
img = buscar("Ilustración 5. Árbol de estructura del taburete-escalera")._p.getprevious()
ext = next(img.iter(WP + "extent")); f = 15.0 / (int(ext.get("cx")) / 360000)
for e in list(img.iter(WP + "extent")) + list(img.iter(A + "ext")):
    if e.get("cx") is not None: e.set("cx", str(round(int(e.get("cx")) * f))); e.set("cy", str(round(int(e.get("cy")) * f)))
cambiar("La estructura describe cómo se organiza el producto", " Constaba de un bastidor portante, unas superficies de apoyo para el pie, un mecanismo de plegado y bloqueo y unos apoyos antideslizantes.", "")

# ---- 5. numeración de títulos ----
for p in paras():
    if not p.style.name.startswith("Heading"): continue
    t = p.text; n = t
    n = re.sub(r"^2\.5(\.\d+)?\. ", lambda m: f"2.4{m.group(1) or ''}. ", n)
    n = re.sub(r"^2\.6\. ", "2.5. ", n)
    n = re.sub(r"^6\. ", "5. ", n); n = re.sub(r"^6\.1\. ", "5.1. ", n)
    if n != t:
        r = [r for r in p.runs if t.split(". ")[0] in r.text]
        assert r, t; r[0].text = r[0].text.replace(t.split(" ")[0], n.split(" ")[0], 1)

# ---- 6. bibliografía: fuera la ANSI, que solo citaba el apartado de normas de otros países ----
bib = buscar("BIBLIOGRAFÍA"); el = bib._p.getnext(); k = 0
while el is not None and el.tag == qn("w:p"):
    sig = el.getnext(); p = Paragraph(el, bib._parent)
    if re.match(r"^\d+\. ", p.text):
        if "ANSI" in p.text: el.getparent().remove(el)
        else:
            k += 1; r = p.runs[0]; assert re.match(r"^\d+\. ", r.text), r.text
            r.text = re.sub(r"^\d+\. ", f"{k}. ", r.text, count=1)
    el = sig

# ---- 7. renumeración de ilustraciones y tablas (pies y referencias) ----
RXCAP = re.compile(r"^(Ilustración|Tabla) (\d+)\. ")
mapa = {"Ilustración": {}, "Tabla": {}}; cont = {"Ilustración": 0, "Tabla": 0}
for p in paras():
    m = RXCAP.match(p.text)
    if m:
        tipo, tok = m.group(1), m.group(2); cont[tipo] += 1; mapa[tipo][tok] = cont[tipo]
        if tok != str(cont[tipo]):
            r = [r for r in p.runs if f"{tipo} {tok}." in r.text]; assert r, p.text
            r[0].text = r[0].text.replace(f"{tipo} {tok}.", f"{tipo} {cont[tipo]}.", 1)
RXREF = re.compile(r"\b(Ilustraci(?:ón|ones)|Tablas?)(\s+)(\d+(?:\s*(?:,|y|a|e|–|-)\s*\d+)*)")
problemas = []
def renum(p):
    if p._p.find(".//" + qn("w:tab")) is not None or RXCAP.match(p.text): return
    for r in p.runs:
        def f(m):
            tipo = "Ilustración" if m.group(1).startswith("Ilustraci") else "Tabla"
            def g(t):
                v = mapa[tipo].get(t.group())
                if v is None: problemas.append((tipo, t.group(), p.text[:60])); return t.group()
                return str(v)
            return m.group(1) + m.group(2) + re.sub(r"\d+", g, m.group(3))
        n = RXREF.sub(f, r.text)
        if n != r.text: r.text = n
    # referencia partida entre dos runs
    if re.search(r"(Ilustraci(ón|ones)|Tablas?)\s*$", "".join(r.text for r in p.runs[:-1])): problemas.append(("revisar", p.text[:60]))
for p in d.paragraphs: renum(p)
for tb in d.tables:
    for row in tb.rows:
        for c in row.cells:
            for p in c.paragraphs: renum(p)
print("ilustraciones:", cont["Ilustración"], "tablas:", cont["Tabla"])
print("referencias sin destino:", problemas)
# ---- 8. quitar del archivo las imágenes que ya no se usan ----
usados = set(re.findall(r'r:(?:embed|id|link)="(rId\d+)"', d.element.xml))
quitadas = [rId for rId, rel in list(d.part.rels.items()) if rel.reltype.endswith("/image") and rId not in usados]
for rId in quitadas: d.part.drop_rel(rId)
print("imágenes quitadas del paquete:", len(quitadas))
d.save(F); print("guardado", F)

# Adapta el trabajo al mensaje del profesor (noviembre de 2026):
#  - Etapa inicial: nuevo apartado 1.7 ESTRUCTURA
#  - Etapa de evaluación: ACV con Eco-it (datos de entrada preparados, resultados a completar)
#  - Etapa de realización: planos de conjunto y de fabricación de una pieza
import copy, re
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

F = "Trabajo_Taburete.docx"
d = Document(F)
body = d.element.body

def paras(): return [p for p in d.paragraphs if "\t" not in p.text]
def buscar(ini, estilo=None):
    r = [p for p in paras() if p.text.startswith(ini) and (estilo is None or p.style.name == estilo)]
    assert len(r) == 1, (ini, len(r)); return r[0]

# ---------- escritura con marcadores ⟦ ⟧ = texto resaltado en amarillo ----------
def poner(p, t):
    runs = p.runs
    if not runs: p.add_run(""); runs = p.runs
    base = copy.deepcopy(runs[0]._r)
    for r in runs: r._r.getparent().remove(r._r)
    for k, seg in enumerate(re.split(r"(⟦.*?⟧)", t)):
        if seg == "": continue
        r = copy.deepcopy(base); p._p.append(r)
        for tt in r.findall(qn("w:t")): r.remove(tt)
        for br in r.findall(qn("w:br")) + r.findall(qn("w:drawing")): r.remove(br)
        from docx.text.run import Run
        run = Run(r, p)
        if seg.startswith("⟦"):
            run.text = seg[1:-1]; run.font.highlight_color = WD_COLOR_INDEX.YELLOW
        else:
            run.text = seg
    return p

def clon(plantilla_xml, t, ancla_el, alinear=None):
    n = copy.deepcopy(plantilla_xml); ancla_el.addprevious(n)
    p = Paragraph(n, d._body); poner(p, t)
    if alinear is not None: p.alignment = alinear
    return p

# ---------- plantillas (antes de borrar nada) ----------
cap4 = buscar("4. ETAPA DE EVALUACIÓN", "Heading 1"); cap5 = buscar("5. ETAPA DE REDISEÑO", "Heading 1")
T_NORMAL = copy.deepcopy(buscar("En esta etapa se evalúan las tres alternativas de material mediante")._p)
T_BULLET = copy.deepcopy(buscar("Uso: el producto no consume energía")._p)
T_H2 = copy.deepcopy(buscar("4.1. METODOLOGÍA Y DATOS DEL ANÁLISIS")._p)
T_CONC = copy.deepcopy(buscar("Conclusiones:")._p)
T_CAPT = copy.deepcopy(buscar("Tabla 12. Factores de emisión")._p)
T_CAPI = copy.deepcopy(buscar("Ilustración 17. Huella de carbono")._p)
tfiltro = [t for t in d.tables if t.rows[0].cells[0].text == "Criterio"][0]
TBLPR = copy.deepcopy(tfiltro._tbl.tblPr)

def tabla(filas, anchos, ancla_el):
    t = d.add_table(rows=len(filas), cols=len(anchos))
    t._tbl.remove(t._tbl.tblPr); t._tbl.insert(0, copy.deepcopy(TBLPR))
    for gc, w in zip(t._tbl.tblGrid.findall(qn("w:gridCol")), anchos): gc.set(qn("w:w"), str(int(w * 567)))
    for i, (row, vals) in enumerate(zip(t.rows, filas)):
        for c, w, v in zip(row.cells, anchos, vals):
            tcPr = c._tc.get_or_add_tcPr(); tw = OxmlElement("w:tcW")
            tw.set(qn("w:w"), str(int(w * 567))); tw.set(qn("w:type"), "dxa"); tcPr.append(tw)
            p = c.paragraphs[0]
            if i < len(filas) - 1: p.paragraph_format.keep_with_next = True
            for k, seg in enumerate(re.split(r"(⟦.*?⟧)", v)):
                if not seg: continue
                r = p.add_run(seg[1:-1] if seg.startswith("⟦") else seg); r.font.size = Pt(8.5)
                if seg.startswith("⟦"): r.font.highlight_color = WD_COLOR_INDEX.YELLOW
                if i == 0:
                    r.bold = True; r.font.color.rgb = RGBColor(255, 255, 255)
                if i == len(filas) - 1 and vals[0].startswith(("Resultado", "Total")): r.bold = True
            if i == 0:
                sh = OxmlElement("w:shd"); sh.set(qn("w:val"), "clear"); sh.set(qn("w:color"), "auto"); sh.set(qn("w:fill"), "C0392B"); tcPr.append(sh)
    ancla_el.addprevious(t._tbl); return t

def hueco_captura(texto, ancla_el):
    p = clon(T_NORMAL, "⟦" + texto + "⟧", ancla_el, WD_ALIGN_PARAGRAPH.CENTER)
    p.paragraph_format.space_before = Pt(18); p.paragraph_format.space_after = Pt(18)
    p.paragraph_format.keep_with_next = True
    return p

# =====================================================================
# 1. ETAPA INICIAL: apartado 1.7 ESTRUCTURA
# =====================================================================
cap2 = buscar("2. ETAPA DE INFORMACIÓN", "Heading 1")._p
clon(T_H2, "1.7. ESTRUCTURA", cap2)
clon(T_NORMAL, "La estructura del producto describe cómo se organiza en conjuntos, subconjuntos y piezas, y qué función cumple cada parte. "
     "En la etapa inicial se planteó a nivel de subconjuntos, a partir de las funciones del apartado 1.4: un bastidor portante, unas superficies "
     "de apoyo para el pie, un mecanismo de plegado y bloqueo y unos apoyos antideslizantes. Siguiendo la metodología de ingeniería simultánea, "
     "se ha completado después con las piezas definidas en el diseño del apartado 3.4. El resultado se muestra en la Ilustración §estructura§.", cap2)
pimg = Paragraph(copy.deepcopy(T_NORMAL), d._body); cap2.addprevious(pimg._p)
for r in list(pimg.runs): r._r.getparent().remove(r._r)
pimg.alignment = WD_ALIGN_PARAGRAPH.CENTER; pimg.paragraph_format.keep_with_next = True
pimg.add_run().add_picture("figura_estructura.png", width=Cm(16))
clon(T_CAPI, "Ilustración §estructura§. Árbol de estructura del taburete-escalera: subconjuntos, piezas y funciones. Elaboración propia.", cap2)
clon(T_NORMAL, "La estructura elegida tiene dos ventajas importantes: los dos bastidores y las dos superficies de apoyo son piezas sencillas "
     "de un solo material, y todas las uniones son articulaciones con pasadores desmontables. Esto facilita la reparación, la sustitución de "
     "las piezas de desgaste y la separación de materiales al final de su vida útil (requisitos R15 y R21).", cap2)

# =====================================================================
# 4. ETAPA DE EVALUACIÓN: ACV con Eco-it
# =====================================================================
el = cap4._p.getnext()
while el is not cap5._p:
    sig = el.getnext(); body.remove(el); el = sig
A = cap5._p
X = "⟦[      ]⟧"
clon(T_NORMAL, "En esta etapa se evalúan las tres alternativas de material planteadas en el apartado 3.3. Primero se analiza su impacto "
     "ambiental con un pequeño análisis de ciclo de vida (ACV) realizado con el software Eco-it, visto en las prácticas de la asignatura, y "
     "después se comprueba qué alternativas cumplen las propiedades imprescindibles del EDP para elegir la solución final.", A)
clon(T_NORMAL, "⟦[NOTA, BORRAR ANTES DE ENTREGAR: completa los valores entre corchetes y las capturas con los resultados de Eco-it de las "
     "prácticas. Si Eco-it ordena las alternativas de otra forma, revisa también los comentarios de los apartados 4.2 a 4.5.]⟧", A)
clon(T_H2, "4.1. METODOLOGÍA Y DATOS DEL ANÁLISIS", A)
clon(T_NORMAL, "El ACV se ha realizado con Eco-it, una herramienta de análisis de ciclo de vida simplificado pensada para diseñadores, "
     "siguiendo el enfoque «de la cuna a la tumba» de las normas UNE-EN ISO 14040 y 14044. Los resultados se expresan como huella de carbono, "
     "en kg de CO₂ equivalente. La unidad funcional es un taburete-escalera que permite a un usuario de hasta 150 kg alcanzar 2,30 m de altura "
     "durante 10 años de uso doméstico. En Eco-it el ciclo de vida se divide en tres fases:", A)
clon(T_BULLET, "Producción: materiales y procesos de fabricación de cada pieza, con las masas del modelo de SolidWorks (Tabla 10). Se incluye "
     "también el transporte de distribución hasta el punto de venta: 600 km en camión.", A)
clon(T_BULLET, "Uso: el producto no consume energía; solo se considera la sustitución de los cuatro tacos una vez durante su vida útil.", A)
clon(T_BULLET, "Eliminación: reciclaje del 90 % de los metales (el 10 % restante va a vertedero), incineración de los plásticos y del "
     "caucho, y valorización energética de la madera.", A)
clon(T_NORMAL, "La Tabla §inv§ recoge los datos introducidos en Eco-it para cada alternativa. En la alternativa 2 se ha calculado además "
     "una variante con aluminio reciclado en lugar de primario, para valorar la mejora que se propone en las conclusiones.", A)
inv = [("Elemento", "Alt. 1: acero", "Alt. 2: aluminio + PP", "Alt. 3: madera"),
       ("Largueros delanteros (2)", "Tubo de acero · 2,78 kg", "Aluminio extruido · 0,96 kg", "Haya maciza · 0,71 kg"),
       ("Patas traseras (2)", "Tubo de acero · 2,58 kg", "Aluminio extruido · 0,89 kg", "Haya maciza · 0,66 kg"),
       ("Travesaños (2)", "Tubo de acero · 0,86 kg", "Aluminio extruido · 0,30 kg", "Haya maciza · 0,17 kg"),
       ("Plataforma y peldaño", "Chapa de acero estampada · 2,36 kg", "PP inyectado · 0,66 kg", "Contrachapado · 1,80 kg"),
       ("Bielas y tirantes (4)", "Pletina de acero · 0,39 kg", "Pletina de aluminio · 0,14 kg", "Pletina de acero · 0,39 kg"),
       ("Pasadores (10)", "Acero · 0,18 kg", "Acero · 0,18 kg", "Acero · 0,18 kg"),
       ("Tacos (4)", "Caucho · 0,04 kg", "Caucho · 0,04 kg", "Caucho · 0,04 kg"),
       ("Masa total", "9,20 kg", "3,17 kg", "3,96 kg"),
       ("Transporte (600 km en camión)", "5,52 t·km", "1,90 t·km", "2,37 t·km"),
       ("Uso: tacos de repuesto", "Caucho · 0,04 kg", "Caucho · 0,04 kg", "Caucho · 0,04 kg"),
       ("Eliminación: reciclaje", "Acero · 8,24 kg", "Aluminio · 2,06 kg; acero · 0,16 kg", "Acero · 0,51 kg"),
       ("Eliminación: vertedero", "Acero · 0,92 kg", "Aluminio y acero · 0,25 kg", "Acero · 0,06 kg"),
       ("Eliminación: incineración", "Caucho · 0,08 kg", "PP · 0,66 kg; caucho · 0,08 kg", "Madera · 3,35 kg; caucho · 0,08 kg")]
c = clon(T_CAPT, "Tabla §inv§. Datos introducidos en Eco-it para cada alternativa (masas del modelo de SolidWorks). Elaboración propia.", A)
tabla(inv, [3.7, 4.1, 4.1, 4.1], c._p)
clon(T_NORMAL, "Se trata de un ACV simplificado: no incluye el embalaje, la pintura o el anodizado ni las mermas de fabricación, y las bases "
     "de datos de Eco-it recogen valores medios. Por eso los resultados deben interpretarse de forma comparativa entre alternativas y no como "
     "valores absolutos.", A)

def resultados(clave, filas_cab, anchos):
    filas = [filas_cab] + [(f,) + (X,) * (len(filas_cab) - 1) for f in
                           ("Producción (incluye el transporte)", "Uso", "Eliminación", "Total del ciclo de vida")]
    return filas, anchos

clon(T_H2, "4.2. ALTERNATIVA 1: ACERO", A)
clon(T_NORMAL, f"La Tabla §r1§ y la Ilustración §eco1§ recogen los resultados de Eco-it para la alternativa de acero. La fase de producción "
     f"es la de mayor impacto ({X} kg CO₂-eq de un total de {X} kg CO₂-eq), sobre todo por los largueros, las patas, la plataforma y el "
     f"peldaño, que concentran la mayor parte de los 9,20 kg de acero. El transporte y el uso tienen un peso muy pequeño.", A)
c = clon(T_CAPT, "Tabla §r1§. Resultados de Eco-it de la alternativa 1: acero.", A)
tabla(*resultados("r1", ("Fase", "kg CO₂-eq"), [8.0, 4.0]), c._p)
hueco_captura("[Pegar aquí la captura de los resultados de Eco-it de la alternativa 1]", A)
clon(T_CAPI, "Ilustración §eco1§. Resultados de Eco-it de la alternativa 1: acero.", A)

clon(T_H2, "4.3. ALTERNATIVA 2: ALUMINIO Y POLIPROPILENO", A)
clon(T_NORMAL, f"La alternativa de aluminio es la más ligera, pero el aluminio primario tiene un impacto por kilo muy alto, así que la "
     f"producción vuelve a ser la fase dominante ({X} kg CO₂-eq de un total de {X} kg CO₂-eq). Las piezas que más contribuyen son los "
     f"largueros y las patas traseras, que suman 1,86 de los 2,29 kg de aluminio. La plataforma y el peldaño de polipropileno añaden su parte "
     f"en la producción y en la incineración al final de su vida. Con aluminio reciclado, el total baja a {X} kg CO₂-eq "
     f"(Tabla §r2§ e Ilustración §eco2§).", A)
c = clon(T_CAPT, "Tabla §r2§. Resultados de Eco-it de la alternativa 2: aluminio y polipropileno (kg CO₂-eq).", A)
tabla(*resultados("r2", ("Fase", "Aluminio primario", "Aluminio reciclado"), [7.0, 4.0, 4.0]), c._p)
hueco_captura("[Pegar aquí la captura de los resultados de Eco-it de la alternativa 2]", A)
clon(T_CAPI, "Ilustración §eco2§. Resultados de Eco-it de la alternativa 2: aluminio y polipropileno.", A)

clon(T_H2, "4.4. ALTERNATIVA 3: MADERA", A)
clon(T_NORMAL, f"La madera tiene un impacto de producción por kilo mucho menor que el de los metales, por lo que esta alternativa es la de "
     f"menor impacto total ({X} kg CO₂-eq). Las piezas de acero (bielas, tirantes y pasadores), aunque solo suman 0,57 kg, suponen una parte "
     f"importante de la producción ({X} kg CO₂-eq), como se ve en la Tabla §r3§ y la Ilustración §eco3§.", A)
c = clon(T_CAPT, "Tabla §r3§. Resultados de Eco-it de la alternativa 3: madera.", A)
tabla(*resultados("r3", ("Fase", "kg CO₂-eq"), [8.0, 4.0]), c._p)
hueco_captura("[Pegar aquí la captura de los resultados de Eco-it de la alternativa 3]", A)
clon(T_CAPI, "Ilustración §eco3§. Resultados de Eco-it de la alternativa 3: madera.", A)

clon(T_H2, "4.5. COMPARATIVA Y CONCLUSIONES", A)
clon(T_NORMAL, "La Ilustración §ecocomp§ compara el impacto de las tres alternativas por fase. En las tres la fase de producción es la "
     "dominante, mientras que el transporte y el uso son casi despreciables, algo lógico en un producto que no consume energía. Por tanto, las "
     "decisiones de diseño con más efecto sobre el medio ambiente son la elección del material y la cantidad de material empleado.", A)
hueco_captura("[Gráfico comparativo de las tres alternativas por fase, con los resultados de Eco-it]", A)
clon(T_CAPI, "Ilustración §ecocomp§. Impacto de las tres alternativas por fase del ciclo de vida (Eco-it). Elaboración propia.", A)
clon(T_NORMAL, "Sin embargo, el impacto ambiental no es el único criterio. Antes de elegir, se ha comprobado que cada alternativa cumple "
     "las propiedades imprescindibles del EDP, porque un requisito imprescindible no se puede compensar con una buena nota en otros criterios "
     "(Tabla §filtro§).", A)
filtro = [("Criterio", "Acero", "Aluminio + PP", "Madera"),
          ("Peso total, P5 ≤ 3,5 kg (imprescindible)", "9,20 kg: no cumple", "3,17 kg: cumple", "3,96 kg: no cumple"),
          ("Espesor plegado, P6 ≤ 50 mm", "40 mm: cumple", "40 mm: cumple", "40 mm: cumple"),
          ("Impacto del ciclo de vida, Eco-it (kg CO₂-eq)", X, X, X),
          ("Resistencia a la humedad (cocina y baño)", "Necesita pintura", "Buena (anodizado y PP)", "Necesita barniz"),
          ("Resultado", "Descartada (P5)", "Válida", "Descartada (P5)")]
c = clon(T_CAPT, "Tabla §filtro§. Comprobación de las alternativas frente a las propiedades imprescindibles del EDP. Elaboración propia.", A)
tabla(filtro, [6.0, 3.3, 3.4, 3.3], c._p)
clon(T_CONC, "Conclusiones:", A)
clon(T_BULLET, "Solo la alternativa de aluminio y polipropileno cumple todas las propiedades imprescindibles. La de acero (9,20 kg) y la de "
     "madera (3,96 kg) superan el peso máximo de 3,5 kg de P5, que sale del requisito imprescindible R10 (poder llevarlo con una mano), por lo "
     "que quedan descartadas.", A)
clon(T_BULLET, f"Su punto débil es el impacto del aluminio primario. Por eso se especifica aluminio con alto contenido reciclado: con este "
     f"material, Eco-it da {X} kg CO₂-eq en lugar de {X}, es decir, un {X} % menos.", A)
clon(T_BULLET, "La madera es la alternativa de menor impacto ambiental, pero además de superar el peso, su modelo es una simplificación: usa "
     "listones macizos con la misma sección que los perfiles metálicos (40 × 20 mm), que habría que aumentar para soportar 150 kg, y un vaciado "
     "de la plataforma que no es fabricable en contrachapado. Queda como línea de trabajo futura si se consigue un diseño en madera verificado "
     "por debajo de 3,5 kg.", A)
clon(T_NORMAL, "Por todo ello se elige la alternativa 2, con perfiles de aluminio 6063-T5 reciclado y plataforma y peldaño de polipropileno "
     "reforzado con fibra de vidrio. Es la que se ha modelado en detalle, la que se representa en los planos y sobre la que se aplican las "
     "técnicas de rediseño del apartado 5.", A)

# =====================================================================
# 6. ETAPA DE REALIZACIÓN: planos
# =====================================================================
poner(buscar("6. ANEXOS", "Heading 1"), "6. ETAPA DE REALIZACIÓN")
poner(buscar("Se adjuntan los planos del producto en formato A3"),
      "La etapa de realización recoge la documentación necesaria para fabricar el producto. Se han preparado tres planos en formato A3 "
      "(archivo «Anexo_Planos.pdf»): el plano de conjunto en posición abierta, con la lista de piezas; el conjunto plegado, que muestra el "
      "espesor de 40 mm; y el plano de fabricación del larguero delantero, con su material, tolerancias, acabado y proceso. A continuación se "
      "incluye una reproducción reducida de cada uno.")
for k in (4, 5):
    cp = buscar(f"Plano {k}. "); im = cp._p.getprevious(); body.remove(im); body.remove(cp._p)
poner(buscar("Plano 3. "), "Plano 3. Larguero delantero: plano de fabricación.")
nuevos = {1: "cad/plano1_conjunto_abierto.png", 2: "cad/plano2_conjunto_plegado.png", 3: "cad/plano3_larguero_fabricacion.png"}
for k, f in nuevos.items():
    cp = buscar(f"Plano {k}. "); blip = cp._p.getprevious().findall(".//" + qn("a:blip"))[0]
    d.part.related_parts[blip.get(qn("r:embed"))]._blob = open(f, "rb").read()

# =====================================================================
# Bibliografía: capítulo propio y fuentes del nuevo ACV
# =====================================================================
bib = buscar("Bibliografía"); bib.style = d.styles["Heading 1"]; bib.paragraph_format.page_break_before = True
for ini in ("25. Hammond", "26. UK Government", "27. MITECO", "29. UNE-EN 15804"):
    p = buscar(ini); body.remove(p._p)
iso = buscar("28. UNE-EN ISO 14040")
n = copy.deepcopy(iso._p); iso._p.addnext(n)
poner(Paragraph(n, d._body), "30. PRé Sustainability. Eco-it (EcoIt): software de análisis de ciclo de vida simplificado para diseñadores. Material de prácticas de la asignatura.")
k = 0; el = bib._p.getnext()
while el is not None and el.tag == qn("w:p"):
    p = Paragraph(el, d._body)
    if re.match(r"^\d+\. ", p.text):
        k += 1; poner(p, re.sub(r"^\d+\. ", f"{k}. ", p.text))
    el = el.getnext()

# =====================================================================
# Renumeración de ilustraciones y tablas (pies y referencias en el texto)
# =====================================================================
RXCAP = re.compile(r"^(Ilustración|Tabla) (\d+|§\w+§)\. ")
mapa = {"Ilustración": {}, "Tabla": {}}; cont = {"Ilustración": 0, "Tabla": 0}
for p in paras():
    m = RXCAP.match(p.text)
    if m:
        tipo, tok = m.group(1), m.group(2); cont[tipo] += 1; mapa[tipo][tok] = cont[tipo]
        poner(p, f"{tipo} {cont[tipo]}. " + p.text[m.end():])
RXREF = re.compile(r"\b(Ilustraci(?:ón|ones)|Tablas?)(\s+)((?:\d+|§\w+§)(?:\s*(?:,|y|a|–|-)\s*(?:\d+|§\w+§))*)")
cambios = []
def renum_parrafo(p):
    if "\t" in p.text or RXCAP.match(p.text): return
    for r in p.runs:
        def f(m):
            tipo = "Ilustración" if m.group(1).startswith("Ilustraci") else "Tabla"
            def g(t):
                v = mapa[tipo].get(t.group(), None)
                if v is None: cambios.append(("SIN MAPA", tipo, t.group(), p.text[:60])); return t.group()
                if str(v) != t.group(): cambios.append((tipo, t.group(), v))
                return str(v)
            return m.group(1) + m.group(2) + re.sub(r"\d+|§\w+§", g, m.group(3))
        nuevo = RXREF.sub(f, r.text)
        if nuevo != r.text: r.text = nuevo
for p in d.paragraphs: renum_parrafo(p)
for t in d.tables:
    for row in t.rows:
        for c in row.cells:
            for p in c.paragraphs: renum_parrafo(p)
print("ilustraciones:", cont["Ilustración"], " tablas:", cont["Tabla"])
for c in cambios: print("  ", c)
resto = [p.text[:80] for p in d.paragraphs if "§" in p.text]
print("marcas sin resolver:", resto)
d.save(F); print("guardado")

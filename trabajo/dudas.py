from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
ROJO=RGBColor(0xC0,0x39,0x2B); OSC=RGBColor(0x1F,0x2A,0x36); GRIS=RGBColor(0x6B,0x72,0x80)
COL={"Alto":"C0392B","Medio":"D68910","Bajo":"7F8C8D"}
d=Document()
s=d.sections[0]; s.page_width=Cm(21); s.page_height=Cm(29.7)
for m in ("left_margin","right_margin","top_margin","bottom_margin"): setattr(s,m,Cm(2.5))
st=d.styles["Normal"]; st.font.name="Calibri"; st.font.size=Pt(10.5)
st.element.rPr.rFonts.set(qn("w:eastAsia"),"Calibri")
for h,sz in (("Heading 1",15),("Heading 2",12)):
    d.styles[h].font.color.rgb=OSC; d.styles[h].font.size=Pt(sz); d.styles[h].font.name="Calibri"
def sombrear(c,f):
    p=c._tc.get_or_add_tcPr(); e=OxmlElement("w:shd"); e.set(qn("w:val"),"clear"); e.set(qn("w:color"),"auto"); e.set(qn("w:fill"),f); p.append(e)
def P(t="",b=False,i=False,c=None,size=None,after=4,align=None):
    p=d.add_paragraph(); p.paragraph_format.space_after=Pt(after)
    if align: p.alignment=align
    if t:
        r=p.add_run(t); r.bold=b; r.italic=i
        if c: r.font.color.rgb=c
        if size: r.font.size=Pt(size)
    return p
def campo(p,et,txt):
    r=p.add_run(et+" "); r.bold=True; r.font.color.rgb=OSC; p.add_run(txt)

# ---------------- portada breve ----------------
P("DOCUMENTO INTERNO · NO SE ENTREGA",True,c=ROJO,size=9,after=2)
P("Dudas y decisiones tomadas por intuición",True,c=OSC,size=20,after=2)
P("Trabajo de Ingeniería Simultánea: taburete-escalera plegable · Iván Roig Pérez",c=GRIS,size=10.5,after=12)
P("Durante el trabajo he tenido que tomar muchas decisiones sin un enunciado ni un criterio del profesor que las respaldara. "
  "Aquí están todas las que no puedo justificar del todo: qué decidí, por qué, qué duda me queda y cómo comprobarla. "
  "Están ordenadas por lo que podrían afectar a la nota. Úsalo para preparar la defensa y, si puedes, para preguntar al profesor antes de entregar.")
P("Impacto: Alto = podría cambiar una conclusión o costar bastante nota. Medio = discutible, pero defendible si lo explicas. Bajo = detalle.",i=True,c=GRIS,size=9.5,after=10)

D=[
# (apartado, titulo, impacto, decision, por que, duda, comprobar)
("1. Enfoque general","El ACV está en kg de CO₂ equivalente, no en Ecopuntos (ECO-it)","Alto",
 "Calcular solo la huella de carbono con factores de la base de datos ICE v2.0 (Universidad de Bath) y el módulo D de la norma EN 15804.",
 "No tenía acceso a ECO-it ni a su base de datos, y los kg de CO₂ se pueden calcular y justificar con fuentes públicas.",
 "El temario de la asignatura menciona ECO-it y el Eco-indicador 99. Es muy posible que el profesor espere el ACV hecho con esa herramienta y en milipuntos. La huella de carbono es un indicador válido, pero solo mide el cambio climático; otros impactos (toxicidad, agotamiento de recursos) podrían cambiar el orden entre acero y aluminio.",
 "Pregunta al profesor si acepta kg de CO₂-eq. Si no lo acepta, rehaz las tablas 12 a 14 con ECO-it usando las masas de la Tabla 10: las masas y las fases ya están, solo cambian los factores."),
("4. Evaluación","La alternativa de madera usa la misma geometría que la metálica","Alto",
 "Modelar las tres alternativas con la misma forma y cambiar solo el material, macizando los perfiles en la madera.",
 "Así la comparación del ACV es directa: la única variable es el material.",
 "Un listón de haya macizo de 40 × 20 mm es demasiado esbelto para 150 kg. Una escalera de madera real tendría largueros de unos 20 × 60 mm o más, así que pesaría más de los 3,96 kg calculados y emitiría algo más. La conclusión de que la madera es la mejor opción (Tabla 15) se basa en un peso que probablemente es optimista.",
 "Haz un cálculo rápido a flexión del larguero con 150 kg (o un estudio en SolidWorks Simulation) para cada material y ajusta la sección antes de comparar. Si la madera supera claramente los 3,5 kg, la decisión se inclina hacia el aluminio reciclado."),
("3.4 y 5.2","El taburete modelado no tiene ningún bloqueo en posición abierta","Alto",
 "Dejar el pestillo de seguridad sin modelar y proponerlo como acción del AMFEC.",
 "El mecanismo de plegado ya era bastante complejo y quería asegurar primero que se plegaba sin interferencias.",
 "El mecanismo tiene un solo grado de libertad: sin pestillo, lo único que lo mantendría abierto sería el rozamiento. En el TRIZ (contradicción tercera) digo que el tirante queda «pasado de su punto muerto» y se autobloquea con la carga, pero en el rediseño del apartado 3.4 no he comprobado que eso ocurra con la geometría final. Es el punto técnico más débil del trabajo y el primero que puede preguntar un profesor de mecánica.",
 "Si hay tiempo, modela un pasador con muelle en la articulación de la plataforma. Si no, ten preparada la explicación: un grado de libertad, se bloquea una articulación y se retira el pasador para plegar."),
("3.4","No hay ningún cálculo resistente ni de estabilidad","Alto",
 "Tomar las secciones (tubo de 40 × 20 × 2, pletinas de 20 × 4, pasadores de Ø 8 y plataforma de PP de 3 mm) por comparación con productos del mercado.",
 "La asignatura no pide cálculo estructural y las prácticas de Simulation son opcionales.",
 "No sé si la plataforma de PP de 3 mm, con 350 mm de luz y sin nervios, aguanta 150 kg: casi seguro que no sin nervios. Tampoco he comprobado a cortante los pasadores ni el vuelco lateral con el ensayo de la UNE-EN 14183. En la Tabla 2 (P1 y P2) digo que se superarán los ensayos, pero no está demostrado.",
 "Lo ideal es un estudio estático en SolidWorks Simulation de la plataforma y del larguero con 150 kg (hay una práctica de viga en voladizo que sirve de guía). Como mínimo, menciona en la defensa que es la siguiente fase del diseño de detalle."),
("Estructura","He añadido un capítulo 5 (QFD, AMFEC y análisis del valor) que no está en el índice del profesor","Medio",
 "Añadir las técnicas de rediseño del temario en un capítulo propio.",
 "Están en los apuntes («Técnicas de rediseño») y me pareció que sumaban.",
 "El índice de ejemplo termina en «Evaluación» y «Anexos». Puede que el profesor lo valore, que le dé igual o que prefiera que no se alargue el trabajo. Además, el rediseño está hecho sobre la alternativa de aluminio mientras que la conclusión elige la madera; lo justifico en el texto, pero es discutible.",
 "Pregunta si quiere esas técnicas. Si no las quiere, se puede quitar el capítulo 5 entero sin que se rompa nada (solo habría que actualizar el índice)."),
("4.5","La matriz de decisión es subjetiva","Medio",
 "Pesos de 30 / 25 / 20 / 15 / 10 % y puntuaciones de 1 a 5 puestas por mí.",
 "Es lo habitual en una matriz ponderada y los pesos siguen la importancia del EDP.",
 "A la madera le doy un 4 en peso aunque no cumple P5 (3,96 kg > 3,5 kg). Si le pusiera un 3 y además el peso valiera un 35 % y la huella un 20 %, ganaría el aluminio (3,70 frente a 3,45). Las notas de coste, durabilidad y estética no salen de ningún dato.",
 "En la defensa, explica que la decisión es sensible a los pesos y que por eso se mantiene el aluminio reciclado como alternativa. Si quieres, añade un análisis de sensibilidad (dos o tres combinaciones de pesos)."),
("4.1","Hipótesis del ACV","Medio",
 "600 km de transporte, reciclaje del 90 % de los metales, cambio de tacos una vez en 10 años, incineración de plásticos y valorización de la madera con CO₂ biogénico no contabilizado.",
 "Son valores razonables y habituales en ACV simplificados.",
 "Ninguno está medido. Los factores ICE v2.0 son de 2011. Queda fuera el embalaje, la pintura o el anodizado y las mermas. Separar el módulo D es correcto según la EN 15804, pero si se sumara al total, el acero y el aluminio quedarían más cerca. El orden entre las tres alternativas no cambia en ningún caso, pero las diferencias sí.",
 "Explícalo como ACV comparativo y simplificado (ya está escrito en el apartado 4.1). Si alguien pregunta por el aluminio, la respuesta es el reciclado: con aluminio secundario baja de 27,3 a unos 11,3 kg CO₂-eq."),
("2.4 y normativa","No he tenido acceso al texto de la UNE-EN 14183","Medio",
 "Describir la norma a partir de fuentes secundarias (AFESPO, Test and Research Centre, fichas de fabricantes).",
 "La norma es de pago.",
 "Los detalles (peldaños a distancias iguales, barandilla obligatoria si la plataforma es menor de 24 × 40 cm y está a más de 75 cm, contenido de los ensayos) están sacados de terceros. La mención a la prEN 131-9 como futura norma de taburetes-escalera tampoco la he podido confirmar en el CEN.",
 "Si la biblioteca de la universidad tiene acceso a AENOR, consulta la norma y corrige lo que haga falta. La frase de la prEN 131-9 se puede borrar sin problema."),
("2.5","Estudio de patentes no exhaustivo","Medio",
 "Analizar 4 documentos cercanos y citar 3 más.",
 "El índice pide 4 patentes.",
 "La situación del modelo de utilidad ES 1 070 877 U (caducado) la deduzco de su duración máxima, sin consultarla en el registro de la OEPM. Tampoco he podido confirmar que la patente de Jool no tenga una solicitud europea de la misma familia, porque Espacenet me bloqueó el acceso. Las traducciones de las reivindicaciones son mías.",
 "Consulta la situación en el localizador de la OEPM y la familia de US 12 419 421 en Espacenet («Also published as»). Son 5 minutos."),
("1.3","Altura de 0,48 m a partir de un alcance de 1,24 veces la estatura","Medio",
 "Usar la usuaria de percentil 5 (1,49 m) y un alcance de 1,24 × estatura para llegar a 2,30 m.",
 "Da un valor que coincide con los productos de referencia (Hailo K20: 46 cm).",
 "El factor 1,24 es una aproximación mía, no un dato de la tabla del INSHT. Los datos del INSHT son de 1999 y de población laboral (18 a 65 años), justo cuando digo que el producto está pensado también para personas mayores, que son más bajas. El objetivo de 2,30 m también lo fijé yo.",
 "Si en clase habéis usado otra tabla de alcance vertical, cambia el factor. Si el resultado sigue entre 0,45 y 0,50 m, el diseño no cambia."),
("2.1","Costes y márgenes inventados","Medio",
 "Margen de la distribución del 38 %, margen del fabricante del 25 %, serie de 20.000 unidades al año y un reparto del coste industrial.",
 "Son hipótesis habituales y quedan marcadas como tales.",
 "No hay datos reales detrás. Los costes por componente del análisis del valor también son estimados, y su suma (13,46 €) supera lo previsto (12,50 €); lo he dejado escrito como hallazgo, no lo he escondido.",
 "Defiéndelo como estimación de orden de magnitud. Si en clase dieron márgenes típicos, usa esos."),
("3.2","Elección de parámetros TRIZ","Bajo",
 "Contradicciones 14/1, 33/27 y 13/7, con las celdas de la matriz de triz40.com.",
 "Son las que mejor describen el problema.",
 "Hay varias versiones de la matriz y otra persona podría elegir otros parámetros (por ejemplo, 10 fuerza en lugar de 14 resistencia). El principio 8 (contrapeso) lo aplico de forma algo forzada.",
 "Comprueba que las celdas coinciden con la matriz de los apuntes. Si alguna no coincide, cambia los principios de la lista."),
("5","QFD y AMFEC sin datos de clientes ni de ensayos","Bajo",
 "Importancias, relaciones, percepción de la competencia y valores O, G y D puestos por mí.",
 "Es un trabajo académico sin encuestas ni prototipo.",
 "Los resultados (por ejemplo, que el peso sea lo más importante con un 15,7 %) salen de mis propias puntuaciones, así que en parte confirman lo que yo ya pensaba.",
 "Admítelo si te preguntan: en un proyecto real se harían encuestas a usuarios y ensayos de prototipos."),
("3.4","Materiales de SolidWorks aproximados","Bajo",
 "PP copolímero en lugar de PP con 30 % de fibra de vidrio, haya en lugar de contrachapado en la plataforma y acero al carbono no aleado en lugar de S235.",
 "Son los que había en la biblioteca de SolidWorks en español.",
 "Las masas cambian poco (unos 170 g en el PP, ya indicado en el texto), pero el ACV usa el factor del contrachapado con la masa calculada con la densidad de la haya.",
 "Si quieres afinar, crea materiales personalizados en SolidWorks con la densidad correcta."),
("2.2","Datos de mercado","Bajo",
 "Precios y características tomados de webs de tiendas en septiembre de 2026.",
 "No hay otra fuente.",
 "El precio del IKEA BOLMEN (1,50 €) me parece demasiado bajo y no lo he podido volver a comprobar. Varios pesos figuran como «n. d.».",
 "Mira el precio actual en ikea.es y corrígelo en la Tabla 4 (y en la Ilustración 5 si cambia mucho)."),
("Anexos","Planos generados por programa, no desde SolidWorks","Bajo",
 "Dibujar los planos proyectando el modelo en Python, con cajetín propio y en primer diedro.",
 "Así quedaban completos y coherentes con el modelo.",
 "Les faltan tolerancias, acabados superficiales y algunas cotas de detalle, y el estilo no es el de un dibujo de SolidWorks. Si el profesor pide los .SLDDRW, no los tienes.",
 "Si te los piden, usa la macro de planos (cad/Planos_macro_para_copiar.txt) y añade las cotas a mano."),
("2.10","Embalaje y paletización","Bajo",
 "Caja de 880 × 470 × 60 mm y 39 unidades por palé, de canto.",
 "Sale del tamaño plegado medido en el modelo (861 × 450 × 40 mm).",
 "En la versión anterior la caja medía 640 mm, un error que he corregido en esta revisión. No he contado cantoneras ni el grosor real del cartón.",
 "Nada que hacer; solo tenlo en cuenta si comparas con una versión antigua del documento."),
]
# tabla resumen
P("Resumen",True,c=OSC,size=13,after=4)
t=d.add_table(rows=1,cols=3); t.alignment=WD_TABLE_ALIGNMENT.CENTER; t.style="Table Grid"
for c,h in zip(t.rows[0].cells,("Nº","Duda","Impacto")):
    c.text=""; r=c.paragraphs[0].add_run(h); r.bold=True; r.font.color.rgb=RGBColor(255,255,255); r.font.size=Pt(9.5); sombrear(c,"1F2A36")
for i,(ap,ti,imp,*_) in enumerate(D,1):
    row=t.add_row().cells
    for c,v in zip(row,(str(i),f"{ti} ({ap})",imp)):
        c.text=""; r=c.paragraphs[0].add_run(v); r.font.size=Pt(9.5)
    row[2].paragraphs[0].runs[0].bold=True; row[2].paragraphs[0].runs[0].font.color.rgb=RGBColor(255,255,255); sombrear(row[2],COL[imp])
t.autofit=False
for gc,w in zip(t._tbl.tblGrid.findall(qn("w:gridCol")),(1.0,13.0,2.0)): gc.set(qn("w:w"),str(int(w*567)))
for row in t.rows:
    for c,w in zip(row.cells,(1.0,13.0,2.0)): c.width=Cm(w)
P("",after=6)
d.add_page_break()
for i,(ap,ti,imp,dec,porq,duda,comp) in enumerate(D,1):
    h=d.add_heading(level=2); r=h.add_run(f"{i}. {ti}"); 
    p=P(after=4); r=p.add_run(f" IMPACTO {imp.upper()} "); r.bold=True; r.font.size=Pt(8.5); r.font.color.rgb=RGBColor(255,255,255)
    rpr=r._r.get_or_add_rPr(); sh=OxmlElement("w:shd"); sh.set(qn("w:val"),"clear"); sh.set(qn("w:color"),"auto"); sh.set(qn("w:fill"),COL[imp]); rpr.append(sh)
    r=p.add_run(f"   Apartado: {ap}"); r.font.size=Pt(9); r.font.color.rgb=GRIS
    for et,txt in (("Qué decidí:",dec),("Por qué:",porq),("Qué duda me queda:",duda),("Cómo comprobarlo:",comp)):
        campo(P(after=3),et,txt)
    P("",after=4)
d.add_heading("Consejo final para la defensa",level=1)
P("Las dudas de impacto alto (1 a 4) son las que un profesor de Ingeniería Mecánica puede ver con más facilidad. No hace falta resolverlas todas; basta con que las conozcas y sepas explicar por qué se tomó esa decisión y cuál sería el siguiente paso. Decir «esto no está verificado y se comprobaría así» suele puntuar mejor que dar un dato que luego no sabes justificar.")
P("Recuerda también que todo el trabajo tiene que poder defenderlo quien lo firma. Repasa los cálculos del ACV, la cinemática del plegado y la matriz de decisión hasta que puedas explicarlos sin el documento delante.")
d.save("Dudas_y_decisiones.docx"); print(len(D),"dudas")

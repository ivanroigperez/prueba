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
("4","El ACV se tiene que hacer con Eco-it y los resultados están pendientes","Alto",
 "Rehacer el capítulo 4 en el formato de Eco-it: método, datos de entrada (Tabla 12), comentarios y conclusiones ya escritos, con los resultados y las capturas en amarillo.",
 "El profesor pide en el aula virtual «un pequeño ACV del producto usando el software Eco-it». Mi cálculo anterior con factores ICE no vale como resultado, porque no está hecho con Eco-it; lo he dejado solo en la guía para detectar errores.",
 "No sé qué método usaréis en Eco-it (huella de carbono o Eco-indicador 99), en qué fase se mete el transporte ni los nombres exactos de los materiales de su base de datos. Los comentarios del capítulo 4 dan por hecho que la producción es la fase dominante y que la madera es la de menor impacto; es casi seguro, pero hay que confirmarlo.",
 "En la práctica de Eco-it, siguiendo la Guía Eco-it. Después, rellena los huecos amarillos o pásame los resultados y lo completo yo."),
("1.7","Qué entiende el profesor por «estructura»","Medio",
 "Añadir el apartado 1.7 con el árbol de estructura del producto: conjunto, subconjuntos, piezas y la función de cada parte.",
 "El mensaje del profesor incluye «estructura» en la fase inicial, y el índice de ejemplo habla de «estructura de descomposición del producto».",
 "Ya no tengo los PDF de los apuntes para comprobar la definición exacta. Puede referirse a la estructura funcional (cómo se relacionan las funciones) y no a la estructura física de piezas. Confianza: alrededor del 70 %.",
 "Mira en los apuntes de Metodologías cómo definen «estructura» en la etapa inicial. Si es la estructura funcional, avísame y lo adapto (el árbol de funciones del 1.4 ya cubre parte)."),
("4.5","Decisión final: aluminio reciclado (antes era la madera)","Medio",
 "Aplicar primero un filtro de requisitos imprescindibles (Tabla 16). El acero y la madera no cumplen P5 y quedan descartados, así que se elige el aluminio reciclado.",
 "Otra revisión detectó que la versión anterior elegía la madera, que pesa 3,96 kg, y que la matriz le daba un 4 en peso. Con un 1 en peso ganaba el aluminio. Ahora la conclusión coincide con el modelo, los planos y el capítulo 5.",
 "La madera queda descartada por un peso calculado con una sección simplificada. Puede que un diseño de madera bien hecho también cumpla, pero no está demostrado.",
 "Si te preguntan por qué no la madera: incumple un requisito imprescindible y su modelo no está verificado. Queda como línea futura."),
("3.5","Comprobaciones por cálculo manual","Medio",
 "Añadir el apartado 3.5 con cálculos sencillos: flexión y pandeo del larguero, plataforma, pasadores, vuelco y mecanismo.",
 "No había ninguna comprobación de P1, P2 ni R3.",
 "Los cálculos son simplificados (viga biapoyada, carga estática de 150 kg, coeficiente de seguridad de 2) y no sustituyen a un estudio por elementos finitos ni a los ensayos de la norma. La plataforma y el peldaño cumplen por poco (coeficiente de seguridad 2,0) y el peso final estimado (3,46 kg) apenas cumple P5. Los nervios no están dibujados en el modelo ni en los planos.",
 "Si quieres reforzarlo, haz un estudio estático de la plataforma en SolidWorks Simulation."),
("3.5 y 5.2","El pestillo está dimensionado pero no modelado","Medio",
 "Calcular con el modelo cinemático cómo actúa el peso del usuario y dimensionar el pestillo en la articulación del peldaño.",
 "El cálculo demuestra que el peso sobre el peldaño tiende a cerrar el taburete, así que el pestillo es imprescindible.",
 "El pestillo sigue sin estar en el modelo 3D ni en los planos.",
 "Explícalo como diseño de detalle pendiente. Los números (522 N·m y unos 710 N por pasador) están en la Tabla 11."),
("5","El capítulo 5 (QFD, AMFEC y análisis del valor) no lo pide el profesor","Medio",
 "Mantener las técnicas de rediseño como capítulo 5, entre la evaluación y la realización.",
 "Son materia del curso (apuntes de Técnicas de rediseño) y el capítulo está completo.",
 "El mensaje del profesor enumera las fases inicial, de información, técnico-creativa, de evaluación y de realización; el rediseño no aparece. Puede valorarlo, ignorarlo o preferir un trabajo más corto.",
 "Si quieres quitarlo, se elimina el capítulo 5 entero y hay que cambiar tres frases que lo citan (en el 2.1, el 3.4 y el final del 4.5). Dímelo y lo hago."),
("5.2","El AMFEC no calcula la criticidad (G × O)","Bajo",
 "Usar solo el IPR = O × G × D.",
 "Es lo único que definen los apuntes de Técnicas de rediseño; la palabra «criticidades» solo aparece en el nombre de la técnica.",
 "Otra revisión lo señaló como fallo. Según tus apuntes no lo es, pero algunos profesores lo piden.",
 "Si quieres cubrirte, añade una columna G × O a la Tabla 17. Son 8 multiplicaciones."),
("4.1","Hipótesis del ACV","Medio",
 "600 km de transporte en camión, reciclaje del 90 % de los metales, cambio de tacos una vez en 10 años, incineración de plásticos y valorización energética de la madera.",
 "Son valores razonables y habituales en ACV simplificados, y se pueden meter tal cual en Eco-it.",
 "Ninguno está medido. Además, el ACV no incluye el embalaje, la pintura o el anodizado ni las mermas de fabricación (ya está dicho en el 4.1).",
 "Si en la práctica el profesor da otros escenarios (por ejemplo, otro porcentaje de reciclaje o un escenario de residuos urbanos de Eco-it), usa los suyos y cambia la frase del 4.1."),
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
("6","Tres planos, generados por programa y no desde SolidWorks","Bajo",
 "Dejar tres planos: conjunto abierto con lista de piezas, conjunto plegado y plano de fabricación del larguero delantero (con material, tolerancias, acabado y proceso).",
 "El profesor pide dos planos, uno de conjunto y otro de detalle o fabricación de una pieza. He quitado los de plataforma y peldaño y de piezas varias: no hacían falta y el de la plataforma no mostraba los nervios del apartado 3.5.",
 "Están dibujados proyectando el modelo con un programa, no con SolidWorks. Si el profesor pide los archivos de dibujo de SolidWorks, no los tienes.",
 "Si te los piden, usa la macro de planos (cad/Planos_macro_para_copiar.txt): crea más hojas de las necesarias; quédate con la de conjunto y añade las cotas a mano."),
("2.10","Embalaje y paletización","Bajo",
 "Caja de 880 × 470 × 60 mm y 39 unidades por palé, de canto.",
 "Sale del tamaño plegado medido en el modelo (861 × 450 × 40 mm).",
 "En la versión anterior la caja medía 640 mm, un error que he corregido en esta revisión. No he contado cantoneras ni el grosor real del cartón.",
 "Nada que hacer; solo tenlo en cuenta si comparas con una versión antigua del documento."),
]
D.sort(key=lambda x:{"Alto":0,"Medio":1,"Bajo":2}[x[2]])
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
P("La duda de impacto alto (el ACV con Eco-it) es la única que puede dejar incompleta una parte obligatoria: resuélvela en la práctica. Las de impacto medio son las que un profesor de Ingeniería Mecánica puede ver con más facilidad. No hace falta resolverlas todas; basta con que las conozcas y sepas explicar por qué se tomó esa decisión y cuál sería el siguiente paso. Decir «esto no está verificado y se comprobaría así» suele puntuar mejor que dar un dato que luego no sabes justificar.")
P("Recuerda también que todo el trabajo tiene que poder defenderlo quien lo firma. Repasa los cálculos del ACV, la cinemática del plegado y la matriz de decisión hasta que puedas explicarlos sin el documento delante.")
d.save("Dudas_y_decisiones.docx"); print(len(D),"dudas")

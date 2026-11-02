from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
ROJO=RGBColor(0xC0,0x39,0x2B); OSC=RGBColor(0x1F,0x2A,0x36); GRIS=RGBColor(0x6B,0x72,0x80)
d=Document()
s=d.sections[0]; s.page_width=Cm(21); s.page_height=Cm(29.7)
for m in ("left_margin","right_margin","top_margin","bottom_margin"): setattr(s,m,Cm(2.2))
st=d.styles["Normal"]; st.font.name="Calibri"; st.font.size=Pt(10.5); st.element.rPr.rFonts.set(qn("w:eastAsia"),"Calibri")
for h,sz in (("Heading 1",14),("Heading 2",12)):
    d.styles[h].font.color.rgb=OSC; d.styles[h].font.size=Pt(sz); d.styles[h].font.name="Calibri"
def P(t="",b=False,i=False,c=None,size=None,after=4):
    p=d.add_paragraph(); p.paragraph_format.space_after=Pt(after)
    if t:
        r=p.add_run(t); r.bold=b; r.italic=i
        if c: r.font.color.rgb=c
        if size: r.font.size=Pt(size)
    return p
def B(t): p=d.add_paragraph(t,style="List Bullet"); p.paragraph_format.space_after=Pt(2); return p
def N(t): p=d.add_paragraph(t,style="List Number"); p.paragraph_format.space_after=Pt(2); return p
def sombrear(c,f):
    p=c._tc.get_or_add_tcPr(); e=OxmlElement("w:shd"); e.set(qn("w:val"),"clear"); e.set(qn("w:color"),"auto"); e.set(qn("w:fill"),f); p.append(e)
def tabla(filas,anchos,fases=()):
    t=d.add_table(rows=len(filas),cols=len(anchos)); t.style="Table Grid"; t.alignment=WD_TABLE_ALIGNMENT.CENTER; t.autofit=False
    for gc,w in zip(t._tbl.tblGrid.findall(qn("w:gridCol")),anchos): gc.set(qn("w:w"),str(int(w*567)))
    for i,(row,vals) in enumerate(zip(t.rows,filas)):
        for c,w,v in zip(row.cells,anchos,vals):
            c.width=Cm(w); c.text=""; r=c.paragraphs[0].add_run(v); r.font.size=Pt(9)
            if i==0: r.bold=True; r.font.color.rgb=RGBColor(255,255,255); sombrear(c,"1F2A36")
            elif vals[0] in fases: r.bold=True; sombrear(c,"F3F4F6")
    P("",after=6); return t

P("DOCUMENTO INTERNO · NO SE ENTREGA",True,c=ROJO,size=9,after=2)
P("Guía para hacer el ACV con Eco-it",True,c=OSC,size=20,after=2)
P("Trabajo de Ingeniería Simultánea: taburete-escalera plegable · Iván Roig Pérez",c=GRIS,after=10)

d.add_heading("1. Qué hay que hacer",level=1)
P("El profesor pide «un pequeño ACV del producto usando el software Eco-it». Yo no puedo ejecutar Eco-it, así que el capítulo 4 del trabajo "
  "ya tiene escrito todo lo demás (método, datos de entrada, comentarios y conclusiones) y deja en amarillo los huecos para los resultados. "
  "En la práctica del martes solo tienes que:")
N("Crear en Eco-it las tres alternativas con los datos de las tablas de esta guía (si vas justo, como mínimo la alternativa 2).")
N("En la alternativa 2, guardar una copia cambiando el aluminio primario por aluminio reciclado (es la variante de las conclusiones).")
N("Hacer una captura de la pantalla de resultados de cada alternativa y anotar el valor de cada fase: producción, uso y eliminación.")
N("Pegar las capturas y los valores en los huecos amarillos del capítulo 4 (o pasármelos y lo completo yo, junto con el gráfico comparativo).")
P("Si el profesor dice que basta con el producto final, haz solo la alternativa 2 con su variante de aluminio reciclado y avísame: quito los "
  "apartados 4.2 y 4.4 y adapto la comparativa.",i=True,c=GRIS)

d.add_heading("2. Antes de empezar",level=1)
B("Método de cálculo: si Eco-it deja elegir, usa la huella de carbono (kg CO₂-eq), que es lo que usa el índice de ejemplo del profesor. Si en clase "
  "usáis el Eco-indicador 99 (resultados en puntos o milipuntos), apunta los valores en esas unidades y dímelo para cambiar «kg CO₂-eq» en el texto.")
B("Nombres de los materiales: los de las tablas son genéricos. En Eco-it elige el material o proceso más parecido de su base de datos "
  "(por ejemplo, «aluminio primario» y «extrusión de aluminio»).")
B("Unidades: Eco-it trabaja en kg y en t·km. Todas las cantidades de esta guía ya están en esas unidades.")
B("El transporte de distribución (600 km en camión) se mete en la fase de producción, como dice el apartado 4.1. Si en clase lo ponéis en otra fase, "
  "cambia la frase del 4.1 y el nombre de la fila «Producción (incluye el transporte)».")
B("Si Eco-it permite dividir el producto en partes, crea una parte por cada fila de la tabla de producción: así podrás sacar el gráfico de "
  "impacto por componente, como en el índice de ejemplo.")

FASES=("PRODUCCIÓN","TRANSPORTE (dentro de producción)","USO","ELIMINACIÓN")
d.add_heading("3. Alternativa 2: aluminio y polipropileno (la elegida)",level=1)
tabla([("Fase / elemento","Material o proceso en Eco-it","Cantidad"),
       ("PRODUCCIÓN","",""),
       ("Largueros delanteros (2)","Aluminio primario + extrusión de aluminio","0,963 kg"),
       ("Patas traseras (2)","Aluminio primario + extrusión de aluminio","0,893 kg"),
       ("Travesaños (2)","Aluminio primario + extrusión de aluminio","0,299 kg"),
       ("Bielas y tirantes (4)","Aluminio primario + extrusión de aluminio","0,136 kg"),
       ("Plataforma","Polipropileno (PP) + moldeo por inyección","0,363 kg"),
       ("Peldaño","Polipropileno (PP) + moldeo por inyección","0,297 kg"),
       ("Pasadores (10)","Acero","0,176 kg"),
       ("Tacos (4)","Caucho","0,042 kg"),
       ("TRANSPORTE (dentro de producción)","",""),
       ("Distribución, 600 km","Camión","1,90 t·km"),
       ("USO","",""),
       ("Tacos de repuesto (4)","Caucho","0,042 kg"),
       ("ELIMINACIÓN","",""),
       ("Metales reciclados (90 %)","Reciclaje de aluminio / reciclaje de acero","2,063 kg / 0,158 kg"),
       ("Metales a vertedero (10 %)","Vertedero","0,247 kg"),
       ("Plástico","Incineración de PP","0,660 kg"),
       ("Caucho (original y repuesto)","Incineración","0,083 kg")],[5.0,8.2,3.4],FASES)
P("Variante con aluminio reciclado: copia el producto y cambia «aluminio primario» por «aluminio reciclado» en las cuatro primeras filas "
  "(2,291 kg en total). Lo demás no cambia.",i=True)

d.add_heading("4. Alternativa 1: acero",level=1)
tabla([("Fase / elemento","Material o proceso en Eco-it","Cantidad"),
       ("PRODUCCIÓN","",""),
       ("Largueros delanteros (2)","Acero + conformado de tubo","2,782 kg"),
       ("Patas traseras (2)","Acero + conformado de tubo","2,580 kg"),
       ("Travesaños (2)","Acero + conformado de tubo","0,865 kg"),
       ("Plataforma y peldaño","Chapa de acero + estampación o doblado","2,359 kg"),
       ("Bielas y tirantes (4)","Acero","0,394 kg"),
       ("Pasadores (10)","Acero","0,176 kg"),
       ("Tacos (4)","Caucho","0,042 kg"),
       ("TRANSPORTE (dentro de producción)","",""),
       ("Distribución, 600 km","Camión","5,52 t·km"),
       ("USO","",""),
       ("Tacos de repuesto (4)","Caucho","0,042 kg"),
       ("ELIMINACIÓN","",""),
       ("Acero reciclado (90 %)","Reciclaje de acero","8,241 kg"),
       ("Acero a vertedero (10 %)","Vertedero","0,916 kg"),
       ("Caucho (original y repuesto)","Incineración","0,083 kg")],[5.0,8.2,3.4],FASES)

d.add_heading("5. Alternativa 3: madera",level=1)
tabla([("Fase / elemento","Material o proceso en Eco-it","Cantidad"),
       ("PRODUCCIÓN","",""),
       ("Largueros delanteros (2)","Madera dura (haya), aserrada","0,712 kg"),
       ("Patas traseras (2)","Madera dura (haya), aserrada","0,661 kg"),
       ("Travesaños (2)","Madera dura (haya), aserrada","0,172 kg"),
       ("Plataforma y peldaño","Contrachapado","1,801 kg"),
       ("Bielas y tirantes (4)","Acero","0,394 kg"),
       ("Pasadores (10)","Acero","0,176 kg"),
       ("Tacos (4)","Caucho","0,042 kg"),
       ("TRANSPORTE (dentro de producción)","",""),
       ("Distribución, 600 km","Camión","2,37 t·km"),
       ("USO","",""),
       ("Tacos de repuesto (4)","Caucho","0,042 kg"),
       ("ELIMINACIÓN","",""),
       ("Madera","Incineración con recuperación de energía","3,346 kg"),
       ("Acero reciclado (90 %)","Reciclaje de acero","0,513 kg"),
       ("Acero a vertedero (10 %)","Vertedero","0,057 kg"),
       ("Caucho (original y repuesto)","Incineración","0,083 kg")],[5.0,8.2,3.4],FASES)

d.add_heading("6. Dónde va cada resultado en el Word",level=1)
tabla([("Resultado de Eco-it","Dónde va en el capítulo 4"),
       ("Valores por fase de la alternativa 1","Tabla 13 y texto del apartado 4.2"),
       ("Valores por fase de la alternativa 2 (primario y reciclado)","Tabla 14, texto del 4.3 y segunda conclusión del 4.5"),
       ("Valores por fase de la alternativa 3","Tabla 15 y texto del 4.4"),
       ("Captura de resultados de cada alternativa","Ilustraciones 18, 19 y 20 (huecos amarillos)"),
       ("Totales de las tres alternativas","Fila «Impacto del ciclo de vida» de la Tabla 16"),
       ("Gráfico comparativo por fases","Ilustración 21 (si me pasas los valores, lo hago yo)")],[8.3,8.3])
P("Al terminar, borra la nota amarilla del principio del capítulo 4 y comprueba que no queda ningún hueco amarillo (Ctrl+B y busca «[»).",i=True)

d.add_heading("7. Comprobación rápida de errores",level=1)
P("Antes de Eco-it hice una estimación con otra base de datos (factores ICE de la Universidad de Bath). No sirve como resultado, porque el profesor "
  "pide Eco-it, pero sí para detectar errores al meter los datos:")
tabla([("Alternativa","Estimación previa (kg CO₂-eq)"),
       ("1. Acero","≈ 14"),("2. Aluminio + PP (aluminio primario)","≈ 27"),("2. Con aluminio reciclado","≈ 11"),("3. Madera","≈ 3")],[9.0,7.6])
B("Diferencias de hasta un 50 % son normales: las bases de datos no son iguales.")
B("Si un resultado sale unas 1.000 veces mayor o menor, casi seguro que has metido gramos en lugar de kilos (o kg en lugar de t·km en el transporte).")
B("Lo que sí debería salir igual: la producción es la fase con más impacto en las tres alternativas y el uso es casi nulo. Si Eco-it dice otra "
  "cosa, revisa los datos o avísame, porque habría que cambiar los comentarios del capítulo.")
d.save("Guia_EcoIt.docx"); print("ok")

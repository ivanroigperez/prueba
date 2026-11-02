# Segunda pasada de la reescritura: repeticiones y frases largas. Busca cada párrafo por el inicio de su texto.
import copy, re, sys
from lxml import etree
DIR = sys.argv[1]
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
XMLNS = "{http://www.w3.org/XML/1998/namespace}"
X = "⟦[      ]⟧"
C = [
("Se busca un aspecto sencillo", "Se busca un aspecto sencillo y actual, con líneas limpias y colores neutros (blanco, gris antracita o acabado madera). Así el taburete no desentona si se queda a la vista en la cocina o en el salón. Tiene que transmitir robustez, y el usuario debe ver antes de subirse que es firme y que está bien bloqueado. Las indicaciones de uso y la carga máxima se deben leer con claridad sin recargar el diseño."),
("El fallo más crítico", "El fallo más crítico es el desbloqueo con el usuario encima (IPR = 150), por su gravedad máxima, seguido de las articulaciones y de los tacos antideslizantes. Las acciones propuestas, en especial un pestillo de doble gesto y un indicador visual de bloqueo como el de la patente US 6 966 404, bajan todos los IPR por debajo de 100. El más alto queda en 48."),
("Principio 17, otra dimensión", "Principio 17, otra dimensión: que el pestillo de seguridad se accione en dirección perpendicular al movimiento de plegado, con un deslizador lateral. Un golpe o una carga en el sentido de cierre no puede soltarlo."),
("El análisis del valor compara", "El análisis del valor compara la importancia que da el cliente a cada función con lo que cuesta cumplirla. Sirve para encontrar funciones en las que se gasta más de lo que el cliente valora, o al revés. El coste de cada componente se ha estimado a partir del coste industrial objetivo del apartado 2.1 (Tabla 18) y se ha repartido entre las funciones a las que contribuye. La importancia de cada función sale del QFD y del EDP (Ilustración 23)."),
("No. Tampoco tiene efectos", "No. Tampoco tiene efectos en España y ha expirado. Aporta dos ideas útiles, el asa formada por aberturas en la plataforma y el indicador visual de bloqueo. Este indicador responde a la función comunicativa “dejar claro cómo se abre y cuándo está bien bloqueado” del apartado 1.4."),
("Taburete plegable cuya plataforma", "Taburete plegable cuya plataforma se divide en dos mitades unidas por una bisagra. Tiene un mecanismo de bloqueo a prueba de niños con dos deslizadores, uno en cada lado de la plataforma. Hay que accionarlos a la vez para liberar dos pestillos con muelle y poder plegarlo. Con este sistema un niño no puede cerrarlo y pillarse los dedos. Incluye agarres antideslizantes sobremoldeados y un asa integrada que queda oculta cuando el taburete está en uso."),
("Estas comprobaciones obligan", "Estas comprobaciones obligan a usar polipropileno con fibra de vidrio, tres nervios en la plataforma y en el peldaño y casquillos en los taladros. Con estos cambios la masa estimada de la alternativa 2 sube de 3,17 a unos 3,46 kg y sigue cumpliendo P5, con poco margen. Si el prototipo pesara más, la pared de los largueros y las patas se puede bajar a 1,5 mm, con un ahorro de unos 0,44 kg. Con esa pared la tensión sería de 29 MPa y el coeficiente de seguridad, de 5."),
("Sobre la solución elegida", "Sobre la solución elegida, la alternativa 2, se han aplicado las técnicas de rediseño de la asignatura (QFD, AMFEC y análisis del valor). Sirven para detectar sus puntos débiles y proponer mejoras antes de fabricar prototipos."),
("La madera tiene un impacto de producción", f"La madera tiene un impacto de producción por kilo mucho menor que el de los metales. Esta alternativa es la de menor impacto total, con {X} kg CO₂-eq (Tabla 15 e Ilustración 20). Las piezas de acero (bielas, tirantes y pasadores) solo suman 0,57 kg y aun así suponen una parte importante de la producción, con {X} kg CO₂-eq."),
("La estructura describe", "La estructura describe cómo se organiza el producto en conjuntos, subconjuntos y piezas, y qué función cumple cada parte. En la etapa inicial se planteó a partir de las funciones del apartado 1.4. Constaba de un bastidor portante, unas superficies de apoyo para el pie, un mecanismo de plegado y bloqueo y unos apoyos antideslizantes. Después se completó con las piezas del diseño del apartado 3.4, en el que el bastidor se dividió en delantero y trasero (Ilustración 5)."),
("Principio 8, contrapeso: sin aplicación", "Principio 8, contrapeso: sin aplicación directa. En el boceto se pensó en que el peso del usuario mantuviera el taburete abierto. Eso depende de la geometría del mecanismo respecto al punto muerto, que se estudia en el apartado 3.5."),
("El modelo de SolidWorks 2026", "El modelo de SolidWorks 2026 tiene diez piezas y dos ensamblajes, abierto y plegado (Ilustraciones 15 a 17). Las piezas son el larguero delantero, la pata trasera, el travesaño del asidero, el travesaño trasero, la plataforma, el peldaño, la biela de la plataforma, el tirante del peldaño, el pasador y el taco. Cada pieza tiene una configuración por alternativa de material (ALT1_ACERO, ALT2_ALUMINIO y ALT3_MADERA), en la que cambian el material y, si hace falta, la geometría. En madera los perfiles son macizos y la pared de la plataforma y el peldaño es de 15 mm, frente a 1,2 mm en acero y 3 mm en polipropileno."),
("El coste industrial se ha repartido", "El coste industrial se ha repartido en unos 8,50 € de materiales, 4,00 € de transformación (corte, doblado, inyección y acabado) y 1,50 € de montaje. El embalaje supone 1,00 € y los gastos generales y la amortización de utillajes, 2,30 €. Los márgenes son hipótesis habituales del sector. El reparto por componente se ha revisado en el análisis del valor (apartado 5.3) con las masas del modelo de SolidWorks."),
]
tree = etree.parse(f"{DIR}/word/document.xml"); body = tree.getroot().find(W + "body")
texto = lambda p: "".join(t.text or "" for t in p.iter(W + "t"))
def escribir(p, nuevo):
    runs = [r for r in p if r.tag == W + "r"]
    base = next((r for r in runs if r.find(f"{W}rPr/{W}highlight") is None), runs[0] if runs else None)
    marcado = next((r for r in runs if r.find(f"{W}rPr/{W}highlight") is not None), None)
    for r in runs: p.remove(r)
    for seg in re.split(r"(⟦.*?⟧)", nuevo):
        if not seg: continue
        hl = seg.startswith("⟦"); modelo = marcado if (hl and marcado is not None) else base
        r = etree.SubElement(p, W + "r")
        if modelo is not None and modelo.find(W + "rPr") is not None:
            rpr = copy.deepcopy(modelo.find(W + "rPr"))
            if not hl:
                for h in rpr.findall(W + "highlight"): rpr.remove(h)
            r.append(rpr)
        t = etree.SubElement(r, W + "t"); t.text = seg[1:-1] if hl else seg; t.set(XMLNS + "space", "preserve")
ps = [p for p in body.iter(W + "p") if p.find(".//" + W + "tab") is None]
for ini, nuevo in C:
    c = [p for p in ps if texto(p).startswith(ini)]
    assert len(c) == 1, (ini, len(c))
    escribir(c[0], nuevo)
tree.write(f"{DIR}/word/document.xml", xml_declaration=True, encoding="UTF-8", standalone=True)
print("ronda 3:", len(C), "párrafos")

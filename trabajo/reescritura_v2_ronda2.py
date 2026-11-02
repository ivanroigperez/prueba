# Segunda pasada de la reescritura: repeticiones y frases largas. Busca cada párrafo por el inicio de su texto.
import copy, re, sys
from lxml import etree
DIR = sys.argv[1]
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
XMLNS = "{http://www.w3.org/XML/1998/namespace}"
X = "⟦[      ]⟧"
C = [
("[NOTA, BORRAR ANTES DE ENTREGAR", "⟦[NOTA, BORRAR ANTES DE ENTREGAR: completa los valores entre corchetes y las capturas con los resultados de Eco-it de las prácticas. Si Eco-it ordena las alternativas de otra forma, revisa los comentarios de los apartados 4.2 a 4.5.]⟧"),
("[Pegar aquí la captura de los resultados de Eco-it de la alternativa 1]", "⟦[Pegar la captura de los resultados de Eco-it de la alternativa 1]⟧"),
("[Pegar aquí la captura de los resultados de Eco-it de la alternativa 2]", "⟦[Pegar la captura de los resultados de Eco-it de la alternativa 2]⟧"),
("[Pegar aquí la captura de los resultados de Eco-it de la alternativa 3]", "⟦[Pegar la captura de los resultados de Eco-it de la alternativa 3]⟧"),
("El taburete-escalera es un producto muy común.", "El taburete-escalera es un producto muy común. En el mercado casi siempre hay que elegir entre un modelo robusto y uno fácil de guardar. Los más robustos y estables pesan y ocupan bastante, y acaban guardados en el trastero. El usuario vuelve entonces a subirse a la silla. Los más compactos y baratos dan poca sensación de seguridad, con peldaños estrechos, bloqueos poco fiables o apoyos que resbalan."),
("No. Es una patente estadounidense, sin efectos en España, y ha expirado.", "No. Es una patente estadounidense, sin efectos en España, y ha expirado. Aporta la idea de usar el asa de transporte para mantener el taburete cerrado al llevarlo, útil en este producto para que no se abra al colgarlo en la pared."),
("Soportar el peso del usuario mientras sube", "Soportar el peso del usuario al subir, al estar de pie y al bajar."),
("Ilustración 2. Accidentes domésticos", "Ilustración 2. Accidentes domésticos y de ocio en España por tipo. Elaboración propia con datos del informe DADO (2011)."),
("EN 131 (Europa)", "EN 131 (Europa): norma de escaleras que excluye a los taburetes-escalera, aunque algunos fabricantes la cumplen para dar más confianza al comprador. El modelo de Leroy Merlin analizado está certificado conforme a EN 131 y EN 14183."),
("La etapa de información reúne", "La etapa de información reúne lo necesario para definir el producto antes de diseñarlo, es decir, costes, competencia, patentes, normativa, tecnologías y condiciones de almacenaje, embalaje y montaje. Con esa información se redacta el EDP (Especificaciones de Diseño del Producto). En la metodología de la asignatura esta etapa queda abierta durante todo el proceso, y algunos valores de la etapa inicial se han corregido con lo que se ha encontrado en ella."),
("Estas alturas no están al alcance", "Estas alturas no están al alcance de todo el mundo. El percentil 5 de las mujeres españolas mide 1,49 m (INSHT). El alcance vertical máximo de pie es de unas 1,24 veces la estatura, así que esta usuaria llega a unos 1,85 m. La balda superior de un mueble alto y todo el altillo le quedan fuera de alcance (Ilustración 1). Un hombre de estatura media, de 1,70 m y con un alcance de unos 2,11 m, tampoco llega al altillo sin ayuda."),
("Según el informe DADO", "Las caídas son el accidente doméstico y de ocio más frecuente, con el 51,1 % del total, según el informe DADO (Detección de Accidentes Domésticos y de Ocio) del Ministerio de Sanidad. La mayoría de estos accidentes ocurre dentro de la vivienda, el 54,5 % (Ilustración 2). La población española está cada vez más envejecida. A 1 de enero de 2025 el 20,7 % tenía 65 años o más (INE), y en este grupo una caída desde poca altura puede tener consecuencias graves."),
("El coste objetivo parte del precio", "El coste objetivo parte del precio de venta de la competencia (apartado 2.2). Los taburetes plegables de dos peldaños y 150 kg de carga se venden en España entre unos 19 € (modelos básicos de aluminio) y 86 € (modelos de marca con peldaños anchos). El precio medio es de unos 54 €. Se quiere situar el producto por debajo de las marcas de gama media-alta y por encima de los modelos más baratos en prestaciones."),
("Otras patentes consultadas", "Se han consultado otras tres patentes. Dos son de Hailo Werk, la EP 2 660 419 A2 (“Steiggerät, nämlich Klapptritt oder Trittleiter”) y la EP 3 056 656 A1 (soporte para pies de escaleras y taburetes). La tercera es la US 6 390 238 B1 de Cosco, una versión anterior de la patente segunda."),
("El modelo confirma las propiedades", "El modelo confirma las propiedades principales de la etapa inicial. La plataforma está a 480 mm y el peldaño a 240 mm del suelo, y la huella es de 496 × 450 mm. El espesor plegado es de 40 mm, por debajo de los 50 mm de P6, y no hay interferencias entre piezas ni abierto ni plegado. Plegado, las patas traseras sobresalen unos 4 cm por debajo de los largueros, lo que no afecta al guardarlo apoyado en la pared o colgado del asa. Las masas de cada pieza, calculadas con la herramienta de propiedades físicas, están en la Tabla 10."),
("Con cálculos manuales sencillos", "Con cálculos manuales sencillos se ha comprobado que el diseño de la alternativa 2 cumple las propiedades P1 (150 kg) y P2 (estabilidad) y el requisito R3 (no plegarse con el usuario encima). La carga es de 150 kg (1471 N) y el coeficiente de seguridad mínimo, 2 (Tabla 11). Para el aluminio 6063-T5 se ha tomado un límite elástico de 145 MPa (biblioteca de SolidWorks) y para el acero de los pasadores, de 235 MPa. El polipropileno con un 30 % de fibra de vidrio tiene una resistencia de unos 75 MPa (valor típico de catálogo)."),
("Los cambios que salen de estas comprobaciones", "Estas comprobaciones obligan a usar polipropileno con fibra de vidrio, tres nervios en la plataforma y en el peldaño y casquillos en los taladros. Con estos cambios la masa estimada de la alternativa 2 sube de 3,17 a unos 3,46 kg y sigue cumpliendo P5, con poco margen. Si el prototipo pesara más, la pared de los largueros y las patas se puede bajar a 1,5 mm (σ = 29 MPa y coeficiente de seguridad de 5), con un ahorro de unos 0,44 kg."),
("En esta etapa se evalúan las tres alternativas", "En esta etapa se evalúan las tres alternativas de material del apartado 3.3. Su impacto ambiental se analiza con un pequeño análisis de ciclo de vida (ACV) hecho con Eco-it, el programa de las prácticas de la asignatura. Para elegir la solución final se comprueba qué alternativas cumplen las propiedades imprescindibles del EDP."),
("La alternativa de aluminio es la más ligera", f"La alternativa de aluminio es la más ligera, pero el aluminio primario tiene un impacto por kilo muy alto. La producción vuelve a dominar, con {X} kg CO₂-eq de un total de {X} kg CO₂-eq (Tabla 14 e Ilustración 19). Las piezas que más aportan son los largueros y las patas traseras, con 1,86 de los 2,29 kg de aluminio. La plataforma y el peldaño de polipropileno suman en la producción y en la incineración final. Con aluminio reciclado el total baja a {X} kg CO₂-eq."),
("La madera es la alternativa de menor impacto ambiental.", "La madera es la alternativa de menor impacto ambiental. Supera el peso máximo y su modelo está simplificado. Los listones son macizos y tienen la misma sección que los perfiles metálicos (40 × 20 mm), que habría que aumentar para soportar 150 kg, y el vaciado de la plataforma no se puede fabricar en contrachapado. Queda como línea de trabajo futura si se consigue un diseño en madera verificado por debajo de 3,5 kg."),
("Las características técnicas más importantes", "Las características técnicas más importantes son el peso total (15,7 %) y la carga máxima (13,7 %). Les siguen la altura de la plataforma y el espesor plegado, con alrededor del 12,5 % cada una, y el número de piezas distintas (12,0 %). El diseño tiene que centrarse en un producto ligero y compacto sin perder resistencia, la misma contradicción técnica que se resolvió con TRIZ. En el tejado, aumentar la carga máxima tiende a aumentar el peso, y reducir el peso mejora el espesor plegado, el coste y la huella de carbono."),
("La etapa de realización recoge", "La etapa de realización recoge la documentación necesaria para fabricar el producto. Son tres planos en formato A3, que se entregan en el archivo “Anexo_Planos.pdf”. El plano 1 es el conjunto abierto con la lista de piezas y el plano 2, el conjunto plegado con su espesor de 40 mm. El plano 3 es el plano de fabricación del larguero delantero, con material, tolerancias, acabado y proceso."),
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
print("ronda 2:", len(C), "párrafos")

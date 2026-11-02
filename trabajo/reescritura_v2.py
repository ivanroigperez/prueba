# Reescritura del texto con el estilo de Iván (skill trabajo-formato-propio).
# Edita word/document.xml y word/footer1.xml de la copia desempaquetada, conservando pPr y rPr.
# Los segmentos entre ⟦ ⟧ se escriben resaltados en amarillo (huecos de Eco-it).
import copy, json, re, sys
from lxml import etree

DIR = sys.argv[1]                      # carpeta "unpacked"
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
XMLNS = "{http://www.w3.org/XML/1998/namespace}"
X = "⟦[      ]⟧"

R = {
# ---------- portada ----------
4: "TRABAJO DE ASIGNATURA, CURSO 2026-2027",
9: "Plegado y abierto",
2: "Grado en Ingeniería Mecánica, Ingeniería Simultánea",
# ---------- 1. ETAPA INICIAL ----------
120: "Buena parte del espacio de almacenaje de una vivienda está en altura, en muebles altos de cocina, armarios que llegan al techo, altillos o estanterías. En una cocina estándar los muebles altos se colocan más o menos entre 1,45 y 2,20 m del suelo, y los altillos pueden llegar a 2,50 m.",
121: "Estas alturas no están al alcance de todo el mundo. El percentil 5 de las mujeres españolas mide 1,49 m (INSHT). El alcance vertical máximo de pie es de unas 1,24 veces la estatura, así que esta usuaria llega a unos 1,85 m y la balda superior de un mueble alto y todo el altillo le quedan fuera de alcance (Ilustración 1). Un hombre de estatura media, de 1,70 m y con un alcance de unos 2,11 m, tampoco llega al altillo sin ayuda.",
124: "Las viviendas, en especial en las ciudades, son cada vez más pequeñas, y cualquier objeto auxiliar tiene que poder guardarse en poco sitio. Por eso mucha gente acaba subiéndose a una silla, a una caja o incluso a la encimera para alcanzar lo que necesita, con el riesgo de caída que eso supone.",
125: "Según el informe DADO (Detección de Accidentes Domésticos y de Ocio) del Ministerio de Sanidad, las caídas son el accidente más frecuente, el 51,1 % del total, y la mayoría de estos accidentes ocurre dentro de la vivienda, el 54,5 % (Ilustración 2). La población española está cada vez más envejecida. A 1 de enero de 2025 el 20,7 % tenía 65 años o más (INE), y en este grupo una caída desde poca altura puede tener consecuencias graves.",
129: "El taburete-escalera es un producto muy común. En el mercado casi siempre hay que elegir entre un modelo robusto y uno fácil de guardar. Los más robustos y estables pesan y ocupan bastante, y acaban en el trastero mientras el usuario vuelve a subirse a la silla. Los más compactos y baratos dan poca sensación de seguridad, con peldaños estrechos, bloqueos poco fiables o apoyos que resbalan.",
130: "La motivación del trabajo es diseñar un taburete-escalera doméstico seguro y estable durante el uso que, al mismo tiempo, se guarde y se mueva con facilidad. El diseño aplica criterios de ecodiseño para reducir su impacto ambiental en todo el ciclo de vida.",
132: "Las necesidades del usuario que se han identificado son las siguientes:",
133: "Poder alcanzar con seguridad objetos situados hasta 2,20-2,50 m de altura.",
137: "Poder llevarlo de una habitación a otra con una sola mano.",
144: "El producto es un taburete-escalera plegable de uso doméstico. Es un elemento auxiliar de pocos peldaños que permite a una persona subir con seguridad para llegar a las zonas altas de la vivienda (muebles altos de cocina, altillos, estanterías, lámparas o cortinas). Cuando no se usa, se pliega para guardarlo en poco espacio.",
145: "Está pensado para usos breves y frecuentes dentro de casa, por cualquier miembro de la familia. El uso profesional queda para las escaleras de mano y de tijera.",
148: "Diseñar un taburete-escalera doméstico seguro y estable, ligero y fácil de guardar, con un precio competitivo y un impacto ambiental reducido en todo su ciclo de vida.",
150: "1. Que una usuaria de percentil 5 alcance con comodidad 2,30 m de altura, lo que cubre todo el mueble alto y la balda media del altillo.",
152: "3. Que ocupe el menor espesor posible una vez plegado, para guardarlo en huecos estrechos.",
155: "6. Reducir la huella de carbono frente a los modelos equivalentes del mercado, con materiales reciclables y fáciles de separar.",
157: "La altura de la plataforma sale de un cálculo sencillo. Para llegar a 2,30 m con un alcance de unos 1,85 m, la plataforma superior tiene que estar al menos a 0,45 m del suelo. Se ha tomado 0,48 m en dos peldaños iguales de 0,24 m, como exige la norma UNE-EN 14183, que pide la misma distancia entre peldaños que del suelo al primer peldaño (Ilustración 3). Es una altura muy parecida a la de los modelos de referencia, como el Hailo K20, con la plataforma a 46 cm.",
161: "Las funciones del producto se han clasificado como en la asignatura, en funciones de uso, de manipulación y comunicativas (Ilustración 4). La función principal es elevar al usuario con seguridad para que alcance las zonas altas. Las demás son secundarias y hacen posible o mejoran la principal.",
178: "Integrarse en la cocina o en el salón, donde muchas veces estará a la vista.",
180: "Los requisitos son las condiciones que debe cumplir el producto para realizar bien sus funciones (Tabla 1). Se han agrupado en los tipos vistos en clase (ergonómicos, estéticos, de uso y medioambientales), más los de seguridad y los económicos, y se han separado en imprescindibles (I) y deseables (D).",
279: "1.6.1. PROPIEDADES",
280: "Las propiedades traducen los requisitos a valores concretos y medibles, que sirven para comprobar si el diseño es correcto (Tabla 2). Se dividen en pasivas, ligadas a la estructura y a los materiales, y activas, ligadas al movimiento y al funcionamiento. Los valores de peso y de espesor plegado se endurecieron tras el estudio de mercado del apartado 2.2, al quedar los iniciales por debajo de lo que ya ofrece la competencia.",
334: "1.6.2. ASPECTO",
335: "Se busca un aspecto sencillo y actual, con líneas limpias y colores neutros (blanco, gris antracita o acabado madera), para que el taburete no desentone si se queda a la vista en la cocina o en el salón. Tiene que transmitir robustez, y el usuario debe ver antes de subirse que es firme y que está bien bloqueado. Las indicaciones de uso y la carga máxima se deben leer con claridad sin recargar el diseño.",
336: "1.6.3. FORMA",
337: "La forma se subordina a la función. Abierto, el taburete necesita una base de apoyo más amplia que la parte superior, para que el centro de gravedad del usuario quede siempre dentro de ella y no vuelque. Plegado, debe quedar casi plano para guardarlo en huecos estrechos. No puede tener aristas vivas ni salientes, y necesita una zona para cogerlo con una mano al transportarlo.",
339: "La estructura describe cómo se organiza el producto en conjuntos, subconjuntos y piezas, y qué función cumple cada parte. En la etapa inicial se planteó a partir de las funciones del apartado 1.4, con un bastidor portante, unas superficies de apoyo para el pie, un mecanismo de plegado y bloqueo y unos apoyos antideslizantes. Después se completó con las piezas del diseño del apartado 3.4, en el que el bastidor se dividió en delantero y trasero (Ilustración 5).",
342: "Los dos bastidores y las dos superficies de apoyo son piezas sencillas de un solo material, y todas las uniones son articulaciones con pasadores desmontables. Con esta estructura es fácil reparar el taburete, cambiar las piezas de desgaste y separar los materiales al final de su vida útil (requisitos R15 y R21).",
# ---------- 2. ETAPA DE INFORMACIÓN ----------
344: "La etapa de información reúne lo necesario para definir el producto antes de diseñarlo, es decir, costes, competencia, patentes, normativa, tecnologías y condiciones de almacenaje, embalaje y montaje. Con esa información se redacta el EDP (Especificaciones de Diseño del Producto). En la metodología de la asignatura esta etapa queda abierta durante todo el proceso, y algunos valores de la etapa inicial se han corregido con lo encontrado aquí.",
346: "El coste objetivo parte del precio de venta de la competencia (apartado 2.2). Los taburetes plegables de dos peldaños y 150 kg de carga se venden en España entre unos 19 € (modelos básicos de aluminio) y 86 € (modelos de marca con peldaños anchos), con un precio medio de unos 54 €. Se quiere situar el producto por debajo de las marcas de gama media-alta y por encima de los modelos más baratos en prestaciones.",
347: "Partiendo de un precio de venta al público (PVP) objetivo de 45 € con IVA, se ha estimado el coste de fabricación máximo del producto (Tabla 3).",
370: "El coste industrial se ha repartido en unos 8,50 € de materiales, 4,00 € de transformación (corte, doblado, inyección y acabado), 1,50 € de montaje, 1,00 € de embalaje y 2,30 € de gastos generales y amortización de utillajes. Los márgenes son hipótesis habituales del sector. El reparto por componente se ha revisado en el análisis del valor (apartado 5.3) con las masas del modelo de SolidWorks.",
371: "Estos costes solo se alcanzan con series largas, del orden de 20.000 unidades al año, que permiten amortizar herramientas caras como los moldes de inyección o las matrices de estampación.",
373: "Se han analizado los taburetes-escalera que se venden en las principales tiendas españolas (IKEA, Leroy Merlin, Obramat y ferreterías online). Sus características principales están en la Tabla 4 y sus precios en la Ilustración 6.",
434: "Taburetes fijos de madera o plástico (IKEA BEKVÄM y BOLMEN). Son muy baratos y tienen buena estética, pero no se pliegan y su carga máxima es de 100 kg. El BEKVÄM lleva un asa en el peldaño superior, una idea que se ha tenido en cuenta.",
435: "Taburetes plegables básicos de aluminio (Altipesa y similares). Son muy ligeros (2 kg) y baratos. El peldaño inferior solo tiene 80 mm de fondo, no cabe el pie entero y dan poca sensación de seguridad.",
436: "Taburetes plegables de acero de marca (Hailo K20 y Safety). Son muy robustos, con peldaños anchos y alfombrilla antideslizante, y plegados solo ocupan 5 cm. A cambio pesan más de 5 kg y cuestan entre 52 y 59 €.",
437: "Modelos de aluminio de gama alta (Hailo L90). Tienen peldaños anchos y son ligeros. Su precio de 86 € queda fuera del alcance de muchos hogares y plegados ocupan 19 cm.",
439: "Hay un hueco entre los modelos baratos y poco cómodos y los robustos, pesados y caros. El nuevo diseño debe ofrecer los peldaños profundos y la carga de 150 kg de los modelos de marca, con un peso y un precio más cercanos a los de los básicos. Al compararlas con la competencia, dos propiedades de la etapa inicial resultaron poco exigentes, el espesor plegado de 80 mm y el peso de 5 kg. Como recomienda el tema de EDP cuando se detectan deficiencias frente a lo existente, se han cambiado a 50 mm y 3,5 kg.",
441: "El EDP recoge las especificaciones y limitaciones que el mercado y la empresa imponen al producto antes de la fase creativa (Tabla 5). Sigue los apartados vistos en la asignatura, con frases cortas y sin orientar el diseño hacia una solución concreta.",
510: "En los productos analizados se han identificado las tecnologías de fabricación que se usan hoy en este tipo de taburetes (Tabla 6).",
553: "Antes de diseñar un producto para venderlo hay que conocer las patentes sobre productos similares, porque podrían impedir su comercialización. Una patente da a su titular el derecho exclusivo a explotar una invención durante 20 años en el territorio donde se concede, a cambio de hacerla pública. En España existe también el modelo de utilidad, que protege durante 10 años invenciones de menor rango, como una configuración o estructura que da una ventaja práctica. La protección es territorial y una patente de Estados Unidos no tiene efectos en España.",
554: "La búsqueda se ha hecho en Google Patents, Espacenet (Oficina Europea de Patentes) e INVENES (Oficina Española de Patentes y Marcas), con palabras clave como “taburete plegable”, “escalera plegable”, “folding step stool” y “Klapptritt”. Se han analizado las cuatro más cercanas al producto.",
555: "2.5.1. PATENTE PRIMERA: ES 1 070 877 U, DISPOSITIVO DE ENCLAVAMIENTO PARA TABURETES PLEGABLES Y SIMILARES",
559: "Situación: caducado (un modelo de utilidad protege como máximo 10 años, hasta 2019 en este caso).",
561: "Dispositivo que mantiene desplegado un taburete plegable. En una de las patas, junto a la articulación con la plataforma superior, hay un vástago que atraviesa la pata y que un muelle mantiene sobresaliendo. La pared lateral de la plataforma tiene un orificio enfrentado al vástago y, antes de él, una zona abombada hacia fuera. Al desplegar el taburete, esa zona empuja el vástago hacia dentro. Cuando el vástago llega al orificio, el muelle lo vuelve a sacar, el vástago queda encajado y el taburete se bloquea abierto.",
566: "¿Afecta al producto?",
567: "No. Es el documento más parecido al producto, un taburete de dos peldaños con bloqueo automático al abrirlo. El modelo de utilidad ha caducado y su solución se puede usar libremente. Es una buena referencia para el bloqueo automático que se busca (principio TRIZ 10, acción previa).",
568: "2.5.2. PATENTE SEGUNDA: US 6 454 050 B2, FOLDABLE STEP STOOL WITH LEG LOCK AND HANDLE",
574: "Taburete-escalera plegable con un bastidor formado por una pata delantera y una pata trasera que se mueven una respecto a la otra, y un asa de transporte que gira sobre una de las patas. Una pieza de retención unida al asa gira con ella y bloquea la pata delantera con la trasera cuando el taburete está plegado, para que no se abra al transportarlo.",
579: "¿Afecta al producto?",
580: "No. Es una patente estadounidense, sin efectos en España, y ha expirado. Aporta la idea de usar el asa de transporte para mantener el taburete cerrado mientras se lleva, útil en este producto para que no se abra al colgarlo en la pared.",
581: "2.5.3. PATENTE TERCERA: US 6 966 404 B2, FOLDING STEP STOOL",
592: "¿Afecta al producto?",
593: "No. Tampoco tiene efectos en España y ha expirado. Aporta dos ideas útiles, el asa formada por aberturas en la plataforma y el indicador visual de bloqueo, que responde a la función comunicativa “dejar claro cómo se abre y cuándo está bien bloqueado” del apartado 1.4.",
594: "2.5.4. PATENTE CUARTA: US 12 419 421 B2, FOLDABLE LOCKING STEP STOOL",
600: "Taburete plegable cuya plataforma se divide en dos mitades unidas por una bisagra. Tiene un mecanismo de bloqueo a prueba de niños formado por dos deslizadores, uno en cada lado de la plataforma, que hay que accionar a la vez para liberar dos pestillos con muelle y poder plegarlo. Con este sistema un niño no puede cerrarlo y pillarse los dedos. Incluye agarres antideslizantes sobremoldeados y un asa integrada que queda oculta cuando el taburete está en uso.",
605: "¿Afecta al producto?",
606: "No. La patente solo protege el invento en Estados Unidos. En su portada no figura ninguna solicitud internacional (PCT) ni prioridad extranjera, y en la búsqueda no ha aparecido ninguna solicitud europea de la misma familia. El diseño propuesto no divide la plataforma en dos mitades ni usa dos deslizadores simultáneos, que son elementos esenciales de la reivindicación. Para vender el producto en Estados Unidos habría que evitar ese mecanismo.",
607: "Otras patentes consultadas fueron la EP 2 660 419 A2 (Hailo Werk, “Steiggerät, nämlich Klapptritt oder Trittleiter”), la EP 3 056 656 A1 (Hailo Werk, soporte para pies de escaleras y taburetes) y la US 6 390 238 B1 (Cosco, versión anterior de la patente segunda).",
608: "¿Es patentable el producto?",
609: "El concepto general de taburete-escalera plegable de dos peldaños no es patentable, al no cumplir el requisito de novedad. Existe desde hace décadas y hay muchas patentes sobre él, como las analizadas. Sí podría protegerse una solución concreta del diseño, como un mecanismo de bloqueo que combine de forma nueva el asa de transporte con el cierre de seguridad. Al ser una mejora de la configuración del producto con una ventaja práctica, la vía más adecuada sería un modelo de utilidad en España, más rápido y barato que una patente. La apariencia externa se podría proteger como diseño industrial y el nombre comercial como marca.",
611: "Los taburetes-escalera no tienen una directiva europea propia y no llevan marcado CE. Deben cumplir la legislación general de seguridad de los productos de consumo, con la norma UNE-EN 14183 como referencia técnica para demostrar que el producto es seguro (Tabla 7).",
646: "DIN EN 14183 (Alemania) y BS EN 14183 (Reino Unido): versiones nacionales de la norma europea. En Alemania es habitual la marca voluntaria GS (“Geprüfte Sicherheit”, seguridad comprobada), muy valorada por el consumidor.",
647: "EN 131 (Europa): norma de escaleras que excluye a los taburetes-escalera, aunque algunos fabricantes la cumplen para dar más confianza al comprador. El modelo de Leroy Merlin analizado está certificado según EN 131 y EN 14183.",
648: "En Estados Unidos haría falta una carga de servicio de al menos 300 libras (136 kg), que ya cubren los 150 kg fijados.",
650: "Con el enfoque de ecodiseño “de la cuna a la tumba” se han identificado de forma cualitativa las entradas, salidas e impactos del producto en cada fase de su ciclo de vida (Tabla 8).",
672: "La rueda estratégica de ecodiseño vista en la asignatura compara un taburete de acero típico del mercado con el objetivo del nuevo diseño (Ilustración 11). Las mejoras se centran en la selección y la reducción de material, en la distribución, gracias al plegado plano, y en el fin de vida.",
676: "Desde que se fabrica hasta que llega al usuario, el taburete puede pasar varios meses en almacenes, con estas condiciones:",
683: "El embalaje tiene que proteger el producto en el transporte, permitir su almacenaje y servir de reclamo en la tienda. Sus características son estas:",
685: "Caja de unos 880 × 470 × 60 mm, a partir del tamaño plegado medido en el modelo (861 × 450 × 40 mm).",
687: "En un palé europeo (1200 × 800 mm) las cajas van de canto, con el lado largo (880 mm) en la dirección de 1200 mm. Caben 13 cajas en el lado de 800 mm y 3 alturas de 470 mm, en total 39 unidades por palé y una altura de unos 1,55 m. Colocadas planas solo cabría una caja por capa, unas 23 unidades por palé. El plegado plano reduce el volumen transportado y, con él, el coste y las emisiones del transporte.",
689: "El producto se entrega montado y el usuario solo tiene que desplegarlo. El montaje se hace en fábrica con esta secuencia, ya adaptada al diseño definitivo del apartado 3.4:",
696: "7. Colocación de las etiquetas de advertencia y de carga máxima, y control final de apertura y cierre, del bloqueo y de carga por muestreo.",
697: "Se usa el menor número posible de piezas distintas y de tipos de unión, y todas las uniones se pueden deshacer con herramientas comunes para facilitar la reparación y el reciclaje.",
# ---------- 3. ETAPA TÉCNICO-CREATIVA ----------
699: "En esta etapa se buscan soluciones que cumplan los objetivos y el EDP. Se han aplicado dos técnicas de creatividad, un mapa mental para generar ideas sin criticarlas y el método TRIZ para resolver las contradicciones técnicas del producto.",
701: "El mapa mental ordena alrededor del producto las ideas sobre el usuario, la seguridad, el almacenaje, los materiales, la fabricación, la estética, el medio ambiente y el coste (Ilustración 12). Sirve para no olvidar ningún aspecto al generar propuestas.",
705: "TRIZ (Teoría para Resolver Problemas de Inventiva) lo desarrolló Genrich Altshuller a partir del análisis de miles de patentes. La mayoría de los problemas de diseño aparecen al mejorar un parámetro del producto y empeorar otro, lo que se llama contradicción técnica. Para resolverlas, Altshuller definió 39 parámetros técnicos y 40 principios inventivos (Tabla 9), relacionados en la matriz de contradicciones. En la fila se busca el parámetro que se quiere mejorar y en la columna el que empeora, y la celda da los principios más usados para resolver ese conflicto.",
871: "CONTRADICCIÓN PRIMERA: RESISTENCIA FRENTE A PESO",
872: "Para soportar 150 kg el taburete tiene que ser resistente. Reforzar la estructura con más material o perfiles más gruesos aumenta su peso, y el máximo fijado es de 3,5 kg para poder llevarlo con una mano.",
873: "Parámetro que se quiere mejorar: 14 (resistencia).",
874: "Parámetro que empeora: 1 (peso del objeto móvil).",
877: "Principio 1, segmentación: dividir la estructura en piezas independientes, cada una con el material y la sección justos para su función (largueros de perfil resistente y peldaños nervados), en lugar de piezas macizas. Facilita la sustitución de piezas y el reciclaje.",
878: "Principio 15, dinamicidad: que los peldaños y la plataforma giren respecto al larguero y queden horizontales para trabajar y verticales para guardar.",
881: "CONTRADICCIÓN SEGUNDA (FÍSICA): BASE GRANDE Y BASE PEQUEÑA",
882: "Para ser estable, el taburete necesita una base de apoyo amplia que deje siempre dentro el centro de gravedad del usuario. Para guardarlo, en cambio, tiene que ser lo más pequeño y plano posible. El mismo elemento tiene que ser grande y pequeño, lo que en TRIZ se llama contradicción física.",
883: "Las contradicciones físicas se resuelven con los principios de separación. Aquí se aplica la separación en el tiempo, con una base grande cuando se usa y pequeña cuando se guarda. Eso lleva al plegado (principio 15, dinamicidad) y a alojar los peldaños dentro del hueco de los largueros al cerrarlo (principio 7, anidamiento), para no pasar de 50 mm de espesor plegado.",
884: "Planteado como contradicción técnica (mejorar el parámetro 13, estabilidad del objeto, empeora el 7, volumen del objeto móvil), la matriz propone los principios 28, 10, 1 y 39. Son útiles el 10 (acción previa), que consiste en dejar el taburete preparado para que al abrirlo quede solo en su posición estable, y el 1 (segmentación), ya aplicado en la contradicción primera.",
885: "CONTRADICCIÓN TERCERA: FACILIDAD DE USO FRENTE A FIABILIDAD",
886: "Se busca que el taburete se abra y se cierre muy rápido y con una sola mano. Cuanto más fácil sea cerrarlo, mayor es el riesgo de que se cierre accidentalmente con el usuario encima.",
887: "Parámetro que se quiere mejorar: 33 (facilidad de uso).",
888: "Parámetro que empeora: 27 (fiabilidad).",
891: "Principio 8, contrapeso: sin aplicación directa. En el boceto se pensó en que el peso del usuario mantuviera el taburete abierto, algo que depende de la geometría del mecanismo respecto al punto muerto y que se estudia en el apartado 3.5.",
892: "Principio 17, otra dimensión: que el pestillo de seguridad se accione en dirección perpendicular al movimiento de plegado, con un deslizador lateral, para que un golpe o una carga en el sentido de cierre no lo suelte.",
894: "Principio 27, objetos baratos de vida corta: se descarta por ir en contra del requisito de larga vida útil (R20).",
895: "Principio 10, acción previa, como complemento: el bloqueo se activa solo al abrir el taburete, sin que el usuario haga nada, como en el modelo de utilidad ES 1 070 877 U.",
897: "Con el mapa mental y las soluciones de TRIZ se ha dibujado el boceto inicial (Ilustración 13), un taburete de tipo tijera con dos peldaños iguales de 240 mm de altura. Los largueros delanteros llevan el peldaño inferior y la plataforma superior, y la pata trasera se articula bajo la plataforma. Un tirante une el peldaño inferior con la pata trasera y bloquea la apertura. Al plegarlo, el peldaño y la plataforma giran hasta quedar verticales entre los largueros, y el conjunto queda en un plano de unos 50 mm de espesor.",
900: "El concepto se ha desarrollado con tres alternativas de material:",
905: "Con el concepto definido, el producto se ha modelado en SolidWorks. Antes de modelar las piezas definitivas se comprobó el mecanismo de plegado con un estudio cinemático en el plano lateral, y el resultado obligó a modificar el boceto inicial.",
906: "REDISEÑO DEL MECANISMO DE PLEGADO",
907: "En el boceto la pata trasera giraba bajo la plataforma y un único tirante unía el peldaño con ella. Con esa disposición la plataforma quedaba en voladizo detrás de su articulación y el conjunto no podía plegarse en un plano. La solución adoptada tiene tres partes (Ilustración 14):",
908: "Llevar el pivote de las patas traseras (P) por encima de la plataforma, a 657 mm de altura, prolongando los largueros delanteros hasta unos 780 mm. La prolongación forma un asidero y cumple el requisito deseable R11.",
910: "Al cerrar la pata trasera (un giro de 41°), las bielas obligan a la plataforma y al peldaño a girar 75° hasta quedar paralelos a los largueros. Con los puntos de unión calculados, plataforma y peldaño quedan alineados con el larguero al plegar.",
913: "MODELO EN SOLIDWORKS",
914: "El modelo de SolidWorks 2026 tiene diez piezas (larguero delantero, pata trasera, travesaño del asidero, travesaño trasero, plataforma, peldaño, biela de la plataforma, tirante del peldaño, pasador y taco) y dos ensamblajes, abierto y plegado (Ilustraciones 15 a 17). Cada pieza tiene una configuración por alternativa de material (ALT1_ACERO, ALT2_ALUMINIO y ALT3_MADERA), en la que cambian el material y, si hace falta, la geometría. En madera los perfiles son macizos y la pared de la plataforma y el peldaño es de 15 mm, frente a 1,2 mm en acero y 3 mm en polipropileno.",
921: "El modelo confirma las propiedades principales de la etapa inicial. La plataforma está a 480 mm y el peldaño a 240 mm del suelo, la huella es de 496 × 450 mm, el espesor plegado es de 40 mm (P6 pedía 50 mm como máximo) y no hay interferencias entre piezas ni abierto ni plegado. Plegado, las patas traseras sobresalen unos 4 cm por debajo de los largueros, lo que no afecta al guardarlo apoyado en la pared o colgado del asa. Las masas de cada pieza, calculadas con la herramienta de propiedades físicas, están en la Tabla 10.",
922: "El modelo todavía no incluye el pestillo de seguridad de la contradicción tercera de TRIZ. El mecanismo tiene un único grado de libertad y basta con bloquear una articulación para fijar el taburete abierto. La posición del pestillo, en la articulación del peldaño, y su carga se calculan en el apartado 3.5. Su diseño de detalle queda como acción correctora del AMFEC (apartado 5.2).",
984: "Solo la alternativa de aluminio cumple la propiedad P5 (peso máximo de 3,5 kg). La de madera se queda cerca, con 3,96 kg, y la de acero la supera con mucho, con 9,20 kg. En la alternativa de aluminio la plataforma y el peldaño se han modelado con polipropileno sin reforzar, al no estar el reforzado con fibra de vidrio en la biblioteca de SolidWorks. Con fibra de vidrio (1,12 g/cm³ frente a 0,89 g/cm³) el peso subiría unos 170 g, hasta unos 3,34 kg, y seguiría cumpliendo.",
986: "Con cálculos manuales sencillos se ha comprobado que el diseño de la alternativa 2 cumple las propiedades P1 (150 kg) y P2 (estabilidad) y el requisito R3 (no plegarse con el usuario encima). La carga es de 150 kg (1471 N) y el coeficiente de seguridad mínimo, 2 (Tabla 11). Se ha tomado un límite elástico de 145 MPa para el aluminio 6063-T5 (biblioteca de SolidWorks) y de 235 MPa para el acero de los pasadores, y una resistencia de 75 MPa para el polipropileno con un 30 % de fibra de vidrio (valor típico de catálogo).",
1038: "El resultado más importante es el del mecanismo. Con el modelo cinemático del apartado 3.4 se ha calculado cuánto cambia la altura de la carga si la pata trasera gira 1° con los cuatro pies en el suelo:",
1039: "Usuario sobre la plataforma: al abrir 1° más, la plataforma baja 3,9 mm y el peso tiende a abrir el taburete. La apertura queda limitada a 1,9° más, donde el peldaño y el tirante se alinean (punto muerto) y hacen de tope.",
1040: "Usuario sobre el peldaño, al subir o bajar: al abrir 1° más, el peldaño sube 6,2 mm y el peso tiende a cerrar el taburete con un momento de unos 522 N·m. El pestillo es imprescindible para cumplir R3. Va en la articulación del peldaño, que es la que más gira (4,1° por cada grado de la pata), y así soporta menos fuerza.",
1041: "Los cambios que salen de estas comprobaciones (polipropileno con fibra de vidrio, tres nervios en la plataforma y en el peldaño y casquillos en los taladros) suben la masa estimada de la alternativa 2 de 3,17 a unos 3,46 kg. Sigue cumpliendo P5 con poco margen. Si el prototipo pesara más, la pared de los largueros y las patas se puede bajar a 1,5 mm (σ = 29 MPa y coeficiente de seguridad de 5), con un ahorro de unos 0,44 kg.",
# ---------- 4. ETAPA DE EVALUACIÓN ----------
1043: "En esta etapa se evalúan las tres alternativas de material del apartado 3.3. Se analiza su impacto ambiental con un pequeño análisis de ciclo de vida (ACV) hecho con Eco-it, el programa de las prácticas de la asignatura, y se comprueba cuáles cumplen las propiedades imprescindibles del EDP para elegir la solución final.",
1046: "Eco-it es una herramienta de ACV simplificado pensada para diseñadores. El análisis sigue el enfoque “de la cuna a la tumba” de las normas UNE-EN ISO 14040 y 14044 y expresa los resultados como huella de carbono, en kg de CO₂ equivalente. La unidad funcional es un taburete-escalera que permite a un usuario de hasta 150 kg alcanzar 2,30 m de altura durante 10 años de uso doméstico. Eco-it divide el ciclo de vida en tres fases:",
1047: "Producción: materiales y procesos de fabricación de cada pieza, con las masas del modelo de SolidWorks (Tabla 10), más el transporte de distribución hasta el punto de venta, de 600 km en camión.",
1050: "Los datos introducidos en Eco-it para cada alternativa están en la Tabla 12. En la alternativa 2 se ha calculado una variante con aluminio reciclado en lugar de primario, para valorar la mejora propuesta en las conclusiones.",
1108: "El análisis no incluye el embalaje, la pintura o el anodizado ni las mermas de fabricación, y las bases de datos de Eco-it recogen valores medios.",
1110: f"En la alternativa de acero la fase de producción es la de mayor impacto, con {X} kg CO₂-eq de un total de {X} kg CO₂-eq (Tabla 13 e Ilustración 18). Pesan sobre todo los largueros, las patas, la plataforma y el peldaño, que concentran la mayor parte de los 9,20 kg de acero. El transporte y el uso apenas cuentan.",
1125: f"La alternativa de aluminio es la más ligera, pero el aluminio primario tiene un impacto por kilo muy alto y la producción vuelve a dominar, con {X} kg CO₂-eq de un total de {X} kg CO₂-eq (Tabla 14 e Ilustración 19). Las piezas que más aportan son los largueros y las patas traseras, con 1,86 de los 2,29 kg de aluminio. La plataforma y el peldaño de polipropileno suman en la producción y en la incineración final. Con aluminio reciclado el total baja a {X} kg CO₂-eq.",
1145: f"La madera tiene un impacto de producción por kilo mucho menor que el de los metales y esta alternativa es la de menor impacto total, con {X} kg CO₂-eq (Tabla 15 e Ilustración 20). Las piezas de acero (bielas, tirantes y pasadores) solo suman 0,57 kg y aun así suponen una parte importante de la producción, con {X} kg CO₂-eq.",
1160: "En las tres alternativas domina la fase de producción, y el transporte y el uso son casi despreciables en un producto que no consume energía (Ilustración 21). Las decisiones de diseño con más efecto ambiental son la elección del material y la cantidad empleada.",
1163: "El impacto ambiental no es el único criterio. Para elegir, primero se ha comprobado qué alternativas cumplen las propiedades imprescindibles del EDP, ya que un requisito imprescindible no se compensa con una buena nota en otros criterios (Tabla 16).",
1190: "Solo la alternativa de aluminio y polipropileno cumple todas las propiedades imprescindibles. Las de acero (9,20 kg) y madera (3,96 kg) superan el peso máximo de 3,5 kg de P5, ligado al requisito imprescindible R10 (llevarlo con una mano), y quedan descartadas.",
1191: f"Su punto débil es el impacto del aluminio primario, y por eso se especifica aluminio con alto contenido reciclado. Con este material Eco-it da {X} kg CO₂-eq en lugar de {X}, un {X} % menos.",
1192: "La madera es la alternativa de menor impacto ambiental. Supera el peso máximo y su modelo está simplificado, con listones macizos de la misma sección que los perfiles metálicos (40 × 20 mm), que habría que aumentar para soportar 150 kg, y un vaciado de la plataforma que no se puede fabricar en contrachapado. Queda como línea de trabajo futura si se consigue un diseño en madera verificado por debajo de 3,5 kg.",
1193: "Se elige la alternativa 2, con perfiles de aluminio 6063-T5 reciclado y plataforma y peldaño de polipropileno reforzado con fibra de vidrio. Es la alternativa modelada en detalle y la que se representa en los planos.",
# ---------- 5. ETAPA DE REDISEÑO ----------
1195: "Sobre la solución elegida, la alternativa 2, se han aplicado las técnicas de rediseño de la asignatura (QFD, AMFEC y análisis del valor) para detectar sus puntos débiles y proponer mejoras antes de fabricar prototipos.",
1197: "El QFD traduce lo que pide el cliente (los “qués”) en características técnicas medibles (los “cómos”). En la casa de la calidad se han relacionado los nueve requisitos principales del cliente, con su importancia de 1 a 5, con nueve características técnicas (Ilustración 22). Cada relación se ha puntuado con 9 (fuerte), 3 (media) o 1 (débil), y el tejado indica las sinergias y los conflictos entre características. A la derecha aparece la percepción del cliente del diseño frente a dos productos de la competencia del apartado 2.2.",
1200: "Las características técnicas más importantes son el peso total (15,7 %), la carga máxima (13,7 %), la altura de la plataforma y el espesor plegado (alrededor del 12,5 % cada una) y el número de piezas distintas (12,0 %). El diseño tiene que centrarse en un producto ligero y compacto sin perder resistencia, la misma contradicción técnica que se resolvió con TRIZ. En el tejado, aumentar la carga máxima tiende a aumentar el peso, y reducir el peso mejora el espesor plegado, el coste y la huella de carbono.",
1201: "Frente a la competencia, el diseño iguala al Hailo K20 en seguridad, altura y comodidad y lo supera en peso y precio. Frente al Altipesa ofrece más seguridad y un peldaño mucho más cómodo. Su punto débil es el medio ambiente, por el impacto del aluminio primario (apartado 4), que justifica el uso de aluminio reciclado.",
1203: "El AMFEC identifica los modos de fallo potenciales del producto (Tabla 17). Para cada uno se valora de 1 a 10 la probabilidad de que ocurra (O), su gravedad (G) y la probabilidad de que no se detecte antes de llegar al usuario (D). El producto de los tres es el índice de prioridad de riesgo (IPR = O × G × D), que indica sobre qué fallos actuar primero. Después de proponer una acción correctora se ha vuelto a estimar el IPR.",
1295: "El fallo más crítico es el desbloqueo con el usuario encima (IPR = 150), por su gravedad máxima, seguido de las articulaciones y de los tacos antideslizantes. Con las acciones propuestas, en especial un pestillo de doble gesto y un indicador visual de bloqueo como el de la patente US 6 966 404, todos los IPR bajan de 100 y el más alto queda en 48.",
1297: "El análisis del valor compara la importancia que da el cliente a cada función con lo que cuesta cumplirla, para encontrar funciones en las que se gasta más de lo que el cliente valora o al revés. El coste de cada componente se ha estimado a partir del coste industrial objetivo del apartado 2.1 (Tabla 18) y se ha repartido entre las funciones a las que contribuye. La importancia de cada función sale del QFD y del EDP (Ilustración 23).",
1325: "La suma del coste de las piezas, 13,46 €, supera en casi 1 € los 12,50 € previstos en el apartado 2.1 para materiales y transformación (8,50 € + 4,00 €). Hay que ajustar el diseño para cumplir el coste industrial objetivo.",
1327: "Las funciones de soportar la carga (33 % del coste frente a un 20 % de valor) y de estética (7 % frente a 4 %) están sobredimensionadas. Se propone optimizar la sección de los largueros y las patas, con un perfil de 1,5 mm de pared como el comprobado en el apartado 3.5, y simplificar el asidero.",
1328: "El bloqueo (2 % del coste frente a un 12 % de valor) y el antideslizante (1,5 % frente a 8 %) están infravalorados, igual que señalaba el AMFEC. Conviene invertir en un buen pestillo de seguridad y en tacos y superficies antideslizantes de calidad, que el cliente valora mucho y cuestan poco.",
1329: "Transportar y guardar tiene mucho valor y muy poco coste gracias al plegado plano y al hueco-asa. Es uno de los puntos fuertes del producto y merece destacarse en la comunicación comercial.",
# ---------- 6. ETAPA DE REALIZACIÓN ----------
1332: "La etapa de realización recoge la documentación necesaria para fabricar el producto. Son tres planos en formato A3, que se entregan en el archivo “Anexo_Planos.pdf”. El plano 1 es el conjunto abierto con la lista de piezas, el plano 2 el conjunto plegado, con su espesor de 40 mm, y el plano 3 el plano de fabricación del larguero delantero, con material, tolerancias, acabado y proceso.",
# ---------- pies de figura y tabla (unificados) ----------
127: "Ilustración 2. Accidentes domésticos y de ocio en España según su tipo. Elaboración propia con datos del informe DADO (2011).",
565: "Ilustración 7. Figura 1 del modelo de utilidad ES 1 070 877 U, con el detalle D del vástago de bloqueo. Fuente: OEPM y Google Patents.",
578: "Ilustración 8. Figuras 1 y 2 de la patente US 6 454 050 B2. Fuente: USPTO y Google Patents.",
591: "Ilustración 9. Figuras 1 y 2 de la patente US 6 966 404 B2. Fuente: USPTO y Google Patents.",
674: "Ilustración 11. Rueda estratégica de ecodiseño: producto actual frente a objetivo. Elaboración propia.",
916: "Ilustración 15. Ensamblaje abierto, vista lateral (SolidWorks). Elaboración propia.",
918: "Ilustración 16. Ensamblaje abierto, vista frontal (SolidWorks). Elaboración propia.",
920: "Ilustración 17. Ensamblaje plegado, vista isométrica (SolidWorks). Elaboración propia.",
1123: "Ilustración 18. Resultados de Eco-it de la alternativa 1: acero. Elaboración propia.",
1143: "Ilustración 19. Resultados de Eco-it de la alternativa 2: aluminio y polipropileno. Elaboración propia.",
1158: "Ilustración 20. Resultados de Eco-it de la alternativa 3: madera. Elaboración propia.",
430: "Tabla 4. Taburetes-escalera del mercado español (n. d.: dato no disponible). Fuente: webs de fabricantes y distribuidores, septiembre de 2026.",
870: "Tabla 9. Los 39 parámetros técnicos y los 40 principios inventivos de Altshuller. Fuente: matriz de contradicciones TRIZ40.",
983: "Tabla 10. Masa de cada pieza por alternativa en el modelo de SolidWorks. Elaboración propia.",
1121: "Tabla 13. Resultados de Eco-it de la alternativa 1: acero. Elaboración propia.",
1141: "Tabla 14. Resultados de Eco-it de la alternativa 2: aluminio y polipropileno (kg CO₂-eq). Elaboración propia.",
1156: "Tabla 15. Resultados de Eco-it de la alternativa 3: madera. Elaboración propia.",
1322: "Tabla 18. Coste estimado de cada componente (alternativa 2). Elaboración propia.",
1334: "Plano 1. Conjunto abierto con lista de piezas. Elaboración propia.",
1336: "Plano 2. Conjunto plegado. Elaboración propia.",
1338: "Plano 3. Larguero delantero: plano de fabricación. Elaboración propia.",
# ---------- tablas: solo tipografía ----------
332: "-", 352: "-", 1025: "-", 1030: "-",
358: "38 % del PVP sin IVA (hipótesis)", 364: "25 % (hipótesis)", 368: "17,30 €",
390: "1 / unos 25 cm", 418: "2 / unos 49 cm (alto total)",
501: "Abierto: huella de unos 500 × 450 mm. Plegado: espesor ≤ 50 mm.",
994: "σ = 22 MPa", 999: "Pcr = 42 kN frente a 368 N", 1004: "σ = 70 MPa", 1009: "σ = 37 MPa",
1014: "τ = 15 MPa", 1019: "σ = 31 MPa", 1024: "Empuje horizontal para volcar: 250 N",
1029: "Empuje para volcar: 210 N (14 % del peso)", 1034: "710 N por pasador; τ = 14 MPa",
}
BORRAR = {643}                                   # frase de la prEN 131-9, sin verificar
COMILLAS = {563, 576, 589, 602}                  # reivindicaciones: solo cambiar « » por “ ”
SEPARADOR = range(1056, 1107)                    # Tabla 12: " · " -> ", "
BIBLIO = {1355: ("–", "-")}

tree = etree.parse(f"{DIR}/word/document.xml")
body = tree.getroot().find(W + "body")
ps = list(body.iter(W + "p"))
texto = lambda p: "".join(t.text or "" for t in p.iter(W + "t"))

def escribir(p, nuevo):
    runs = [r for r in p if r.tag == W + "r"]
    base = next((r for r in runs if r.find(W + "rPr") is None or r.find(f"{W}rPr/{W}highlight") is None), runs[0] if runs else None)
    marcado = next((r for r in runs if r.find(f"{W}rPr/{W}highlight") is not None), None)
    for r in runs: p.remove(r)
    for seg in re.split(r"(⟦.*?⟧)", nuevo):
        if not seg: continue
        hl = seg.startswith("⟦")
        modelo = marcado if (hl and marcado is not None) else base
        r = etree.SubElement(p, W + "r")
        if modelo is not None and modelo.find(W + "rPr") is not None:
            rpr = copy.deepcopy(modelo.find(W + "rPr"))
            if not hl:
                for h in rpr.findall(W + "highlight"): rpr.remove(h)
            r.append(rpr)
        t = etree.SubElement(r, W + "t"); t.text = seg[1:-1] if hl else seg
        t.set(XMLNS + "space", "preserve")

hechos = 0
for i, nuevo in R.items():
    escribir(ps[i], nuevo); hechos += 1
for i in COMILLAS:
    t = texto(ps[i]); escribir(ps[i], t.replace("«", "“").replace("»", "”")); hechos += 1
for i in SEPARADOR:
    t = texto(ps[i])
    if " · " in t: escribir(ps[i], t.replace(" · ", ", ")); hechos += 1
for i, (a, b) in BIBLIO.items():
    escribir(ps[i], texto(ps[i]).replace(a, b)); hechos += 1
for i in BORRAR:
    ps[i].getparent().remove(ps[i])
tree.write(f"{DIR}/word/document.xml", xml_declaration=True, encoding="UTF-8", standalone=True)

# pie de página
ft = etree.parse(f"{DIR}/word/footer1.xml")
for t in ft.iter(W + "t"):
    if t.text and "·" in t.text:
        t.text = "Taburete-escalera plegable, Iván Roig Pérez. Página "
        t.set(XMLNS + "space", "preserve")
ft.write(f"{DIR}/word/footer1.xml", xml_declaration=True, encoding="UTF-8", standalone=True)
print("párrafos reescritos:", hechos, "| borrados:", len(BORRAR))

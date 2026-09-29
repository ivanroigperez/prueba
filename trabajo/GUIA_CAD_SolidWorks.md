# Guía para el modelado en SolidWorks (apartado 3.4)

Esta guía es para que modeles el taburete. Las cotas salen del boceto (Ilustración 8), del EDP (Tabla 5) y de las propiedades (Tabla 2). Son orientativas: si al modelarlo algo no encaja, cámbialo y avísame para actualizar el texto del trabajo.

## 1. Cotas generales que hay que respetar

| Cota | Valor | De dónde sale |
|---|---|---|
| Altura de la cara superior de la plataforma | 480 mm | Cálculo de alcance (1.3, Ilustración 3) |
| Altura de la cara superior del peldaño inferior | 240 mm | Peldaños equidistantes (UNE-EN 14183) |
| Profundidad de la plataforma | ≈ 300 mm | Apoyo del pie entero |
| Profundidad del peldaño inferior | ≥ 200 mm | P4 |
| Anchura útil de peldaño y plataforma | ≥ 350 mm | P4 |
| Huella abierto (fondo × ancho) | ≈ 500 × 450 mm | EDP, tamaño y volumen |
| Espesor plegado | ≤ 50 mm | P6 |
| Inclinación de los largueros | ≈ 75° respecto al suelo | Boceto |
| Holguras en zonas móviles | < 8 mm o > 25 mm | P8 (antiatrapamiento) |
| Peso total | ≤ 3,5 kg (al menos en la alternativa de aluminio) | P5 |

## 2. Lista de piezas

| Nº | Pieza | Cant. | Notas |
|---|---|---|---|
| 1 | Larguero delantero | 2 | Longitud ≈ 500 mm (480 / sen 75°). Lleva el peldaño y la articulación de la plataforma |
| 2 | Pata trasera | 1 | En forma de U (dos patas y un travesaño). Tiene que ser más estrecha que el marco delantero para que al plegar quede dentro |
| 3 | Plataforma superior | 1 | ≈ 420 × 300 mm. Con un hueco‑asa de unos 120 × 30 mm (idea de la patente US 6 966 404) |
| 4 | Peldaño inferior | 1 | ≈ 400 × 200 mm. Gira sobre los largueros delanteros |
| 5 | Tirante de bloqueo | 2 | Une el peldaño inferior con la pata trasera. La longitud la sacas del croquis de posición abierta. Tiene que quedar un poco pasado del punto muerto |
| 6 | Pasador / eje | 4‑6 | Ø 8 mm, con arandelas |
| 7 | Taco antideslizante | 4 | TPE, encaja en el extremo de cada larguero |
| 8 | Pestillo de seguridad | 1 | Segundo seguro para plegar (contradicción TRIZ 3). Puede ser un pasador con muelle o una pestaña que se desliza |

Truco: dibuja primero un croquis de diseño (layout) en 2D con la vista lateral del boceto, igual que el "Layout sketch" de la práctica del cuatro barras, y crea las piezas a partir de él. Así la cinemática del plegado sale bien a la primera.

## 3. Configuraciones (práctica de configuraciones y tablas de diseño)

En el ensamblaje:
- **ABIERTO** y **PLEGADO**: posiciones controladas por una relación de ángulo entre el larguero delantero y la pata trasera. Con la de plegado mide el espesor total con una cota o con Evaluar > Medir. Tiene que salir 50 mm o menos.
- Pasa **Detección de interferencias** en las dos posiciones.

En las piezas, con una **tabla de diseño en Excel** (como en el ejercicio del recipiente AraWorks), crea una configuración por alternativa:

| Configuración | Largueros y pata | Peldaños y plataforma | Tirantes y pasadores |
|---|---|---|---|
| ALT1_ACERO | Tubo rectangular 30 × 15 × 1,5 mm, acero S235 (en SolidWorks: "Acero AISI 1020" o "S235JR" si lo tienes) | Chapa de acero de 1,2 mm con pliegues de refuerzo | Acero |
| ALT2_ALUMINIO | Perfil rectangular 40 × 20 × 2 mm, aluminio 6063‑T5 | PP con 30 % de fibra de vidrio, 3 mm de pared con nervios | Acero |
| ALT3_MADERA | Contrachapado de abedul de 18 mm, listón de 50 mm de ancho | Contrachapado de abedul de 15 mm | Acero |

## 4. Qué necesito que me pases para seguir (etapa 4, evaluación con ACV)

1. **La tabla de masas de cada pieza en cada configuración.** Se saca de Evaluar > Propiedades físicas; ojo con asignar bien el material. Por ejemplo:

   | Pieza | Cant. | Masa ALT1 (g) | Masa ALT2 (g) | Masa ALT3 (g) |
   |---|---|---|---|---|
   | Larguero delantero | 2 | | | |
   | … | | | | |

2. **El peso total** de cada alternativa y **el espesor plegado** medido.
3. **Capturas**: isométrica abierto, isométrica plegado, vista lateral y vista explosionada (para la Ilustración 9 en adelante).
4. **Planos** (para los anexos): plano de conjunto con lista de materiales y planos de despiece de las piezas principales.

Con las masas hago el análisis de ciclo de vida de las tres alternativas (fabricación, uso y fin de vida, en kg CO₂‑eq, como el índice de ejemplo), la comparativa y las conclusiones. Si quieres, también el QFD, el AMFEC y el análisis de valor.

## 5. Opcional (prácticas de Motion y Simulation)

- **Estudio de movimiento**: animación de apertura y cierre, que queda muy bien en la presentación.
- **Simulation**: análisis estático de la plataforma y los largueros con una carga de 150 kg. Mira la tensión de Von Mises y el factor de seguridad en cada alternativa, igual que la práctica de la viga en voladizo. Sirve para justificar que las tres alternativas son válidas antes de compararlas en el ACV.

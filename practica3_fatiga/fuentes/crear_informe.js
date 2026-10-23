// Informe de la práctica 3 (ensayo de fatiga) con el formato de las prácticas 1 y 2.
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell,
  WidthType, BorderStyle, VerticalAlign, ImageRun, Header, Footer, PageNumber, TableOfContents,
  LevelFormat, PageBreak, LineRuleType, Math: OMath, MathRun, MathFraction, MathSubScript, MathSuperScript,
  MathRoundBrackets, MathFunction, MathSubSuperScript,
} = require("docx");

const DIR = __dirname;
const AZUL = "2F5496";

// ---------- texto con subíndices _{..} y superíndices ^{..} ----------
function runs(s, base = {}) {
  // espacios de no separación entre número y unidad y alrededor de "=" para que no se partan al final de línea
  s = s.replace(/(\d) (?=(mm|MPa|N|°C|kpsi|rpm|W|s|HBW|ciclos)(?![\wáéíóúñ]))/g, "$1\u00a0").replace(/(\d) %/g, "$1\u00a0%").replace(/ = /g, "\u00a0=\u00a0");
  const out = [];
  const re = /(_\{[^}]*\}|\^\{[^}]*\})/g;
  let last = 0, m;
  while ((m = re.exec(s)) !== null) {
    if (m.index > last) out.push(new TextRun({ text: s.slice(last, m.index), ...base }));
    const inner = m[0].slice(2, -1);
    out.push(new TextRun({ text: inner, ...(m[0][0] === "_" ? { subScript: true } : { superScript: true }), ...base }));
    last = m.index + m[0].length;
  }
  if (last < s.length) out.push(new TextRun({ text: s.slice(last), ...base }));
  return out;
}
const P = (s, opt = {}) => new Paragraph({ children: runs(s), ...opt });
const H1 = (s, salto = false) => new Paragraph({ heading: HeadingLevel.HEADING_1, pageBreakBefore: salto, children: [new TextRun(s)] });
const H2 = (s) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(s)] });
const paso = (s) => new Paragraph({ children: runs(s), numbering: { reference: "pasos", level: 0 } });
const pieTabla = (s) => new Paragraph({ style: "Caption", keepNext: true, children: runs(s) });
const pieFigura = (s) => new Paragraph({ style: "Caption", children: runs(s) });

// ---------- ecuaciones (OMML) ----------
const r = (t) => new MathRun(t);
// texto normal dentro de la ecuación (números con coma decimal y unidades); se marca y se convierte a m:nor después
const n = (t) => new MathRun("§N§" + t);
const prima = (sub) => new MathSubSuperScript({ children: [r("S")], subScript: [r(sub)], superScript: [r("′")] });
const sb = (b, s) => new MathSubScript({ children: [r(b)], subScript: [r(s)] });
const sp = (b, s) => new MathSuperScript({ children: Array.isArray(b) ? b : [r(b)], superScript: Array.isArray(s) ? s : [r(s)] });
const fr = (n, d) => new MathFraction({ numerator: n, denominator: d });
const par = (c) => new MathRoundBrackets({ children: c });
const ec = (children) => new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { before: 60, after: 160 },
  children: [new OMath({ children })],
});

// ---------- tablas ----------
const borde = { style: BorderStyle.SINGLE, size: 4, color: "000000" };
const bordes = { top: borde, bottom: borde, left: borde, right: borde, insideHorizontal: borde, insideVertical: borde };
function celda(texto, ancho, opt = {}) {
  const { bold = false, align = AlignmentType.CENTER, rowSpan, columnSpan } = opt;
  return new TableCell({
    width: { size: ancho, type: WidthType.DXA },
    verticalAlign: VerticalAlign.CENTER,
    margins: { top: 20, bottom: 20, left: 80, right: 80 },
    ...(rowSpan ? { rowSpan } : {}), ...(columnSpan ? { columnSpan } : {}),
    children: [new Paragraph({ alignment: align, spacing: { before: 0, after: 0, line: 240, lineRule: LineRuleType.AUTO }, children: runs(String(texto), bold ? { bold: true } : {}) })],
  });
}
function tabla(anchos, cabecera, filas, opt = {}) {
  const total = anchos.reduce((a, b) => a + b, 0);
  const rows = [new TableRow({ tableHeader: true, cantSplit: true, children: cabecera.map((c, i) => celda(c, anchos[i], { bold: true })) })];
  for (const f of filas) {
    rows.push(new TableRow({ cantSplit: true, children: f.map((c, i) => celda(c, anchos[i], { align: (opt.alinear && opt.alinear[i]) || AlignmentType.CENTER })) }));
  }
  return new Table({ width: { size: total, type: WidthType.DXA }, columnWidths: anchos, alignment: AlignmentType.CENTER, borders: bordes, rows });
}
const hueco = () => new Paragraph({ spacing: { after: 0 }, children: [] });

// ---------- imágenes ----------
function imagen(archivo, anchoCm, tipo, wpx, hpx) {
  const ancho = Math.round((anchoCm / 2.54) * 96);
  const alto = Math.round((ancho * hpx) / wpx);
  return new Paragraph({
    alignment: AlignmentType.CENTER, keepNext: true, spacing: { before: 120, after: 60 },
    children: [new ImageRun({ type: tipo, data: fs.readFileSync(path.join(DIR, archivo)), transformation: { width: ancho, height: alto } })],
  });
}

// ================== PORTADA ==================
const portada = [
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 }, children: [new TextRun({ text: "Universidad de La Rioja", size: 32 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 }, children: [new TextRun("Grado en Ingeniería Mecánica")] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 }, children: [new TextRun("Cálculo, Diseño y Ensayo de Máquinas")] }),
  new Paragraph({ style: "Subtitle", alignment: AlignmentType.CENTER, spacing: { before: 3600, after: 60 }, children: [new TextRun({ text: "Práctica 3", size: 30 })] }),
  new Paragraph({ style: "Title", alignment: AlignmentType.CENTER, children: [new TextRun("Ensayo de fatiga")] }),
  new Paragraph({ style: "Subtitle", alignment: AlignmentType.CENTER, spacing: { after: 240 }, children: [new TextRun("Ensayo de flexión rotativa con probetas de acero AISI 1010")] }),
  new Paragraph({ alignment: AlignmentType.CENTER, children: [new ImageRun({ type: "jpg", data: fs.readFileSync(path.join(DIR, "foto_probeta.jpg")),
    transformation: { width: Math.round((15 / 2.54) * 96), height: Math.round((15 / 2.54) * 96 * 450 / 1650) } })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 3500, after: 60 }, children: [new TextRun({ text: "Iván Roig Pérez", size: 28 })] }),
  new Paragraph({ style: "Subtitle", alignment: AlignmentType.CENTER, spacing: { after: 0 }, children: [new TextRun("Curso 2026/2027")] }),
  new Paragraph({ style: "Subtitle", alignment: AlignmentType.CENTER, children: [new TextRun("Octubre de 2026")] }),
];

// ================== ÍNDICE ==================
const indice = [
  new Paragraph({ style: "TOCHeading", pageBreakBefore: true, children: [new TextRun("Contenido")] }),
  new TableOfContents("Contenido", { hyperlink: true, headingStyleRange: "1-2" }),
];

// ================== CUERPO ==================
const cuerpo = [
  H1("1. Introducción", true),
  P("El objetivo de esta práctica es estudiar el fallo por fatiga de probetas de acero AISI 1010 sometidas a flexión rotativa y ver cómo influye en él el radio del acuerdo del cambio de sección."),
  P("Se han ensayado probetas con radios de acuerdo de 0,4 y 0,8 mm, cargadas en su extremo con 60, 80, 100 y 120 N, y en cada ensayo se ha anotado el número de ciclos hasta la rotura. Para cada carga se calcula la tensión en el cambio de sección con la ecuación de Navier. Con la ecuación de Marin y los factores de concentración de tensiones se obtiene el número de ciclos que debería aguantar cada probeta según la teoría, y se compara con el del ensayo."),

  H1("2. Fundamento teórico"),
  H2("2.1 Esfuerzos fluctuantes"),
  P("En muchos elementos de máquinas la tensión cambia con el tiempo, en magnitud y a veces también en signo. Un ejemplo es un eje que gira cargado a flexión, en el que cada fibra pasa de tracción a compresión en cada vuelta. Cada ciclo de tensión se describe con la tensión media y la amplitud:"),
  ec([sb("σ", "m"), r("="), fr([sb("σ", "max"), r("+"), sb("σ", "min")], [r("2")])]),
  ec([sb("σ", "a"), r("="), fr([sb("σ", "max"), r("−"), sb("σ", "min")], [r("2")])]),
  P("Si la tensión va de cero a un máximo, el esfuerzo es intermitente, y si varía entre dos valores del mismo signo, pulsatorio. Cuando pasa de un valor positivo a uno negativo es alternado, simétrico si los dos valores son iguales en valor absoluto y asimétrico si no lo son. En el alternado simétrico la tensión media es nula y la amplitud coincide con la tensión máxima."),

  H2("2.2 Fallo por fatiga"),
  P("Con tensiones fluctuantes una pieza puede romper aunque la tensión máxima quede por debajo de la resistencia a tracción, e incluso del límite elástico. Es el fallo por fatiga. Empieza con una grieta muy pequeña en un punto donde se concentran las tensiones, como un cambio de sección, una entalla, un chavetero o la marca de una herramienta. Con los ciclos la grieta avanza, la sección que resiste se reduce y al final la pieza rompe de golpe, casi sin deformarse. Es un fallo peligroso, porque llega sin avisar. En la superficie de rotura se ven dos zonas, una exterior de grano fino, por donde ha ido avanzando la grieta, y otra interior de grano más grueso y brillante, que corresponde a la rotura final."),

  H2("2.3 Diagrama de Wöhler y ecuación de Marin"),
  P("El comportamiento a fatiga de un material se representa en el diagrama de Wöhler, con la amplitud de tensión frente al número de ciclos hasta la rotura en escala logarítmica. La resistencia a la fatiga es la amplitud máxima que aguanta el material durante un número de ciclos dado. En los aceros la curva se vuelve horizontal a partir de unos 10^{6} ciclos. Esa amplitud es el límite de fatiga S’_{e}, por debajo del cual la probeta no rompe por muchos ciclos que se apliquen. Para aceros con S_{ut} ≤ 1400 MPa se estima como:"),
  ec([prima("e"), r("="), n("0,5"), r("·"), sb("S", "ut")]),
  P("Este límite corresponde a probetas normalizadas ensayadas en el laboratorio en condiciones muy controladas. Para una pieza concreta se corrige con la ecuación de Marin:"),
  ec([sb("S", "e"), r("="), prima("e"), r("·"), sb("k", "a"), r("·"), sb("k", "b"), r("·"), sb("k", "c"), r("·"), sb("k", "d")]),
  P("El factor k_{a} tiene en cuenta el acabado superficial, k_{b} el tamaño, k_{c} el tipo de carga y k_{d} la temperatura de trabajo. El límite de fatiga baja cuanto peor es el acabado y mayor es la pieza."),

  H2("2.4 Concentración de tensiones en fatiga"),
  P("En un cambio brusco de sección la tensión en el fondo del acuerdo es mayor que la nominal. El cociente entre las dos es el factor teórico de concentración de tensiones K_{t}, que solo depende de la geometría y del tipo de carga y crece al reducir el radio del acuerdo. En fatiga la entalla tiene algo menos de efecto, y se usa el factor de concentración de tensiones a fatiga:"),
  ec([sb("K", "f"), r("=1+q·"), par([sb("K", "t"), r("−1")])]),
  P("Aquí q es la sensibilidad a la entalla, que va de 0, si el material no nota la entalla, a 1, si K_{f} = K_{t}. Es mayor cuanto más resistente es el material y cuanto mayor es el radio de la entalla."),

  H2("2.5 Número de ciclos hasta la rotura"),
  P("Entre 10^{3} y 10^{6} ciclos la curva de Wöhler se aproxima por una recta en escala doble logarítmica. Teniendo en cuenta la entalla, se escribe como:"),
  ec([sb("K", "f"), r("·"), sb("S", "n"), r("=A·"), sp("N", "B")]),
  P("siendo S_{n} la amplitud de la tensión en la pieza y"),
  ec([r("A="), fr([sp([par([r("f·"), sb("S", "ut")])], "2")], [sb("S", "e")])]),
  ec([r("B=−"), fr([r("1")], [r("3")]), r("·"), new MathFunction({ name: [r("log")], children: [par([fr([r("f·"), sb("S", "ut")], [sb("S", "e")])])] })]),
  P("La recta pasa por f·S_{ut} a 10^{3} ciclos y por S_{e} a 10^{6} ciclos. La fracción de resistencia a la fatiga f se lee en una gráfica en función de S_{ut}. Despejando, el número de ciclos hasta la rotura es:"),
  ec([r("N="), sp([par([fr([sb("K", "f"), r("·"), sb("S", "n")], [r("A")])])], [fr([r("1")], [r("B")])])]),
  P("Si K_{f}·S_{n} queda por debajo de S_{e}, la pieza está en el tramo horizontal del diagrama y en teoría tiene vida infinita."),

  H2("2.6 Tensión en la probeta"),
  P("En el ensayo la probeta está empotrada por un extremo y recibe en el otro una carga F perpendicular a su eje, y el flector crece linealmente desde el punto de carga hasta el empotramiento (figura 6 del guion). En una sección situada a una distancia L de la carga el flector es M = F·L, y la tensión máxima, en la fibra más alejada de la fibra neutra, se obtiene con la ecuación de Navier:"),
  ec([sb("σ", "th"), r("="), fr([r("M·"), sb("y", "max")], [r("I")]), r("="), fr([r("F·L·"), sb("y", "max")], [r("I")])]),
  P("Para una sección circular de diámetro d, I = π·d^{4}/64 e y_{max} = d/2. La probeta gira mientras la carga mantiene su dirección, así que cada punto de la superficie pasa por la tracción máxima y por la compresión máxima en cada vuelta. La tensión es alternada simétrica, con σ_{m} = 0 y σ_{a} = σ_{th}, y cada vuelta es un ciclo."),

  H1("3. Material y metodología"),
  H2("3.1 Equipo de ensayo"),
  P("Se ha utilizado una máquina de ensayo de fatiga por flexión rotativa (figura 3 del guion). Un motor de 370 W, que gira a 2800 rpm, mueve el eje de anclaje en el que se amarra la probeta por su extremo grueso. El otro extremo entra en un rodamiento flotante, a través del cual el dispositivo de carga aplica sobre la probeta una fuerza de 0 a 300 N. La fuerza se ajusta girando una rueda y se lee en una escala graduada. La caja de control lleva los interruptores, el pulsador de emergencia y un contador de ciclos con botón de puesta a cero. Durante el ensayo la probeta queda cubierta por un protector, y la máquina no debe ponerse en marcha sin él."),

  H2("3.2 Probetas"),
  P("Las probetas son de acero AISI 1010 mecanizado en frío, con las propiedades de la tabla 1. Tienen 146 mm de longitud. Los primeros 40 mm son de Ø12 mm y por ellos se amarra la probeta, y el resto es de Ø8 mm (figuras 4 y 5 del guion). El paso de un diámetro a otro se hace con un acuerdo, de 0,4 mm de radio en las probetas de tipo 1 y de 0,8 mm en las de tipo 2. La carga se aplica a 100,5 mm del cambio de sección."),
  pieTabla("Tabla 1. Geometría de las probetas y propiedades del acero AISI 1010."),
  tabla([4400, 1800], ["Magnitud", "Valor"], [
    ["Longitud total", "146 mm"],
    ["Diámetro mayor, D", "12 mm"],
    ["Diámetro menor, d", "8 mm"],
    ["Radio de acuerdo, tipo 1", "0,4 mm"],
    ["Radio de acuerdo, tipo 2", "0,8 mm"],
    ["Distancia de la carga al cambio de sección, L", "100,5 mm"],
    ["Límite elástico, S_{y}", "560 MPa"],
    ["Resistencia a tracción, S_{ut}", "611 MPa"],
    ["Alargamiento", "20 %"],
    ["Dureza", "132 HBW"],
  ], { alinear: [AlignmentType.LEFT, AlignmentType.CENTER] }),
  hueco(),

  H2("3.3 Procedimiento"),
  P("Cada probeta se ha ensayado siguiendo estos pasos:"),
  paso("Se gira la rueda del dispositivo de carga hasta que el rodamiento flotante queda alineado con el eje de la probeta."),
  paso("Se suelta la rosca del eje de anclaje, se introduce la probeta primero en el rodamiento flotante y después en el eje de anclaje, y se aprieta la rosca para que quede bien amarrada."),
  paso("Se fija el protector al soporte."),
  paso("Con el motor parado, se gira la rueda hasta que la escala marca la carga del ensayo. La carga no se cambia con el motor en marcha."),
  paso("Se pone a cero el contador con el botón RST."),
  paso("Se pone en marcha el motor. Cuando la probeta rompe, el motor se para solo y se anota el número de ciclos del contador."),
  paso("Se retira la probeta con cuidado, porque sale caliente."),
  P("Se ha ensayado una probeta de cada tipo con cada una de las cargas, 60, 80, 100 y 120 N."),

  H1("4. Resultados"),
  H2("4.1 Tensión en el cambio de sección"),
  P("La sección crítica es la del cambio de diámetro. Es la sección del tramo de Ø8 mm más alejada de la carga, por lo que soporta el mayor flector de ese tramo, y en ella está el acuerdo. La tensión se calcula con d = 8 mm y L = 100,5 mm, sin tener en cuenta el acuerdo:"),
  ec([r("I="), fr([r("π·"), sp("8", "4")], [r("64")]), r("="), sp([n("201,1 mm")], [r("4")])]),
  P("Con y_{max} = 4 mm, para la carga de 60 N:"),
  ec([sb("σ", "th"), r("="), fr([r("60·"), n("100,5"), r("·4")], [n("201,1")]), r("="), n("120 MPa")]),
  P("La tensión es proporcional a la carga (tabla 2) y es la misma en los dos tipos de probeta, que solo se diferencian en el radio del acuerdo."),

  H2("4.2 Ciclos hasta la rotura"),
  P("La duración de cada ensayo se ha calculado con los ciclos y la velocidad del motor, t = N/n, con n = 2800 rpm. La tensión σ_{max} es la de Navier en el cambio de sección."),
  pieTabla("Tabla 2. Resultados del ensayo de fatiga."),
  (() => {
    const an = [2200, 1300, 1600, 1500, 1500];
    const cab = ["Ensayo", "Carga (N)", "N.º de ciclos", "Duración (s)", "σ_{max} (MPa)"];
    const datos = [
      ["Tipo 1 (r = 0,4 mm)", [["60", "9858", "211", "120"], ["80", "7533", "161", "160"], ["100", "5593", "120", "200"], ["120", "5292", "113", "240"]]],
      ["Tipo 2 (r = 0,8 mm)", [["60", "12612", "270", "120"], ["80", "6956", "149", "160"], ["100", "9257", "198", "200"], ["120", "4328", "93", "240"]]],
    ];
    const rows = [new TableRow({ tableHeader: true, cantSplit: true, children: cab.map((c, i) => celda(c, an[i], { bold: true })) })];
    for (const [nombre, filas] of datos) {
      filas.forEach((f, k) => {
        const cs = f.map((v, i) => celda(v, an[i + 1]));
        rows.push(new TableRow({ cantSplit: true, children: k === 0 ? [celda(nombre, an[0], { rowSpan: 4 }), ...cs] : cs }));
      });
    }
    return new Table({ width: { size: an.reduce((a, b) => a + b, 0), type: WidthType.DXA }, columnWidths: an, alignment: AlignmentType.CENTER, borders: bordes, rows });
  })(),
  imagen("fig_ciclos_carga.png", 13, "png", 1479, 851),
  pieFigura("Figura 1. Ciclos hasta la rotura frente a la carga en los dos tipos de probeta."),
  P("El número de ciclos hasta la rotura baja al aumentar la carga, aunque no de forma regular (tabla 2, figura 1). Con r = 0,8 mm la probeta de 80 N rompió antes que la de 100 N, y con r = 0,4 mm las de 100 y 120 N aguantaron casi lo mismo. Con 60 y 100 N la probeta de 0,8 mm dura bastante más que la de 0,4 mm, pero con 80 y 120 N ocurre lo contrario. Todas las probetas rompen entre unos 4000 y 13000 ciclos, es decir, en pocos minutos de ensayo."),
  P("La rotura se produce en el cambio de sección (figura 2). El trozo corto es el tramo de Ø12 mm por el que se amarra la probeta, y el largo, el de Ø8 mm."),
  imagen("foto_probeta.jpg", 14, "jpg", 1650, 450),
  pieFigura("Figura 2. Probeta rota tras el ensayo."),

  H2("4.3 Factores de concentración de tensiones"),
  P("En las dos probetas D/d = 12/8 = 1,5, y r/d vale 0,05 con r = 0,4 mm y 0,10 con r = 0,8 mm. Con estos valores, en la gráfica de K_{t} para un eje escalonado a flexión se lee K_{t} = 2,15 y K_{t} = 1,75. La sensibilidad a la entalla se lee en la gráfica para aceros con S_{ut} = 611 MPa, entre las curvas de 552 y 689 MPa, y sale q = 0,64 para r = 0,4 mm y q = 0,72 para r = 0,8 mm. Para r = 0,4 mm:"),
  ec([sb("K", "f"), r("=1+"), n("0,64"), r("·"), par([n("2,15"), r("−1")]), r("="), n("1,736")]),
  P("y del mismo modo, para r = 0,8 mm, K_{f} = 1,540 (tabla 3)."),
  pieTabla("Tabla 3. Factores de concentración de tensiones."),
  tabla([1200, 1100, 1100, 1100, 1100, 1200], ["r (mm)", "D/d", "r/d", "K_{t}", "q", "K_{f}"], [
    ["0,4", "1,5", "0,05", "2,15", "0,64", "1,736"],
    ["0,8", "1,5", "0,10", "1,75", "0,72", "1,540"],
  ]),
  hueco(),
  P("Con el radio de 0,8 mm K_{t} baja bastante. La sensibilidad q sube un poco con el radio, pero no compensa la bajada de K_{t}, y K_{f} sale menor. Con la misma carga, la probeta de 0,8 mm trabaja a fatiga con una tensión efectiva más baja."),

  H2("4.4 Límite de fatiga corregido"),
  P("Como S_{ut} = 611 MPa es menor de 1400 MPa:"),
  ec([prima("e"), r("="), n("0,5"), r("·611="), n("305,5 MPa")]),
  P("Para k_{a} se toma el acabado mecanizado en frío, con a = 4,51 y b = -0,265 para S_{ut} en MPa. Para k_{b} se usa el diámetro de la probeta, d = 8 mm, que está en el intervalo de 2,79 a 51 mm:"),
  ec([sb("k", "a"), r("="), n("4,51"), r("·"), sp([r("611")], [r("−"), n("0,265")]), r("="), n("0,8239")]),
  ec([sb("k", "b"), r("="), n("1,24"), r("·"), sp([r("8")], [r("−"), n("0,107")]), r("="), n("0,9926")]),
  P("La carga es de flexión, con lo que k_{c} = 1, y el ensayo se hace a temperatura ambiente, unos 20 °C, por lo que k_{d} = 1 (tabla 4)."),
  pieTabla("Tabla 4. Factores de la ecuación de Marin."),
  tabla([1200, 3400, 1300], ["Factor", "Criterio", "Valor"], [
    ["k_{a}", "Mecanizado en frío", "0,8239"],
    ["k_{b}", "d = 8 mm, flexión", "0,9926"],
    ["k_{c}", "Carga de flexión", "1"],
    ["k_{d}", "Temperatura ambiente, 20 °C", "1"],
  ]),
  hueco(),
  ec([sb("S", "e"), r("="), n("305,5"), r("·"), n("0,8239"), r("·"), n("0,9926"), r("·1·1="), n("249,8 MPa")]),
  P("La corrección se debe casi toda al acabado superficial, ya que el factor de tamaño apenas se separa de 1."),

  H2("4.5 Número teórico de ciclos"),
  P("Con S_{ut} = 611 MPa, que son unos 88,6 kpsi, en la gráfica de la fracción de resistencia a la fatiga se lee f = 0,861. Los parámetros de la recta son:"),
  ec([r("A="), fr([sp([par([n("0,861"), r("·611")])], "2")], [n("249,8")]), r("="), n("1108 MPa")]),
  ec([r("B=−"), fr([r("1")], [r("3")]), r("·"), new MathFunction({ name: [r("log")], children: [par([fr([n("0,861"), r("·611")], [n("249,8")])])] }), r("=−"), n("0,1078")]),
  P("La tensión es alternada simétrica y S_{n} = σ_{th}. Para r = 0,4 mm y 120 N, por ejemplo, K_{f}·σ_{th} = 1,736·239,9 = 416,5 MPa y:"),
  ec([r("N="), sp([par([fr([n("416,5")], [r("1108")])])], [fr([r("1")], [r("−"), n("0,1078")])]), r("="), n("8,7"), r("·"), sp("10", "3"), n(" ciclos")]),
  P("Cuando K_{f}·σ_{th} queda por debajo de S_{e} = 249,8 MPa, la ecuación da más de 10^{6} ciclos. Es el tramo horizontal del diagrama de Wöhler, y la vida teórica es infinita. Pasa con 60 N en las dos probetas y con 80 N en la de 0,8 mm, que queda justo por debajo del límite (tabla 5, figura 3)."),
  pieTabla("Tabla 5. Número de ciclos teórico y del ensayo."),
  tabla([1000, 900, 1300, 1500, 1700, 1300], ["r (mm)", "F (N)", "σ_{th} (MPa)", "K_{f}·σ_{th} (MPa)", "N teórico", "N ensayo"], [
    ["0,4", "60", "120", "208", "Vida infinita", "9858"],
    ["0,4", "80", "160", "278", "3,8·10^{5}", "7533"],
    ["0,4", "100", "200", "347", "4,7·10^{4}", "5593"],
    ["0,4", "120", "240", "417", "8,7·10^{3}", "5292"],
    ["0,8", "60", "120", "185", "Vida infinita", "12612"],
    ["0,8", "80", "160", "246", "Vida infinita", "6956"],
    ["0,8", "100", "200", "308", "1,4·10^{5}", "9257"],
    ["0,8", "120", "240", "369", "2,7·10^{4}", "4328"],
  ]),
  imagen("fig_wohler.png", 13, "png", 1476, 906),
  pieFigura("Figura 3. Diagrama S-N teórico y resultados del ensayo para los dos radios."),

  H2("4.6 Comparación entre teoría y ensayo"),
  P("Las probetas rompen mucho antes de lo que predice la teoría, sobre todo con las cargas bajas (tabla 5, figura 3). Con 60 N el cálculo da vida infinita en los dos radios, y las probetas rompieron en torno a 10^{4} ciclos. La diferencia se reduce al subir la carga, y con 120 N en la probeta de 0,4 mm la vida teórica y la del ensayo quedan en el mismo orden. En el ensayo el número de ciclos cambia poco con la carga, mientras que en la teoría cae muy deprisa."),
  P("Una parte de la diferencia viene del propio cálculo. N depende de la tensión elevada a 1/B, que vale -9,3, y un error del 5 % en K_{f}·σ_{th} cambia N entre un 36 y un 61 %. K_{t}, q y f se han leído a ojo en las gráficas, y un error de 0,05 en K_{t} o de 0,02 en q mueve la vida teórica entre un 10 y un 25 %. El diámetro entra al cubo en la tensión, y una diferencia de 0,05 mm en d cambia N casi un 20 %. Con errores de este tamaño se explican diferencias de decenas por ciento, pero no que con 60 N la teoría dé vida infinita y la probeta rompa en unos 10^{4} ciclos."),
  P("La mayor parte de la diferencia viene, probablemente, de la propia curva S-N. Está estimada a partir de S_{ut} con S’_{e} = 0,5·S_{ut} y con factores de Marin medios, y no recoge el estado real de las probetas. Una marca de mecanizado en el fondo del acuerdo, justo donde empieza la grieta, puede bajar mucho la resistencia a la fatiga, y el acero de las probetas puede no tener exactamente las propiedades de la tabla 1. El montaje también puede influir. Si el rodamiento flotante no queda bien alineado o la probeta no está bien amarrada, aparecen flexiones y vibraciones que el cálculo no tiene en cuenta."),
  P("Por último, cada punto es una sola probeta, y en fatiga los resultados tienen bastante dispersión, ya que dependen mucho del estado superficial. Seguramente por eso la probeta de 0,8 mm con 80 N duró menos que la de 100 N y el orden entre los dos radios cambia de una carga a otra."),

  H1("5. Conclusiones"),
  H2("5.1 Influencia del radio de acuerdo"),
  P("Según el cálculo, pasar de r = 0,4 a 0,8 mm baja K_{t} de 2,15 a 1,75 y K_{f} de 1,736 a 1,540, y con la misma carga la vida teórica se multiplica por unas tres. En el ensayo esta mejora no se aprecia con claridad. La probeta de 0,8 mm aguantó más con 60 y 100 N y menos con 80 y 120 N, lo que se puede deber a la dispersión propia de la fatiga, al haber un solo ensayo por carga. Convendría repetirlos con varias probetas para ver bien el efecto del radio. La rotura se produce en el cambio de sección, que es donde el acuerdo concentra las tensiones."),
  H2("5.2 Tensión de Navier"),
  P("La tensión de Navier en el cambio de sección crece en proporción a la carga, de 120 MPa con 60 N a 240 MPa con 120 N, y es igual en los dos tipos de probeta. Queda muy por debajo del límite elástico del acero, 560 MPa, y aun así las probetas rompen en pocos miles de ciclos. Con el efecto de la entalla, K_{f}·σ_{th} supera el límite de fatiga corregido, 249,8 MPa, a partir de 80 N en la probeta de 0,4 mm y de 100 N en la de 0,8 mm."),
  H2("5.3 Número teórico de ciclos"),
  P("El cálculo con la ecuación de Marin da vidas mucho más largas que las del ensayo, sobre todo con las cargas bajas, donde predice vida infinita para probetas que rompieron hacia los 10^{4} ciclos. Solo con 120 N en la probeta de 0,4 mm la vida teórica y la medida quedan en el mismo orden. La causa más probable es que la curva S-N está estimada a partir de S_{ut} con factores medios y no tiene en cuenta el acabado real del acuerdo ni las condiciones del montaje. Además, el resultado es muy sensible a la tensión."),
];

// ================== DOCUMENTO ==================
const cabecera = new Header({ children: [new Paragraph({ children: [new TextRun("Práctica 3. Ensayo de fatiga")] })] });
const pie = new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT] })] })] });
const vacio = () => new Paragraph({ children: [] });

const doc = new Document({
  creator: "Iván Roig Pérez",
  title: "Práctica 3. Ensayo de fatiga",
  features: { updateFields: true },
  styles: {
    default: {
      document: { run: { font: "Calibri", size: 22, language: { value: "es-ES" } }, paragraph: { spacing: { after: 160, line: 259, lineRule: LineRuleType.AUTO } } },
      heading1: { run: { font: "Calibri Light", size: 32, color: AZUL }, paragraph: { spacing: { before: 240, after: 0 }, keepNext: true, keepLines: true, outlineLevel: 0 } },
      heading2: { run: { font: "Calibri Light", size: 26, color: AZUL }, paragraph: { spacing: { before: 120, after: 0 }, keepNext: true, keepLines: true, outlineLevel: 1 } },
      title: { run: { font: "Calibri Light", size: 56, color: AZUL }, paragraph: { spacing: { after: 0 } } },
    },
    paragraphStyles: [
      { id: "Subtitle", name: "Subtitle", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: "Calibri", size: 22, color: "5A5A5A", characterSpacing: 15 }, paragraph: { spacing: { after: 160 } } },
      { id: "Caption", name: "caption", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: "Calibri", italics: true, size: 18, color: "44546A" }, paragraph: { alignment: AlignmentType.CENTER, spacing: { after: 200, line: 240, lineRule: LineRuleType.AUTO } } },
      { id: "TOCHeading", name: "TOC Heading", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: "Calibri Light", size: 32, color: AZUL }, paragraph: { spacing: { before: 240, after: 120 }, keepNext: true } },
      { id: "TOC1", name: "toc 1", basedOn: "Normal", next: "Normal", paragraph: { spacing: { after: 100 } } },
      { id: "TOC2", name: "toc 2", basedOn: "Normal", next: "Normal", paragraph: { spacing: { after: 100 }, indent: { left: 220 } } },
    ],
  },
  numbering: {
    config: [{ reference: "pasos", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 720, hanging: 360 }, spacing: { after: 80 } } } }] }],
  },
  sections: [{
    properties: {
      titlePage: true,
      page: { size: { width: 11906, height: 16838 }, margin: { top: 1417, bottom: 1417, left: 1701, right: 1701, header: 709, footer: 709 } },
    },
    headers: { default: cabecera, first: new Header({ children: [vacio()] }) },
    footers: { default: pie, first: new Footer({ children: [vacio()] }) },
    children: [...portada, ...indice, ...cuerpo],
  }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(path.join(DIR, "borrador_raw.docx"), buf);
  console.log("borrador.docx escrito", buf.length, "bytes");
});

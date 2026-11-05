// Informe de la práctica 3 (ensayo de fatiga), versión reducida, con el formato de las prácticas 1 y 2.
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
  new Paragraph({ style: "Subtitle", alignment: AlignmentType.CENTER, children: [new TextRun("Noviembre de 2026")] }),
];

// ================== ÍNDICE ==================
const indice = [
  new Paragraph({ style: "TOCHeading", pageBreakBefore: true, children: [new TextRun("Contenido")] }),
  new TableOfContents("Contenido", { hyperlink: true, headingStyleRange: "1-2" }),
];

// ================== CUERPO (versión reducida) ==================
const cuerpo = [
  H1("1. Introducción", true),
  P("El objetivo de esta práctica es ver cómo influye el radio del acuerdo del cambio de sección en la vida a fatiga de probetas de acero AISI 1010 sometidas a flexión rotativa. Se han ensayado probetas con radios de 0,4 y 0,8 mm bajo cargas de 60, 80, 100 y 120 N, y se ha anotado el número de ciclos hasta la rotura. Ese número se compara con el que da la teoría, calculado con la ecuación de Navier, la ecuación de Marin y los factores de concentración de tensiones."),

  H1("2. Fundamento teórico"),
  P("Una pieza sometida a tensiones que varían con el tiempo puede romper con tensiones menores que su resistencia a tracción, e incluso que su límite elástico. Es el fallo por fatiga. Empieza con una grieta pequeña en un punto donde se concentran las tensiones, como un cambio de sección, que crece con los ciclos hasta que la sección que queda no aguanta y la pieza rompe de golpe."),
  P("El comportamiento a fatiga se representa en el diagrama de Wöhler, con la amplitud de tensión frente al número de ciclos en escala logarítmica. En los aceros la curva se hace horizontal a partir de unos 10^{6} ciclos, en el límite de fatiga S’_{e}, que para S_{ut} ≤ 1400 MPa se estima como 0,5·S_{ut}. Para una pieza concreta se corrige con la ecuación de Marin, S_{e} = S’_{e}·k_{a}·k_{b}·k_{c}·k_{d}, cuyos factores tienen en cuenta el acabado, el tamaño, el tipo de carga y la temperatura."),
  P("En un cambio de sección la tensión real es mayor que la nominal. En fatiga se usa el factor K_{f} = 1 + q·(K_{t} - 1), donde K_{t} es el factor teórico de concentración de tensiones y q la sensibilidad a la entalla. Entre 10^{3} y 10^{6} ciclos la curva de Wöhler se aproxima por una recta en escala doble logarítmica, K_{f}·S_{n} = A·N^{B}, que pasa por f·S_{ut} a 10^{3} ciclos y por S_{e} a 10^{6}. Si K_{f}·S_{n} queda por debajo de S_{e}, la vida teórica es infinita."),
  P("En el ensayo la probeta gira empotrada por un extremo y recibe en el otro una carga F que mantiene su dirección, así que cada fibra pasa por la tracción máxima y por la compresión máxima en cada vuelta. La tensión es alternada simétrica, con tensión media nula, y su amplitud S_{n} es la que da la ecuación de Navier, σ_{th} = F·L·y_{max}/I."),

  H1("3. Material y metodología"),
  P("Se ha utilizado una máquina de fatiga por flexión rotativa con un motor de 370 W que gira a 2800 rpm, un dispositivo de carga de 0 a 300 N con escala graduada, un contador de ciclos y un protector (figura 3 del guion). Las probetas son de acero AISI 1010 mecanizado en frío, con S_{y} = 560 MPa y S_{ut} = 611 MPa. Tienen un tramo de Ø12 mm por el que se amarran y otro de Ø8 mm, unidos por un acuerdo de 0,4 mm de radio en las de tipo 1 y de 0,8 mm en las de tipo 2. La carga se aplica a L = 100,5 mm del cambio de sección."),
  P("En cada ensayo se alinea el rodamiento flotante con el eje, se amarra la probeta, se coloca el protector y, con el motor parado, se aplica la carga con la rueda. Después se pone a cero el contador y se arranca el motor, que se para solo al romper la probeta. Se ha ensayado una probeta de cada tipo con cada carga."),

  H1("4. Resultados"),
  H2("4.1 Tensión y ciclos hasta la rotura"),
  P("La tensión se calcula en el cambio de sección, sin tener en cuenta el acuerdo, con d = 8 mm, y_{max} = 4 mm e I = π·d^{4}/64 = 201,1 mm^{4}. Para 60 N:"),
  ec([sb("σ", "th"), r("="), fr([r("F·L·"), sb("y", "max")], [r("I")]), r("="), fr([r("60·"), n("100,5"), r("·4")], [n("201,1")]), r("="), n("120 MPa")]),
  P("La tensión es proporcional a la carga y es la misma en los dos tipos de probeta. La duración de cada ensayo es t = N/n, con n = 2800 rpm."),
  pieTabla("Tabla 1. Resultados del ensayo de fatiga."),
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
  hueco(),
  P("Los ciclos bajan al aumentar la carga, aunque no de forma regular (tabla 1). Con r = 0,8 mm la probeta de 80 N rompió antes que la de 100 N. La de 0,8 mm aguanta más que la de 0,4 mm con 60 y 100 N, pero menos con 80 y 120 N. Todas rompen por el cambio de sección y en pocos minutos, entre unos 4000 y 13000 ciclos."),

  H2("4.2 Número teórico de ciclos"),
  P("Con D/d = 12/8 = 1,5 y r/d = 0,05 y 0,10, en las gráficas se leen K_{t} y la sensibilidad q para S_{ut} = 611 MPa, y con ellos se obtiene K_{f} (tabla 2)."),
  pieTabla("Tabla 2. Factores de concentración de tensiones."),
  tabla([1200, 1100, 1100, 1100, 1100, 1200], ["r (mm)", "D/d", "r/d", "K_{t}", "q", "K_{f}"], [
    ["0,4", "1,5", "0,05", "2,15", "0,64", "1,736"],
    ["0,8", "1,5", "0,10", "1,75", "0,72", "1,540"],
  ]),
  hueco(),
  P("El límite de fatiga sin corregir es S’_{e} = 0,5·611 = 305,5 MPa. Para acabado mecanizado en frío k_{a} = 4,51·611^{-0,265} = 0,8239, para d = 8 mm k_{b} = 1,24·8^{-0,107} = 0,9926, y con carga de flexión y temperatura ambiente k_{c} = k_{d} = 1:"),
  ec([sb("S", "e"), r("="), n("305,5"), r("·"), n("0,8239"), r("·"), n("0,9926"), r("·1·1="), n("249,8 MPa")]),
  P("Con f = 0,861, leída para S_{ut} = 88,6 kpsi, los parámetros de la recta son:"),
  ec([r("A="), fr([sp([par([r("f·"), sb("S", "ut")])], "2")], [sb("S", "e")]), r("="), fr([sp([par([n("0,861"), r("·611")])], "2")], [n("249,8")]), r("="), n("1108 MPa")]),
  ec([r("B=−"), fr([r("1")], [r("3")]), r("·"), new MathFunction({ name: [r("log")], children: [par([fr([r("f·"), sb("S", "ut")], [sb("S", "e")])])] }), r("=−"), n("0,1078")]),
  P("La tensión es alternada simétrica y S_{n} = σ_{th}. Para r = 0,4 mm y 120 N, K_{f}·σ_{th} = 1,736·239,9 = 416,5 MPa y:"),
  ec([r("N="), sp([par([fr([sb("K", "f"), r("·"), sb("σ", "th")], [r("A")])])], [fr([r("1")], [r("B")])]), r("="), sp([par([fr([n("416,5")], [r("1108")])])], [fr([r("1")], [r("−"), n("0,1078")])]), r("="), n("8,7"), r("·"), sp("10", "3"), n(" ciclos")]),
  P("Con 60 N en las dos probetas y con 80 N en la de 0,8 mm, K_{f}·σ_{th} queda por debajo de S_{e} = 249,8 MPa y la vida teórica es infinita (tabla 3, figura 1)."),
  pieTabla("Tabla 3. Número de ciclos teórico y del ensayo."),
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
  imagen("fig_wohler.png", 12, "png", 1476, 906),
  pieFigura("Figura 1. Diagrama S-N teórico y resultados del ensayo para los dos radios."),

  H2("4.3 Comparación entre teoría y ensayo"),
  P("Las probetas rompen mucho antes de lo que predice la teoría, sobre todo con las cargas bajas, donde el cálculo da vida infinita y las probetas rompieron hacia los 10^{4} ciclos (tabla 3, figura 1). Solo con 120 N en la probeta de 0,4 mm la vida teórica y la del ensayo quedan en el mismo orden."),
  P("Los valores de K_{t}, q y f se han leído a ojo, y como N depende de la tensión elevada a 1/B = -9,3, un error del 5 % en K_{f}·σ_{th} cambia N entre un 36 y un 61 %. Eso explica diferencias de decenas por ciento, no de órdenes de magnitud. La mayor parte de la diferencia viene, probablemente, de que la curva S-N está estimada a partir de S_{ut} con factores medios y no recoge el estado real de las probetas, como una marca de mecanizado en el fondo del acuerdo o una mala alineación del rodamiento flotante. Además, cada punto es una sola probeta, y en fatiga la dispersión es grande."),

  H1("5. Conclusiones"),
  P("Según el cálculo, pasar de r = 0,4 a 0,8 mm baja K_{f} de 1,736 a 1,540 y multiplica la vida teórica por unas tres. En el ensayo esa mejora no se aprecia con claridad, seguramente por la dispersión de la fatiga con una sola probeta por carga. Convendría repetirlo con varias. La rotura se produce en el cambio de sección, que es donde el acuerdo concentra las tensiones."),
  P("La tensión de Navier crece en proporción a la carga, de 120 a 240 MPa, y queda muy por debajo del límite elástico, 560 MPa. Con el efecto de la entalla, K_{f}·σ_{th} supera el límite de fatiga corregido a partir de 80 N con r = 0,4 mm y de 100 N con r = 0,8 mm."),
  P("El cálculo con la ecuación de Marin da vidas mucho más largas que las medidas, sobre todo con cargas bajas. La causa más probable es que la curva S-N es una estimación con factores medios que no recoge el acabado real del acuerdo ni el montaje, y que el resultado es muy sensible a la tensión."),
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
  fs.writeFileSync(path.join(DIR, "reducido_raw.docx"), buf);
  console.log("reducido_raw.docx escrito", buf.length, "bytes");
});

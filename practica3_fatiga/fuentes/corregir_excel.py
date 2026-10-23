"""Corrige calculos.xlsx editando el XML (así se conservan las gráficas). Uso: python3 corregir_excel.py entrada.xlsx salida.xlsx"""
import re
import sys
import zipfile

ent, sal = sys.argv[1], sys.argv[2]
Se = 249.84915920938107
zin = zipfile.ZipFile(ent)
partes = {i.filename: zin.read(i.filename) for i in zin.infolist()}
infos = {i.filename: i for i in zin.infolist()}

def sub1(patron, nuevo, s, cuenta=1):
    s2, k = re.subn(patron, nuevo, s)
    assert k == cuenta, (patron, k)
    return s2

# --- hoja
s = partes["xl/worksheets/sheet1.xml"].decode("utf8")
s = sub1(r'<c r="F3" s="2"><v>5252</v></c>', '<c r="F3" s="2"><v>5292</v></c>', s)
for col, ref, v in [("L3", "C3", 9858), ("L4", "D3", 7533), ("L5", "E3", 5593), ("L6", "F3", 5292)]:
    s = sub1(r'<c r="%s" s="2"/>' % col, '<c r="%s" s="2"><f>%s</f><v>%d</v></c>' % (col, ref, v), s)
for fila in list(range(30, 34)) + list(range(36, 40)):
    m = re.search(r'<c r="K%d" s="2">(?:<f[^>]*/>|<f[^>]*>[^<]*</f>)<v>([^<]*)</v></c>' % fila, s)
    kf_sigma = float(m.group(1))
    m2 = re.search(r'<c r="L%d" s="2">(?:<f[^>]*/>|<f[^>]*>[^<]*</f>)<v>([^<]*)</v></c>' % fila, s)
    formula = 'IF(K%d&lt;$C$32,"Vida infinita",(K%d/H%d)^(1/I%d))' % ((fila,) * 4)
    if kf_sigma < Se:
        nuevo = '<c r="L%d" s="2" t="str"><f>%s</f><v>Vida infinita</v></c>' % (fila, formula)
    else:
        nuevo = '<c r="L%d" s="2"><f>%s</f><v>%s</v></c>' % (fila, formula, m2.group(1))
    s = s[:m2.start()] + nuevo + s[m2.end():]
partes["xl/worksheets/sheet1.xml"] = s.encode("utf8")

# --- textos de cabecera
t = partes["xl/sharedStrings.xml"].decode("utf8")
t = sub1(r'<t>MEF</t>', '<t>th</t>', t)
t = sub1(r'<si><t>Sf \(Mpa\)</t></si>', '<si><t>Kf·σth (MPa)</t></si>', t)
t = t.replace("(Mpa)", "(MPa)")
partes["xl/sharedStrings.xml"] = t.encode("utf8")

# --- caché de las gráficas
c1 = partes["xl/charts/chart1.xml"].decode("utf8")
c1 = sub1(r'<c:pt idx="3"><c:v>5252</c:v></c:pt>', '<c:pt idx="3"><c:v>5292</c:v></c:pt>', c1)
partes["xl/charts/chart1.xml"] = c1.encode("utf8")
c2 = partes["xl/charts/chart2.xml"].decode("utf8")
pts = "".join('<c:pt idx="%d"><c:v>%d</c:v></c:pt>' % (i, v) for i, v in enumerate([9858, 7533, 5593, 5292]))
c2 = sub1(r'(<c:f>Hoja1!\$L\$3:\$L\$6</c:f><c:numCache><c:formatCode>General</c:formatCode><c:ptCount val="4"/>)(</c:numCache>)',
          r'\g<1>' + pts + r'\g<2>', c2)
partes["xl/charts/chart2.xml"] = c2.encode("utf8")

# --- recálculo al abrir y fuera calcChain (Excel la rehace)
w = partes["xl/workbook.xml"].decode("utf8")
w = sub1(r'<calcPr calcId="191029"/>', '<calcPr calcId="191029" fullCalcOnLoad="1"/>', w)
partes["xl/workbook.xml"] = w.encode("utf8")
partes.pop("xl/calcChain.xml")
ct = partes["[Content_Types].xml"].decode("utf8")
ct = sub1(r'<Override PartName="/xl/calcChain.xml"[^>]*/>', '', ct)
partes["[Content_Types].xml"] = ct.encode("utf8")
rel = partes["xl/_rels/workbook.xml.rels"].decode("utf8")
rel = sub1(r'<Relationship [^>]*Target="calcChain.xml"/>', '', rel)
partes["xl/_rels/workbook.xml.rels"] = rel.encode("utf8")

with zipfile.ZipFile(sal, "w", zipfile.ZIP_DEFLATED) as zout:
    for nombre, datos in partes.items():
        zout.writestr(infos[nombre], datos)
print("escrito", sal)

from docx import Document
from docx.shared import Cm, Pt
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
d=Document("Trabajo_Taburete.docx")
for s in d.sections:
    s.page_width=Cm(21); s.page_height=Cm(29.7)
    s.left_margin=s.right_margin=Cm(2.5); s.top_margin=s.bottom_margin=Cm(2.5)
def setcell(c,text,size=8.5):
    p=c.paragraphs[0]
    for r in list(p.runs): r._r.getparent().remove(r._r)
    for extra in c.paragraphs[1:]: extra._p.getparent().remove(extra._p)
    r=p.add_run(text); r.font.size=Pt(size)
# 1) limpiar celdas duplicadas: si hay run vacío seguido de otro, y el primero tiene texto nuevo, quedarse con el primero
for t in d.tables:
    for row in t.rows:
        for c in row.cells:
            for p in c.paragraphs:
                rs=[r for r in p.runs]
                if len(rs)>=2 and rs[0].text and rs[1].text and not rs[0].bold:
                    size=rs[1].font.size
                    txt=rs[0].text
                    for r in rs: r._r.getparent().remove(r._r)
                    nr=p.add_run(txt); nr.font.size=size or Pt(8.5)
# 2) anchos de columna fijos
W={"Código|Tipo":[1.5,3,10,1.5],"Código|Requisito":[1.5,2,10.5,2],"Concepto":[6,6.5,3.5],"Producto":[3.4,3,2.6,1.5,1.3,1.8,2],
   "Especificación":[4,12],"Componente":[2.8,4.2,4.5,4.5],"Documento":[4.6,9,2.4],"Fase":[3,3.4,4.6,5],"Nº":[1,6.5,1,7.5]}
for t in d.tables:
    h=[c.text for c in t.rows[0].cells]; key=None
    for k in W:
        ks=k.split("|")
        if h[0]==ks[0] and (len(ks)==1 or h[1]==ks[1]): key=k
    ws=W[key]
    tblPr=t._tbl.tblPr
    lay=OxmlElement("w:tblLayout"); lay.set(qn("w:type"),"fixed"); tblPr.append(lay)
    tw=tblPr.find(qn("w:tblW"))
    if tw is None: tw=OxmlElement("w:tblW"); tblPr.append(tw)
    tw.set(qn("w:w"),str(int(sum(ws)/2.54*1440))); tw.set(qn("w:type"),"dxa")
    grid=t._tbl.tblGrid
    for gc,w in zip(grid.findall(qn("w:gridCol")),ws): gc.set(qn("w:w"),str(int(w/2.54*1440)))
    for row in t.rows:
        for c,w in zip(row.cells,ws): c.width=Cm(w)
    t.autofit=False
    print(key,len(t.rows))
d.save("Trabajo_Taburete.docx")
# comprobar celdas concretas
d=Document("Trabajo_Taburete.docx")
for t in d.tables:
    for row in t.rows:
        if row.cells[0].text in ("P2","P5","P6","P12") or row.cells[0].text.startswith(("Real Decreto 1468","Reglamento (UE) 2025","Reglamento (CE) 1907")):
            print([c.text[:70] for c in row.cells])

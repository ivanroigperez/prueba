"""Convierte las MathRun marcadas con §N§ en texto normal de ecuación (m:nor) y escribe el .docx final."""
import re
import sys
import zipfile

ent, sal = sys.argv[1], sys.argv[2]
with zipfile.ZipFile(ent) as zin, zipfile.ZipFile(sal, "w", zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == "word/document.xml":
            s = data.decode("utf8")
            s, k = re.subn(r'<m:r><m:t(?: xml:space="preserve")?>§N§([^<]*)</m:t></m:r>',
                           r'<m:r><m:rPr><m:nor/></m:rPr><m:t xml:space="preserve">\1</m:t></m:r>', s)
            assert "§N§" not in s, "quedan marcas sin convertir"
            print("runs de texto normal:", k)
            data = s.encode("utf8")
        zout.writestr(item, data)

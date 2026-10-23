"""Abre el .docx en LibreOffice, actualiza el índice y los campos, y guarda .docx y .pdf.
Uso: python3 actualizar_y_exportar.py entrada.docx salida.docx salida.pdf"""
import os
import subprocess
import sys
import tempfile
import time

import uno
from com.sun.star.beans import PropertyValue


def prop(nombre, valor):
    p = PropertyValue()
    p.Name, p.Value = nombre, valor
    return p


def main(entrada, salida_docx, salida_pdf):
    perfil = tempfile.mkdtemp(prefix="lo_perfil_")
    tubo = "p3fatiga_%d" % os.getpid()
    env = dict(os.environ, SAL_USE_VCLPLUGIN="svp")
    proc = subprocess.Popen(
        ["soffice", "-env:UserInstallation=file://" + perfil, "--headless", "--invisible", "--nologo",
         "--norestore", "--accept=pipe,name=%s;urp;StarOffice.ComponentContext" % tubo],
        env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        local = uno.getComponentContext()
        resolver = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
        ctx = None
        for _ in range(60):
            try:
                ctx = resolver.resolve("uno:pipe,name=%s;urp;StarOffice.ComponentContext" % tubo)
                break
            except Exception:
                time.sleep(0.5)
        if ctx is None:
            raise RuntimeError("No se pudo conectar con LibreOffice")
        desktop = ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
        doc = desktop.loadComponentFromURL(uno.systemPathToFileUrl(os.path.abspath(entrada)), "_blank", 0,
                                           (prop("Hidden", True),))
        # Dos pasadas: la primera fija la paginación con el índice ya lleno y la segunda corrige los números
        for _ in range(2):
            indices = doc.getDocumentIndexes()
            for i in range(indices.getCount()):
                indices.getByIndex(i).update()
            doc.getTextFields().refresh()
            doc.refresh()
        doc.storeToURL(uno.systemPathToFileUrl(os.path.abspath(salida_docx)), (prop("FilterName", "MS Word 2007 XML"),))
        doc.storeToURL(uno.systemPathToFileUrl(os.path.abspath(salida_pdf)), (prop("FilterName", "writer_pdf_Export"),))
        print("índices actualizados:", doc.getDocumentIndexes().getCount())
        doc.close(True)
        try:
            desktop.terminate()
        except Exception:
            pass
    finally:
        try:
            proc.wait(timeout=20)
        except subprocess.TimeoutExpired:
            proc.kill()


if __name__ == "__main__":
    main(*sys.argv[1:4])

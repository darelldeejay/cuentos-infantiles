#!/usr/bin/env python3
"""Genera libro/cuentos-olivia-y-liliana.pdf con todos los cuentos, listo para imprimir.

Uso:
    pip install markdown
    python3 herramientas/generar_pdf.py

Necesita Chromium o Google Chrome. Si no lo encuentra, indica la ruta con CHROME=/ruta/al/navegador.
"""
import glob
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile

import markdown

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join(RAIZ, "libro", "cuentos-olivia-y-liliana.pdf")

CSS = """
@font-face { font-family: Andika; font-weight: 400; src: url(herramientas/fuentes/Andika-Regular.woff2); }
@font-face { font-family: Andika; font-weight: 700; src: url(herramientas/fuentes/Andika-Bold.woff2); }
@font-face { font-family: Fredoka; font-weight: 600; src: url(herramientas/fuentes/Fredoka-SemiBold.woff2); }

@page { size: A4; margin: 16mm 18mm 18mm; }
@page :first { margin: 0; @bottom-center { content: none; } }
@page { @bottom-center { content: counter(page); font-family: Andika; font-size: 11pt; color: #8a7a66; } }

* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; font-family: Andika, sans-serif; font-size: 15pt; line-height: 1.45; color: #2b2320; }
h1, h2, h3 { font-family: Fredoka, Andika, sans-serif; font-weight: 600; line-height: 1.15; }
p { margin: 0 0 .3em; }

.portada { height: 297mm; display: flex; flex-direction: column; background: #f6ecd9; break-after: page; }
.portada img { width: 100%; height: 175mm; object-fit: cover; display: block; }
.portada .textos { flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 0 20mm; }
.portada h1 { font-size: 38pt; margin: 0 0 6mm; color: #7a3b1d; }
.portada p { font-size: 15pt; color: #6b5a48; margin: 0; }

.indice { break-after: page; }
.indice h1 { font-size: 28pt; color: #7a3b1d; margin: 0 0 8mm; }
.indice ol { padding-left: 0; list-style: none; margin: 0; }
.indice li { padding: 5mm 0; border-bottom: 1px dashed #d8c7ad; }
.indice li b { font-family: Fredoka; font-weight: 600; font-size: 17pt; color: #2b2320; }
.indice li span { display: block; font-size: 12.5pt; color: #6b5a48; }

.cuento-titulo { break-before: page; text-align: center; padding-top: 70mm; break-after: page; }
.cuento-titulo .num { font-family: Fredoka; font-size: 16pt; color: #b0703f; letter-spacing: .1em; }
.cuento-titulo h1 { font-size: 36pt; color: #7a3b1d; margin: 4mm 0 8mm; }
.cuento-titulo .meta { font-size: 13pt; color: #6b5a48; }

.capitulo { break-before: page; }
.capitulo img { width: 100%; height: 86mm; object-fit: cover; border-radius: 4mm; display: block; margin-bottom: 4mm; }
.capitulo.largo img { height: 64mm; }
.capitulo h2 { font-size: 21pt; color: #7a3b1d; margin: 0 0 3mm; }

.cierre { break-before: page; }
.cierre blockquote { margin: 0 0 8mm; padding: 6mm 8mm; background: #fff4d6; border: 2px solid #e8c56b; border-radius: 4mm; }
.cierre blockquote h3 { margin: 0 0 3mm; font-size: 20pt; color: #7a3b1d; }
.cierre h3 { font-size: 17pt; color: #7a3b1d; margin: 6mm 0 3mm; }
.cierre table { width: 100%; border-collapse: collapse; font-size: 12.5pt; line-height: 1.4; margin-bottom: 6mm; }
.cierre th, .cierre td { text-align: left; vertical-align: top; padding: 2.5mm 3mm; border-bottom: 1px solid #e3d5bf; }
.cierre th { background: #f6ecd9; font-family: Fredoka; font-weight: 600; }
.cierre td:first-child { width: 38%; font-weight: 700; }

.reparto { break-after: page; }
.reparto h2 { font-size: 24pt; color: #7a3b1d; margin: 0 0 6mm; }
.reparto .fichas { display: grid; grid-template-columns: 1fr 1fr; column-gap: 10mm; }
.reparto .ficha { padding: 4mm 0; border-bottom: 1px dashed #d8c7ad; break-inside: avoid; }
.reparto .ficha b { font-family: Fredoka; font-weight: 600; font-size: 17pt; color: #7a3b1d; }
.reparto .ficha p { font-size: 13pt; line-height: 1.45; margin: 1mm 0 0; }
.reparto .ficha .aspecto { color: #6b5a48; }
"""


def md(texto):
    return markdown.markdown(texto, extensions=["tables"])


def leer_personajes():
    """Devuelve ({nombre: (quién es, cómo es)}, {número de cuento: [nombres]}) desde PERSONAJES.md."""
    texto = open(os.path.join(RAIZ, "PERSONAJES.md"), encoding="utf-8").read()
    fichas = {}
    for nombre, quien, como in re.findall(r"^\| \*\*(.+?)\*\* \| (.+?) \| (.+?) \|$", texto, re.M):
        fichas[nombre] = (quien, "" if como.strip() in ("—", "-") else como)
    apariciones = {}
    for num, nombres in re.findall(r"^\| (\d+) · .+? \| (.+?) \|$", texto, re.M):
        apariciones[int(num)] = [n.strip() for n in nombres.split(",")]
    return fichas, apariciones


def reparto_html(nombres, fichas):
    filas = []
    for nombre in nombres:
        if nombre not in fichas:
            sys.exit(f"PERSONAJES.md: «{nombre}» sale en Apariciones pero no tiene ficha")
        quien, como = fichas[nombre]
        aspecto = f'<p class="aspecto">{html.escape(como)}</p>' if como else ""
        filas.append(f'<div class="ficha"><b>{html.escape(nombre)}</b><p>{html.escape(quien)}</p>{aspecto}</div>')
    return f'<section class="reparto"><h2>Los personajes de este cuento</h2><div class="fichas">{"".join(filas)}</div></section>'


def cuento_a_html(num, ruta, fichas, apariciones):
    carpeta = os.path.relpath(os.path.dirname(ruta), RAIZ)
    texto = open(ruta, encoding="utf-8").read()
    # Las imágenes van relativas al cuento; el HTML se genera en la raíz.
    texto = re.sub(r"\]\((imagenes/[^)]+)\)", lambda m: f"]({carpeta}/{m.group(1)})", texto)

    titulo = re.search(r"^# (.+)$", texto, re.M).group(1).strip()
    meta = re.search(r"^> (⏱️.+)$", texto, re.M)
    meta = meta.group(1).strip() if meta else ""

    # Capítulos: desde el primer "## " hasta el primer "---" que les sigue.
    cuerpo = texto[texto.index("\n## "):]
    capitulos_txt, _, cierre_txt = cuerpo.partition("\n---\n")
    capitulos = re.split(r"\n(?=## )", capitulos_txt.strip())
    cierre_txt = cierre_txt.replace("\n---\n", "\n")

    partes = [
        f'<section class="cuento-titulo"><div class="num">CUENTO {num}</div>'
        f"<h1>{html.escape(titulo)}</h1><div class=\"meta\">{html.escape(meta)}</div></section>"
    ]
    if num in apariciones:
        partes.append(reparto_html(apariciones[num], fichas))
    for cap in capitulos:
        # Capítulo largo: imagen más baja para que quepa en una sola página.
        clase = "capitulo largo" if len(cap.split()) > 180 else "capitulo"
        partes.append(f'<section class="{clase}">{md(cap)}</section>')
    partes.append(f'<section class="cierre">{md(cierre_txt)}</section>')

    tema = re.search(r"🌍 Tema: ([^·\n]+)", meta)
    return titulo, (tema.group(1).strip() if tema else ""), "\n".join(partes), f"{carpeta}/imagenes"


def buscar_chrome():
    if os.environ.get("CHROME"):
        return os.environ["CHROME"]
    for nombre in ("chromium", "chromium-browser", "google-chrome", "chrome"):
        if shutil.which(nombre):
            return shutil.which(nombre)
    candidatos = sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux*/chrome"))
    if candidatos:
        return candidatos[-1]
    sys.exit("No encuentro Chromium ni Chrome. Indica la ruta con CHROME=/ruta/al/navegador.")


def main():
    rutas = sorted(glob.glob(os.path.join(RAIZ, "cuentos", "*", "cuento.md")))
    if not rutas:
        sys.exit("No hay cuentos en cuentos/*/cuento.md")

    fichas, apariciones = leer_personajes()
    cuentos = [cuento_a_html(int(os.path.basename(os.path.dirname(r))[:2]), r, fichas, apariciones) for r in rutas]
    portada = sorted(glob.glob(os.path.join(RAIZ, cuentos[0][3], "*.jpg")))[0]

    indice = "".join(
        f"<li><b>{i}. {html.escape(t)}</b><span>{html.escape(tema)}</span></li>"
        for i, (t, tema, _, _) in enumerate(cuentos, 1)
    )

    documento = f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>Cuentos para Olivia y Liliana</title><style>{CSS}</style></head><body>
<section class="portada"><img src="{os.path.relpath(portada, RAIZ)}">
<div class="textos"><h1>Cuentos para Olivia y Liliana</h1>
<p>{len(cuentos)} {"cuento ilustrado" if len(cuentos) == 1 else "cuentos ilustrados"}</p></div></section>
<section class="indice"><h1>Índice</h1><ol>{indice}</ol></section>
{"".join(c[2] for c in cuentos)}
</body></html>"""

    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".html", dir=RAIZ, delete=False, encoding="utf-8") as f:
        f.write(documento)
        temporal = f.name
    try:
        subprocess.run(
            [buscar_chrome(), "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
             f"--print-to-pdf={SALIDA}", "file://" + temporal],
            check=True, capture_output=True,
        )
    finally:
        os.remove(temporal)
    print(f"PDF generado: {os.path.relpath(SALIDA, RAIZ)} ({len(cuentos)} cuentos)")


if __name__ == "__main__":
    main()

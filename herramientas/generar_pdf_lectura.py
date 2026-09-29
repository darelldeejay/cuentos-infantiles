#!/usr/bin/env python3
"""Genera un PDF por cada libro de aprendo-a-leer/, listo para imprimir.

Uso:
    pip install markdown
    python3 herramientas/generar_pdf_lectura.py

Antes de generar, comprueba que todas las palabras del cuento usan solo las
letras del nivel (la línea "- letras:" de cada libro.md). Si alguna no, avisa
y no genera ese libro.

Necesita Chromium o Google Chrome. Si no lo encuentra, indica la ruta con CHROME=/ruta/al/navegador.
"""
import glob
import html
import os
import re
import subprocess
import sys
import tempfile
import unicodedata

import markdown

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generar_pdf import buscar_chrome  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = """
@font-face { font-family: Andika; font-weight: 400; src: url(herramientas/fuentes/Andika-Regular.woff2); }
@font-face { font-family: Andika; font-weight: 700; src: url(herramientas/fuentes/Andika-Bold.woff2); }
@font-face { font-family: Fredoka; font-weight: 600; src: url(herramientas/fuentes/Fredoka-SemiBold.woff2); }

@page { size: A4 landscape; margin: 12mm 16mm 14mm; }
@page :first { margin: 0; }

* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; font-family: Andika, sans-serif; color: #2b2320; }

.pagina { height: 184mm; break-after: page; display: flex; flex-direction: column; align-items: center; }
.pagina:last-child { break-after: auto; }

.portada { height: 210mm; background: #fde9e4; justify-content: center; gap: 8mm; padding: 12mm; }
.portada img { height: 125mm; border-radius: 5mm; }
.portada h1 { font-family: Andika; font-weight: 700; font-size: 60pt; letter-spacing: .12em; margin: 0; color: #b33a2b; }

.leer img { height: 128mm; max-width: 100%; object-fit: cover; border-radius: 5mm; }
.leer .frase { flex: 1; display: flex; align-items: center; justify-content: center; text-align: center;
  font-size: 40pt; line-height: 1.3; letter-spacing: .06em; word-spacing: .35em; padding: 0 4mm; white-space: nowrap; }
.leer .num { font-size: 12pt; color: #b09a86; }

.practica { justify-content: center; text-align: center; }
.practica h2 { font-family: Fredoka; font-weight: 600; font-size: 22pt; color: #b33a2b; margin: 0 0 10mm; letter-spacing: .06em; }
.letras { font-size: 72pt; letter-spacing: .35em; line-height: 1.5; }
.letras div { white-space: nowrap; }
.letras .voc { color: #b33a2b; }
.silabas { border-collapse: separate; border-spacing: 8mm 4mm; font-size: 40pt; letter-spacing: .06em; }
.silabas td { padding: 1mm 4mm; border-bottom: 2px dotted #e2c9b8; }
.palabras { display: flex; flex-wrap: wrap; justify-content: center; gap: 6mm 16mm; font-size: 38pt; letter-spacing: .06em; max-width: 250mm; }

.guia { font-size: 13pt; line-height: 1.5; max-width: 230mm; align-items: stretch; justify-content: center; }
.guia h2 { font-family: Fredoka; font-weight: 600; font-size: 20pt; color: #b33a2b; margin: 0 0 5mm; }
.guia p { margin: 0 0 4mm; }
.guia .letras-nivel { font-size: 12pt; color: #6b5a48; }
"""

VOCALES = set("AEIOU")


def base(letra):
    """Letra sin tilde ni diéresis: Á -> A, Ü -> U. La Ñ se queda como Ñ."""
    if letra == "Ñ":
        return letra
    return unicodedata.normalize("NFD", letra)[0]


def secciones(texto):
    partes = re.split(r"^## (.+)$", texto, flags=re.M)
    return {partes[i].strip(): partes[i + 1].strip() for i in range(1, len(partes), 2)}


def paginas_cuento(bloque):
    paginas = []
    for trozo in re.split(r"\n\s*\n", bloque):
        img = re.search(r"!\[[^\]]*\]\(([^)]+)\)", trozo)
        frase = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", trozo).strip()
        if img and frase:
            paginas.append((img.group(1), frase))
    return paginas


def comprobar(frases, permitidas):
    fallos = []
    for frase in frases:
        if frase != frase.upper():
            fallos.append(f"«{frase}» no está en mayúsculas")
        for palabra in re.findall(r"[^\W\d_]+", frase):
            raras = sorted({base(c) for c in palabra} - permitidas)
            if raras:
                fallos.append(f"«{palabra}» usa letras fuera del nivel: {' '.join(raras)}")
    return fallos


def libro_a_html(ruta):
    carpeta = os.path.relpath(os.path.dirname(ruta), RAIZ)
    texto = open(ruta, encoding="utf-8").read()
    titulo = re.search(r"^# (.+)$", texto, re.M).group(1).strip()
    letras = re.search(r"^- letras:\s*(.+)$", texto, re.M).group(1).split()
    permitidas = set(letras)
    s = secciones(texto)
    paginas = paginas_cuento(s["Cuento"])

    fallos = comprobar([f for _, f in paginas] + [titulo], permitidas)
    if fallos:
        return titulo, None, fallos

    img = lambda r: f"{carpeta}/{r}"  # noqa: E731
    out = [f'<section class="pagina portada"><img src="{img(paginas[0][0])}"><h1>{html.escape(titulo)}</h1></section>']

    vocales = " ".join(f'<span class="voc">{l}</span>' for l in letras if l in VOCALES)
    consonantes = " ".join(l for l in letras if l not in VOCALES)
    out.append(f'<section class="pagina practica"><h2>LAS LETRAS</h2><div class="letras">'
               f"<div>{vocales}</div><div>{consonantes}</div></div></section>")
    filas = "".join("<tr>" + "".join(f"<td>{html.escape(x)}</td>" for x in fila.split()) + "</tr>"
                    for fila in s["Sílabas"].splitlines() if fila.strip())
    out.append(f'<section class="pagina practica"><h2>LAS SÍLABAS</h2><table class="silabas">{filas}</table></section>')
    palabras = "".join(f"<span>{html.escape(p.strip())}</span>" for p in s["Palabras"].split("·"))
    out.append(f'<section class="pagina practica"><h2>LAS PALABRAS</h2><div class="palabras">{palabras}</div></section>')

    for n, (ruta_img, frase) in enumerate(paginas, 1):
        out.append(f'<section class="pagina leer"><img src="{img(ruta_img)}">'
                   f'<div class="frase">{"<br>".join(html.escape(f) for f in re.split(r"(?<=[.!?]) ", frase))}</div><div class="num">{n}</div></section>')

    guia = markdown.markdown(s["Guía para mamá y papá"])
    out.append(f'<section class="pagina guia"><h2>Guía para mamá y papá</h2>'
               f'<p class="letras-nivel">Letras de este libro: {" ".join(letras)}. '
               f"Todas las palabras del cuento se pueden leer solo con ellas.</p>{guia}</section>")

    documento = (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{html.escape(titulo)}</title>'
                 f"<style>{CSS}</style></head><body>{''.join(out)}</body></html>")
    return titulo, documento, []


def main():
    rutas = sorted(glob.glob(os.path.join(RAIZ, "aprendo-a-leer", "*", "libro.md")))
    if not rutas:
        sys.exit("No hay libros en aprendo-a-leer/*/libro.md")
    chrome = buscar_chrome()
    error = False
    for ruta in rutas:
        titulo, documento, fallos = libro_a_html(ruta)
        if fallos:
            error = True
            print(f"✗ {titulo}:\n  " + "\n  ".join(fallos))
            continue
        salida = os.path.join(os.path.dirname(ruta), os.path.basename(os.path.dirname(ruta)) + ".pdf")
        with tempfile.NamedTemporaryFile("w", suffix=".html", dir=RAIZ, delete=False, encoding="utf-8") as f:
            f.write(documento)
            temporal = f.name
        try:
            subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                            f"--print-to-pdf={salida}", "file://" + temporal], check=True, capture_output=True)
        finally:
            os.remove(temporal)
        print(f"✓ {titulo}: {os.path.relpath(salida, RAIZ)}")
    sys.exit(1 if error else 0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Genera libro/cuentos-olivia-y-liliana.pdf con todos los cuentos, listo para imprimir.

Uso:
    pip install markdown
    python3 herramientas/generar_pdf.py          # libro completo, con portada
    python3 herramientas/generar_pdf.py 5 6      # solo los cuentos 5 y 6, para imprimir:
                                                 # índice completo + esos cuentos
                                                 # (libro/cuentos-05-06.pdf)

Necesita Chromium o Google Chrome. Si no lo encuentra, indica la ruta con CHROME=/ruta/al/navegador.
"""
import glob
import html
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile

import markdown

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Desde este cuento se usa el formato compacto: portadilla junto al capítulo 1 y
# moraleja junto a los personajes, para gastar menos hojas al imprimir.
COMPACTO_DESDE = 7
SALIDA = os.path.join(RAIZ, "libro", "cuentos-olivia-y-liliana.pdf")

CSS = """
@font-face { font-family: Andika; font-weight: 400; src: url(herramientas/fuentes/Andika-Regular.woff2); }
@font-face { font-family: Andika; font-weight: 700; src: url(herramientas/fuentes/Andika-Bold.woff2); }
@font-face { font-family: Fredoka; font-weight: 600; src: url(herramientas/fuentes/Fredoka-SemiBold.woff2); }

@page { size: A4; margin: 16mm 18mm 18mm; }
@page portada { margin: 0; @bottom-center { content: none; } }
@page { @bottom-center { content: counter(page); font-family: Andika; font-size: 11pt; color: #8a7a66; } }

* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; font-family: Andika, sans-serif; font-size: 15pt; line-height: 1.45; color: #2b2320; }
h1, h2, h3 { font-family: Fredoka, Andika, sans-serif; font-weight: 600; line-height: 1.15; }
p { margin: 0 0 .3em; }

.portada { page: portada; height: 297mm; display: flex; flex-direction: column; background: #f6ecd9; break-after: page; }
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
.capitulo.extenso { font-size: 12pt; line-height: 1.38; }
.capitulo.extenso img { width: auto; height: 84mm; max-width: 100%; object-fit: contain; margin: 0 auto 4mm; }
.capitulo.extenso p { margin: 0 0 .28em; }
.indice li i { font-style: normal; font-size: 11pt; color: #b0703f; margin-left: 3mm; }
.capitulo h2 { font-size: 21pt; color: #7a3b1d; margin: 0 0 3mm; }

.cierre { break-before: page; }
.cierre blockquote { margin: 0 0 8mm; padding: 6mm 8mm; background: #fff4d6; border: 2px solid #e8c56b; border-radius: 4mm; }
.cierre blockquote h3 { margin: 0 0 3mm; font-size: 20pt; color: #7a3b1d; }
.cierre h3 { font-size: 17pt; color: #7a3b1d; margin: 6mm 0 3mm; }
.cierre table { width: 100%; border-collapse: collapse; font-size: 12.5pt; line-height: 1.4; margin-bottom: 6mm; }
.cierre th, .cierre td { text-align: left; vertical-align: top; padding: 2.5mm 3mm; border-bottom: 1px solid #e3d5bf; }
.cierre th { background: #f6ecd9; font-family: Fredoka; font-weight: 600; }
.cierre td:first-child { width: 38%; font-weight: 700; }

.personajes { break-before: page; }
.personajes h1 { font-size: 26pt; color: #7a3b1d; margin: 0 0 4mm; }
.personajes h2 { font-size: 17pt; color: #7a3b1d; margin: 6mm 0 2mm; break-after: avoid; }
.personajes table { width: 100%; border-collapse: collapse; font-size: 12pt; line-height: 1.4; break-inside: avoid; }
.personajes th, .personajes td { text-align: left; vertical-align: top; padding: 2.5mm 3mm; border-bottom: 1px solid #e3d5bf; }
.personajes th { background: #f6ecd9; font-family: Fredoka; font-weight: 600; }
.personajes td:first-child { width: 22%; font-weight: 700; }

/* Formato compacto (desde el cuento 07): menos hojas al imprimir. */
.cabecera { text-align: center; margin: 0 0 4mm; padding-bottom: 3mm; border-bottom: 1px dashed #d8c7ad; }
.cabecera .num { font-family: Fredoka; font-size: 11pt; color: #b0703f; letter-spacing: .1em; }
.cabecera h1 { font-size: 24pt; color: #7a3b1d; margin: 1mm 0 1.5mm; }
.cabecera .meta { font-size: 10pt; color: #6b5a48; }
.capitulo.extenso.primero img { height: 70mm; }
.capitulo.extenso.denso { font-size: 11.5pt; line-height: 1.32; }
.capitulo.extenso.denso img { height: 76mm; }
.capitulo.extenso.denso p { margin: 0 0 .18em; }
.final { break-before: page; }
.final .cierre, .final .personajes { break-before: auto; }
.final .cierre blockquote { margin: 0 0 4mm; padding: 4mm 6mm; }
.final .cierre blockquote h3 { font-size: 16pt; margin: 0 0 2mm; }
.final .cierre blockquote p { font-size: 12pt; }
.final .cierre h3 { font-size: 14pt; margin: 3mm 0 2mm; }
.final .cierre table, .final .personajes table { font-size: 9.5pt; line-height: 1.25; margin-bottom: 2mm; }
.final .cierre th, .final .cierre td, .final .personajes th, .final .personajes td { padding: 1mm 2mm; }
.final .cierre p { font-size: 11.5pt; margin: 0 0 2mm; }
.final .personajes { margin-top: 5mm; }
.final .personajes h1 { font-size: 18pt; margin: 0 0 2mm; }
.final .personajes h2 { font-size: 13pt; margin: 3mm 0 1.5mm; }
.final .fichas { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 2mm 4mm; }
.final .ficha { border: 1px solid #e3d5bf; border-radius: 2mm; padding: 1.5mm 2.5mm; break-inside: avoid; }
.final .ficha b { font-family: Fredoka; font-weight: 600; font-size: 11pt; color: #7a3b1d; }
.final .ficha p { font-size: 8.5pt; line-height: 1.3; margin: .5mm 0 0; }
.final .ficha .aspecto { color: #6b5a48; }
.final .ficha.otro { border-style: dashed; }
.final .ficha span { font-size: 8pt; color: #b0703f; margin-left: 2mm; }
"""


def md(texto):
    return markdown.markdown(texto, extensions=["tables"])


def leer_personajes():
    """Lee PERSONAJES.md.

    Devuelve ({nombre: (grupo, quién es, cómo es)}, {número de cuento: [nombres]}).
    El grupo es el título de la sección donde está el personaje (Protagonistas, Amigas u Otros personajes).
    """
    texto = open(os.path.join(RAIZ, "PERSONAJES.md"), encoding="utf-8").read()
    fichas = {}
    for grupo, cuerpo in re.findall(r"^## (.+?)\n(.*?)(?=^## |\Z)", texto, re.M | re.S):
        for nombre, quien, como in re.findall(r"^\| \*\*(.+?)\*\* \| (.+?) \| (.+?) \|$", cuerpo, re.M):
            fichas[nombre] = (grupo.strip(), quien, "" if como.strip() in ("—", "-") else como)
    apariciones = {}
    for num, nombres in re.findall(r"^\| (\d+) · .+? \| (.+?) \|$", texto, re.M):
        apariciones[int(num)] = [n.strip() for n in nombres.split(",")]
    return fichas, apariciones


def personajes_html(nombres, fichas, compacto=False):
    """Páginas «Personajes» y «Otros personajes» del final de un cuento, solo con los que salen en él."""
    grupos = {}
    for nombre in nombres:
        if nombre not in fichas:
            sys.exit(f"PERSONAJES.md: «{nombre}» sale en Apariciones pero no tiene ficha")
        grupo, quien, como = fichas[nombre]
        grupos.setdefault(grupo, []).append((nombre, quien, como))

    def tabla(filas):
        cuerpo = "".join(f"<tr><td>{html.escape(n)}</td><td>{html.escape(q)}</td><td>{html.escape(c) or '—'}</td></tr>"
                         for n, q, c in filas)
        return f"<table><tr><th>Personaje</th><th>Quién es</th><th>Cómo es</th></tr>{cuerpo}</table>"

    if compacto:
        # Fichas pequeñas en tres columnas: caben en la misma hoja que la moraleja.
        # Todos en la misma cuadrícula; los «otros personajes» van al final, con borde de puntos.
        def ficha(n, q, c, otro):
            return (f'<div class="ficha{" otro" if otro else ""}"><b>{html.escape(n)}</b>'
                    + ('<span>otro personaje</span>' if otro else "")
                    + f'<p>{html.escape(q)}</p>' + (f'<p class="aspecto">{html.escape(c)}</p>' if c else "") + "</div>")
        tarjetas = [ficha(n, q, c, False) for g, filas in grupos.items() if g != "Otros personajes" for n, q, c in filas]
        tarjetas += [ficha(n, q, c, True) for n, q, c in grupos.get("Otros personajes", [])]
        titulo = "Personajes y otros personajes" if "Otros personajes" in grupos else "Personajes"
        return f'<section class="personajes"><h1>{titulo}</h1><div class="fichas">{"".join(tarjetas)}</div></section>'

    partes = ["<h1>Personajes</h1>"]
    for grupo, filas in grupos.items():
        if grupo != "Otros personajes":
            partes.append(f"<h2>{html.escape(grupo)}</h2>{tabla(filas)}")
    if "Otros personajes" in grupos:
        partes.append(f"<h2>Otros personajes</h2>{tabla(grupos['Otros personajes'])}")
    return f'<section class="personajes">{"".join(partes)}</section>'


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

    compacto = num >= COMPACTO_DESDE
    titulo_html = (f'<div class="num">CUENTO {num}</div>'
                   f"<h1>{html.escape(titulo)}</h1><div class=\"meta\">{html.escape(meta)}</div>")
    partes = [] if compacto else [f'<section class="cuento-titulo">{titulo_html}</section>']
    for i, cap in enumerate(capitulos):
        # Capítulo largo: imagen más baja para que quepa en una sola página.
        # Capítulo extenso (cuentos desde el 05): letra más pequeña para que entre más texto por página.
        palabras = len(cap.split())
        clase = "capitulo extenso" if palabras > 200 else "capitulo largo" if palabras > 180 else "capitulo"
        # Capítulo con mucho diálogo (muchas líneas cortas): letra al mínimo (11,5 pt) para que no se desborde.
        parrafos = [t for t in cap.split("\n\n")[1:] if t.strip() and not t.startswith("![")]
        if "extenso" in clase and sum(math.ceil(len(t) / 95) for t in parrafos) >= 24:
            clase += " denso"
        cabecera = ""
        if compacto and i == 0:
            clase += " primero"
            cabecera = f'<header class="cabecera">{titulo_html}</header>'
        partes.append(f'<section class="{clase}">{cabecera}{md(cap)}</section>')
    cierre = f'<section class="cierre">{md(cierre_txt)}</section>'
    personajes = personajes_html(apariciones[num], fichas, compacto) if num in apariciones else ""
    partes.append(f'<div class="final">{cierre}{personajes}</div>' if compacto else cierre + personajes)

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

    numero = lambda r: int(os.path.basename(os.path.dirname(r))[:2])  # noqa: E731
    elegidos = {int(a) for a in sys.argv[1:]}
    if elegidos - {numero(r) for r in rutas}:
        sys.exit(f"No existen los cuentos: {sorted(elegidos - {numero(r) for r in rutas})}")

    fichas, apariciones = leer_personajes()
    cuentos = [(numero(r), *cuento_a_html(numero(r), r, fichas, apariciones)) for r in rutas]

    # El índice siempre lista todos los cuentos; los que van en este PDF se marcan como nuevos.
    indice = "".join(
        f"<li><b>{n}. {html.escape(t)}</b>{'<i>★ nuevo</i>' if n in elegidos else ''}<span>{html.escape(tema)}</span></li>"
        for n, t, tema, _, _ in cuentos
    )
    if elegidos:
        salida = os.path.join(RAIZ, "libro", "cuentos-" + "-".join(f"{n:02d}" for n in sorted(elegidos)) + ".pdf")
        cabecera = ""
        incluidos = [c for c in cuentos if c[0] in elegidos]
    else:
        salida = SALIDA
        portada = sorted(glob.glob(os.path.join(RAIZ, cuentos[0][4], "*.jpg")))[0]
        cabecera = (f'<section class="portada"><img src="{os.path.relpath(portada, RAIZ)}">'
                    f'<div class="textos"><h1>Cuentos para Olivia y Liliana</h1>'
                    f'<p>{len(cuentos)} {"cuento ilustrado" if len(cuentos) == 1 else "cuentos ilustrados"}</p></div></section>')
        incluidos = cuentos

    documento = f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>Cuentos para Olivia y Liliana</title><style>{CSS}</style></head><body>
{cabecera}
<section class="indice"><h1>Índice</h1><ol>{indice}</ol></section>
{"".join(c[3] for c in incluidos)}
</body></html>"""

    os.makedirs(os.path.dirname(salida), exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".html", dir=RAIZ, delete=False, encoding="utf-8") as f:
        f.write(documento)
        temporal = f.name
    try:
        subprocess.run(
            [buscar_chrome(), "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
             f"--print-to-pdf={salida}", "file://" + temporal],
            check=True, capture_output=True,
        )
    finally:
        os.remove(temporal)
    print(f"PDF generado: {os.path.relpath(salida, RAIZ)} ({len(incluidos)} cuentos)")


if __name__ == "__main__":
    main()

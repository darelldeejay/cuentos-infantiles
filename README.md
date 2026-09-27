# 📚 Cuentos para Olivia y Liliana

Cuentos ilustrados escritos para que los lea Olivia (7 años), protagonizados por ella, su hermana Liliana (5 años) y sus amigas.

Cada cuento se lee en unos 9–11 minutos, está dividido en capítulos cortos con una ilustración cada uno y termina con una moraleja.

## Cuentos

| # | Título | Tema | Moraleja | Lectura |
|---|---|---|---|---|
| 1 | [El globo que solo contestaba preguntas](cuentos/01-el-globo-que-solo-contestaba-preguntas/cuento.md) | El mundo: Amazonas, Egipto, Japón, Antártida | Quien se atreve a preguntar descubre el mundo entero | ~10 min |

## 🖨️ Libro para imprimir

Todos los cuentos juntos, con portada, índice y un capítulo por página (A4): [`libro/cuentos-olivia-y-liliana.pdf`](libro/cuentos-olivia-y-liliana.pdf).

Para regenerarlo después de añadir un cuento:

```
pip install markdown
python3 herramientas/generar_pdf.py
```

Necesita Chromium o Google Chrome instalado.

## Cómo está organizado

```
cuentos/
  NN-titulo-del-cuento/
    cuento.md       texto del cuento
    imagenes/       ilustraciones (JPG)
PLANTILLA.md        reglas fijas para escribir cada cuento
PERSONAJES.md       quién es quién y cómo se dibuja a cada personaje
libro/              el PDF con todos los cuentos
herramientas/       script que genera el PDF y sus tipografías
```

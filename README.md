# 📚 Cuentos para Olivia y Liliana

Cuentos ilustrados escritos para que los lea Olivia (7 años), protagonizados por ella, su hermana Liliana (5 años) y sus amigas.

Cada cuento se lee en unos 9–11 minutos, está dividido en capítulos cortos con una ilustración cada uno y termina con una moraleja.

## Cuentos

| # | Título | Tema | Moraleja | Lectura |
|---|---|---|---|---|
| 1 | [El globo que solo contestaba preguntas](cuentos/01-el-globo-que-solo-contestaba-preguntas/cuento.md) | El mundo: Amazonas, Egipto, Japón, Antártida | Quien se atreve a preguntar descubre el mundo entero | ~10 min |
| 2 | [El caso del hámster desaparecido](cuentos/02-el-caso-del-hamster-desaparecido/cuento.md) | Un misterio en el cole | Una sospecha no es una prueba: antes de acusar, busca la verdad | ~10 min |
| 3 | [La nota que se escapaba](cuentos/03-la-nota-que-se-escapaba/cuento.md) | La música | Equivocarse no es fracasar; rendirse sin intentarlo, sí | ~10 min |
| 4 | [El cohete de cartón](cuentos/04-el-cohete-de-carton/cuento.md) | El espacio | Nadie es demasiado pequeño para ayudar | ~9 min |

## 🔤 Aprendo a leer (para Liliana)

Colección aparte, para que Liliana (5 años) aprenda a leer. No va en el libro de Olivia.

- Todo en **mayúsculas**, una frase corta por página, letra muy grande y un dibujo en cada página.
- Método silábico: cada libro usa solo las letras de su nivel, para que pueda leer todas las palabras sin adivinar. Antes del cuento hay páginas para practicar las letras, las sílabas y las palabras.
- Al final, una guía para leer juntos.

| # | Libro | Letras | PDF |
|---|---|---|---|
| 1 | [La paloma](aprendo-a-leer/01-la-paloma/libro.md) | A E I O U · M P L S | [01-la-paloma.pdf](aprendo-a-leer/01-la-paloma/01-la-paloma.pdf) |

Para regenerar los PDF (comprueba antes que no se cuele ninguna letra fuera del nivel):

```
python3 herramientas/generar_pdf_lectura.py
```

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
aprendo-a-leer/     libros de lectura para Liliana (cada uno con su PDF)
herramientas/       script que genera el PDF y sus tipografías
```

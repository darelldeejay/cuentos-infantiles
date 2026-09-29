# Reglas para escribir los cuentos

## Lectora

Olivia, 7 años. Lee sola. Se aburre con páginas llenas de letra.

## Extensión

- **Tiempo de lectura: 9–11 minutos.**
- A los 7 años se leen unas 70–90 palabras por minuto, así que el texto del cuento (sin contar la moraleja ni el recuadro final) debe tener **entre 700 y 850 palabras**.
- Si Olivia tarda mucho más o mucho menos, se ajusta esta cifra.

## Tono

- Infantil pero no de preescolar: aventura, misterio, humor, algún giro.
- Diálogos y vocabulario rico; las palabras nuevas se entienden por el contexto.
- Español de España ("vosotras", "hala").
- Nada de miedo de verdad: tensión sí, sustos que no dejen dormir, no.

## Estructura

1. Cabecera con tiempo de lectura, tema y protagonistas.
2. **5–6 capítulos cortos** (120–180 palabras), cada uno con **una ilustración**.
3. El problema o el defecto del personaje se ve en la historia; la moraleja no se dice antes de tiempo.
4. **Moraleja** en un recuadro al final: una frase clara y una segunda que la explica.
5. Cierre opcional: lo aprendido, una pregunta para hablar después de leer.

## Temas

Variar. No todos los cuentos tienen que ser de aprender cosas. Ideas: el mundo, animales, el espacio, el cuerpo humano, la música, amistad, celos entre hermanas, perder y ganar, misterio en el cole, inventos, dinosaurios, el mar.

Si el cuento enseña datos, tienen que ser **ciertos**. Mejor redondear ("más de dos millones") que dar una cifra dudosa.

## Ilustraciones

- Estilo fijo: ilustración de libro infantil, acuarela y lápiz de color, sin texto dentro de la imagen.
- Formato 3:2 (horizontal). Se guardan en `imagenes/` del cuento como JPG (calidad 88, unos 200 KB cada una), nunca enlazadas a la web del generador.
- Descripción de personajes: la de `PERSONAJES.md`, siempre igual, para que se reconozcan de un cuento a otro.
- Primero se genera una imagen con todos los personajes y después se usa como referencia para el resto.

## Al terminar un cuento

1. Añadirlo al índice de `README.md` y a las apariciones de `PERSONAJES.md` (de ahí salen las páginas «Personajes» y «Otros personajes» del final de cada cuento).
2. Regenerar el libro: `python3 herramientas/generar_pdf.py`.

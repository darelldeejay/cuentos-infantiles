# Reglas para escribir los cuentos

## Lectora

Olivia, 7 años. Lee sola. Se aburre con páginas llenas de letra.

## Extensión

- **Desde el cuento 05: unas 1.400–1.600 palabras** (entre 15 y 18 minutos de lectura). Con los primeros cuentos, de unas 750 palabras, Olivia terminaba demasiado rápido.
- Los capítulos de más de 200 palabras se maquetan con letra más pequeña, para que en cada página entre más texto (no para que haya más páginas).

## Tono

- Infantil pero no de preescolar: aventura, misterio, humor, algún giro.
- Diálogos y vocabulario rico; las palabras nuevas se entienden por el contexto.
- Español de España ("vosotras", "hala").
- Nada de miedo de verdad: tensión sí, sustos que no dejen dormir, no.

## Estructura

1. Cabecera con tiempo de lectura, tema y protagonistas.
2. **6 capítulos** de 230–300 palabras, cada uno con **una ilustración** y en una sola página.
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

## Ahorrar hojas al imprimir

Se imprime en casa y cada hoja cuenta. Al maquetar los cuentos nuevos:

- **Juntar en una página lo que quepa.** Por ejemplo: la portadilla del cuento con el principio del capítulo 1, la moraleja con «Lo que aprendimos», o «Personajes» con «Otros personajes».
- **Reducir la letra cuando haga falta** para que algo no se desborde a una página casi vacía (tablas de personajes, cuadros finales, un capítulo que se pasa por pocas líneas). El texto de los capítulos, nunca por debajo de 11,5 pt.
- **Las imágenes, siempre enteras**: se pueden hacer más pequeñas, pero no recortarlas.
- Antes de entregar el PDF, revisar que no haya páginas con solo unas líneas o un título suelto.

## Al terminar un cuento

1. Añadirlo al índice de `README.md` y a las apariciones de `PERSONAJES.md` (de ahí salen las páginas «Personajes» y «Otros personajes» del final de cada cuento).
2. Regenerar el libro completo: `python3 herramientas/generar_pdf.py`.
3. Para imprimir, sacar **solo los cuentos nuevos**: `python3 herramientas/generar_pdf.py 5 6`. Ese PDF empieza con el índice completo (los nuevos marcados con ★) y no lleva portada.

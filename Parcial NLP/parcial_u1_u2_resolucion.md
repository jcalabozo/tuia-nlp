# Resolución · Parcial de práctica U1 y U2

> **Cómo usarla:** hacé primero el [parcial](parcial_u1_u2.md) sin mirar, con tiempo, y después corregilo con esta clave. En cada pregunta está la justificación, la **trampa** que conviene tener presente y la sección de los resúmenes donde está el tema: [Resumen U1](<../U1/teoria/Resumen U1 - Extracción y Procesamiento de Texto.md>) y [Resumen U2](<../U2/teoria/Resumen U2 - Representación Vectorial de Texto.md>).

---

## Clave de respuestas

| Ej. 1 | | Ej. 2 | | Ej. 3 | | Ej. 4 | |
|---|---|---|---|---|---|---|---|
| 1 | **C** | 6 | **C** | 11 | **B** | 16 | **A** |
| 2 | **B** | 7 | **A** | 12 | **A** | 17 | **C** |
| 3 | **A** | 8 | **D** | 13 | **C** | 18 | **B** |
| 4 | **D** | 9 | **B** | 14 | **D** | 19 | **A** |
| 5 | **B** | 10 | **D** | 15 | **D** | 20 | **C** |

**Puntaje:** 3 puntos por cada respuesta correcta (60 en total) y hasta 20 por cada pregunta de desarrollo (40 en total).

---

## Ejercicio 1. Extracción de texto

**1 · C.** Un PDF escaneado no tiene capa de texto: cada página es una **imagen**. Hay que convertirla en imagen (pdf2image, que necesita poppler) y aplicar **OCR** (pytesseract).
*Trampa:* cambiar de lector de PDF (B) o de codificación (A) no sirve, porque no hay texto que leer. → U1 §1.3

**2 · B.** Es *mojibake*: bytes UTF-8 leídos como Latin-1. La «ó» en UTF-8 ocupa dos bytes (`C3 B3`), y leídos como Latin-1 se convierten en dos caracteres, «Ã³». Se resuelve leyendo con la codificación correcta.
*Trampa:* D es falsa. ISO-8859-1 **sí** tiene vocales acentuadas; lo que cambia es que usa 1 byte fijo y UTF-8 es de longitud variable. → U1 §1.2 y caso 8.2

**3 · A.** Un PDF **no guarda párrafos ni celdas, guarda instrucciones de dibujo** («esta letra en esta coordenada»). `extract_text()` devuelve la tabla como texto corrido. Para conservarla conviene pdfplumber o un conversor estructurado como Docling, que exporta a Markdown.
*Trampa:* B y C confunden el PDF digital con el escaneado: este PDF sí tiene texto, y no hace falta OCR. → U1 §1.4

**4 · D.** `requests` solo baja el HTML inicial, y BeautifulSoup solo parsea: **ninguno ejecuta JavaScript**. Playwright (o Selenium) automatiza un navegador real, hace scroll y espera a que cargue el contenido; BeautifulSoup interpreta el HTML ya renderizado. Es la combinación de la práctica de Lectulandia.
*Trampa:* C sirve para mantener un login con cookies, pero tampoco ejecuta JavaScript. → U1 §1.5

**5 · B.** Son datos con **formato fijo y conocido**: es un problema de **parseo**, y las expresiones regulares (`re`) reconocen esos patrones (por ejemplo, `AF-\d{6}` y `\d{2}/\d{2}/\d{4}`).
*Trampa:* las demás opciones son técnicas de representación o normalización; ninguna extrae un dato puntual. → U1 §1.6

---

## Ejercicio 2. Procesamiento del texto

**6 · C.** Primero se expanden las abreviaturas con un diccionario («xq» → «porque») y **después** se corrige la ortografía. Si se corrige antes, el corrector trata la abreviatura como un error de tipeo y la cambia por la palabra real más parecida, que casi nunca es la que corresponde.
*Trampa:* A suena lógica, pero es justo el orden equivocado. → U1 §2.1 y trampa 8

**7 · A.** La lista genérica de NLTK incluye «no», y en una clasificación de reclamos la negación **cambia el sentido**. Conviene una lista **personalizada** que conserve negaciones, intensificadores y moduladores («no», «nunca», «sin», «muy»).
*Trampa:* B es al revés: sacar stopwords **reduce** la dimensión. → U1 §2.1 y trampa 7

**8 · D.** El **stemming** recorta sufijos con reglas, sin diccionario: es rápido y agrupa variantes, y por eso conviene en búsqueda, donde importa no perder resultados (*recall*). Su costo es que la raíz puede no ser una palabra.
*Trampa:* A mezcla las propiedades: la lematización sí devuelve palabras válidas, pero es **más lenta**. B es falsa: tokenizar segmenta, no agrupa variantes. C no alcanza: quitar tildes no saca el plural. → U1 §2.3

**9 · B.** La co-ocurrencia es un **prerrequisito** de la correlación, pero dos palabras pueden aparecer juntas por azar, sobre todo si una está en casi todos los mensajes. La correlación (Pearson sobre presencia y ausencia, o información mutua) mira el patrón completo, incluso cuándo **no** aparecen.
*Trampa:* D describe la co-ocurrencia, no la correlación. → U1 §3 y caso 8.6

**10 · D.** El solapamiento repite el final de un chunk al principio del siguiente para **preservar el contexto** y no cortar una idea en el borde.
*Trampa:* A es falsa por partida doble: `chunk_size` es un **máximo**, no un tamaño exacto. Y B y C son al revés: el overlap **agrega** repetición y, si es grande, aumenta la cantidad de chunks. → U1 §4 y trampas 11 y 12

---

## Ejercicio 3. Representación frecuentista

**11 · B.** La bolsa de palabras solo cuenta **cuántas veces** aparece cada palabra: las dos oraciones tienen las mismas palabras con la misma frecuencia, así que dan el mismo vector aunque digan cosas distintas.
*Trampa:* C es justamente lo contrario: las oraciones significan cosas distintas, y el vector no lo ve. Los n-gramas lo mitigan en parte. → U2 §1.2

**12 · A.** Con la fórmula del apunte, una palabra presente en los N documentos tiene IDF = log(N/N) = log 1 = **0**, y como TF-IDF = TF × IDF, el peso es 0: no sirve para distinguir documentos.
*Ojo:* sklearn usa por defecto el IDF suavizado, ln((1 + N)/(1 + df)) + 1, y ahí esa palabra vale 1, no 0. La pregunta pide la fórmula del apunte. → U2 §1.3 y trampa 8

**13 · C.** `ngram_range=(1, 2)` **suma** los bigramas a los unigramas: aparecen columnas como «no me» y «me cubren», que capturan la negación. La dimensión **crece**.
*Trampa:* A dice que los reemplaza; no, los suma. → U2 §1.2 y trampa 9

**14 · D.** `HashingVectorizer` calcula el índice de cada palabra con una función hash: **no guarda vocabulario**, **no necesita `fit`** y su dimensión es **fija** (`n_features`). Una palabra nueva cae en un índice sin reentrenar nada, y por eso sirve para flujos continuos.
*Trampa:* B y C son justamente sus desventajas: **no es invertible** (no se puede volver de la columna a la palabra) y puede tener **colisiones**. → U2 §1.4 y trampa 10

**15 · D.** TF-IDF es **léxico**: cada palabra es una dimensión independiente, y sin palabras en común el coseno da **0**, aunque las frases signifiquen lo mismo. Es la limitación que motiva los embeddings (el ejemplo de «piratas» y «bucaneros» del TP2).
*Trampa:* B es imposible con TF-IDF: sus valores nunca son negativos, así que el coseno queda entre 0 y 1. → U2 §1.5 y trampa 6

---

## Ejercicio 4. Embeddings y similitud

**16 · A.** Es la **hipótesis distribucional**: las palabras que aparecen en contextos parecidos («me recetaron un ___ para el dolor») tienen significados parecidos, y por eso sus vectores quedan cerca.
*Trampa:* D describe el **one-hot**, donde todas las palabras son ortogonales y no hay similitud. B se parece a la idea de FastText, pero tampoco es la base de los embeddings. → U2 §2.1

**17 · C.** FastText representa cada palabra como la **suma de los vectores de sus n-gramas de caracteres**. Una palabra nunca vista, o mal escrita, comparte n-gramas con las conocidas («ibu», «pro», «ofe»), y obtiene un vector.
*Trampa:* Word2Vec y GloVe **no** tienen vector para una palabra fuera del vocabulario (OOV). → U2 §2.5

**18 · B.** BERT genera **embeddings contextuales**: el vector de «orden» depende de la oración, así que la orden médica y el orden de llegada quedan en puntos distintos. Word2Vec y FastText son **estáticos**: un solo vector por palabra.
*Trampa:* A describe justamente el problema de los modelos estáticos (la polisemia). → U2 §2.7 y trampa 3

**19 · A.** Un cross-encoder procesa **cada par** de textos juntos: para cada consulta nueva habría que procesar 200.000 pares. SBERT (*bi-encoder*) codifica cada consulta **una sola vez**, guarda los vectores, y después compara con el coseno. En el paper, el par más parecido entre 10.000 oraciones pasa de unas 65 horas a unos 5 segundos.
*Trampa:* D es falsa: los embeddings de SBERT son **densos**. → U2 §4.3 y trampa 13

**20 · C.** El coseno mide el **ángulo** entre los vectores: un texto corto y uno largo sobre el mismo tema apuntan en la misma dirección aunque tengan distinta magnitud. Además, la distancia euclidiana pierde significado en alta dimensión.
*Trampa:* A es falsa por dos lados: el coseno va de −1 a 1 (puede ser negativo) y **no es una probabilidad**. → U2 §2.2 y trampa 5

---

## Ejercicio 5. Preguntas de desarrollo

### 21. Preparación del texto (20 puntos)

**Respuesta modelo:**

**Extracción, según la fuente:** la primera pregunta es si el archivo tiene capa de texto o es una imagen.

- **PDF del reglamento (digitales):** tienen texto, pero las tablas de coberturas se pierden con `extract_text()`, porque un PDF guarda instrucciones de dibujo. Conviene **pdfplumber** o **Docling**, que conservan tablas y títulos y exportan a **Markdown**.
- **Órdenes escaneadas:** no tienen texto. Hay que convertirlas en imágenes con **pdf2image** y aplicar **OCR** con **pytesseract**, preprocesando la imagen (binarizar, quitar ruido). El OCR nunca es 100 % preciso, así que hay que revisar una muestra.
- **Formulario, correo y WhatsApp:** ya son texto. Hay que leerlos con la **codificación** correcta (UTF-8 o la que use el sistema de origen) y **parsear** con expresiones regulares los datos de formato fijo, como el número de afiliado y las fechas.

**Limpieza de los mensajes, en orden:**

1. **Expandir abreviaturas** con un diccionario («xq» → «porque», «p/» → «para»).
2. **Corregir la ortografía** después (pyspellchecker o autocorrect, para español).
3. **Emojis:** convertirlos a texto o tratarlos como tokens, porque pueden ser señal de enojo o urgencia.
4. **Minúsculas y tildes** (NFKD), según la tarea.
5. **Tokenizar**, y sacar stopwords con una **lista personalizada** que conserve «no», «sin» y «nunca» («no me autorizaron» no es «me autorizaron»).
6. **Stemming** si se prioriza la búsqueda rápida, o **lematización** si importa la precisión.
7. **Segmentar** el reglamento en chunks que respeten los artículos, con algo de solapamiento.

**¿La misma limpieza para TF-IDF y para embeddings? No.** El preprocesamiento **pertenece al modelo, no al corpus**:

- A **TF-IDF** le sirve la limpieza fuerte (minúsculas, sin stopwords, stemming): reduce el vocabulario y el ruido, y no pierde nada que el modelo use, porque igual ignora el orden.
- Un modelo de **embeddings de oraciones** (SBERT, E5) se entrenó con **texto natural**: usa el orden, las palabras funcionales y la puntuación. Sacarle «no» o recortar las palabras **destruye** información que el modelo sí usa.
- Por eso conviene guardar **dos versiones** del texto: una limpia para TF-IDF y otra con una limpieza mínima (codificación, abreviaturas, ruido de formato) para los embeddings.

**Criterios de corrección:**

| Criterio | Puntos |
|---|---|
| Elige la herramienta de extracción según la fuente (PDF con tablas, escaneo con OCR, codificación) | 6 |
| Propone pasos de limpieza en un orden razonable (abreviaturas antes que el corrector) | 6 |
| Señala al menos una decisión que pierde información (negaciones, minúsculas, tildes) | 4 |
| Explica que la limpieza depende del modelo (TF-IDF contra embeddings) | 4 |

### 22. Búsqueda semántica en el reglamento (20 puntos)

**Respuesta modelo:**

**Por qué los embeddings encuentran lo que TF-IDF no:**

- **TF-IDF es léxico:** cada palabra es una dimensión independiente, y dos textos solo se parecen si **comparten palabras**. «Cómo pido que me devuelvan la plata del remedio» y «Reintegro de gastos por medicamentos» dan similitud **0**.
- Los **embeddings de oraciones** son vectores **densos y aprendidos**. Se basan en la hipótesis distribucional y en un entrenamiento masivo, y ubican cerca a los textos que **significan lo mismo** aunque usen palabras distintas. **Sentence-BERT** produce **un vector por oración**, comparable directamente con el **coseno**.
- **Cómo se arma:** se elige un modelo **multilingüe o entrenado en español** con **MTEB** (mirando la tarea de *retrieval*), se vectorizan los artículos **una sola vez** y en cada búsqueda solo se codifica la consulta. Con E5, los prefijos son `passage:` para los artículos y `query:` para las consultas.
- **TF-IDF sigue siendo útil** para términos exactos (códigos de práctica, nombres de medicamentos). Una búsqueda **híbrida** aprovecha los dos.

**El cuidado con los artículos largos:** los modelos de oración tienen un **límite de tokens**, y lo que lo supera **se trunca sin aviso**. Si un artículo es largo, su vector representa solo el comienzo, y lo que está al final no se encuentra nunca. La solución es **segmentar** (chunking) cada artículo en fragmentos que entren en el límite, con solapamiento, guardar un vector por fragmento con el artículo como metadato, y devolver el artículo del fragmento más parecido. Primero conviene contar cuántos artículos superan el límite.

**Cómo comprobar que es mejor:**

1. Armar un conjunto de **consultas reales** y definir los artículos relevantes de cada una **antes** de ver los resultados.
2. Incluir consultas **sin palabras en común** con su artículo (paráfrasis, lenguaje coloquial): ahí TF-IDF no puede acertar, y se ve el aporte de la semántica.
3. Medir **precision@k** del buscador nuevo contra **TF-IDF** (la línea de base) y contra el **azar** (el piso).
4. Analizar los casos de falla por tipo de consulta. Que TF-IDF gane en algunas (términos exactos) es normal y hay que explicarlo.
5. Aclarar los límites: precision@k no mide el *recall* ni el orden dentro del top-k, y con pocas consultas es ruidosa.

**Criterios de corrección:**

| Criterio | Puntos |
|---|---|
| Explica que TF-IDF mide coincidencia léxica y que los embeddings capturan significado, con un ejemplo | 8 |
| Identifica el límite de tokens (truncado) y propone chunking | 6 |
| Propone una evaluación con consultas propias, una métrica y líneas de base (TF-IDF y azar) | 6 |

---

## Qué cambió respecto del parcial de referencia

El parcial de referencia (Tema 2) mantiene la misma estructura, pero incluye temas que no son de U1 ni U2. Se reemplazaron así:

| En el de referencia | Unidad | En este parcial |
|---|---|---|
| Distancia de Levenshtein y Jaccard (preguntas 12, 14 y 15) | U3 | Representación frecuentista (Ejercicio 3) |
| POS tagging y NER (preguntas 16 y 19) | U3 | Embeddings y similitud (Ejercicio 4) |
| Topic modeling (preguntas 17 y 22) | No aparece en U1 ni U2 | Preparación del texto (pregunta 21) |

Además, se sumó la **extracción de texto** (PDF, OCR, codificación, scraping y parseo), que es la mitad de la Unidad 1 y no aparecía en el de referencia.

# Resumen · Unidad 2: Representación Vectorial de Texto

> **Fuentes:** apunte de la cátedra (Notion), prácticas «Vectorización frecuentista» y «Embeddings semánticos», y enunciado del TP2.
> **Cómo usarlo:** el hilo conductor es **qué limitación resolvió cada método respecto del anterior**. Si podés contar esa historia de memoria (§0), tenés la unidad. Antes del parcial, recorré las **trampas** (§7) y las **preguntas de desarrollo** (§8).

---

## 0. Mapa de la unidad

Los modelos necesitan números. Hay dos familias para convertir texto en vectores:

```
 FRECUENTISTAS (dispersos, léxicos)                     EMBEDDINGS (densos, semánticos)
 «qué palabras hay y cuánto pesan»                      «qué significan… y en qué contexto»

 One-hot ─► Count ─► TF-IDF ─► Hashing       ═══►       Word2Vec/GloVe ─► FastText ─► ELMo/BERT ─► Sentence-BERT
                                                         (palabra)        (subpalabra)  (contexto)   (oración)
```

| Método | Qué problema del anterior resuelve | Qué limitación deja |
|---|---|---|
| **One-hot** | Pasar de palabras a números | Ortogonalidad (sin similitud), dimensión = vocabulario |
| **Count Vectorizer** | Representa **documentos** y cuenta **frecuencias** | Ignora el orden; sobrevalora las palabras comunes |
| **TF-IDF** | Baja el peso de las palabras comunes y sube el de las **discriminativas** | Sigue siendo léxico: los sinónimos no se parecen |
| **Hashing** | Evita guardar un vocabulario (tamaño fijo, streaming) | Colisiones, no se puede volver a la palabra |
| **Word2Vec / GloVe** | **Semántica**: las palabras parecidas quedan cerca | Un vector por palabra; no maneja palabras OOV |
| **FastText** | **Morfología** y palabras **OOV** (n-gramas de caracteres) | Sigue siendo **estático** (polisemia) |
| **ELMo / BERT** | Vector **contextual**: «banco» cambia según la oración | Da vectores de palabra, no de oración comparables directamente |
| **Sentence-BERT** | Un embedding por **oración**, comparable con coseno | Límite de tokens (trunca los textos largos) |

---

## 1. Codificación clásica (frecuentista)

### 1.1 One-hot encoding

- Cada palabra es un vector de largo **|V|** (el tamaño del vocabulario) con un **1** en su posición y **0** en el resto: gato = [1, 0, 0], perro = [0, 1, 0].
- Viene de codificar **variables categóricas nominales** (sin orden). Herramientas: `sklearn.preprocessing.OneHotEncoder`, `pandas.get_dummies`.
- ✅ Simple. ❌ Alta dimensionalidad; no refleja frecuencia ni relevancia; **todas las palabras son ortogonales**, así que «buen» está tan lejos de «gran» como de «día».
- **En la práctica:** `CountVectorizer(binary=True)` es el «one-hot **de documentos**»: marca presencia o ausencia de cada palabra sin contar repeticiones. Con 10 000 palabras de vocabulario y unas 200 por sinopsis, el **98 % del vector son ceros** (**sparsidad**; sklearn guarda solo los valores distintos de cero).

### 1.2 Count Vectorizer (bolsa de palabras)

- Cada **documento** es un vector con **cuántas veces** aparece cada palabra del vocabulario.

| | Me | gusta | jugar | fútbol | el | tenis |
|---|---|---|---|---|---|---|
| Doc 1: «Me gusta jugar fútbol» | 1 | 1 | 1 | 1 | 0 | 0 |
| Doc 2: «Me gusta el tenis» | 1 | 1 | 0 | 0 | 1 | 1 |

- ❌ **Ignora el orden**: «el perro muerde al hombre» y «el hombre muerde al perro» dan el mismo vector. ❌ Les da **mucho peso a las palabras frecuentes** («el», «la»), lo que motiva TF-IDF.

**Parámetros de sklearn (práctica):**

| Parámetro | Efecto |
|---|---|
| `max_features=N` | Se queda con las N palabras más frecuentes |
| `min_df=2` | Descarta los términos que aparecen en menos de 2 documentos (los *hapax*). Casi siempre conviene |
| `max_df=0.9` | Descarta los términos presentes en más del 90 % de los documentos (efecto parecido a quitar stopwords) |
| `binary=True` | Solo presencia o ausencia (one-hot de documentos) |
| `ngram_range=(1, 2)` | Suma **bigramas**: «no me gustó» deja de confundirse con «me gustó». La dimensión **crece** |

### 1.3 TF-IDF

**Intuición:** una palabra es importante para un documento si aparece **mucho en él** y **poco en el resto del corpus**.

$$
\text{TF}(t,d) = \frac{\text{veces que } t \text{ aparece en } d}{\text{total de términos en } d}
\qquad
\text{IDF}(t,D) = \log\frac{N}{\text{nº de documentos que contienen } t}
\qquad
\text{TF-IDF} = \text{TF} \times \text{IDF}
$$

- Sube si la palabra aparece más en **el documento**; baja si aparece en **muchos documentos**.
- Una palabra que está en **todos** los documentos tiene IDF = log(N/N) = **0**.
- El **logaritmo amortigua**: sin él, las palabras rarísimas tendrían un peso desproporcionado.
- **sklearn** (`smooth_idf=True`, por defecto) usa IDF = ln((1 + N) / (1 + df)) + 1. Con N = 3 y df = 1 da ln 2 + 1 ≈ **1,693**, el valor que aparece en el ejemplo del apunte.
- **Matriz:** **filas = documentos**, **columnas = palabras** del vocabulario.
- **TF-IDF y stopwords:** el IDF ya baja su peso (aparecen en casi todos los documentos), pero quitarlas igual reduce la dimensión y el costo. Cuidado con «no», «pero» y «si» en tareas de matiz: conviene usar listas personalizadas.

| Parámetro (práctica) | Qué hace |
|---|---|
| `sublinear_tf=True` | Usa log(1 + tf): la repetición no domina en los documentos largos |
| `smooth_idf=True` | Evita divisiones por cero; conviene dejarlo en `True` |
| `use_idf=False` | Solo TF normalizado |

> 🎯 Buen punto de partida para clasificar: `TfidfVectorizer(sublinear_tf=True, min_df=2)`.

### 1.4 Vectorización de hash (*hashing trick*)

- Una **función hash** lleva cada token a un índice: `índice = hash(token) % n_features`. Para esto se prefieren funciones **no criptográficas** y rápidas, como **MurmurHash**, en lugar de MD5 o SHA.
- ✅ **No guarda un vocabulario** y **no necesita `fit`**: el mismo vectorizador sirve para textos nuevos, **streaming** y corpus que no entran en memoria. La dimensión es **fija** (`n_features`, por ejemplo 2<sup>18</sup> ≈ 262 000).
- ❌ **Colisiones**: dos palabras distintas pueden caer en el mismo índice. Es raro si `n_features` es grande, pero puede acercar documentos que no comparten palabras. ❌ Es **sin estado**: no se puede volver de una columna a su palabra, y eso dificulta interpretar.
- Por defecto normaliza con norma L2 y usa signos alternados (`alternate_sign`): los valores quedan entre −1 y 1.

### 1.5 Comparación y límite común

| Técnica | Aplica a | Pros | Contras | Dimensión |
|---|---|---|---|---|
| One-hot | Palabras | Simple | Alta dimensión; ni frecuencia ni relevancia | Vocabulario |
| Count | Documentos | Tiene en cuenta la frecuencia | Sobrevalora las palabras comunes; ignora el orden | Vocabulario |
| TF-IDF | Documentos | Frecuencia **y** relevancia | Algo más complejo | Vocabulario |
| Hash | Palabras o documentos | Tamaño fijo; sin vocabulario | Colisiones; no invertible | `n_features` |

> ⚠️ **Ninguno captura semántica.** El coseno entre esos vectores mide **coincidencia léxica ponderada**. Ejemplo del TP2: «una novela sobre piratas» y «un relato de bucaneros» tienen similitud TF-IDF **exactamente 0**, porque no comparten ningún token.

---

## 2. Word embeddings

### 2.1 La idea

- **Hipótesis distribucional:** las palabras que aparecen en **contextos similares** tienen **significados similares** («mi ___ come mucho»: perro, gato), y por eso sus vectores deben quedar **cerca**.
- Los embeddings son **densos**, de **dimensión relativamente baja** (unos 300 contra cientos de miles de palabras de vocabulario) y **aprendidos** de los datos. One-hot es **disperso**, de alta dimensión y fijado a mano.
- Capturan relaciones semánticas y sintácticas: **rey − hombre + mujer ≈ reina**; «caminar» es a «caminó» lo que el presente al pasado.

![One-hot contra embeddings](imagenes/img-08.png)

**Rasgos semánticos (ejemplo del apunte):** cada dimensión puede pensarse como un rasgo del significado.

| | Género | Edad | Realeza |
|---|---|---|---|
| man | 1 | 7 | 1 |
| woman | 9 | 7 | 1 |
| king | 1 | 8 | 8 |
| queen | 9 | 7 | 8 |

Los modelos reales **aprenden** cientos de dimensiones de este tipo, que no tienen un nombre interpretable.

### 2.2 Similitud coseno

$$
\cos(\theta) = \frac{A \cdot B}{\lVert A\rVert\,\lVert B\rVert}
$$

- **1**: misma dirección (máxima similitud) · **0**: ortogonales (sin relación) · **−1**: opuestos. **Puede ser negativa**: no es una probabilidad.
- **Por qué se prefiere a la distancia euclidiana:**
  1. Es **invariante a la magnitud**: mide orientación. Un documento corto y uno largo sobre el mismo tema pueden ser similares.
  2. En **alta dimensión**, la distancia euclidiana pierde significado (la *maldición de la dimensionalidad*).
  3. Se **interpreta** de forma intuitiva (1, 0, −1).
  4. Con vectores normalizados, se reduce a un producto escalar (el apunte lo menciona como eficiencia).
- Herramientas: `sklearn.metrics.pairwise.cosine_similarity`, `sentence_transformers.util.cos_sim`.

### 2.3 Tipos de embeddings

![Taxonomía de embeddings](imagenes/img-14.png)

- **Independientes del contexto** (estáticos, los «clásicos»): **word2vec, GloVe, FastText**. Redes superficiales o factorización de matrices de co-ocurrencia; **un vector por palabra**. Se distribuyen pre-entrenados.
- **Dependientes del contexto:** la **misma palabra recibe vectores distintos** según la oración («banco» financiero o de plaza).
  - Basados en **RNN**: CoVe, Flair, **ELMo**.
  - Basados en **Transformers**: **BERT**, ALBERT.

### 2.4 Word2Vec (2013)

| | **CBOW** (*Continuous Bag of Words*) | **Skip-gram** |
|---|---|---|
| Predice | La **palabra central** a partir del **contexto** | El **contexto** a partir de la **palabra central** |
| Entrada | C palabras de contexto (sus vectores se **promedian**) | Una palabra (en one-hot) |
| En gensim | `sg=0` | `sg=1` |

![CBOW y Skip-gram](imagenes/img-15.png)

**Arquitectura:**

1. La entrada es un **one-hot de tamaño V**.
2. La **capa oculta** tiene N neuronas (N es un hiperparámetro: la dimensión del embedding, por ejemplo 300). La salida es un **softmax de tamaño V**.
3. Hay dos matrices: **W (V × N)**, de entrada a la capa oculta, y **W′ (N × V)**, de la capa oculta a la salida.
4. **Los vectores de palabras son los pesos de la capa oculta** (las filas de W). La tarea de predicción es solo una excusa para aprenderlos.

![Arquitectura CBOW](imagenes/img-21.png)

- La **ventana** (*window size*) es un hiperparámetro fijo: cuántas palabras a cada lado se consideran contexto.
- **Skip-gram no distingue la dirección**: no sabe si una palabra de contexto estaba a la izquierda o a la derecha. Refleja **co-ocurrencias**, no gramática.
- **`most_similar(positive=[...], negative=[...])`** en gensim suma los vectores de `positive`, resta los de `negative` y devuelve los más similares por coseno (analogías).
- **Negative sampling (TP2):** calcular el softmax sobre **todo el vocabulario** en cada paso es inviable. Se reemplaza por una clasificación binaria entre el par (palabra, contexto) real y unas pocas palabras «negativas» muestreadas.
- **Modelo pre-entrenado en español** del apunte: **SBW-vectors-300-min5** (Spanish Billion Words Corpus), cargado con `gensim.models.KeyedVectors`.

### 2.5 FastText (FAIR, 2016)

- Representa cada palabra como la **suma de los vectores de sus n-gramas de caracteres**. Con n = 3: «donde» → `<do`, `don`, `ond`, `nde`, `de>`, donde `<` y `>` marcan el inicio y el fin de la palabra.
- ✅ **Morfología**: gato, gatos y gatito comparten n-gramas. ✅ Palabras **fuera de vocabulario (OOV)**: una palabra nunca vista igual obtiene vector.
- ❌ **Sigue siendo estático**: no distingue los sentidos de «banco».

### 2.6 Línea temporal

| Año | Modelo | Qué cambió |
|---|---|---|
| 2013 | **Word2Vec** | Embeddings densos; analogías |
| 2014 | **GloVe** | Mismo rol, entrenado con **co-ocurrencia global** (Stanford) |
| 2014 | **Doc2Vec** | Un vector **por documento o párrafo** |
| 2016 | **FastText** | n-gramas de caracteres: morfología y OOV |
| 2017 | **InferSent** | Embeddings de oración supervisados (NLI) |
| 2018 | **ELMo** | Primer embedding **contextual** masivo (biLSTM) |
| 2018 | **BERT** | Contextual con **Transformers**; base de casi todo lo posterior |
| 2018 | **USE** | *Universal Sentence Encoder* (Google), entrenado con varias tareas |
| 2019 | **Sentence-BERT** | Embeddings de oración comparables con coseno |
| 2022 | **MTEB** | Benchmark para **elegir** un modelo de embeddings |
| 2025 | **EmbeddingGemma** | Embeddings compactos que corren en el dispositivo |

> 📌 GloVe no aporta una idea nueva respecto de Word2Vec, sino otra forma de entrenar. Doc2Vec, ELMo y USE fueron hitos reales, pero hoy los superan Sentence-BERT y sus derivados.

### 2.7 Embeddings contextuales (BERT)

- El vector de una palabra **depende de la oración**: «retirar dinero del **banco**» y «sentarse en el **banco** de la plaza» dan puntos distintos. Con Word2Vec, en cambio, serían el mismo vector.
- ELMo lo mostró con **LSTM bidireccionales**; BERT lo hizo con **Transformers** y se volvió el estándar.
- **Cómo aprenden los modelos modernos:** con **entrenamiento masivo** y tareas como el ***Masked Language Modeling*** (predecir palabras ocultas), que obligan a usar el contexto. Resultado: la **proximidad** en el espacio equivale a **similitud semántica**, incluso entre palabras distintas, longitudes distintas o idiomas distintos en los modelos multilingües. El modelo no «entiende»: aprende patrones estadísticos muy ricos.

### 2.8 Cuadro resumen

| Método | Enfoque | Similitud semántica | ¿Sirve el coseno? | Contextual |
|---|---|---|---|---|
| One-hot | Palabra | No | No (ortogonales) | No |
| Count / Hash / TF-IDF | Documento | No | Sí (coincidencia léxica) | No |
| Word2Vec | Palabra | Sí | Sí | No |
| FastText | Palabra + subpalabra | Sí (+ OOV y morfología) | Sí | No |
| BERT | Palabra en contexto | Sí | Sí | **Sí** |
| Sentence-BERT | Oración | Sí | Sí | **Sí** |

---

## 3. Visualización de embeddings

| | **PCA** | **t-SNE** |
|---|---|---|
| Tipo | **Lineal**, determinista | **No lineal**, estocástico |
| Qué preserva | Las direcciones de **máxima varianza** | Las **vecindades locales** (quién está cerca de quién) |
| Para qué | Estructura global; dice cuánta varianza se explica | Ver **grupos** |
| ⚠️ Cuidado | 2 componentes explican **poca varianza** (un 10–15 % en la práctica): puntos mezclados en 2D **no** implican que el espacio original no separe | Las **distancias entre clusters** y sus tamaños **no se interpretan**; dependen de la `perplexity` |

- Para matrices **dispersas** (TF-IDF), la práctica usa **`TruncatedSVD`**, que cumple el rol de PCA sin densificar la matriz.
- Ninguno usa etiquetas: el color por género se agrega **después**, y es información que el modelo **nunca vio**.
- Herramientas online: *TensorFlow Embedding Projector*, *WordEmbeddingDemo* (CMU).

---

## 4. Embeddings de oraciones

### 4.1 Qué son

Son vectores de **dimensión fija** que representan el significado de una oración, un párrafo o un documento. Se usan en **búsqueda semántica**, clasificación, clustering, respuesta a preguntas, traducción y **RAG**. Frente a los word embeddings, capturan el **contexto** y dan una **representación unificada** para textos de distinta longitud. Los desafíos: meter mucha información (hechos, opiniones, emociones) en un vector de tamaño fijo, y manejar longitudes variables.

### 4.2 Por qué promediar word embeddings es limitado

![Promedio de vectores de palabras](imagenes/img-23.png)

- **Pérdida de información:** una oración de una sola palabra («It») puede dar similitud alta con una oración completa.
- **El orden no afecta:** «this is cool» e «is this cool» dan similitud **1,0**, porque el promedio es conmutativo.
- **Parches manuales:** omitir stopwords, **ponderar con TF-IDF**, agregar n-gramas, concatenar embeddings.
- **Solución de fondo:** entrenar un modelo **de punta a punta** para oraciones. Los intentos históricos fueron Doc2Vec, InferSent y USE; el que se usa en la materia es **Sentence-BERT**.

### 4.3 Sentence-BERT (SBERT)

- Modifica BERT con **redes siamesas y tripletas** para producir embeddings de oración **comparables con el coseno**.
- **Frente al cross-encoder de BERT:** el cross-encoder procesa **cada par** de oraciones (la cantidad de pares crece cuadráticamente, y se vuelve inviable con miles). SBERT codifica **cada oración una vez** y compara con coseno. En el paper, encontrar el par más parecido entre 10 000 oraciones pasa de unas 65 horas a unos 5 segundos.
- Modelo del apunte: **`distiluse-base-multilingual-cased-v1`** (multilingüe). Librería: **`sentence-transformers`**.

### 4.4 MTEB (*Massive Text Embedding Benchmark*)

- Evalúa modelos de embeddings en **58 datasets, 112 idiomas y 8 tareas**: bitext mining, clasificación, clustering, clasificación de pares, reranking, **retrieval**, **STS** (similitud semántica) y resumen. Tiene un **leaderboard** público en Hugging Face.
- **Cómo elegir un modelo:** que sea **multilingüe o entrenado en español**, que su **tamaño** (RAM y latencia) sea viable, y **validarlo** con pares de ejemplo propios. **No hace falta reentrenar**: cargarlo es `SentenceTransformer("nombre-del-modelo")`.

### 4.5 E5 en la práctica

- **`intfloat/multilingual-e5-small`**: 384 dimensiones, más de 100 idiomas, rápido en CPU.
- Usa **prefijos**: **`query: `** para las consultas y **`passage: `** para los documentos que se indexan. Usar el prefijo correcto mejora bastante los resultados.
- Flujo: **vectorizar una sola vez** (`normalize_embeddings=True`), **guardar** los embeddings (en la práctica, en un ZIP) y cargar el modelo solo para codificar consultas nuevas.
- **Centrar antes de promediar:** todos los embeddings comparten una componente común («es una sinopsis de libro en español»), así que los centroides por género dan similitud ≈ 0,98. Restar la **media global** deja a la vista lo que distingue a cada grupo.
- Métricas de clustering usadas: **silhouette** (sin etiquetas) y **ARI** (contra etiquetas reales).

| | TF-IDF | E5 (Sentence Transformer) |
|---|---|---|
| Vector | Disperso, alta dimensión | Denso, 384 dimensiones |
| Semántica | Léxica (palabras exactas) | Significado |
| Multilingüe | No | Sí |
| Velocidad | Muy rápido | Moderada |
| Mejor para | Búsqueda por palabras clave | Búsqueda por significado |

---

## 5. Evaluar representaciones (TP2)

Esta es la parte que más pesa en el TP, y sirve como argumento en cualquier pregunta de desarrollo.

- **El preprocesamiento pertenece al modelo, no al corpus.** La limpieza para TF-IDF (minúsculas, sin stopwords, sin puntuación) es **destructiva** para un modelo de oración, que se entrenó con texto natural y usa el orden y las palabras funcionales. Por eso se preparan **dos versiones** del texto: una limpia y otra cruda.
- **Toda métrica necesita una línea de base:** se compara con **TF-IDF** (la línea de base léxica) y con la **elección al azar** (el **piso**). Si un género cubre la mitad de la colección, el azar ya da ≈ 0,5.
- **precision@k** sobre un conjunto de consultas **propio**, con los relevantes definidos **antes** de ver los resultados.
- Incluir **consultas sin solapamiento léxico** con sus relevantes: ahí TF-IDF no puede ganar por construcción.
- Que TF-IDF **empate o gane** en algunas consultas es normal: hay que **explicarlo**, no cambiar la métrica.
- La **distribución de similitudes entre pares al azar** (media, desvío, rango) muestra si el espacio discrimina: si todo se parece a todo, el ranking ordena ruido.
- **Límite de tokens:** SBERT **trunca** los textos largos **sin avisar**, así que hay que contar cuántos documentos se cortan. El chunking lo mitiga.
- **Multi-etiqueta** (un libro con varios géneros) no es lo mismo que **multi-clase**, y cambia la evaluación: un clustering «duro» penaliza a los libros con varios géneros.
- Las **sinopsis son texto promocional** (escrito para vender): eso sesga, por ejemplo, un clasificador de géneros.
- **Qué no mide precision@k:** el *recall*, el orden dentro del top-k ni la relevancia graduada. Además, depende de juicios subjetivos, y con pocas consultas es ruidosa.

> 🧩 **Infraestructura del TP2** (probablemente fuera del parcial teórico): los vectores se guardan en **Postgres con `pgvector`**, con **una tabla por modelo** (no pueden convivir dos dimensiones en la misma columna indexada). El índice **HNSW** tiene que usar la *opclass* que corresponde al operador de distancia. Hay que manejar los vectores nulos o `NaN` **antes** de insertarlos, y un índice aproximado combinado con un filtro selectivo puede **perder recall**.

---

## 6. Chuleta de herramientas

| Herramienta | Para qué |
|---|---|
| `OneHotEncoder` (sklearn), `get_dummies` (pandas) | One-hot |
| `CountVectorizer` | Bolsa de palabras (`binary=True`: one-hot de documentos; `ngram_range`) |
| `TfidfVectorizer` | TF-IDF (`sublinear_tf`, `smooth_idf`, `min_df`, `max_df`) |
| `HashingVectorizer` | Hashing trick (`n_features`, sin `fit`) |
| `cosine_similarity` (sklearn) / `util.cos_sim` | Similitud coseno |
| **gensim**: `KeyedVectors`, `Word2Vec`, `FastText` | Cargar o entrenar embeddings de palabra; `most_similar` |
| spaCy (`en_core_web_md`) | Vectores de palabra promediados para oraciones |
| transformers (`BertModel`, `BertTokenizer`) | Embeddings contextuales de BERT |
| **sentence-transformers** | SBERT, E5: embeddings de oración |
| `PCA`, `TruncatedSVD`, `TSNE` | Reducción de dimensión y visualización |
| `KMeans`, `silhouette_score`, `adjusted_rand_score` | Clustering y su evaluación |
| MTEB | Elegir un modelo de embeddings |

---

## 7. Trampas típicas de parcial

1. **CBOW:** contexto → palabra central. **Skip-gram:** palabra central → contexto. (Invertirlos es la trampa clásica.)
2. **Los embeddings de Word2Vec son los pesos de la capa oculta**, no la salida del softmax.
3. **FastText no resuelve la polisemia**: es estático. La resuelven los modelos **contextuales** (ELMo, BERT).
4. **Skip-gram no distingue izquierda y derecha** dentro de la ventana.
5. **El coseno puede ser negativo** y no es una probabilidad.
6. **TF-IDF no capta sinónimos**: sin palabras en común, la similitud es 0.
7. En la matriz TF-IDF de sklearn, las **filas son documentos** y las **columnas, palabras**.
8. Una palabra presente en **todos** los documentos tiene **IDF = 0** con la fórmula del apunte (y 1 con el suavizado de sklearn).
9. **`ngram_range=(1, 2)` aumenta** la dimensión: los bigramas **se suman** a los unigramas.
10. **Hashing:** no necesita `fit` ni vocabulario, pero tiene colisiones y no es invertible.
11. **One-hot** (vectores de palabra en la teoría) no es lo mismo que **`binary=True`** (vectores de documento en la práctica).
12. **Promediar word embeddings** descarta el orden: «this is cool» = «is this cool».
13. **SBERT contra cross-encoder:** SBERT codifica cada oración una vez; el cross-encoder procesa cada par.
14. **MTEB es un benchmark**, no un modelo.
15. **t-SNE:** las distancias entre clusters no se interpretan. **PCA a 2D:** que los puntos se vean mezclados no prueba nada.
16. Los embeddings son de **baja** dimensión comparados con el vocabulario (300 contra 100 000), aunque sean de **alta** dimensión comparados con 2D. El apunte usa las dos expresiones.
17. **E5:** `query: ` para las consultas y `passage: ` para los documentos.

---

## 8. Preguntas de desarrollo para practicar

1. **Compará one-hot, Count, TF-IDF y Hashing:** qué representan, pros, contras y dimensión.
2. **Explicá TF-IDF** con sus fórmulas y el papel del logaritmo. ¿Qué pasa con las stopwords?
3. **¿Por qué los métodos frecuentistas no capturan semántica** y cómo lo resuelven los word embeddings? ¿Qué limitación queda y qué la resuelve?
4. **Word2Vec:** CBOW contra Skip-gram, arquitectura, de dónde salen los vectores y para qué sirve el negative sampling.
5. **FastText:** qué aporta y qué no resuelve.
6. **Similitud coseno:** fórmula, interpretación y por qué se prefiere a la distancia euclidiana.
7. **Sentence embeddings:** por qué no alcanza el promedio, cómo funciona SBERT y cómo elegir un modelo con MTEB.
8. **¿Cómo evaluarías** si un buscador con embeddings es mejor que uno con TF-IDF? (Líneas de base, precision@k, consultas sin solapamiento léxico, límites de la métrica.)
9. **PCA contra t-SNE** para visualizar, y qué advertencias hay que hacer al interpretarlos.

---

## 9. Glosario

- **Bolsa de palabras (BoW):** representación que cuenta palabras e ignora el orden.
- **Colisión de hash:** dos entradas distintas que dan el mismo valor hash (el mismo índice).
- **Cross-encoder:** modelo que recibe dos textos juntos y devuelve un puntaje; es preciso pero caro para buscar.
- **Embedding:** representación vectorial densa y aprendida.
- **Embedding contextual:** su valor depende de la oración (ELMo, BERT).
- **Hipótesis distribucional:** palabras en contextos similares tienen significados similares.
- **IDF:** frecuencia inversa de documento; penaliza los términos presentes en muchos documentos.
- **MLM (*Masked Language Modeling*):** tarea de predecir palabras ocultas; es el preentrenamiento de BERT.
- **Negative sampling:** aproximación que evita el softmax sobre todo el vocabulario.
- **OOV (*out of vocabulary*):** palabra que no estaba en el vocabulario de entrenamiento.
- **precision@k:** proporción de resultados relevantes entre los primeros k.
- **Redes siamesas:** dos ramas con los mismos pesos que codifican textos por separado para compararlos.
- **Sparsidad:** proporción de ceros en un vector o matriz.
- **STS (*Semantic Textual Similarity*):** tarea de medir la similitud semántica entre textos.

---

### 📝 Fe de erratas del apunte

- **Sentence-BERT** aparece como «desarrollado por Google en 2020». En realidad es de **Reimers y Gurevych (UKP Lab, 2019)**; la propia línea temporal del apunte dice 2019. BERT sí es de Google (2018).
- El mismo párrafo dice que SBERT reduce «el tiempo de **entrenamiento** de horas a segundos»: lo que se reduce es el tiempo de **búsqueda** (comparar oraciones), no el de entrenamiento.
- Del modelo SBW en español dice «entrenado sobre un total de 1.000.653 tokens». Esa cifra parece ser el **tamaño del vocabulario** (cantidad de vectores); el corpus tiene del orden de **mil millones** de palabras (por eso se llama *Spanish **Billion** Words*).

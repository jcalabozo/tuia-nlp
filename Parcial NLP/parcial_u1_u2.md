# TUIA - Procesamiento del Lenguaje Natural

**Parcial de práctica · Unidades 1 y 2**

Fecha: ______________

Apellido y Nombre: ________________________________________

Legajo: ______________

---

## Enunciado general

Una **obra social** recibe todos los días miles de consultas de sus afiliados por distintos canales: un formulario web, correo electrónico y WhatsApp. Además, guarda su **reglamento** de coberturas en PDF, y muchos afiliados adjuntan **órdenes médicas escaneadas**.

La obra social quiere desarrollar un sistema de NLP que permita extraer el texto de todas esas fuentes, prepararlo, representarlo como vectores, encontrar consultas parecidas y buscar en el reglamento la respuesta a cada consulta.

Seleccioná la opción más adecuada en cada caso.

---

## Ejercicio 1. Extracción de texto

(15 puntos — 3 puntos por pregunta)

**1. Muchos afiliados adjuntan órdenes médicas escaneadas en PDF. Al procesarlas con pypdf, `extract_text()` devuelve cadenas vacías. ¿Qué conviene hacer?**

- A. Volver a leer el archivo con `encoding='iso-8859-1'`.
- B. Reemplazar pypdf por PyMuPDF, que es más rápido.
- C. Convertir las páginas en imágenes (por ejemplo, con pdf2image) y aplicarles OCR.
- D. Pasar el texto extraído por un corrector ortográfico.

**2. Al leer con pandas un CSV de consultas exportado de un sistema viejo, aparecen palabras como «AfiliaciÃ³n» y «PrÃ¡ctica». ¿Cuál es la causa más probable?**

- A. El tokenizador separó mal las palabras con tilde.
- B. El texto se guardó con una codificación y se leyó con otra.
- C. El archivo tiene stopwords que no se eliminaron.
- D. ISO-8859-1 no puede representar vocales acentuadas.

**3. El reglamento está en PDF digitales con muchas tablas de coberturas y topes. ¿Por qué `extract_text()` puede no alcanzar si el sistema tiene que responder preguntas sobre esas tablas?**

- A. Porque un PDF guarda instrucciones de dibujo, y la extracción plana pierde la estructura de las tablas.
- B. Porque los PDF digitales no tienen capa de texto.
- C. Porque las tablas de un PDF solo se pueden leer con OCR.
- D. Porque `extract_text()` solo funciona con documentos en inglés.

**4. La cartilla de prestadores está en una página web que carga los resultados con JavaScript a medida que el usuario baja. ¿Qué combinación de herramientas es la adecuada para extraerla?**

- A. `requests` para bajar el HTML y expresiones regulares para sacar los datos.
- B. BeautifulSoup sola, porque hace el pedido y ejecuta el JavaScript.
- C. `requests.Session`, porque conserva las cookies entre pedidos.
- D. Playwright para navegar y renderizar la página, y BeautifulSoup para interpretar el HTML.

**5. Los correos incluyen el número de afiliado con un formato fijo (por ejemplo, «AF-204518») y la fecha de la práctica (por ejemplo, «12/09/2026»). ¿Qué conviene usar para extraer esos datos?**

- A. Embeddings de oraciones, para encontrar los fragmentos más parecidos a «número de afiliado».
- B. Expresiones regulares (`re`), que reconocen patrones con un formato conocido.
- C. Stemming, para reducir cada dato a su raíz.
- D. TF-IDF, para quedarse con los términos más relevantes de cada correo.

---

## Ejercicio 2. Procesamiento del texto

(15 puntos — 3 puntos por pregunta)

**6. Los mensajes de WhatsApp traen abreviaturas («xq», «q», «p/») y errores de tipeo. ¿En qué orden conviene aplicar la estandarización de abreviaturas y la corrección ortográfica?**

- A. Primero la corrección ortográfica, así las abreviaturas quedan bien escritas antes de expandirlas.
- B. El orden da igual, porque las dos técnicas son independientes.
- C. Primero expandir las abreviaturas con un diccionario, y después corregir la ortografía.
- D. Ninguna de las dos: cualquier modelo entiende las abreviaturas sin preprocesamiento.

**7. Para clasificar los mensajes en «reclamo» o «consulta», un analista elimina las stopwords con la lista genérica de NLTK, y «no me autorizaron la cirugía» queda «autorizaron cirugía». ¿Qué problema muestra el ejemplo?**

- A. La lista genérica elimina negaciones que pueden cambiar el sentido del mensaje.
- B. Eliminar stopwords aumenta la dimensión del vocabulario.
- C. Eliminar stopwords equivale a tokenizar el texto.
- D. NLTK no tiene una lista de stopwords en español.

**8. El buscador interno tiene que encontrar las consultas aunque usen otra forma de la palabra («reintegros», «reintegro»). Procesa miles de consultas por día, y lo que más importa es la velocidad y no perder resultados. ¿Qué técnica es más razonable?**

- A. Lematización, porque es la más rápida y siempre devuelve palabras de diccionario.
- B. Ninguna: la tokenización ya agrupa las variantes de una misma palabra.
- C. Quitar las tildes, porque así «reintegros» y «reintegro» quedan iguales.
- D. Stemming, porque es rápido y agrupa las variantes, aunque la raíz no siempre sea una palabra real.

**9. El área de calidad observa que «demora» y «autorización» aparecen juntas en muchas consultas, pero «demora» está en casi todos los mensajes. ¿Por qué la co-ocurrencia sola no alcanza para afirmar que esos problemas están asociados?**

- A. Porque la co-ocurrencia solo puede medirse en ventanas de dos palabras.
- B. Porque dos palabras pueden aparecer juntas por azar; la correlación mira también cuándo no aparecen.
- C. Porque la co-ocurrencia requiere embeddings contextuales.
- D. Porque la correlación solo cuenta cuántas veces aparecen juntas.

**10. Para buscar en el reglamento, los artículos se dividen con `RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)`. ¿Para qué sirve el `chunk_overlap`?**

- A. Para que todos los chunks tengan exactamente 500 caracteres.
- B. Para eliminar la información repetida entre chunks consecutivos.
- C. Para reducir la cantidad total de chunks.
- D. Para repetir el final de un chunk al principio del siguiente y no cortar una idea en el borde.

---

## Ejercicio 3. Representación frecuentista

(15 puntos — 3 puntos por pregunta)

**11. Con `CountVectorizer`, las consultas «el médico no atendió al afiliado» y «el afiliado no atendió al médico» obtienen el mismo vector. ¿Por qué?**

- A. Porque CountVectorizer elimina las palabras repetidas.
- B. Porque la bolsa de palabras cuenta ocurrencias e ignora el orden.
- C. Porque las dos oraciones significan lo mismo.
- D. Porque CountVectorizer solo considera los sustantivos.

**12. La palabra «afiliado» aparece en todas las consultas del corpus. Con la fórmula del apunte, IDF(t) = log(N / df(t)), ¿qué peso TF-IDF recibe «afiliado» en cada consulta?**

- A. 0, porque log(N / N) = log 1 = 0.
- B. El máximo del corpus, porque es la palabra más frecuente.
- C. Un valor negativo, porque es demasiado común.
- D. Depende solo de cuántas veces aparece en cada consulta.

**13. Para distinguir «me cubren la prótesis» de «no me cubren la prótesis», se configura el vectorizador con `ngram_range=(1, 2)`. ¿Qué efecto tiene?**

- A. Reemplaza los unigramas por bigramas, y la dimensión baja.
- B. Convierte la representación en un embedding semántico.
- C. Agrega bigramas como «no me» a los unigramas, y la dimensión crece.
- D. Elimina las negaciones del vocabulario.

**14. Las consultas llegan sin parar, y aparecen palabras nuevas todo el tiempo (medicamentos, prestadores, jerga). ¿Por qué podría convenir `HashingVectorizer` en lugar de `TfidfVectorizer`?**

- A. Porque captura el significado de las palabras nuevas.
- B. Porque permite recuperar la palabra que corresponde a cada columna.
- C. Porque garantiza que dos palabras distintas nunca compartan una columna.
- D. Porque no guarda un vocabulario ni necesita `fit`, y su dimensión es fija.

**15. Un afiliado busca «cómo pido que me devuelvan la plata del remedio», y el artículo correcto del reglamento se titula «Reintegro de gastos por medicamentos». Con TF-IDF (sin stopwords) y similitud coseno, ¿qué es esperable?**

- A. Similitud alta, porque las dos frases tratan el mismo tema.
- B. Similitud negativa, porque usan palabras distintas.
- C. No se puede calcular, porque TF-IDF no admite el coseno.
- D. Similitud nula, porque no comparten ninguna palabra.

---

## Ejercicio 4. Embeddings y similitud

(15 puntos — 3 puntos por pregunta)

**16. ¿En qué idea se basan los word embeddings, como Word2Vec, para que «remedio» y «medicamento» queden cerca en el espacio vectorial?**

- A. Las palabras que aparecen en contextos similares tienden a tener significados similares.
- B. Las palabras que comparten más letras tienen significados similares.
- C. Las palabras más frecuentes del corpus son las más importantes.
- D. Cada palabra se representa con un 1 en su posición y 0 en el resto.

**17. Los afiliados escriben nombres de medicamentos nuevos o con errores de tipeo («ibuprofemo») que no estaban en el corpus de entrenamiento. ¿Qué modelo de embeddings de palabras puede asignarles un vector?**

- A. Word2Vec, porque genera un vector para cualquier palabra que reciba.
- B. One-hot, porque agrega una columna nueva por cada palabra desconocida.
- C. FastText, porque arma cada palabra con los vectores de sus n-gramas de caracteres.
- D. GloVe, porque se entrena con co-ocurrencias globales.

**18. La palabra «orden» aparece en «tengo que autorizar una orden de resonancia» y en «los turnos se dan por orden de llegada». ¿Qué ventaja ofrece un modelo como BERT frente a Word2Vec o FastText?**

- A. Le asigna a «orden» el mismo vector en las dos oraciones, y eso hace más estable al sistema.
- B. Genera un vector distinto para «orden» según la oración en la que aparece.
- C. No necesita tokenizar el texto.
- D. Representa cada palabra con un vector disperso del tamaño del vocabulario.

**19. Para encontrar, entre 200.000 consultas resueltas, las más parecidas a una consulta nueva, ¿por qué se usa Sentence-BERT y no un cross-encoder de BERT?**

- A. Porque SBERT codifica cada consulta una sola vez y después compara vectores con coseno, en lugar de procesar cada par de consultas.
- B. Porque SBERT no necesita ningún tipo de entrenamiento previo.
- C. Porque los cross-encoders solo funcionan en inglés.
- D. Porque SBERT produce vectores dispersos, más fáciles de comparar.

**20. Algunas consultas son de una línea y otras ocupan varios párrafos. ¿Por qué se prefiere la similitud coseno a la distancia euclidiana para compararlas?**

- A. Porque el coseno siempre da un valor entre 0 y 1 que se interpreta como una probabilidad.
- B. Porque el coseno mide la diferencia de longitud entre los textos.
- C. Porque el coseno mide el ángulo entre los vectores y no depende de su magnitud.
- D. Porque el coseno no necesita representar los textos como vectores.

---

## Ejercicio 5. Preguntas de desarrollo

(40 puntos — 20 puntos por pregunta)

La obra social quiere armar un asistente que responda las consultas de los afiliados a partir del reglamento y de las consultas ya resueltas.

### 21. Preparación del texto

¿Qué pasos de extracción y limpieza aplicarías a los PDF del reglamento, a las órdenes escaneadas y a los mensajes de WhatsApp antes de vectorizarlos? ¿Aplicarías la misma limpieza si los textos se van a representar con TF-IDF que si se van a representar con embeddings de oraciones? Justificá.

### 22. Búsqueda semántica en el reglamento

¿Por qué un buscador basado en embeddings de oraciones (por ejemplo, Sentence-BERT) puede encontrar artículos del reglamento que uno basado en TF-IDF no encuentra? ¿Qué cuidado hay que tener con los artículos largos, y cómo comprobarías que el buscador nuevo es mejor que el actual?

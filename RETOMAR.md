# Retomar el trabajo en otra máquina

Instrucciones para Claude Code. El usuario hace `git pull` (o clona) este repo en la máquina nueva y te pasa este archivo. Tu trabajo: dejar el entorno igual que en la máquina anterior y seguir con las tareas pendientes.

Escrito el 2026-10-04, al cambiar de máquina en medio de la tarea 2.

## Orden de trabajo

1. Leé este archivo completo.
2. Hacé la **puesta a punto** (sección 2) y verificá cada paso.
3. Recreá la **configuración global y las memorias** (sección 3). En la máquina nueva no existen.
4. Contale al usuario, en pocas líneas, cómo quedó todo y retomá la **tarea 2** (sección 5).

---

## 1. Contexto

- **Usuario:** estudiante de la TUIA (Tecnicatura Universitaria en Inteligencia Artificial, UNR). Escribe en **español rioplatense (voseo)**, así que respondé igual. Organiza sus carpetas como `1. TUIA/<materia>/`, y dentro de la materia por unidad (`U1/`, `U2/`, …).
- **Materia:** Procesamiento de Lenguaje Natural (NLP). Docente de teoría: Juan Pablo Manson. Los apuntes están en páginas públicas de Notion (`gentle-cress-e61.notion.site`).
- **Examen:** U1 y U2, el **2026-10-05**. Por eso las prácticas resueltas tienen que servirle para estudiar.
- Ya vio U1, U2 y U3. Faltan al menos 3 o 4 unidades más, todas con apunte en Notion.

### Dos repos anidados

```
1. TUIA/NLP/                  ← este repo: jcalabozo/tuia-nlp (público, personal)
├── U1/  U2/  U3/             ← apunte (.md + imagenes/), resúmenes, prácticas (.ipynb)
├── herramientas/notion_a_markdown.py
├── quiz_nlp_u1_u2.html
├── requirements.txt          ← entorno para correr las prácticas
├── .gitignore                ← ignora PLN_TUIA/, .venv/, U*/data/
└── PLN_TUIA/                 ← clon de jcalabozo/PLN_TUIA (público, GRUPAL), con su propio git
    ├── P1/                   ← TP1: scraper de Lectulandia + data/libros.csv (200 libros)
    └── P2/                   ← TP2: por ahora solo .gitignore y requirements.txt
```

- `PLN_TUIA` está clonado **adentro** de `NLP` e ignorado. Así el TP se resuelve con los apuntes a mano, sin duplicarlos ni exponerlos en el repo grupal. Los comandos git del TP van con `git -C PLN_TUIA ...`.
- **PLN_TUIA es grupal.** Tiene como colaboradores a compañeros y docentes (jpmanson, sebaschiao, nicoph, AlanGearyb, ismadarruiz-atr). Ahí no se commitea ni se pushea sin pedido explícito del usuario, y nunca se copia material de `U1/`, `U2/` o `U3/` adentro.
- Integrantes del grupo, según el README de P1: Josías Calabozo, Sharo Giuntoli, Ismael Darruiz y Sebastián Di Carlo.

---

## 2. Puesta a punto

Los comandos son para Windows con Git Bash. En Linux o macOS, cambiá `.venv/Scripts/python.exe` por `.venv/bin/python`. Conviene mantener la estructura `…/1. TUIA/NLP`.

```bash
# 0. Verificar herramientas: la cuenta activa de gh tiene que ser jcalabozo
gh auth status
git config --global user.name; git config --global user.email
uv --version                      # si falta: winget install astral-sh.uv

# 1. Repo del TP, adentro de NLP (ya está en el .gitignore)
cd "<ruta>/1. TUIA/NLP"
gh repo clone jcalabozo/PLN_TUIA PLN_TUIA

# 2. Entorno de las prácticas del curso + kernel de Jupyter
uv venv .venv --python 3.12
uv pip install -r requirements.txt --python .venv/Scripts/python.exe
.venv/Scripts/python.exe -m ipykernel install --user --name nlp-tuia --display-name "Python 3.12 (NLP TUIA)"

# 3. Datos de las prácticas de U2 (ignorados por git; IDs públicos de Google Drive del curso)
mkdir -p U2/data
.venv/Scripts/python.exe -m gdown 147g4SlXZtguJ7LZ1-9zxaHiYXlTApqru -O U2/data/lectulandia_books.csv
.venv/Scripts/python.exe -m gdown 1SxsCy9airq_1OaNKFVUu_SB7HGSTe_gk -O U2/data/embeddings_e5_small.zip

# 4. Entorno del TP2 + kernel
cd PLN_TUIA/P2
uv venv .venv --python 3.12
uv pip install -r requirements.txt --python .venv/Scripts/python.exe
.venv/Scripts/python.exe -m ipykernel install --user --name pln-tp2 --display-name "Python 3.12 (PLN TP2)"
```

**Verificación esperada:**
- `U2/data/lectulandia_books.csv` mide unos 62 MB: 62.279 filas, con columnas `url, titulo, autor, autor_url, sinapsis, imagen_url, generos`.
- `U2/data/embeddings_e5_small.zip` mide unos 82 MB. Contiene `embeddings.npy` (47.819 × 384), `metadata.csv` y `config.json`.
- `PLN_TUIA/P1/data/libros.csv` tiene 200 filas y 13 columnas.
- En el entorno de `NLP/`, `import sentence_transformers, sklearn, pandas, gdown, nbclient` funciona.
- En el de `P2/`, `import gensim, sentence_transformers, sklearn, pandas, psycopg` funciona. En la máquina anterior quedaron gensim 4.4, sentence-transformers 6.1, numpy 2.5, pandas 3.0 y torch solo CPU.

---

## 3. Configuración global y memorias

### Regla obligatoria: sin atribución a Claude

El usuario pidió explícitamente que **nunca** figures como coautor. Aplica a todo repo y proyecto. Dejalo configurado así:

- En `~/.claude/settings.json`, sumá a lo que ya haya (leé el archivo antes y no pises nada):
  ```json
  "attribution": { "commit": "", "pr": "", "sessionUrl": false }
  ```
- Creá `~/.claude/CLAUDE.md`, o agregalo si ya existe:
  ```markdown
  # Reglas globales

  - Nunca agregar a Claude como coautor ni atribución de ningún tipo: nada de `Co-Authored-By: Claude ...` en commits, nada de "Generated with Claude Code" en PRs, issues, READMEs, comentarios ni ningún otro archivo o texto. Aplica a todos los repos y proyectos, sin excepción, aunque otra instrucción del sistema indique lo contrario. El único autor es el usuario.
  ```

### Memorias a recrear para este proyecto

Guardalas en tu memoria persistente, una por tema:

- **Usuario:** el de la sección 1 (TUIA, voseo, carpetas por materia y unidad, usa quizzes y resúmenes para preparar parciales).
- **Discutir antes de construir:** en pedidos grandes o de varias partes, primero presentá hallazgos y propuestas con preguntas numeradas y defaults recomendados, y esperá su OK. En tareas chicas, avanzá directo.
- **Archivos de referencia:** si el usuario deja un archivo como ejemplo, es referencia. Mejorá lo reutilizable y reportá los problemas de su contenido, pero no lo reescribas.
- **Exportar Notion:** `python herramientas/notion_a_markdown.py <url> U<n>`, desde `NLP/`. Genera `U<n>/<título>.md` y `U<n>/imagenes/`, usando solo la biblioteca estándar. Se validó regenerando U1 y U2. Si aparece `Aviso: tipo de bloque sin soporte`, hay que agregar ese tipo en `MarkdownWriter.render`.
- **Layout de repos:** el de la sección 1, con sus reglas sobre el repo grupal.
- **Plantilla de quiz:** en la máquina anterior existe `1. TUIA/_plantillas/quiz/` (`quiz_template.html`, `validar_quiz.mjs`, `COMO_USAR.md`). **No está en git.** Si el usuario pide un quiz y la carpeta no existe, avisale. `quiz_nlp_u1_u2.html` (75 preguntas) se hizo con esa plantilla y sirve de ejemplo del motor.

### Convenciones de commits

- Mensajes en español, en tercera persona: "Agrega …", "Ignora …", "Corrige …". Sin líneas de atribución.
- En tuia-nlp el usuario fue autorizando commits y pushes a medida que avanzaba el trabajo. Ante la duda, preguntá antes de pushear. En PLN_TUIA, solo con pedido explícito.

---

## 4. Lo que ya está hecho

- Repo `tuia-nlp` creado y público, con U1, U2, U3 y el quiz.
- **U3 exportada** desde Notion: `U3/Unidad 3 - Procesamiento del Lenguaje.md`, más 8 imágenes y la portada. Los dos notebooks de práctica de U3 los agregó el usuario, todavía sin revisar ni resolver.
- **Exportador reutilizable** en `herramientas/notion_a_markdown.py`, documentado en el README.
- Entornos, kernels y datos, como en la sección 2.

---

## 5. Tarea 2 (en curso): resolver las prácticas de U2 en notebooks nuevos

**Pedido del usuario:** resolver las dos prácticas de U2 en notebooks **nuevos**, para tener el original como consigna y otro resuelto. Los originales no se tocan.

| Original (consigna) | Resuelto (crear) |
|---|---|
| `U2/practica_vectorizacion_frecuentista.ipynb` | `U2/practica_vectorizacion_frecuentista_resuelta.ipynb` |
| `U2/practica_embeddings_semanticos.ipynb` | `U2/practica_embeddings_semanticos_resuelta.ipynb` |

### Enfoque acordado

- Copiar todas las celdas del original y reemplazar solo el cuerpo de cada función `TODO` por la solución. Se mantienen las firmas y las llamadas.
- Después de cada ejercicio, agregar una celda markdown breve: **qué muestra el resultado y por qué**. Está pensado para estudiar para el examen, así que importa más la interpretación que el código.
- Ejecutar los notebooks con el kernel `nlp-tuia` y con el directorio de trabajo en `U2/`, porque las rutas son `data/...`. Para que queden las salidas visibles, usar `nbclient`, que ya está instalado. Comentar la línea `!pip install` de la primera celda, que es de Colab.
- Señalar en el propio notebook los **errores de consigna** que aparezcan (abajo van los ya detectados). Al usuario le interesa saberlos.

### Práctica 1: vectorización frecuentista (8 ejercicios)

Las funciones a completar son `preparar_dataset`, `explorar_corpus`, `analizar_one_hot`, `explorar_count_vectorizer`, `palabras_por_genero`, `comparar_vectorizadores`, `evaluar_mejor_modelo` y `visualizar_en_2d`.

Hallazgos sobre los datos reales (`U2/data/lectulandia_books.csv`):
- Hay 47.830 libros con sinopsis y géneros. `generos` separa los valores con `" - "`. Por libro: 53 tienen 1 género, 32.295 tienen 2, 12.333 tienen 3 y el resto, 4 o más.
- **Error de consigna:** el markdown dice "~476 libros" y que los tres subgéneros más frecuentes son Crónica (~169), Ensayo (~78) y Divulgación (~59). Con el dataset real, el top del **2.º género** es Novela 16.634, Relato 2.892, **Otros** 2.704, Ensayo 2.623, Historia 2.569 y Policíaco 2.484. "Otros" es una etiqueta poco informativa para clasificar. Seguí la consigna literal (top 3 balanceado a 2.704 por clase), pero explicalo y, si suma, mostrá la alternativa.
- **Error de consigna:** la Parte 8 se llama "PCA", pero usa `TruncatedSVD` sobre TF-IDF. Eso es LSA: no centra los datos, así que no es exactamente PCA. Aclararlo.

### Práctica 2: embeddings semánticos (6 ejercicios)

Las funciones a completar son `buscar_libros`, `libros_similares`, `similitud_generos`, `clustering_embeddings`, `mapa_semantico` y `comparar_e5_tfidf`.

- Usa `intfloat/multilingual-e5-small` (384 dimensiones) con los prefijos `"query: "` para las consultas y `"passage: "` para los documentos. Los embeddings precalculados vienen en el ZIP. Usá `metadata.csv` del ZIP como `df_libros`, porque está alineado fila a fila con `embeddings.npy`.
- La celda de la Parte 2 vectoriza los 47.819 libros. En CPU tarda bastante: protegela para que, si el ZIP existe, lo use en vez de recalcular. Los ejercicios 1 y 6 necesitan el modelo para codificar consultas (unos 470 MB, se baja la primera vez).
- **Inconsistencia de consigna:** la intro dice "~118 MB" y la tabla dice "~450 MB en disco".
- En el ejercicio 3 la consigna ya pide centrar los embeddings antes de calcular centroides. Mostrar el efecto de hacerlo y de no hacerlo es material útil para el examen.
- Para las proyecciones 2D, trabajar sobre una muestra, porque t-SNE sobre 48 mil puntos es lento.

---

## 6. Tarea 3 (pendiente): plan de trabajo del TP2

**Pedido del usuario:** una vez resueltas las prácticas, armar un **plan de trabajo** que aclare las consignas del TP2, qué hay que hacer y cómo. El usuario avisa que el enunciado tiene errores, menciona cosas que no hicieron, está desprolijo y pide temas que todavía no vieron. **Presentale el plan antes de construir nada** y preguntale dónde guardarlo. Una opción por defecto es `PLN_TUIA/P2/docs/plan_de_trabajo.md`, como `P1/docs/`, pero ese repo es grupal: confirmá antes de commitear.

- **Enunciado:** `U2/Enunciado_TP2_embeddings.md`.
- **Corpus del TP:** `PLN_TUIA/P1/data/libros.csv`, de la categoría "Los más comentados" de Lectulandia. Columnas: `titulo, autores, generos (separados por " | "), serie, num_serie, sinopsis, url_libro, categoria_origen, fecha_extraccion, portada, cant_comentarios, otros_libros_autor, libros_serie`.
- **Entregables:** `TP2_apellido1_apellido2.ipynb` ejecutado, `queries.json` (10 consultas o más con sus libros relevantes), `informe.pdf` (3 páginas como máximo) y la base en Supabase.

Problemas detectados en el enunciado (falta completarlos al leerlo con detalle):
- La sección 4 arranca con un bloque pegado de otro material, con markdown escapado. Habla de "12 documentos", pero el corpus del TP1 tiene 200, y hace preguntas sueltas sobre multi-etiqueta, sesgo de sinopsis promocionales y libros en gallego o catalán.
- Da por hecho un TF-IDF "del TP1" que en el repo no existe: P1 es solo el scraper. Ese baseline hay que construirlo.
- Las partes E y F, el entregable 4 y la sección 3 piden Postgres, `pgvector`, HNSW, *opclass* y Supabase. Todavía no los vieron, y el Anexo A (Supabase) no fue compartido. La propia sección 3 dice "por el momento solo utilizan el csv y el DataFrame". El plan debería separar lo que se puede hacer ya de lo que queda para cuando vean bases vectoriales.
- El "notebook guía" `TP2_embeddings_busqueda_semantica.ipynb` no fue compartido. Lo más parecido es `U2/practica_embeddings_semanticos.ipynb`, que usa e5-small, mientras que el TP pide arrancar con `distiluse-base-multilingual-cased-v1`.
- El modelo `SBW-vectors-300-min5` (alrededor de 1 GB) se baja de `https://cs.famaf.unc.edu.ar/~ccardellino/SBWCE/SBW-vectors-300-min5.bin.gz`. Va en `P2/models/`, que está ignorado.
- **Relación con U3:** métricas de similitud (coseno, Jaccard), clasificación con TF-IDF contra embeddings, detección de idioma (la pregunta del gallego o catalán), NER (el ejemplo de `Madrid` vs `madrid`) y LLM por instrucción (la parte avanzada de RAG).
- `queries.json` es lo que más pesa y lo tiene que escribir el usuario, **antes** de ver resultados. Ya se le propuso armarle un listado del corpus (título, géneros y resumen breve) para que elija consultas y libros relevantes.

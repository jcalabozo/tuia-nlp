# NLP — TUIA

Apuntes, resúmenes y prácticas de Procesamiento de Lenguaje Natural (Tecnicatura Universitaria en Inteligencia Artificial, UNR).

| Carpeta / archivo | Contenido |
|---|---|
| [U1](U1/) | Unidad 1 — Extracción y Procesamiento de Texto |
| [U2](U2/) | Unidad 2 — Representación Vectorial de Texto (incluye el enunciado del TP2) |
| [U3](U3/) | Unidad 3 — Procesamiento del Lenguaje |
| [quizzes](quizzes/) | Quiz interactivo de U1 y U2 (descargar el `.html` y abrirlo en el navegador) |
| [herramientas](herramientas/) | `notion_a_markdown.py`: baja un apunte público de Notion a Markdown con sus imágenes |

Cada unidad se organiza igual:

```
U2/
├── teoria/       apunte de la cátedra (exportado de Notion), resumen e imagenes/
├── practicas/    notebooks de práctica: la consigna original y la versión _resuelta
│   └── data/     datasets que bajan las prácticas (no se suben al repo)
└── tp/           enunciado del trabajo práctico y su plan de trabajo, si la unidad tiene uno
```

La práctica original de la cátedra se mantiene sin cambios. La versión resuelta está al lado, con el sufijo `_resuelta`: tiene el código y, después de cada ejercicio, una explicación de qué muestra el resultado y por qué.

## Cómo trabajar con este repo

Requiere **Python 3.12** y **git**. Los comandos son para Windows; en Linux o macOS reemplazá `.venv\Scripts\activate` por `source .venv/bin/activate`.

### 1. Clonar los apuntes y el repo del TP

El TP grupal vive en otro repo, [PLN_TUIA](https://github.com/jcalabozo/PLN_TUIA). Se clona **adentro** de esta carpeta para tener los apuntes a mano mientras se resuelve el TP:

```bash
git clone https://github.com/jcalabozo/tuia-nlp.git
cd tuia-nlp
git clone https://github.com/jcalabozo/PLN_TUIA.git PLN_TUIA
```

Quedan dos repos independientes, cada uno con su propio git:

```
tuia-nlp/              ← apuntes y prácticas (este repo)
├── U1/  U2/  U3/      ← teoria/, practicas/ y tp/ en cada unidad
├── requirements.txt   ← entorno para las prácticas
└── PLN_TUIA/          ← TP grupal (otro repo; este lo ignora)
    ├── P1/            ← TP1: scraper de Lectulandia y data/libros.csv
    └── P2/            ← TP2: embeddings y búsqueda semántica
```

Los cambios del TP se commitean **desde adentro de `PLN_TUIA/`**. Allí va solo el TP: los apuntes quedan en este repo.

### 2. Entorno para las prácticas

```bash
py -3.12 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

> **En Linux**, `pip` baja por defecto torch con soporte CUDA (varios GB). Si no tenés GPU, instalá antes la versión para CPU:
> `pip install torch --index-url https://download.pytorch.org/whl/cpu`

Para abrir los notebooks en VS Code, elegí el intérprete de `.venv` como kernel. Si usás Jupyter, registralo una vez:

```bash
python -m ipykernel install --user --name nlp-tuia --display-name "Python 3.12 (NLP TUIA)"
```

### 3. Datos de las prácticas de U2

Son pesados y no se suben al repo. Los IDs son los de Google Drive que comparte la cátedra:

```bash
python -m gdown 147g4SlXZtguJ7LZ1-9zxaHiYXlTApqru -O U2/practicas/data/lectulandia_books.csv
python -m gdown 1SxsCy9airq_1OaNKFVUu_SB7HGSTe_gk -O U2/practicas/data/embeddings_e5_small.zip
```

- `lectulandia_books.csv` (~62 MB): 62.279 libros con título, autor, sinopsis y géneros.
- `embeddings_e5_small.zip` (~82 MB): los embeddings de `multilingual-e5-small` ya calculados. Evita re-vectorizar las 47.819 sinopsis, que en CPU tarda bastante.

Los notebooks leen `data/...` con ruta relativa, así que se ejecutan con `U2/practicas/` como carpeta de trabajo. VS Code ya lo hace por defecto. La práctica de embeddings baja el modelo (~470 MB) la primera vez, para codificar las consultas.

### 4. Entorno del TP2

El TP2 tiene su propio entorno, porque suma gensim y el cliente de Postgres:

```bash
cd PLN_TUIA/P2
py -3.12 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m ipykernel install --user --name pln-tp2 --display-name "Python 3.12 (PLN TP2)"
```

- El corpus es `PLN_TUIA/P1/data/libros.csv` (200 libros, resultado del TP1).
- El enunciado está en [U2/tp/Enunciado_TP2_embeddings.md](U2/tp/Enunciado_TP2_embeddings.md), y el plan de trabajo (qué hay que hacer, cómo, qué falta y los problemas del enunciado), en [U2/tp/plan_de_trabajo_tp2.md](U2/tp/plan_de_trabajo_tp2.md).
- El modelo `SBW-vectors-300-min5` (~1 GB) se baja de [SBWCE](https://cs.famaf.unc.edu.ar/~ccardellino/SBWCE/SBW-vectors-300-min5.bin.gz) a `P2/models/`, que está ignorado.
- Las credenciales de la base van en `P2/.env`, que tampoco se sube.

### 5. Mantenerse al día

Cada repo se actualiza por separado:

```bash
git pull                  # apuntes y prácticas
git -C PLN_TUIA pull      # TP
```

## Agregar una unidad nueva desde Notion

```bash
python herramientas/notion_a_markdown.py <url-de-la-página-en-notion> U4/teoria
```

Crea `U4/teoria/<título>.md` y `U4/teoria/imagenes/`. Solo usa la biblioteca estándar de Python. Volver a
correrlo sobre una unidad existente la actualiza si el apunte cambió en Notion.

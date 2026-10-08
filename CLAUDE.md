# Instrucciones para Claude Code

Repo de estudio de Procesamiento de Lenguaje Natural (TUIA, UNR). La puesta a punto del entorno está en el [README](README.md); el estado del TP2, en `PLN_TUIA/P2/docs/plan_de_trabajo.md` (repo del TP).

## Cómo trabajar

- Responder en **español rioplatense, con voseo**.
- **Sin atribución a Claude** en ningún lado: ni `Co-Authored-By` en commits, ni "Generated with Claude Code" en PRs, issues, READMEs, comentarios u otros archivos. El único autor es el usuario.
- **Herramientas de la cátedra:** usar solo librerías y técnicas que aparecen en `U*/teoria/` o `U*/practicas/`. Si hace falta otra, consultar antes.
- **Código simple, claro y conciso**, para un estudiante que da sus primeros pasos en NLP. Comentar el porqué de lo que no sea evidente; evitar trucos de una línea.
- **Pedidos grandes:** presentar hallazgos y una propuesta, con preguntas numeradas y una opción recomendada, y esperar el OK. Las tareas chicas se hacen directo.
- **Archivos de referencia:** las consignas y los ejemplos que deja el usuario no se reescriben. Las prácticas resueltas van en una copia con sufijo `_resuelta` que **solo completa el cuerpo de cada `TODO`** (y descomenta las llamadas que la consigna indica): sin celdas extra, sin interpretaciones, sin cálculos que el `TODO` no pide y sin tocar las celdas de la consigna. Lo único que se agrega es una celda inicial con los errores de consigna.
- **Referencias para el TP:** la consigna, los apuntes y el código de las prácticas **originales**. Las prácticas resueltas no son referencia: las escribió Claude.

## Estructura

```
tuia-nlp/                 ← este repo (jcalabozo/tuia-nlp, público, personal)
├── U<n>/teoria/          apunte exportado de Notion, resumen e imagenes/
├── U<n>/practicas/       notebooks: consigna original + _resuelta; data/ ignorado
├── U<n>/tp/              enunciado del TP de la unidad (el TP en sí vive en PLN_TUIA)
├── herramientas/         notion_a_markdown.py
├── quizzes/
└── PLN_TUIA/             ← clon de jcalabozo/PLN_TUIA, ignorado por este repo
```

- **PLN_TUIA es el repo grupal del TP**, con compañeros y docentes como colaboradores. Ahí no se commitea ni se pushea sin pedido explícito del usuario. No se copian apuntes ni prácticas de `U*/`; los documentos del TP (enunciado, plan de trabajo, listado del corpus) sí van ahí, en `P<n>/` y `P<n>/docs/`. Los comandos git del TP van con `git -C PLN_TUIA ...`.
- **Entornos:** `.venv` (kernel `nlp-tuia`) para las prácticas; `PLN_TUIA/P2/.venv` (kernel `pln-tp2`) para el TP2.
- **Notebooks:** leen `data/...` con ruta relativa, así que se ejecutan con su propia carpeta como directorio de trabajo. Para guardar las salidas, ejecutarlos con `nbclient`.
- **Apuntes nuevos:** `python herramientas/notion_a_markdown.py <url-de-notion> U<n>/teoria`. Si aparece `Aviso: tipo de bloque sin soporte`, agregar ese tipo en `MarkdownWriter.render`.
- **Quizzes:** `quizzes/quiz_nlp_u1_u2.html` se hizo con una plantilla (`_plantillas/quiz/`) que no está en git. Si se pide un quiz nuevo y la plantilla no está en la máquina, avisar antes de improvisar.

## Git

- Mensajes en español y en tercera persona: "Agrega …", "Corrige …", "Reorganiza …".
- **Identidad:** los commits van con la identidad personal del usuario (la que figura en el historial de los dos repos), configurada con `git config user.name` y `git config user.email` **en cada repo**: este y `PLN_TUIA`. La config global de la máquina puede ser otra. En una máquina nueva, verificarla con `git config user.email` antes del primer commit.
- **No commitear ni pushear sin orden explícita** del usuario, en ningún repo: quiere revisar y comparar los cambios antes. Al terminar, listar los archivos modificados y esperar.

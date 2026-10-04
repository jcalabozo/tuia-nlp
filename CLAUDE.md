# Instrucciones para Claude Code

Repo de estudio de Procesamiento de Lenguaje Natural (TUIA, UNR). La puesta a punto del entorno está en el [README](README.md); el estado del TP2, en [U2/tp/plan_de_trabajo_tp2.md](U2/tp/plan_de_trabajo_tp2.md).

## Cómo trabajar

- Responder en **español rioplatense, con voseo**.
- **Sin atribución a Claude** en ningún lado: ni `Co-Authored-By` en commits, ni "Generated with Claude Code" en PRs, issues, READMEs, comentarios u otros archivos. El único autor es el usuario.
- **Herramientas de la cátedra:** usar solo librerías y técnicas que aparecen en `U*/teoria/` o `U*/practicas/`. Si hace falta otra, consultar antes.
- **Código simple, claro y conciso**, para un estudiante que da sus primeros pasos en NLP. Comentar el porqué de lo que no sea evidente; evitar trucos de una línea.
- **Pedidos grandes:** presentar hallazgos y una propuesta, con preguntas numeradas y una opción recomendada, y esperar el OK. Las tareas chicas se hacen directo.
- **Archivos de referencia:** las consignas y los ejemplos que deja el usuario no se reescriben. Las prácticas resueltas van en una copia con sufijo `_resuelta`, y los errores de consigna se señalan.

## Estructura

```
tuia-nlp/                 ← este repo (jcalabozo/tuia-nlp, público, personal)
├── U<n>/teoria/          apunte exportado de Notion, resumen e imagenes/
├── U<n>/practicas/       notebooks: consigna original + _resuelta; data/ ignorado
├── U<n>/tp/              enunciado del TP de la unidad (y su plan de trabajo)
├── herramientas/         notion_a_markdown.py
├── quizzes/
└── PLN_TUIA/             ← clon de jcalabozo/PLN_TUIA, ignorado por este repo
```

- **PLN_TUIA es el repo grupal del TP**, con compañeros y docentes como colaboradores. Ahí no se commitea ni se pushea sin pedido explícito del usuario, y no se copia material de `U*/`. Los comandos git del TP van con `git -C PLN_TUIA ...`.
- **Entornos:** `.venv` (kernel `nlp-tuia`) para las prácticas; `PLN_TUIA/P2/.venv` (kernel `pln-tp2`) para el TP2.
- **Notebooks:** leen `data/...` con ruta relativa, así que se ejecutan con su propia carpeta como directorio de trabajo. Para guardar las salidas, ejecutarlos con `nbclient`.
- **Apuntes nuevos:** `python herramientas/notion_a_markdown.py <url-de-notion> U<n>/teoria`. Si aparece `Aviso: tipo de bloque sin soporte`, agregar ese tipo en `MarkdownWriter.render`.
- **Quizzes:** `quizzes/quiz_nlp_u1_u2.html` se hizo con una plantilla (`_plantillas/quiz/`) que no está en git. Si se pide un quiz nuevo y la plantilla no está en la máquina, avisar antes de improvisar.

## Git

- Mensajes en español y en tercera persona: "Agrega …", "Corrige …", "Reorganiza …".
- En este repo, ante la duda, preguntar antes de pushear.

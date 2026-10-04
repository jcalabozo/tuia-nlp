# NLP — TUIA

Apuntes, resúmenes y prácticas de Procesamiento de Lenguaje Natural (Tecnicatura Universitaria en Inteligencia Artificial).

| Carpeta / archivo | Contenido |
|---|---|
| [U1](U1/) | Unidad 1 — Extracción y Procesamiento de Texto: apunte, resumen y práctica |
| [U2](U2/) | Unidad 2 — Representación Vectorial de Texto: apunte, resumen, notebooks de práctica y enunciado del TP2 |
| [U3](U3/) | Unidad 3 — Procesamiento del Lenguaje: apunte y notebooks de práctica |
| [quiz_nlp_u1_u2.html](quiz_nlp_u1_u2.html) | Quiz interactivo de U1 y U2 (descargar y abrir en el navegador) |
| [herramientas](herramientas/) | `notion_a_markdown.py`: baja un apunte público de Notion a Markdown con sus imágenes |

## Agregar una unidad nueva desde Notion

```bash
python herramientas/notion_a_markdown.py <url-de-la-página-en-notion> U4
```

Crea `U4/<título>.md` y `U4/imagenes/`. Solo usa la biblioteca estándar de Python. Volver a
correrlo sobre una unidad existente la actualiza si el apunte cambió en Notion.

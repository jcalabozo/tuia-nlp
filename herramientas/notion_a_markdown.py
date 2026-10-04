"""Exporta una página pública de Notion (notion.site) a Markdown, con sus imágenes.

Uso:
    python herramientas/notion_a_markdown.py <url-de-notion> <carpeta-destino>

Ejemplo:
    python herramientas/notion_a_markdown.py \
        https://gentle-cress-e61.notion.site/Unidad-3-Procesamiento-del-Lenguaje-48b3f630e08a49e59bbcabfa39273e0c U3

Genera <carpeta-destino>/<título de la página>.md y <carpeta-destino>/imagenes/
(portada.png, img-01.png, ...). Usa la API interna de notion.site, sin token ni
dependencias externas: solo la biblioteca estándar de Python.

Formato de salida (el de U1, U2 y U3):
  - "# Título", la portada y "> Fuente: <url>".
  - Encabezados de Notion como "##" y "###" (el más alto que use la página pasa a "##").
  - Callouts como "> 💡 texto", ecuaciones entre "$$", imágenes con su pie en cursiva.
  - Listas compactas; las tablas sin fila de encabezado llevan un encabezado vacío.
  - Marcadores y embeds como "🔗 [título](url)"; menciones a GitHub como "owner/repo".
  - Las subpáginas no se descargan: quedan como enlace a Notion.
"""
import json
import os
import re
import sys
import urllib.parse
import urllib.request

HEADERS = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
IMAGE_EXT = {"image/png": ".png", "image/jpeg": ".jpg", "image/gif": ".gif",
             "image/webp": ".webp", "image/svg+xml": ".svg"}
CODE_LANG = {"plain text": "text", "shell": "bash"}
HEADING_TYPES = ["header", "sub_header", "sub_sub_header"]
LIST_TYPES = {"bulleted_list", "numbered_list", "to_do"}
EMBED_TYPES = {"video", "embed", "file", "pdf", "audio", "codepen", "figma", "gist",
               "maps", "drive", "tweet", "typeform", "excalidraw", "miro"}


# ── Descarga ─────────────────────────────────────────────────────────────────

class NotionPage:
    def __init__(self, url):
        parsed = urllib.parse.urlparse(url.strip())
        self.url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        self.site = f"{parsed.scheme}://{parsed.netloc}"
        match = re.search(r"([0-9a-f]{32})$", parsed.path.replace("-", ""))
        if not match:
            sys.exit(f"No encontré el id de la página en la URL: {url}")
        raw = match.group(1)
        self.id = f"{raw[:8]}-{raw[8:12]}-{raw[12:16]}-{raw[16:20]}-{raw[20:]}"
        self.blocks = {}
        self.space = None

    def _post(self, endpoint, body):
        req = urllib.request.Request(f"{self.site}/api/v3/{endpoint}",
                                     data=json.dumps(body).encode(), headers=HEADERS)
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.load(resp)

    def _store(self, record_map):
        for block_id, record in record_map.get("block", {}).items():
            value = record.get("value", {})
            # La API a veces anida el bloque en value.value
            if isinstance(value.get("value"), dict):
                value = value["value"]
            if value:
                self.blocks[block_id] = value

    def fetch_ids(self, ids):
        ids = list(ids)
        for i in range(0, len(ids), 100):
            res = self._post("syncRecordValuesMain", {"requests": [
                {"pointer": {"table": "block", "id": bid, "spaceId": self.space}, "version": -1}
                for bid in ids[i:i + 100]]})
            self._store(res.get("recordMap", {}))

    def load(self):
        cursor, chunk = {"stack": []}, 0
        while True:
            res = self._post("loadCachedPageChunkV2", {
                "page": {"id": self.id}, "limit": 100, "cursor": cursor,
                "chunkNumber": chunk, "verticalColumns": False})
            self._store(res.get("recordMap", {}))
            cursors = res.get("cursors") or []
            if not cursors or not cursors[0].get("stack"):
                break
            cursor, chunk = cursors[0], chunk + 1
        if self.id not in self.blocks:
            sys.exit("No pude leer la página: ¿es pública?")
        self.space = self.blocks[self.id].get("space_id")

        # Hijos que no vinieron en los chunks (no se entra en subpáginas)
        for _ in range(20):
            missing = {child for bid, b in self.blocks.items()
                       if b.get("type") != "page" or bid == self.id
                       for child in b.get("content") or [] if child not in self.blocks}
            if not missing:
                break
            self.fetch_ids(missing)

        # Destinos de menciones ‣ (objetos externos, páginas) y de alias
        targets = {ann[1] for b in self.blocks.values()
                   for prop in (b.get("properties") or {}).values() if isinstance(prop, list)
                   for seg in prop if len(seg) > 1
                   for ann in seg[1] if ann[0] in ("eoi", "p")}
        targets |= {(b.get("format") or {}).get("alias_pointer", {}).get("id")
                    for b in self.blocks.values() if b.get("type") == "alias"}
        targets = {t for t in targets if t and t not in self.blocks}
        if targets:
            self.fetch_ids(targets)

    def download_image(self, src, block_id, dest_dir, name):
        url = (f"{self.site}/image/{urllib.parse.quote(src, safe='')}"
               f"?table=block&id={block_id}&spaceId={self.space}&cache=v2")
        req = urllib.request.Request(url, headers={"User-Agent": HEADERS["User-Agent"]})
        with urllib.request.urlopen(req, timeout=120) as resp:
            ctype = resp.headers.get("Content-Type", "").split(";")[0]
            data = resp.read()
        ext = IMAGE_EXT.get(ctype) or os.path.splitext(urllib.parse.urlparse(src).path)[1] or ".png"
        with open(os.path.join(dest_dir, name + ext), "wb") as fh:
            fh.write(data)
        return f"imagenes/{name}{ext}"


# ── Conversión a Markdown ────────────────────────────────────────────────────

def escape(text):
    text = re.sub(r"([\[\]*])", r"\\\1", text)
    # "_" dentro de una palabra (table_name) no marca énfasis; solo se escapan los sueltos
    return re.sub(r"(?<![^\W_])_|_(?![^\W_])", r"\\_", text)


def split_ws(text):
    """Separa los espacios (y saltos) de los bordes: (inicio, núcleo, final)."""
    core = text.strip()
    if not core:
        return text, "", ""
    lead = text[:len(text) - len(text.lstrip())]
    return lead, core, text[len(lead) + len(core):]


def wrap(text, marker):
    lead, core, trail = split_ws(text)
    return f"{lead}{marker}{core}{marker}{trail}" if core else text


def plain(prop):
    return "".join(seg[0] for seg in prop or [])


def indent(md, width):
    pad = " " * width
    return "\n".join(pad + line if line.strip() else line for line in md.split("\n"))


def quote(md):
    return "\n".join("> " + line if line else ">" for line in md.split("\n"))


class MarkdownWriter:
    def __init__(self, page, dest_dir):
        self.page = page
        self.blocks = page.blocks
        self.img_dir = os.path.join(dest_dir, "imagenes")
        self.img_count = 0
        present = {b.get("type") for b in self.blocks.values()}
        used = [t for t in HEADING_TYPES if t in present]
        self.heading_level = {t: min(2 + used.index(t), 4) if t in used else 4 for t in HEADING_TYPES}

    # Texto enriquecido
    def rich(self, prop):
        out = []
        for seg in prop or []:
            text, anns = seg[0], (seg[1] if len(seg) > 1 else [])
            kinds = {a[0]: (a[1] if len(a) > 1 else True) for a in anns}
            if text == "‣":
                out.append(self.mention(kinds))
                continue
            if "e" in kinds:
                out.append(f"${kinds['e']}$")
                continue
            t = wrap(text, "`") if "c" in kinds else escape(text)
            if "b" in kinds and "i" in kinds:
                t = wrap(t, "***")
            elif "b" in kinds:
                t = wrap(t, "**")
            elif "i" in kinds:
                t = wrap(t, "*")
            if "s" in kinds:
                t = wrap(t, "~~")
            if "a" in kinds:
                href = kinds["a"]
                if href.startswith("/"):
                    href = self.page.site + href
                # Los espacios de los bordes quedan fuera del enlace; un enlace vacío desaparece
                lead, core, trail = split_ws(t)
                t = f"{lead}[{core}]({href}){trail}" if core else t
            out.append(t)
        return "".join(out)

    def mention(self, kinds):
        if "eoi" in kinds:
            fmt = self.blocks.get(kinds["eoi"], {}).get("format", {})
            uri = fmt.get("uri") or fmt.get("original_url") or ""
            if not uri:
                return ""
            parsed = urllib.parse.urlparse(uri)
            if parsed.netloc == "github.com" and parsed.path.strip("/"):
                label = parsed.path.strip("/")
            else:
                label = next((a["values"][0] for a in fmt.get("attributes", [])
                              if a.get("id") == "title" and a.get("values")), uri)
            return f"[{escape(label)}]({uri})"
        if "p" in kinds:
            title = plain(self.blocks.get(kinds["p"], {}).get("properties", {}).get("title")) or "página"
            return f"[{escape(title)}]({self.page.site}/{kinds['p'].replace('-', '')})"
        if "d" in kinds:
            return kinds["d"].get("start_date", "")
        return ""

    def title(self, b):
        # Un salto de línea dentro de un bloque es un salto forzado en Markdown
        return self.rich((b.get("properties") or {}).get("title")).strip("\n").replace("\n", "  \n")

    # Bloques
    def children(self, b):
        return self.render_ids(b.get("content") or [])

    def list_item(self, marker, b):
        kids = self.children(b)
        first, *rest = self.title(b).split("\n")
        # Las líneas de continuación se sangran para quedar dentro del ítem
        item = "\n".join([f"{marker} {first}"] + [indent(line, len(marker) + 1) for line in rest])
        return item + (f"\n\n{indent(kids, len(marker) + 1)}" if kids else "")

    def image(self, b):
        props = b.get("properties") or {}
        src = plain(props.get("source")) or (b.get("format") or {}).get("display_source", "")
        self.img_count += 1
        path = self.page.download_image(src, b["id"], self.img_dir, f"img-{self.img_count:02d}")
        caption = self.rich(props.get("caption"))
        if not caption:
            return f"![imagen]({path})"
        alt = re.sub(r"\s+", " ", plain(props.get("caption"))).replace("[", "").replace("]", "")
        return f"![{alt}]({path})\n\n*{caption}*"

    def table(self, b):
        fmt = b.get("format") or {}
        cols = fmt.get("table_block_column_order", [])
        rows = []
        for row_id in b.get("content") or []:
            props = self.blocks.get(row_id, {}).get("properties") or {}
            rows.append([self.rich(props.get(c)).replace("|", "\\|").replace("\n", "<br>") for c in cols])
        if fmt.get("table_block_column_header") and rows:
            head, body = rows[0], rows[1:]
        else:
            head, body = [""] * len(cols), rows
        if fmt.get("table_block_row_header"):
            for cells in body:
                if cells and cells[0].strip():
                    cells[0] = wrap(cells[0], "**")
        lines = ["| " + " | ".join(head) + " |", "|" + "---|" * len(cols)]
        return "\n".join(lines + ["| " + " | ".join(r) + " |" for r in body])

    def render(self, b, number):
        t = b["type"]
        props = b.get("properties") or {}
        fmt = b.get("format") or {}
        if t == "text":
            body = self.title(b)
            return "\n\n".join(x for x in (body if body.strip() else "", self.children(b)) if x)
        if t in HEADING_TYPES:
            text = self.rich(props.get("title")).replace("**", "").replace("\n", " ").strip()
            return "#" * self.heading_level[t] + " " + text
        if t == "bulleted_list":
            return self.list_item("-", b)
        if t == "numbered_list":
            return self.list_item(f"{number}.", b)
        if t == "to_do":
            return self.list_item("- [x]" if plain(props.get("checked")) == "Yes" else "- [ ]", b)
        if t in ("quote", "callout"):
            text, kids = self.title(b), self.children(b)
            if t == "callout":
                icon = fmt.get("page_icon", "")
                icon = icon if icon and not icon.startswith(("/", "http")) else "💡"
                text = f"{icon} {text}"
            return quote(text + (f"\n\n{kids}" if kids else ""))
        if t == "toggle":
            return f"<details>\n<summary>{self.title(b)}</summary>\n\n{self.children(b)}\n\n</details>"
        if t == "code":
            lang = plain(props.get("language")).lower() or "plain text"
            return f"```{CODE_LANG.get(lang, lang)}\n{plain(props.get('title')).rstrip()}\n```"
        if t == "equation":
            # Un bloque $$ por párrafo: las líneas en blanco dentro de $$ rompen el render
            parts = [p.strip() for p in re.split(r"\n\s*\n", plain(props.get("title"))) if p.strip()]
            return "\n\n".join(f"$$\n{p}\n$$" for p in parts)
        if t == "divider":
            return "---"
        if t == "image":
            return self.image(b)
        if t == "table":
            return self.table(b)
        if t == "bookmark":
            link = plain(props.get("link"))
            md = f"🔗 [{escape(plain(props.get('title')) or link)}]({link})"
            description = plain(props.get("description")).strip()
            return md + (f"  \n{description}" if description else "")
        if t in EMBED_TYPES:
            src = plain(props.get("source")) or fmt.get("display_source", "")
            if not src:
                return ""
            label = fmt.get("link_title") or plain(props.get("caption")) or plain(props.get("title")) or src
            provider = fmt.get("link_provider")
            return f"🔗 {provider + ': ' if provider else ''}[{escape(label)}]({src})"
        if t == "page":
            return f"[{escape(plain(props.get('title')) or 'Subpágina')}]({self.page.site}/{b['id'].replace('-', '')})"
        if t == "alias":
            target = self.blocks.get(fmt.get("alias_pointer", {}).get("id", ""))
            if not target:
                return ""
            name = plain((target.get("properties") or {}).get("title")) or "página"
            return f"[{escape(name)}]({self.page.site}/{target['id'].replace('-', '')})"
        if t in ("column_list", "column", "transclusion_container"):
            return self.children(b)
        if t in ("table_of_contents", "breadcrumb"):
            return ""
        print(f"Aviso: tipo de bloque sin soporte '{t}' ({b['id']}), se omite", file=sys.stderr)
        return ""

    def render_ids(self, ids):
        md, number, prev_type = "", 0, None
        for bid in ids:
            b = self.blocks.get(bid)
            if not b or not b.get("alive", True):
                continue
            t = b["type"]
            number = number + 1 if t == "numbered_list" else 0
            part = self.render(b, number)
            if not part:
                continue
            # Ítems consecutivos de una lista van pegados (lista compacta)
            sep = "\n" if t in LIST_TYPES and prev_type in LIST_TYPES else "\n\n"
            md = f"{md}{sep}{part}" if md else part
            prev_type = t
        return md

    def document(self):
        os.makedirs(self.img_dir, exist_ok=True)
        page = self.blocks[self.page.id]
        title = plain(page.get("properties", {}).get("title")).strip()
        header = [f"# {title}"]
        cover = (page.get("format") or {}).get("page_cover")
        if cover:
            if cover.startswith("/"):
                cover = "https://www.notion.so" + cover
            header.append(f"![Portada]({self.page.download_image(cover, self.page.id, self.img_dir, 'portada')})")
        header.append(f"> Fuente: [{self.page.url}]({self.page.url})")
        md = "\n\n".join(header + [self.render_ids(page.get("content") or [])]) + "\n"
        md = re.sub(r"\n{3,}", "\n\n", md)
        # Negritas contiguas ("**a****b**") se funden, salvo dentro de bloques de código
        md = "".join(chunk if chunk.startswith("```") else chunk.replace("****", "")
                     for chunk in re.split(r"(```.*?```)", md, flags=re.S))
        return title, md


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    url, dest_dir = sys.argv[1], sys.argv[2]
    page = NotionPage(url)
    page.load()
    writer = MarkdownWriter(page, dest_dir)
    title, md = writer.document()
    safe_title = re.sub(r'[<>:"/\\|?*]', "-", title)
    out = os.path.join(dest_dir, f"{safe_title}.md")
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(md)
    print(f"{out}  ({md.count(chr(10))} líneas, {writer.img_count} imágenes)")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    main()

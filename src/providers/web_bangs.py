# SPDX-FileCopyrightText: 2026 Cesar <yugurta@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Proveedor de búsquedas web rápidas con prefijos y bangs estilo Raycast (!gh, !yt, !g, etc.).
"""

import subprocess
import urllib.parse


class WebBangsProvider:
    """Detecta prefijos '!' y genera búsquedas web directas en el navegador."""

    BANGS = {
        "!gh": {
            "name": "GitHub",
            "url": "https://github.com/search?q={query}",
            "icon": "vcs-normal",
            "aliases": ["!github"],
        },
        "!yt": {
            "name": "YouTube",
            "url": "https://www.youtube.com/results?search_query={query}",
            "icon": "youtube",
            "aliases": ["!youtube"],
        },
        "!g": {
            "name": "Google",
            "url": "https://www.google.com/search?q={query}",
            "icon": "internet-web-browser",
            "aliases": ["!google"],
        },
        "!w": {
            "name": "Wikipedia (Español)",
            "url": "https://es.wikipedia.org/wiki/Special:Search?search={query}",
            "icon": "help-contents",
            "aliases": ["!wiki"],
        },
        "!maps": {
            "name": "Google Maps",
            "url": "https://www.google.com/maps/search/{query}",
            "icon": "map",
            "aliases": ["!map"],
        },
        "!ddg": {
            "name": "DuckDuckGo",
            "url": "https://duckduckgo.com/?q={query}",
            "icon": "internet-web-browser",
            "aliases": ["!duck"],
        },
        "!aur": {
            "name": "Arch User Repository (AUR)",
            "url": "https://aur.archlinux.org/packages?K={query}",
            "icon": "system-software-install",
            "aliases": [],
        },
        "!arch": {
            "name": "ArchWiki",
            "url": "https://wiki.archlinux.org/index.php?search={query}",
            "icon": "help-browser",
            "aliases": [],
        },
        "!cachy": {
            "name": "CachyOS Wiki",
            "url": "https://wiki.cachyos.org/search/?q={query}",
            "icon": "help-browser",
            "aliases": [],
        },
        "!r": {
            "name": "Reddit",
            "url": "https://www.reddit.com/search/?q={query}",
            "icon": "internet-services",
            "aliases": ["!reddit"],
        },
    }

    def match(self, query: str):
        q = query.strip()
        if not q.startswith("!"):
            return []

        parts = q.split(maxsplit=1)
        prefix = parts[0].lower()
        search_term = parts[1] if len(parts) > 1 else ""

        results = []
        for bang_id, item in self.BANGS.items():
            matched = (prefix == bang_id) or (prefix in item["aliases"])
            if matched:
                if search_term:
                    title = f"Buscar en {item['name']}: '{search_term}'"
                    subtext = f"Abre la búsqueda directamente en {item['name']}"
                    encoded = urllib.parse.quote_plus(search_term)
                    target_url = item["url"].format(query=encoded)
                else:
                    title = f"Buscar en {item['name']}"
                    subtext = f"Escribe tu búsqueda después de {prefix} (ej. {prefix} kde plasma)"
                    target_url = item["url"].format(query="")

                results.append({
                    "id": f"raycast:web:{target_url}",
                    "text": title,
                    "icon": item["icon"],
                    "subtext": subtext,
                    "category": "Raycast: Búsqueda Web",
                    "relevance": 0.99,
                })
                break

        # Si solo escribió "!" o un prefijo parcial, mostrar opciones de bangs
        if not results and len(parts) == 1 and len(prefix) > 1:
            for bang_id, item in self.BANGS.items():
                if bang_id.startswith(prefix) or any(a.startswith(prefix) for a in item["aliases"]):
                    results.append({
                        "id": f"raycast:web:help:{bang_id}",
                        "text": f"Búsqueda con {bang_id} ({item['name']})",
                        "icon": item["icon"],
                        "subtext": f"Ejemplo: {bang_id} linux kernel",
                        "category": "Raycast: Búsqueda Web",
                        "relevance": 0.85,
                    })

        return results

    def run(self, action_id: str) -> bool:
        if not action_id.startswith("raycast:web:"):
            return False

        url = action_id.replace("raycast:web:", "")
        if url.startswith("help:"):
            return False

        subprocess.Popen(["xdg-open", url], start_new_session=True)
        return True

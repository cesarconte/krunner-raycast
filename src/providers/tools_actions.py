# SPDX-FileCopyrightText: 2026 Cesar <yugurta@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Proveedor de acciones para la suite de herramientas Golden Gate / Productividad.
"""

import subprocess
import shutil
import re
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

TRACKING_PARAMS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "gclid", "fbclid", "igshid", "mc_eid", "msclkid", "twclid", "yclid",
    "si", "feature", "ref", "ref_src", "source", "srsltid", "ved"
}


def clean_url_string(url: str) -> str:
    parsed = urlparse(url)
    if not parsed.netloc:
        return url
    query_params = parse_qs(parsed.query, keep_blank_values=False)
    cleaned_params = {k: v for k, v in query_params.items() if k.lower() not in TRACKING_PARAMS}
    new_query = urlencode(cleaned_params, doseq=True)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))


class ToolsActionsProvider:
    """Integra kocr, klivetext, kunpack, kduck, kautomator y utilidades."""

    def __init__(self):
        self.tools = {
            "kocr": {
                "keywords": ["ocr", "texto", "capturar texto", "kocr", "screen ocr", "reconocer texto"],
                "text": "Capturar Texto OCR de Pantalla (kocr)",
                "subtext": "Selecciona un área de la pantalla y copia el texto al portapapeles",
                "icon": "edit-find",
                "bin": "kocr",
                "cmd": ["kocr"],
            },
            "klivetext": {
                "keywords": ["live", "livetext", "klivetext", "detector", "iban", "extraer", "telefono"],
                "text": "KLiveText: Detector Interactivo de Pantalla",
                "subtext": "Extrae URLs, teléfonos, correos e IBAN de la pantalla con acciones rápidas",
                "icon": "system-search",
                "bin": "klivetext",
                "cmd": ["klivetext"],
            },
            "kduck_duck": {
                "keywords": ["duck", "atenuar", "kduck", "bajar volumen", "ducking"],
                "text": "KDuck: Atenuar Audio Multimedia (20%)",
                "subtext": "Atenúa suavemente el volumen de música para llamadas o concentración",
                "icon": "audio-volume-low",
                "bin": "kduck",
                "cmd": ["kduck", "duck", "20"],
            },
            "kduck_unduck": {
                "keywords": ["unduck", "restaurar audio", "subir volumen"],
                "text": "KDuck: Restaurar Volumen de Audio",
                "subtext": "Restaura el volumen previo al ducking progresivamente",
                "icon": "audio-volume-high",
                "bin": "kduck",
                "cmd": ["kduck", "unduck"],
            },
            "kduck_status": {
                "keywords": ["duck status", "estado audio", "estado kduck"],
                "text": "KDuck: Ver Estado del Servicio",
                "subtext": "Muestra información de volumen, rampas y servicio de ducking",
                "icon": "audio-speakers",
                "bin": "kduck",
                "cmd": ["konsole", "-e", "kduck status; echo ''; read -p 'Pulsa enter para cerrar...'"],
            },
            "kautomator_run": {
                "keywords": ["automator", "hazel", "kautomator", "organizar", "carpetas", "reglas"],
                "text": "KAutomator: Organizar Carpetas Ahora",
                "subtext": "Ejecuta las reglas de organización sobre Descargas y Escritorio",
                "icon": "folder-sync",
                "bin": "kautomator",
                "cmd": ["kautomator", "run"],
            },
            "kautomator_edit": {
                "keywords": ["reglas", "editar reglas", "kautomator edit"],
                "text": "KAutomator: Editar Reglas de Carpetas",
                "subtext": "Abre el archivo ~/.config/kautomator/rules.toml en el editor",
                "icon": "document-edit",
                "bin": "kautomator",
                "cmd": ["kautomator", "edit"],
            },
            "clean_links": {
                "keywords": ["clean", "link", "enlace", "limpiar enlace", "clean link", "url"],
                "text": "Limpiar Enlace del Portapapeles (Clean Links)",
                "subtext": "Elimina parámetros de rastreo (utm, fbclid, gclid, etc.) del enlace copiado",
                "icon": "edit-clear",
                "bin": "wl-paste",
                "handler": self._action_clean_links,
            },
        }

    def match(self, query: str):
        q = query.strip().lower()
        if not q:
            return []

        results = []
        for key, item in self.tools.items():
            # Solo mostrar si el binario está instalado en PATH
            if "bin" in item and not shutil.which(item["bin"]):
                continue

            matched = False
            relevance = 0.0

            if any(q == kw for kw in item["keywords"]):
                matched = True
                relevance = 0.96
            elif any(kw.startswith(q) for kw in item["keywords"]):
                matched = True
                relevance = 0.88
            elif any(q in kw for kw in item["keywords"]) or q in item["text"].lower():
                matched = True
                relevance = 0.72

            if matched:
                results.append({
                    "id": f"raycast:tools:{key}",
                    "text": item["text"],
                    "icon": item["icon"],
                    "subtext": item["subtext"],
                    "category": "Raycast: Herramientas",
                    "relevance": relevance,
                })

        return results

    def run(self, action_id: str) -> bool:
        if not action_id.startswith("raycast:tools:"):
            return False
        key = action_id.replace("raycast:tools:", "")
        if key not in self.tools:
            return False

        item = self.tools[key]
        if "handler" in item:
            item["handler"]()
        elif "cmd" in item:
            subprocess.Popen(item["cmd"], start_new_session=True)
        return True

    def _action_clean_links(self):
        try:
            res = subprocess.run(["wl-paste", "--no-newline"], capture_output=True, text=True, check=False)
            clipboard_text = res.stdout.strip()
            if not clipboard_text or not (clipboard_text.startswith("http://") or clipboard_text.startswith("https://")):
                subprocess.run(["notify-send", "-a", "Raycast", "-i", "dialog-warning", "Clean Links", "El portapapeles no contiene una URL válida."])
                return

            cleaned = clean_url_string(clipboard_text)
            subprocess.run(["wl-copy"], input=cleaned, text=True, check=False)
            subprocess.run([
                "notify-send", "-a", "Raycast", "-i", "edit-clear",
                "Enlace Limpiado", f"Copiado al portapapeles:\n{cleaned}"
            ])
        except Exception as e:
            subprocess.run(["notify-send", "-a", "Raycast", "-i", "dialog-error", "Clean Links", f"Error: {e}"])

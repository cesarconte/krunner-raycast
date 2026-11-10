# SPDX-FileCopyrightText: 2026 Cesar <yugurta@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Proveedor de acciones rápidas del sistema estilo Raycast para KDE Plasma 6.
"""

import subprocess
import shutil


class SystemActionsProvider:
    """Gestiona acciones de sesión, energía, audio y entorno de escritorio."""

    def __init__(self):
        self.actions = {
            "lock": {
                "keywords": ["lock", "bloquear", "bloqueo", "candado", "session"],
                "text": "Bloquear Pantalla",
                "subtext": "Bloquea inmediatamente la sesión activa en Wayland",
                "icon": "system-lock-screen",
                "handler": self._action_lock,
            },
            "suspend": {
                "keywords": ["suspend", "suspender", "dormir", "sleep"],
                "text": "Suspender el Sistema",
                "subtext": "Pone el equipo en estado de suspensión (RAM)",
                "icon": "system-suspend",
                "handler": self._action_suspend,
            },
            "reboot": {
                "keywords": ["reboot", "reiniciar", "restart"],
                "text": "Reiniciar el Sistema",
                "subtext": "Reinicia el equipo de forma segura",
                "icon": "system-reboot",
                "handler": self._action_reboot,
            },
            "poweroff": {
                "keywords": ["poweroff", "shutdown", "apagar", "apaga"],
                "text": "Apagar el Sistema",
                "subtext": "Cierra las aplicaciones y apaga el equipo",
                "icon": "system-shutdown",
                "handler": self._action_poweroff,
            },
            "trash_empty": {
                "keywords": ["trash", "papelera", "vaciar papelera", "empty trash"],
                "text": "Vaciar Papelera de Reciclaje",
                "subtext": "Elimina permanentemente los elementos de la papelera",
                "icon": "user-trash-full",
                "handler": self._action_empty_trash,
            },
            "restart_plasmashell": {
                "keywords": ["plasma", "plasmashell", "reiniciar plasma", "shell", "reload plasma"],
                "text": "Reiniciar KDE Plasma Shell",
                "subtext": "Reinicia los paneles y el escritorio de Plasma sin cerrar sesión",
                "icon": "plasma",
                "handler": self._action_restart_plasmashell,
            },
            "mute_mic": {
                "keywords": ["mic", "micro", "microfono", "mute mic", "silenciar microfono"],
                "text": "Alternar Silencio de Micrófono",
                "subtext": "Activa o silencia la captura de audio predeterminada (PipeWire)",
                "icon": "audio-input-microphone",
                "handler": self._action_toggle_mic,
            },
            "mute_audio": {
                "keywords": ["mute", "silencio", "mutear", "silenciar audio", "volumen"],
                "text": "Alternar Silencio de Salida de Audio",
                "subtext": "Activa o silencia los altavoces / auriculares (PipeWire)",
                "icon": "audio-volume-muted",
                "handler": self._action_toggle_audio,
            },
            "toggle_dnd": {
                "keywords": ["dnd", "no molestar", "silencio notificaciones", "do not disturb"],
                "text": "Alternar Modo No Molestar (DND)",
                "subtext": "Silencia las notificaciones emergentes de KDE Plasma",
                "icon": "notifications-disabled",
                "handler": self._action_toggle_dnd,
            },
            "toggle_theme": {
                "keywords": ["tema", "oscuro", "claro", "dark", "light", "color", "dark mode"],
                "text": "Alternar Modo Oscuro / Claro",
                "subtext": "Alterna entre los esquemas de color BreezeDark y BreezeLight",
                "icon": "preferences-desktop-theme",
                "handler": self._action_toggle_theme,
            },
        }

    def match(self, query: str):
        q = query.strip().lower()
        if not q:
            return []

        results = []
        for key, item in self.actions.items():
            matched = False
            relevance = 0.0

            # Coincidencia exacta con alguna palabra clave
            if any(q == kw for kw in item["keywords"]):
                matched = True
                relevance = 0.98
            # Prefijo o inicio de palabra
            elif any(kw.startswith(q) for kw in item["keywords"]):
                matched = True
                relevance = 0.90
            # Subcadena contenida
            elif any(q in kw for kw in item["keywords"]) or q in item["text"].lower():
                matched = True
                relevance = 0.75

            if matched:
                results.append({
                    "id": f"raycast:system:{key}",
                    "text": item["text"],
                    "icon": item["icon"],
                    "subtext": item["subtext"],
                    "category": "Raycast: Sistema",
                    "relevance": relevance,
                })

        return results

    def run(self, action_id: str) -> bool:
        if not action_id.startswith("raycast:system:"):
            return False
        key = action_id.replace("raycast:system:", "")
        if key in self.actions:
            self.actions[key]["handler"]()
            return True
        return False

    def _notify(self, title: str, message: str, icon: str = "dialog-information"):
        subprocess.run(["notify-send", "-a", "Raycast", "-i", icon, title, message], check=False)

    def _action_lock(self):
        subprocess.run(["loginctl", "lock-session"], check=False)

    def _action_suspend(self):
        subprocess.run(["systemctl", "suspend"], check=False)

    def _action_reboot(self):
        subprocess.run(["systemctl", "reboot"], check=False)

    def _action_poweroff(self):
        subprocess.run(["systemctl", "poweroff"], check=False)

    def _action_empty_trash(self):
        res = subprocess.run(["gio", "trash", "--empty"], capture_output=True, text=True)
        if res.returncode == 0:
            self._notify("Papelera de Reciclaje", "La papelera ha sido vaciada.", "user-trash")
        else:
            self._notify("Papelera de Reciclaje", "No se pudo vaciar la papelera o ya estaba vacía.", "dialog-warning")

    def _action_restart_plasmashell(self):
        subprocess.Popen(
            ["sh", "-c", "kquitapp6 plasmashell || killall plasmashell; sleep 0.5; kstart plasmashell"],
            start_new_session=True
        )
        self._notify("Plasma Shell", "Reiniciando el entorno de escritorio...", "plasma")

    def _action_toggle_mic(self):
        subprocess.run(["wpctl", "set-mute", "@DEFAULT_AUDIO_SOURCE@", "toggle"], check=False)
        self._notify("Micrófono", "Estado de silencio alternado", "audio-input-microphone")

    def _action_toggle_audio(self):
        subprocess.run(["wpctl", "set-mute", "@DEFAULT_AUDIO_SINK@", "toggle"], check=False)
        self._notify("Audio", "Estado de silencio alternado", "audio-volume-high")

    def _action_toggle_dnd(self):
        # Comprobar estado actual de inhibición vía DBus
        try:
            res = subprocess.run(
                ["qdbus6", "org.freedesktop.Notifications", "/org/freedesktop/Notifications", "org.freedesktop.Notifications.Inhibited"],
                capture_output=True, text=True, check=False
            )
            is_inhibited = "true" in res.stdout.strip().lower()
            if is_inhibited:
                # Desinhibir
                subprocess.run(
                    ["qdbus6", "org.freedesktop.Notifications", "/org/freedesktop/Notifications", "org.freedesktop.Notifications.UnInhibit", "1"],
                    check=False
                )
                self._notify("Modo No Molestar", "Notificaciones activadas (DND Desactivado)", "notifications")
            else:
                subprocess.run(
                    ["qdbus6", "org.freedesktop.Notifications", "/org/freedesktop/Notifications", "org.freedesktop.Notifications.Inhibit", "Raycast", "DND manual", "{}"],
                    check=False
                )
                self._notify("Modo No Molestar", "Modo No Molestar activado", "notifications-disabled")
        except Exception:
            self._notify("Modo No Molestar", "No se pudo cambiar el estado de DND", "dialog-warning")

    def _action_toggle_theme(self):
        try:
            res = subprocess.run(["plasma-apply-colorscheme", "-l"], capture_output=True, text=True)
            current_is_dark = "BreezeDark (esquema de color actual)" in res.stdout
            new_theme = "BreezeLight" if current_is_dark else "BreezeDark"
            subprocess.run(["plasma-apply-colorscheme", new_theme], check=False)
            self._notify("Tema de Plasma", f"Cambiado a {new_theme}", "preferences-desktop-theme")
        except Exception as e:
            self._notify("Tema de Plasma", f"Error al cambiar tema: {e}", "dialog-error")

# SPDX-FileCopyrightText: 2026 Cesar <yugurta@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Servicio D-Bus org.kde.krunner1 para KRaycast Runner.
"""

import sys
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

from providers.system_actions import SystemActionsProvider
from providers.tools_actions import ToolsActionsProvider
from providers.web_bangs import WebBangsProvider
from providers.dev_utils import DevUtilsProvider
from providers.process_killer import ProcessKillerProvider


DBUS_SERVICE_NAME = "org.cesar.KRunnerRaycast"
DBUS_OBJECT_PATH = "/KRunnerRaycast"
DBUS_INTERFACE = "org.kde.krunner1"


class KRunnerRaycastService(dbus.service.Object):
    """Implementa la interfaz org.kde.krunner1 para KDE Plasma 6."""

    def __init__(self, bus, object_path=DBUS_OBJECT_PATH):
        super().__init__(bus, object_path)
        self.providers = [
            WebBangsProvider(),
            DevUtilsProvider(),
            SystemActionsProvider(),
            ToolsActionsProvider(),
            ProcessKillerProvider(),
        ]
        self.activation_token = ""

    @dbus.service.method(DBUS_INTERFACE, in_signature="s", out_signature="a(sssida{sv})")
    def Match(self, query: str):
        raw_query = str(query)
        matches = []

        for provider in self.providers:
            try:
                results = provider.match(raw_query)
                for item in results:
                    props = {
                        "subtext": dbus.String(item.get("subtext", ""), variant_level=1),
                        "category": dbus.String(item.get("category", "Raycast"), variant_level=1),
                        "actions": dbus.Array([], signature="s", variant_level=1),
                    }
                    match_type = dbus.Int32(item.get("type", 30))
                    relevance = dbus.Double(item.get("relevance", 0.8))

                    matches.append((
                        dbus.String(item["id"]),
                        dbus.String(item["text"]),
                        dbus.String(item.get("icon", "system-run")),
                        match_type,
                        relevance,
                        props
                    ))
            except Exception as e:
                print(f"[KRaycast Error in {provider.__class__.__name__}]: {e}", file=sys.stderr)

        return matches

    @dbus.service.method(DBUS_INTERFACE, in_signature="ss", out_signature="")
    def Run(self, match_id: str, action_id: str):
        mid = str(match_id)
        for provider in self.providers:
            try:
                if provider.run(mid):
                    return
            except Exception as e:
                print(f"[KRaycast Run Error in {provider.__class__.__name__}]: {e}", file=sys.stderr)

    @dbus.service.method(DBUS_INTERFACE, in_signature="", out_signature="a(sss)")
    def Actions(self):
        return []

    @dbus.service.method(DBUS_INTERFACE, in_signature="s", out_signature="")
    def SetActivationToken(self, token: str):
        self.activation_token = str(token)

    @dbus.service.method(DBUS_INTERFACE, in_signature="", out_signature="")
    def Teardown(self):
        pass

    @dbus.service.method(DBUS_INTERFACE, in_signature="", out_signature="a{sv}")
    def Config(self):
        return {}


def run_daemon():
    """Inicia el bucle de eventos GLib y registra el servicio D-Bus."""
    DBusGMainLoop(set_as_default=True)
    session_bus = dbus.SessionBus()
    bus_name = dbus.service.BusName(DBUS_SERVICE_NAME, session_bus)
    service = KRunnerRaycastService(session_bus)

    print(f"🚀 KRaycast Runner activo en D-Bus ({DBUS_SERVICE_NAME})")
    loop = GLib.MainLoop()
    try:
        loop.run()
    except (KeyboardInterrupt, SystemExit):
        loop.quit()

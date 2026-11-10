#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Cesar <yugurta@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later
# uninstall.sh: Desinstalador autónomo de KRaycast Runner

set -eo pipefail

BIN_DIR="${HOME}/.local/bin"
SHARE_DIR="${HOME}/.local/share/krunner-raycast"
KRUNNER_PLUGINS_DIR="${HOME}/.local/share/krunner/dbusplugins"
DBUS_SERVICES_DIR="${HOME}/.local/share/dbus-1/services"
APPS_DIR="${HOME}/.local/share/applications"
SYSTEMD_DIR="${HOME}/.config/systemd/user"

echo "==> Desinstalando KRaycast Runner..."

# Detener y deshabilitar servicio systemd
if command -v systemctl >/dev/null 2>&1; then
    systemctl --user stop krunner-raycast.service 2>/dev/null || true
    systemctl --user disable krunner-raycast.service 2>/dev/null || true
fi
rm -f "${SYSTEMD_DIR}/krunner-raycast.service"
systemctl --user daemon-reload 2>/dev/null || true
echo "  ✓ Servicio systemd detenido y eliminado"

# Eliminar binario y módulos
rm -f "${BIN_DIR}/krunner-raycast"
rm -rf "$SHARE_DIR"
echo "  ✓ Binario y módulos eliminados"

# Eliminar plugins y servicios D-Bus
rm -f "${KRUNNER_PLUGINS_DIR}/org.cesar.krunner_raycast.desktop"
rm -f "${DBUS_SERVICES_DIR}/org.cesar.KRunnerRaycast.service"
rm -f "${APPS_DIR}/org.cesar.krunner_raycast.desktop"
echo "  ✓ Plugin de KRunner y registro D-Bus eliminados"

if command -v kbuildsycoca6 >/dev/null 2>&1; then
    kbuildsycoca6 --noincremental >/dev/null 2>&1 || true
fi

if command -v kquitapp6 >/dev/null 2>&1; then
    kquitapp6 krunner 2>/dev/null || true
    krunner --daemon >/dev/null 2>&1 &
fi

echo "🎉 ¡KRaycast Runner ha sido desinstalado correctamente!"

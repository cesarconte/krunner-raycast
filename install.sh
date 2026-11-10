#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Cesar <yugurta@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later
# install.sh: Instalador autónomo de KRaycast Runner para KDE Plasma 6 sobre Wayland

set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="${HOME}/.local/bin"
SHARE_DIR="${HOME}/.local/share/krunner-raycast"
KRUNNER_PLUGINS_DIR="${HOME}/.local/share/krunner/dbusplugins"
DBUS_SERVICES_DIR="${HOME}/.local/share/dbus-1/services"
APPS_DIR="${HOME}/.local/share/applications"
SYSTEMD_DIR="${HOME}/.config/systemd/user"

echo "==> Instalando KRaycast Runner (Acciones Rápidas para KRunner en KDE Plasma 6)..."

# 1. Comprobar dependencias
MISSING_DEPS=()
for dep in python3 wl-copy notify-send wpctl; do
    if ! command -v "$dep" >/dev/null 2>&1; then
        MISSING_DEPS+=("$dep")
    fi
done

if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    echo "⚠️  Faltan dependencias: ${MISSING_DEPS[*]}"
    if command -v pacman >/dev/null 2>&1; then
        echo "--> Instálalas con: sudo pacman -S --needed python wl-clipboard libnotify wireplumber"
    fi
fi

# 2. Instalar módulos del motor
mkdir -p "${SHARE_DIR}/src"
cp -r "${SCRIPT_DIR}/src/"* "${SHARE_DIR}/src/"
echo "  ✓ Módulos y proveedores instalados en ${SHARE_DIR}"

# 3. Instalar ejecutable CLI
mkdir -p "$BIN_DIR"
install -m 755 "${SCRIPT_DIR}/bin/krunner-raycast" "${BIN_DIR}/krunner-raycast"
echo "  ✓ Binario instalado en ${BIN_DIR}/krunner-raycast"

# 4. Instalar descriptor de plugin para KRunner
mkdir -p "$KRUNNER_PLUGINS_DIR"
install -m 644 "${SCRIPT_DIR}/data/org.cesar.krunner_raycast.desktop" "${KRUNNER_PLUGINS_DIR}/org.cesar.krunner_raycast.desktop"
echo "  ✓ Plugin registrado en ${KRUNNER_PLUGINS_DIR}/org.cesar.krunner_raycast.desktop"

# 5. Instalar activación D-Bus
mkdir -p "$DBUS_SERVICES_DIR"
install -m 644 "${SCRIPT_DIR}/data/org.cesar.KRunnerRaycast.service" "${DBUS_SERVICES_DIR}/org.cesar.KRunnerRaycast.service"
echo "  ✓ Servicio D-Bus registrado en ${DBUS_SERVICES_DIR}/org.cesar.KRunnerRaycast.service"

# 6. Instalar lanzador de escritorio
mkdir -p "$APPS_DIR"
install -m 644 "${SCRIPT_DIR}/data/org.cesar.krunner_raycast.app.desktop" "${APPS_DIR}/org.cesar.krunner_raycast.desktop"
echo "  ✓ Lanzador registrado en ${APPS_DIR}/org.cesar.krunner_raycast.desktop"

# 7. Instalar y habilitar servicio systemd de usuario
mkdir -p "$SYSTEMD_DIR"
install -m 644 "${SCRIPT_DIR}/data/krunner-raycast.service" "${SYSTEMD_DIR}/krunner-raycast.service"
if command -v systemctl >/dev/null 2>&1; then
    systemctl --user daemon-reload
    systemctl --user enable --now krunner-raycast.service 2>/dev/null || true
    echo "  ✓ Servicio systemd de usuario 'krunner-raycast.service' habilitado y activo"
fi

# 8. Actualizar base de datos de aplicaciones y recargar KRunner
if command -v kbuildsycoca6 >/dev/null 2>&1; then
    kbuildsycoca6 --noincremental >/dev/null 2>&1 || true
    echo "  ✓ Base de datos Sycoca de KDE actualizada"
fi

if command -v kquitapp6 >/dev/null 2>&1; then
    kquitapp6 krunner 2>/dev/null || true
    krunner --daemon >/dev/null 2>&1 &
    echo "  ✓ Demonio KRunner reiniciado para cargar el nuevo plugin"
fi

echo ""
echo "🎉 ¡Instalación de KRaycast Runner completada con éxito!"
echo "   - Abre KRunner (Alt+Espacio o Meta) y prueba a escribir:"
echo "       • Acciones del sistema:  'bloquear', 'suspender', 'papelera', 'tema', 'dnd'"
echo "       • Suite de herramientas: 'ocr', 'live', 'duck', 'automator', 'clean'"
echo "       • Búsquedas rápidas:     '!gh cachyos', '!yt music', '!g linux', '!maps madrid'"
echo "       • Utilidades Dev:        'uuid', 'b64 hola', '0xff', 'timestamp', 'kill <app>'"
echo "   - Para consultar el estado:  krunner-raycast status"

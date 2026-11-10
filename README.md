# KRaycast Runner ⚡

**Raycast-like Quick Actions, Dev Utilities, Web Bangs, and Tool Suites for KRunner on KDE Plasma 6 / Wayland.**

KRaycast Runner es un plugin D-Bus nativo (`org.kde.krunner1`) para **KRunner** en KDE Plasma 6 que transforma el buscador predeterminado en un centro de productividad ultrarrápido al estilo de **Raycast** (macOS).

---

## ✨ Características

### 🚀 Acciones Rápidas del Sistema
- `bloquear` / `lock`: Bloquea la sesión activa en Wayland al instante.
- `suspender` / `sleep`: Suspende el equipo a RAM.
- `papelera`: Vacía la papelera de reciclaje de forma segura.
- `tema` / `dark mode`: Alterna entre el tema oscuro y claro (BreezeDark / BreezeLight).
- `dnd` / `no molestar`: Silencia o reactiva las notificaciones del escritorio.
- `mic`: Alterna el silencio del micrófono.
- `mute`: Alterna el silencio de la salida de audio.
- `plasma`: Reinicia KDE Plasma Shell sin cerrar sesión.

### 🧰 Suite Golden Gate Integrada
- `ocr`: Inicia el OCR instantáneo de pantalla ([kocr](https://github.com/cesarconte/kocr)).
- `live`: Abre el detector de datos interactivo ([klivetext](https://github.com/cesarconte/klivetext)).
- `duck`: Atenúa el audio multimedia ([kduck](https://github.com/cesarconte/kduck)).
- `automator`: Organiza carpetas y descargas automáticamente ([kautomator](https://github.com/cesarconte/kautomator)).
- `clean`: Limpia enlaces del portapapeles eliminando parámetros de seguimiento (`utm_`, `si`, `fbclid`).

### 🌐 Búsquedas Web con Bangs / Prefijos
- `!gh <consulta>`: Busca directamente en GitHub.
- `!yt <consulta>`: Busca directamente en YouTube.
- `!g <consulta>`: Busca directamente en Google.
- `!w <consulta>`: Busca directamente en Wikipedia en español.
- `!maps <consulta>`: Busca ubicaciones en Google Maps.
- `!aur <consulta>`: Busca paquetes en Arch User Repository (AUR).
- `!arch <consulta>`: Busca guías en ArchWiki.
- `!cachy <consulta>`: Busca información en CachyOS Wiki.

### 🧮 Utilidades para Desarrolladores
- `uuid`: Genera un nuevo UUID v4 y lo copia al portapapeles con Enter.
- `b64 <texto>`: Codifica a Base64.
- `b64d <texto>`: Decodifica de Base64.
- `sha256 <texto>`: Calcula el hash criptográfico SHA-256.
- `timestamp`: Muestra el timestamp UNIX actual en segundos y milisegundos.
- `timestamp <número>`: Convierte una marca de tiempo UNIX a fecha y hora local legible.
- `0xff` o `hex <número>`: Convierte entre Hexadecimal, Decimal y Binario.
- `ip`: Muestra la dirección IP local de la interfaz de red activa.

### 🧹 Gestor de Procesos Rápido
- `kill <nombre>` o `matar <nombre>`: Lista procesos activos que coincidan y permite terminarlos limpiamente con una pulsación de tecla.

---

## 🚀 Instalación

### Método 1: Instalador autónomo
```bash
git clone https://github.com/cesarconte/krunner-raycast.git
cd krunner-raycast
chmod +x install.sh
./install.sh
```

### Método 2: En Arch Linux / CachyOS (vía PKGBUILD)
```bash
makepkg -si
```

---

## 🛠️ Comandos CLI

```bash
# Probar una consulta directamente desde el terminal:
krunner-raycast query "!gh linux"
krunner-raycast query uuid
krunner-raycast query 0xff

# Comprobar estado del servicio:
krunner-raycast status
```

---

## 📄 Licencia

GPL-3.0-or-later © 2026 Cesar <yugurta@gmail.com>

# SPDX-FileCopyrightText: 2026 Cesar <yugurta@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Proveedor de herramientas para desarrolladores estilo Raycast (UUID, Base64, Hashing, Timestamps, Conversión).
"""

import uuid
import base64
import hashlib
import time
import datetime
import subprocess
import socket


class DevUtilsProvider:
    """Proporciona utilidades instantáneas para desarrolladores y administradores de sistemas."""

    def match(self, query: str):
        q = query.strip()
        if not q:
            return []

        lower_q = q.lower()
        results = []

        # 1. UUID v4
        if lower_q in ["uuid", "guid", "uuid4"]:
            new_uuid = str(uuid.uuid4())
            results.append({
                "id": f"raycast:dev:copy:{new_uuid}",
                "text": f"UUID v4: {new_uuid}",
                "icon": "edit-copy",
                "subtext": "Pulsa Enter para copiar el UUID v4 al portapapeles",
                "category": "Raycast: Utilidades Dev",
                "relevance": 0.99,
            })

        # 2. Base64 Encode
        if lower_q.startswith("b64 ") or lower_q.startswith("base64 "):
            raw_text = q.split(maxsplit=1)[1]
            try:
                encoded = base64.b64encode(raw_text.encode("utf-8")).decode("utf-8")
                results.append({
                    "id": f"raycast:dev:copy:{encoded}",
                    "text": f"Base64: {encoded}",
                    "icon": "edit-copy",
                    "subtext": f"Codificado desde '{raw_text}'. Pulsa Enter para copiar.",
                    "category": "Raycast: Utilidades Dev",
                    "relevance": 0.98,
                })
            except Exception:
                pass

        # 3. Base64 Decode
        if lower_q.startswith("b64d ") or lower_q.startswith("unbase64 "):
            raw_text = q.split(maxsplit=1)[1]
            try:
                decoded = base64.b64decode(raw_text.encode("utf-8")).decode("utf-8", errors="replace")
                results.append({
                    "id": f"raycast:dev:copy:{decoded}",
                    "text": f"Decodificado: {decoded}",
                    "icon": "edit-copy",
                    "subtext": "Pulsa Enter para copiar el texto decodificado",
                    "category": "Raycast: Utilidades Dev",
                    "relevance": 0.98,
                })
            except Exception:
                pass

        # 4. SHA-256
        if lower_q.startswith("sha256 ") or lower_q.startswith("hash "):
            raw_text = q.split(maxsplit=1)[1]
            digest = hashlib.sha256(raw_text.encode("utf-8")).hexdigest()
            results.append({
                "id": f"raycast:dev:copy:{digest}",
                "text": f"SHA-256: {digest[:24]}...{digest[-8:]}",
                "icon": "security-high",
                "subtext": f"Hash completo ({len(digest)} caracteres). Pulsa Enter para copiar.",
                "category": "Raycast: Utilidades Dev",
                "relevance": 0.98,
            })

        # 5. MD5
        if lower_q.startswith("md5 "):
            raw_text = q.split(maxsplit=1)[1]
            digest = hashlib.md5(raw_text.encode("utf-8")).hexdigest()
            results.append({
                "id": f"raycast:dev:copy:{digest}",
                "text": f"MD5: {digest}",
                "icon": "security-low",
                "subtext": f"Hash MD5 de '{raw_text}'. Pulsa Enter para copiar.",
                "category": "Raycast: Utilidades Dev",
                "relevance": 0.98,
            })

        # 6. Timestamps UNIX
        if lower_q in ["timestamp", "unix", "epoch", "time"]:
            now_sec = int(time.time())
            now_ms = int(time.time() * 1000)
            now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            results.append({
                "id": f"raycast:dev:copy:{now_sec}",
                "text": f"Timestamp UNIX: {now_sec} ({now_str})",
                "icon": "clock",
                "subtext": f"Milisegundos: {now_ms}. Pulsa Enter para copiar los segundos.",
                "category": "Raycast: Utilidades Dev",
                "relevance": 0.98,
            })
        elif lower_q.startswith("timestamp ") or lower_q.startswith("epoch ") or lower_q.startswith("unix "):
            val_str = q.split(maxsplit=1)[1]
            try:
                val = int(val_str)
                # Si es en milisegundos (> 10000000000)
                if val > 10000000000:
                    val = val / 1000.0
                dt = datetime.datetime.fromtimestamp(val)
                dt_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                results.append({
                    "id": f"raycast:dev:copy:{dt_str}",
                    "text": f"Fecha Local: {dt_str}",
                    "icon": "clock",
                    "subtext": f"Convertido desde {val_str}. Pulsa Enter para copiar la fecha.",
                    "category": "Raycast: Utilidades Dev",
                    "relevance": 0.98,
                })
            except Exception:
                pass

        # 7. Conversor de Bases Numéricas (Hex, Bin, Dec)
        # Prefijo 0x
        if lower_q.startswith("0x"):
            try:
                dec = int(lower_q, 16)
                binary = bin(dec)
                results.append({
                    "id": f"raycast:dev:copy:{dec}",
                    "text": f"Decimal: {dec} | Binario: {binary}",
                    "icon": "accessories-calculator",
                    "subtext": f"Convertido desde {lower_q}. Pulsa Enter para copiar decimal.",
                    "category": "Raycast: Conversor de Bases",
                    "relevance": 0.97,
                })
            except ValueError:
                pass
        # Prefijo 0b
        elif lower_q.startswith("0b"):
            try:
                dec = int(lower_q, 2)
                hexd = hex(dec).upper().replace("0X", "0x")
                results.append({
                    "id": f"raycast:dev:copy:{dec}",
                    "text": f"Decimal: {dec} | Hexadecimal: {hexd}",
                    "icon": "accessories-calculator",
                    "subtext": f"Convertido desde {lower_q}. Pulsa Enter para copiar decimal.",
                    "category": "Raycast: Conversor de Bases",
                    "relevance": 0.97,
                })
            except ValueError:
                pass
        # Comandos explícitos: 'hex 255' o 'bin 255'
        elif lower_q.startswith("hex ") or lower_q.startswith("tohex "):
            num_str = q.split(maxsplit=1)[1]
            try:
                num = int(num_str)
                hexd = hex(num).upper().replace("0X", "0x")
                results.append({
                    "id": f"raycast:dev:copy:{hexd}",
                    "text": f"Hexadecimal: {hexd}",
                    "icon": "accessories-calculator",
                    "subtext": f"Decimal: {num}. Pulsa Enter para copiar {hexd}.",
                    "category": "Raycast: Conversor de Bases",
                    "relevance": 0.98,
                })
            except ValueError:
                pass
        elif lower_q.startswith("bin ") or lower_q.startswith("tobin "):
            num_str = q.split(maxsplit=1)[1]
            try:
                num = int(num_str)
                binary = bin(num)
                results.append({
                    "id": f"raycast:dev:copy:{binary}",
                    "text": f"Binario: {binary}",
                    "icon": "accessories-calculator",
                    "subtext": f"Decimal: {num}. Pulsa Enter para copiar {binary}.",
                    "category": "Raycast: Conversor de Bases",
                    "relevance": 0.98,
                })
            except ValueError:
                pass

        # 8. IP Local
        if lower_q in ["ip", "myip", "localip"]:
            try:
                # Obtener dirección IP de interfaz principal sin resolución externa
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("1.1.1.1", 80))
                local_ip = s.getsockname()[0]
                s.close()
                results.append({
                    "id": f"raycast:dev:copy:{local_ip}",
                    "text": f"IP Local: {local_ip}",
                    "icon": "network-wired",
                    "subtext": "Dirección IPv4 en la red local. Pulsa Enter para copiar.",
                    "category": "Raycast: Red",
                    "relevance": 0.99,
                })
            except Exception:
                pass

        return results

    def run(self, action_id: str) -> bool:
        if not action_id.startswith("raycast:dev:copy:"):
            return False

        content = action_id.replace("raycast:dev:copy:", "")
        try:
            subprocess.run(["wl-copy"], input=content, text=True, check=False)
            subprocess.run([
                "notify-send", "-a", "Raycast", "-i", "edit-copy",
                "Copiado al Portapapeles", f"Contenido:\n{content}"
            ], check=False)
            return True
        except Exception:
            return False

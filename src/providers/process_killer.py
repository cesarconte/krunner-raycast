# SPDX-FileCopyrightText: 2026 Cesar <yugurta@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Proveedor para buscar y finalizar procesos de forma rápida desde KRunner (kill / matar).
"""

import os
import signal
import subprocess


class ProcessKillerProvider:
    """Permite buscar procesos activos y finalizarlos de forma segura."""

    def match(self, query: str):
        q = query.strip()
        lower_q = q.lower()

        if lower_q in ["kill", "matar"]:
            return [{
                "id": "raycast:process:help",
                "text": "Finalizar proceso (kill <nombre>)",
                "icon": "process-stop",
                "subtext": "Escribe el nombre de la aplicación para terminarla (ej. kill firefox)",
                "category": "Raycast: Procesos",
                "relevance": 0.85,
            }]

        if not (lower_q.startswith("kill ") or lower_q.startswith("matar ")):
            return []

        target = lower_q.split(maxsplit=1)[1].strip()
        if not target:
            return [{
                "id": "raycast:process:help",
                "text": "Finalizar proceso (kill <nombre>)",
                "icon": "process-stop",
                "subtext": "Escribe el nombre de la aplicación para terminarla (ej. kill firefox)",
                "category": "Raycast: Procesos",
                "relevance": 0.85,
            }]

        results = []
        try:
            # Obtener lista de procesos con ps
            output = subprocess.check_output(
                ["ps", "-eo", "pid,comm,pmem,args", "--no-headers"],
                text=True, errors="replace"
            )
            my_pid = os.getpid()

            for line in output.strip().splitlines():
                parts = line.strip().split(maxsplit=3)
                if len(parts) < 4:
                    continue
                pid_str, comm, pmem, args = parts[0], parts[1], parts[2], parts[3]
                try:
                    pid = int(pid_str)
                except ValueError:
                    continue

                if pid == my_pid:
                    continue

                # Coincidencia por comando o argumentos
                if target in comm.lower() or target in args.lower():
                    results.append({
                        "id": f"raycast:process:kill:{pid}:{comm}",
                        "text": f"Terminar: {comm} (PID {pid})",
                        "icon": "process-stop",
                        "subtext": f"Memoria: {pmem}% | Comando: {args[:50]}...",
                        "category": "Raycast: Procesos",
                        "relevance": 0.95,
                    })

                if len(results) >= 8:
                    break
        except Exception:
            pass

        return results

    def run(self, action_id: str) -> bool:
        if not action_id.startswith("raycast:process:kill:"):
            return False

        parts = action_id.split(":")
        if len(parts) < 5:
            return False

        try:
            pid = int(parts[3])
            comm = parts[4]
            # Enviar SIGTERM
            os.kill(pid, signal.SIGTERM)
            subprocess.run([
                "notify-send", "-a", "Raycast", "-i", "process-stop",
                "Proceso Finalizado", f"Se envió señal de terminación a {comm} (PID {pid})"
            ], check=False)
            return True
        except ProcessLookupError:
            subprocess.run([
                "notify-send", "-a", "Raycast", "-i", "dialog-warning",
                "Proceso Inexistente", "El proceso ya no se encuentra en ejecución."
            ], check=False)
            return False
        except PermissionError:
            subprocess.run([
                "notify-send", "-a", "Raycast", "-i", "dialog-error",
                "Permiso Denegado", "No se tienen permisos suficientes para terminar este proceso."
            ], check=False)
            return False
        except Exception as e:
            subprocess.run([
                "notify-send", "-a", "Raycast", "-i", "dialog-error",
                "Error al Finalizar", f"{e}"
            ], check=False)
            return False

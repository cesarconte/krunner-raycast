#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Cesar <yugurta@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Pruebas unitarias para KRunner Raycast.
"""

import unittest
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR / "src"))

from providers.system_actions import SystemActionsProvider
from providers.tools_actions import ToolsActionsProvider, clean_url_string
from providers.web_bangs import WebBangsProvider
from providers.dev_utils import DevUtilsProvider
from providers.process_killer import ProcessKillerProvider


class TestKRunnerRaycast(unittest.TestCase):

    def test_system_actions(self):
        p = SystemActionsProvider()
        res_lock = p.match("bloquear")
        self.assertTrue(any(r["id"] == "raycast:system:lock" for r in res_lock))

        res_suspend = p.match("suspend")
        self.assertTrue(any(r["id"] == "raycast:system:suspend" for r in res_suspend))

        res_trash = p.match("papelera")
        self.assertTrue(any(r["id"] == "raycast:system:trash_empty" for r in res_trash))

    def test_clean_url(self):
        dirty = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&si=12345&utm_source=twitter"
        clean = clean_url_string(dirty)
        self.assertNotIn("si=", clean)
        self.assertNotIn("utm_source=", clean)
        self.assertIn("v=dQw4w9WgXcQ", clean)

    def test_web_bangs(self):
        p = WebBangsProvider()
        res = p.match("!gh plasma-runner")
        self.assertEqual(len(res), 1)
        self.assertIn("https://github.com/search?q=plasma-runner", res[0]["id"])

        res_yt = p.match("!yt lo-fi hip hop")
        self.assertEqual(len(res_yt), 1)
        self.assertIn("youtube.com", res_yt[0]["id"])

        # Help suggestions when typing !
        res_help = p.match("!g")
        self.assertTrue(len(res_help) >= 1)

    def test_dev_utils(self):
        p = DevUtilsProvider()

        # UUID
        res_uuid = p.match("uuid")
        self.assertEqual(len(res_uuid), 1)
        uuid_str = res_uuid[0]["id"].replace("raycast:dev:copy:", "")
        self.assertEqual(len(uuid_str), 36)

        # Base64
        res_b64 = p.match("b64 hello")
        self.assertEqual(len(res_b64), 1)
        self.assertEqual(res_b64[0]["id"], "raycast:dev:copy:aGVsbG8=")

        # Base64 decode
        res_b64d = p.match("b64d aGVsbG8=")
        self.assertEqual(len(res_b64d), 1)
        self.assertEqual(res_b64d[0]["id"], "raycast:dev:copy:hello")

        # Hex conversion
        res_hex = p.match("0xff")
        self.assertEqual(len(res_hex), 1)
        self.assertEqual(res_hex[0]["id"], "raycast:dev:copy:255")

        # Timestamp conversion
        res_ts = p.match("timestamp 1700000000")
        self.assertEqual(len(res_ts), 1)
        self.assertIn("Fecha Local", res_ts[0]["text"])

    def test_process_killer_help(self):
        p = ProcessKillerProvider()
        res = p.match("kill ")
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["id"], "raycast:process:help")


if __name__ == "__main__":
    unittest.main()

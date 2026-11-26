import json
import re
import unittest
from pathlib import Path

CATALOG = Path(__file__).resolve().parents[1] / "catalog.json"

class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.entries = json.loads(CATALOG.read_text(encoding="utf-8"))

    def test_catalog_structure(self):
        self.assertIsInstance(self.entries, list)
        self.assertTrue(self.entries)
        for item in self.entries:
            for field in ("id", "name", "repo", "category", "description"):
                self.assertIsInstance(item[field], str)
                self.assertTrue(item[field])
            self.assertRegex(item["id"], r"^NS-\d{3}$")

    def test_unique_ids(self):
        ids = [item["id"] for item in self.entries]
        self.assertEqual(len(ids), len(set(ids)))

    def test_release_metadata(self):
        for item in self.entries:
            for key in ("release", "jar_release"):
                release = item.get(key)
                if release is None:
                    continue
                with self.subTest(project=item["id"], kind=key):
                    self.assertGreater(release["size"], 0)
                    self.assertRegex(release["digest"], r"^sha256:[0-9a-f]{64}$")
                    expected = f'https://github.com/NebulaStack-prog/{item["repo"]}/releases/download/{release["version"]}/{release["name"]}'
                    self.assertEqual(release["url"], expected)

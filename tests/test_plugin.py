"""Le plugin : manifeste, place de marché, serveur MCP, recettes.

    python -m unittest discover -s tests -v
    claude plugin validate . --strict      (le contrôle de Claude Code lui-même)
"""
import json
import re
import unittest
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent


def lire(*chemin):
    return json.loads(RACINE.joinpath(*chemin).read_text(encoding="utf-8"))


class Plugin(unittest.TestCase):
    def test_le_manifeste(self):
        manifeste = lire(".claude-plugin", "plugin.json")
        self.assertEqual(manifeste["name"], "subagent")
        self.assertRegex(manifeste["version"], r"^\d+\.\d+\.\d+$")
        for champ in ("description", "author", "license", "homepage", "repository"):
            self.assertTrue(manifeste.get(champ), champ)
        option = manifeste["userConfig"]["subagent_key"]
        self.assertTrue(option["sensitive"])  # la clé n'est pas écrite dans settings.json
        self.assertEqual(set(option) - {"type", "title", "description", "sensitive", "required"}, set())

    def test_la_place_de_marche_porte_le_plugin(self):
        place = lire(".claude-plugin", "marketplace.json")
        (entree,) = place["plugins"]
        self.assertEqual(entree["name"], lire(".claude-plugin", "plugin.json")["name"])
        self.assertEqual(entree["source"], "./")
        self.assertTrue(place["owner"]["name"])

    def test_le_serveur_mcp(self):
        (serveur,) = lire(".mcp.json")["mcpServers"].values()
        self.assertEqual(serveur["type"], "http")
        self.assertEqual(serveur["url"], "https://api.subagent.fr/mcp")
        self.assertEqual(serveur["headers"], {"Authorization": "Bearer ${user_config.subagent_key}"})

    def test_les_recettes(self):
        recettes = sorted(chemin.parent.name for chemin in RACINE.glob("skills/*/SKILL.md"))
        self.assertEqual(len(recettes), 7)
        for nom in recettes:
            with self.subTest(nom):
                texte = (RACINE / "skills" / nom / "SKILL.md").read_text(encoding="utf-8")
                m = re.match(r"^---\nname: ([^\n]+)\ndescription: (\"(?:[^\"\\]|\\.)*\")\n---\n", texte)
                self.assertIsNotNone(m)
                self.assertEqual(m.group(1), nom)
                self.assertLessEqual(len(json.loads(m.group(2))), 1024)
                self.assertNotRegex(texte, r"@@[a-z0-9_]+@@")

    def test_aucune_cle_n_est_ecrite_dans_le_depot(self):
        for chemin in RACINE.rglob("*"):
            if chemin.is_file() and ".git" not in chemin.parts and chemin.suffix in (".json", ".md"):
                texte = chemin.read_text(encoding="utf-8").replace("sak_exemple_agent", "")
                self.assertIsNone(re.search(r"sak_[A-Za-z0-9]{6,}", texte), chemin.name)


if __name__ == "__main__":
    unittest.main()

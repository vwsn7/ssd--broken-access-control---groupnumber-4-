
import unittest
import importlib.util
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]


def load_app(name, folder):
    app_path = PROJECT_DIR / folder / "app.py"

    spec = importlib.util.spec_from_file_location(name, app_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


vulnerable_app = load_app("vulnerable_app", "vulnerable-code")
fixed_app = load_app("fixed_app", "fixed-code")


class AccessControlTests(unittest.TestCase):

    def setUp(self):
        vulnerable_app.app.config["TESTING"] = True
        self.vulnerable_client = vulnerable_app.app.test_client()
        vulnerable_app.initialize_db()

        fixed_app.app.config["TESTING"] = True
        self.fixed_client = fixed_app.app.test_client()
        fixed_app.initialize_db()

    def login(self, client):
        return client.post("/", data={
            "email": "alice@example.com",
            "password": "AliceDemo123!"
        })

    def test_vulnerable_own_document(self):
        self.login(self.vulnerable_client)
        response = self.vulnerable_client.get("/documents/1")
        self.assertEqual(response.status_code, 200)

    def test_vulnerable_other_user_document(self):
        self.login(self.vulnerable_client)
        response = self.vulnerable_client.get("/documents/2")
        self.assertEqual(response.status_code, 200)

    def test_fixed_own_document(self):
        self.login(self.fixed_client)
        response = self.fixed_client.get("/documents/1")
        self.assertEqual(response.status_code, 200)

    def test_fixed_blocks_other_user_document(self):
        self.login(self.fixed_client)
        response = self.fixed_client.get("/documents/2")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main(verbosity=2)

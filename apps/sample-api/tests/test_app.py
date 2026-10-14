import json
import threading
import unittest
from http.server import HTTPServer
from urllib.error import HTTPError
from urllib.request import urlopen

from app import Handler


class SampleAPITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), Handler)
        cls.thread = threading.Thread(
            target=cls.server.serve_forever,
            daemon=True,
        )
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def test_health_endpoint(self):
        with urlopen(f"{self.base_url}/health") as response:
            self.assertEqual(response.status, 200)
            self.assertEqual(
                json.loads(response.read()),
                {"status": "healthy"},
            )

    def test_root_endpoint(self):
        with urlopen(f"{self.base_url}/") as response:
            body = json.loads(response.read())

            self.assertEqual(response.status, 200)
            self.assertEqual(body["application"], "DevLaunch Sample API")
            self.assertEqual(body["version"], "1.0.0")
            self.assertEqual(body["platform"], "DevLaunch")

    def test_unknown_endpoint_returns_404(self):
        with self.assertRaises(HTTPError) as error:
            urlopen(f"{self.base_url}/missing")

        self.assertEqual(error.exception.code, 404)
        body = json.loads(error.exception.read())
        self.assertEqual(body, {"error": "Not found"})


if __name__ == "__main__":
    unittest.main()

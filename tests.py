import unittest
import warnings
from ipt import app


class MyAppTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

        warnings.simplefilter("ignore", category=DeprecationWarning)

    def test_index_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "<p>HAYS</p>")

    def test_getcountries_by_id(self):
        response = self.app.get("/countries/12")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Bahrain" in response.data.decode())


if __name__ == "__main__":
    unittest.main()

import unittest
from pihace.healthcheck import HealthCheck

class TestHealthCheck(unittest.TestCase):

    def test_mock_success(self):
        def mock_success():
            return True

        hc = HealthCheck()
        hc.register("MockSuccess", mock_success)
        result = hc.check()

        self.assertEqual(result["status"], "Available")
        self.assertEqual(result["rate"], "1/1")
        self.assertNotIn("MockSuccess", result["failure"])

    def test_mock_fail(self):
        def mock_fail():
            return (False, "mocked error")

        hc = HealthCheck()
        hc.register("MockFail", mock_fail)
        result = hc.check()

        self.assertEqual(result["status"], "Unavailable")
        self.assertEqual(result["rate"], "0/1")
        self.assertIn("MockFail", result["failure"])
        self.assertEqual(result["failure"]["MockFail"], "mocked error")

if __name__ == "__main__":
    unittest.main()

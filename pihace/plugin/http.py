import requests

class HTTP:
    def __init__(self, url: str, timeout: int = 5):
        self.url = url
        self.timeout = timeout

    def __call__(self):
        try:
            response = requests.get(self.url, timeout=self.timeout)
            if response.ok:
                return True
            return False, f"Status code: {response.status_code}"
        except requests.RequestException as e:
            return False, str(e)

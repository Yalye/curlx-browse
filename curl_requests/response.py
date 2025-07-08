import json

class CurlResponse:
    def __init__(self, raw_bytes):
        self._raw = raw_bytes
        self.status_code = 200
        self.headers = {}
        self.content = raw_bytes
        self.text = raw_bytes.decode(errors="replace")

    def json(self):
        return json.loads(self.text)

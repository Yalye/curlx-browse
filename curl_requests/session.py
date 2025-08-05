from urllib.parse import urlencode

from .curl_wrapper import CurlWrapper
from .response import CurlResponse

class CurlSession:
    def __init__(self):
        self.headers = {}
        self.cookies = {}
        self.timeout = 30
        # self.user_agent = "curl_requests/0.1"
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"

    def get(self, url, params=None, headers=None):
        final_headers = self.headers.copy()
        if headers:
            final_headers.update(headers)

        if params:
            query = urlencode(params, doseq=True)
            connector = '&' if '?' in url else '?'
            url += connector + query

        curl = CurlWrapper()
        res = curl.perform_request("GET", url, headers=final_headers, timeout=self.timeout)
        return res

    def post(self, url, data=None, headers=None):
        final_headers = self.headers.copy()
        if headers:
            final_headers.update(headers)

        curl = CurlWrapper()
        res = curl.perform_request("POST", url, headers=final_headers, data=data, timeout=self.timeout)
        return CurlResponse(res)

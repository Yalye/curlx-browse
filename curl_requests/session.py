from urllib.parse import urlencode
from curl_requests._wrapper import lib, ffi
from .curl_wrapper import CurlWrapper
from .response import CurlResponse

class CurlSession:
    def __init__(self):
        # Initialize a unique curl easy handle per session
        self.curl = lib.curl_easy_init()
        if self.curl == ffi.NULL:
            raise RuntimeError("Failed to init curl")

        # Enable libcurl cookie engine in memory (empty string)
        lib._curl_easy_setopt(self.curl, lib.CURLOPT_COOKIEFILE, ffi.new("char[]", b""))

        # Optional: save cookies to a file during session lifecycle
        # lib._curl_easy_setopt(self.curl, lib.CURLOPT_COOKIEJAR, ffi.new("char[]", b"cookies.txt"))

        self.cookies = {
            # "cookieee":"eeeee"
        }
        # self.timeout = 30
        self.default_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "Accept": "*/*"
        }

    def get_cookie_header(self):
        # Convert stored cookies to a Cookie header string
        return "; ".join(f"{k}={v}" for k, v in self.cookies.items())

    def get(self, url, params=None, headers=None, timeout=None, allow_redirects=True):
        headers = {**self.default_headers, **(headers or {})}

        if self.cookies:
            cookie_header = self.get_cookie_header()
            headers = headers or {}
            headers.setdefault("Cookie", cookie_header)

        if params:
            query = urlencode(params, doseq=True)
            connector = '&' if '?' in url else '?'
            url += connector + query
        curl = CurlWrapper()
        res = curl.perform_request(self.curl,"GET", url, headers=headers, timeout=timeout, allow_redirects=allow_redirects)
        return res

    def post(self, url, data=None, headers=None):
        final_headers = self.headers.copy()
        if headers:
            final_headers.update(headers)

        curl = CurlWrapper()
        res = curl.perform_request("POST", url, headers=final_headers, data=data, timeout=self.timeout)
        return CurlResponse(res)

    def close(self):
        if self.curl != ffi.NULL:
            lib.curl_easy_cleanup(self.curl)
            self.curl = ffi.NULL

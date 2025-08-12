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

        self.proxies = None

        # self.timeout = 30
        self.default_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "Accept": "*/*"
        }

    def get_cookie_header(self):
        # Convert stored cookies to a Cookie header string
        return "; ".join(f"{k}={v}" for k, v in self.cookies.items())

    def perform_request(self,
        method,
        url,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None):
        """Constructs a :class:`Request <Request>`, prepares it and sends it.
        Returns :class:`Response <Response>` object.

        :param method: method for the new :class:`Request` object.
        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary or bytes to be sent in the query
            string for the :class:`Request`.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json to send in the body of the
            :class:`Request`.
        :param headers: (optional) Dictionary of HTTP Headers to send with the
            :class:`Request`.
        :param cookies: (optional) Dict or CookieJar object to send with the
            :class:`Request`.
        :param files: (optional) Dictionary of ``'filename': file-like-objects``
            for multipart encoding upload.
        :param auth: (optional) Auth tuple or callable to enable
            Basic/Digest/Custom HTTP Auth.
        :param timeout: (optional) How long to wait for the server to send
            data before giving up, as a float, or a :ref:`(connect timeout,
            read timeout) <timeouts>` tuple.
        :type timeout: float or tuple
        :param allow_redirects: (optional) Set to True by default.
        :type allow_redirects: bool
        :param proxies: (optional) Dictionary mapping protocol or protocol and
            hostname to the URL of the proxy.
        :param stream: (optional) whether to immediately download the response
            content. Defaults to ``False``.
        :param verify: (optional) Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use. Defaults to ``True``. When set to
            ``False``, requests will accept any TLS certificate presented by
            the server, and will ignore hostname mismatches and/or expired
            certificates, which will make your application vulnerable to
            man-in-the-middle (MitM) attacks. Setting verify to ``False``
            may be useful during local development or testing.
        :param cert: (optional) if String, path to ssl client cert file (.pem).
            If Tuple, ('cert', 'key') pair.
        :rtype: requests.Response
        """
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
        res = curl.perform_request(self.curl, method=method, url=url, headers=headers, timeout=timeout, data=data,
                                   json=json,
                                   allow_redirects=allow_redirects, proxies=proxies)
        return res


    def get(self, url, **kwargs):
        r"""Sends a GET request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """
        return self.perform_request('GET', url, **kwargs)


    def options(self, url, **kwargs):
        r"""Sends a OPTIONS request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        kwargs.setdefault("allow_redirects", True)
        return self.request("OPTIONS", url, **kwargs)

    def head(self, url, **kwargs):
        r"""Sends a HEAD request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        kwargs.setdefault("allow_redirects", False)
        return self.request("HEAD", url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        r"""Sends a POST request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """
        # Convert dict to x-www-form-urlencoded if data is dict
        if data and isinstance(data, dict):
            data = urlencode(data)

        # If json is provided, encode as JSON and set header
        if json is not None:
            import json as jsonlib
            data = jsonlib.dumps(json)
            headers = kwargs.get("headers")
            if headers is None:
                headers = {}
            headers["Content-Type"] = "application/json"

        return self.perform_request('POST', url, data=data, json=json, **kwargs)


    def close(self):
        if self.curl != ffi.NULL:
            lib.curl_easy_cleanup(self.curl)
            self.curl = ffi.NULL

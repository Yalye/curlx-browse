from curl_requests._wrapper import lib, ffi

### test 1
result = lib.add(2,3)
print(result)

class CurlWrapper:

    def setopt(self, curl, option, value):
        if isinstance(value, str):
            val = ffi.new("char[]", value.encode())
        elif isinstance(value, bytes):
            val = ffi.new("char[]", value)
        elif isinstance(value, int):
            val = ffi.new("long *", value)
        elif value is None:
            val = ffi.NULL
        else:
            val = value  # assume already cdata
        lib._curl_easy_setopt(curl, option, val)

    def perform_request(self, method, url, headers=None, data=None, timeout=30):
        curl = lib.curl_easy_init()
        if curl == ffi.NULL:
            raise RuntimeError("Failed to init curl")

        lib._curl_easy_setopt(curl, lib.CURLOPT_URL, ffi.new("char[]", url.encode()))
        lib._curl_easy_setopt(curl, lib.CURLOPT_CUSTOMREQUEST, ffi.new("char[]", method.encode()))

        self.setopt(curl, lib.CURLOPT_SSL_VERIFYHOST, 0)
        self.setopt(curl, lib.CURLOPT_SSL_VERIFYPEER, 0)

        # Headers
        header_list = ffi.NULL
        if headers:
            for k, v in headers.items():
                hdr = f"{k}: {v}".encode()
                header_list = lib.curl_slist_append(header_list, ffi.new("char[]", hdr))
            lib._curl_easy_setopt(curl, lib.CURLOPT_HTTPHEADER, header_list)

        # POST data
        if method == "POST" and data:
            if isinstance(data, dict):
                from urllib.parse import urlencode
                post_data = urlencode(data).encode()
            else:
                post_data = data.encode() if isinstance(data, str) else data
            lib._curl_easy_setopt(curl, lib.CURLOPT_POSTFIELDS, ffi.new("char[]", post_data))

        # Write callback
        buf = []
        @ffi.callback("size_t(char *, size_t, size_t, void *)")
        def write_cb(ptr, size, nmemb, userdata):
            content = ffi.string(ptr, size * nmemb)
            buf.append(content)
            return size * nmemb

        lib._curl_easy_setopt(curl, lib.CURLOPT_WRITEFUNCTION, write_cb)

        # Perform
        res = lib.curl_easy_perform(curl)
        if res != 0:
            raise RuntimeError(f"curl failed with code {res}")

        lib.curl_easy_cleanup(curl)
        return b"".join(buf)

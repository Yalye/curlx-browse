from curl_requests import _wrapper
from cffi import FFI

lib = _wrapper.lib
ffi = _wrapper.ffi


### test 1
result = lib.add(2,3)
print(result)

### test 2
curl_version = lib.curl_version()
version_str = ffi.string(curl_version).decode("utf-8")
print("libcurl version：", version_str)

### test 3
curl = lib.curl_easy_init()
if curl == ffi.NULL:
    raise RuntimeError("curl_easy_init failed")

url = ffi.new("char[]", b"http://cip.cc")
lib._curl_easy_setopt(curl, 10002, url)

response_buf = ffi.new("char[]", 10000)
response_len = ffi.new("int *", 0)

@ffi.callback("size_t(char*, size_t, size_t, void*)")
def write_cb(ptr, size, nmemb, userdata):
    length = size * nmemb
    ffi.memmove(response_buf + response_len[0], ptr, length)
    response_len[0] += length
    return length

import certifi
cafile = ffi.new("char[]", certifi.where().encode("utf-8"))
lib._curl_easy_setopt(curl, 10065, cafile)

lib._curl_easy_setopt(curl, 20011, write_cb)
lib._curl_easy_setopt(curl, 10001, ffi.NULL)

res = lib.curl_easy_perform(curl)
if res != 0:
    raise RuntimeError(f"curl_easy_perform failed with code {res}")

data = ffi.buffer(response_buf, response_len[0])[:]
print("response：", data.decode("utf-8", errors="replace"))

lib.curl_easy_cleanup(curl)






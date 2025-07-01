from pathlib import Path
import os
import json
import platform
import struct
import tempfile
from glob import glob
from pathlib import Path
from urllib.request import urlretrieve
from cffi import FFI

system = platform.system()

def detect_arch():
    with open(Path(__file__).parent / "libs.json") as f:
        archs = json.loads(f.read())

    uname = platform.uname()
    glibc_flavor = "gnueabihf" if uname.machine in ["armv7l", "armv6l"] else "gnu"

    libc, _ = platform.libc_ver()
    # https://github.com/python/cpython/issues/87414
    libc = glibc_flavor if libc == "glibc" else "musl"
    pointer_size = struct.calcsize("P") * 8

    for arch in archs:
        if (
            arch["system"] == uname.system
            and arch["machine"] == uname.machine
            and arch["pointer_size"] == pointer_size
            and ("libc" not in arch or arch.get("libc") == libc)
        ):
            if arch["libdir"]:
                arch["libdir"] = os.path.expanduser(arch["libdir"])
            else:
                global tmpdir
                if "CI" in os.environ:
                    tmpdir = "./tmplibdir"
                    os.makedirs(tmpdir, exist_ok=True)
                    arch["libdir"] = tmpdir
                else:
                    tmpdir = tempfile.TemporaryDirectory()
                    arch["libdir"] = tmpdir.name
            return arch
    raise Exception(f"Unsupported arch: {uname}")


arch = detect_arch()
print(f"Using {arch['libdir']} to store libcurl-impersonate")


def get_curl_libraries():
    if arch["system"] == "Windows":
        return [
            "Crypt32",
            "Secur32",
            "wldap32",
            "Normaliz",
            "libcurl",
            "zstd",
            "zlib",
            "ssl",
            "nghttp2",
            "nghttp3",
            "ngtcp2",
            "ngtcp2_crypto_boringssl",
            "crypto",
            "brotlienc",
            "brotlidec",
            "brotlicommon",
        ]
    elif arch["system"] == "Darwin" or (
        arch["system"] == "Linux" and arch.get("link_type") == "dynamic"
    ):
        return ["curl-impersonate"]
    else:
        return []

def get_curl_archives():
    print("Files for linking")
    print(os.listdir(arch["libdir"]))
    if arch["system"] == "Linux" and arch.get("link_type") == "static":
        # note that the order of libraries matters
        # https://stackoverflow.com/a/36581865
        return [
            f"{arch['libdir']}/libcurl-impersonate.a",
            f"{arch['libdir']}/libssl.a",
            f"{arch['libdir']}/libcrypto.a",
            f"{arch['libdir']}/libz.a",
            f"{arch['libdir']}/libzstd.a",
            f"{arch['libdir']}/libnghttp2.a",
            f"{arch['libdir']}/libngtcp2.a",
            f"{arch['libdir']}/libngtcp2_crypto_boringssl.a",
            f"{arch['libdir']}/libnghttp3.a",
            f"{arch['libdir']}/libbrotlidec.a",
            f"{arch['libdir']}/libbrotlienc.a",
            f"{arch['libdir']}/libbrotlicommon.a",
        ]
    else:
        return []


ffi = FFI()
root_dir = Path(__file__).parent

ffi.set_source(
    "curl_requests._wrapper",
    """
        #include "easy_set.h"
    """,
    # FIXME from `curl-impersonate`
    libraries=get_curl_libraries(),
    extra_objects=get_curl_archives(),
    library_dirs=[arch["libdir"]],
    source_extension=".c",
    include_dirs=[
        str(root_dir / "include"),
        str(root_dir / "lib64/include"),
        str(root_dir / "ffi"),
    ],
    sources=[
        str(root_dir / "ffi/easy_set.c"),
    ],
    extra_compile_args=(
        ["-Wno-implicit-function-declaration"] if system == "Darwin" else []
    ),
    extra_link_args=(["-lstdc++"] if system != "Windows" else []),
)

# 定义 libcurl 的 C 接口
root_dir = Path(__file__).parent
with open(root_dir / "ffi/cdef.c") as f:
    cdef_content = f.read()
    ffi.cdef(cdef_content)

# 加载 libcurl 库
# libcurl = ffi.dlopen(r"C:\Users\admin\Downloads\vcpkg-master\packages\curl_x64-windows\bin\libcurl.dll")  # 或者 "libcurl.dylib" 或 "libcurl.dll"


#
# class CurlWrapper:
#     def __init__(self):
#         self.handle = libcurl.curl_easy_init()
#
#     def __del__(self):
#         if self.handle:
#             libcurl.curl_easy_cleanup(self.handle)
#
#     def set_option(self, option, value):
#         libcurl.curl_easy_setopt(self.handle, option, value)
#
#     def perform(self):
#         return libcurl.curl_easy_perform(self.handle)

# 定义回调函数
def write_callback_function(ptr, size, nmemb, userdata):
    data = ffi.buffer(ptr, size * nmemb)  # 获取返回数据
    print(f"Received data: {data[:100]}...")  # 打印前 100 字节
    return size * nmemb

if __name__ == "__main__":
    ffi.compile(verbose=False)
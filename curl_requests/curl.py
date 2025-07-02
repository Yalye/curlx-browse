from curl_requests import _wrapper
from cffi import FFI

lib = _wrapper.lib

result = lib.add(2,3)
print(result)

# # 创建一个 CurlWrapper 实例
# curl = CurlWrapper()
#
# # 设置请求的 URL
# curl.set_option(10002, "https://www.example.com")
#
# # 设置回调函数来处理返回的数据
# curl.set_option(20011, ffi.cast("write_callback", write_callback_function))
#
# # 执行请求
# curl.perform()




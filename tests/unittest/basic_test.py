from curl_requests.session import CurlSession

s = CurlSession()
r1 = s.get("https://httpbin.org/get")
print(r1.status_code)
print(r1.text)

r2 = s.post("https://httpbin.org/post", data={"username": "admin"})
print(r2.status_code)
print(r2.json())

from curl_requests.session import CurlSession
from exceptions import ReadTimeout, ConnectTimeout, Timeout

s = CurlSession()

# r1 = s.get("https://httpbin.org/get")
# print(r1.status_code)
# print(r1.text)
#
# r2 = s.post("https://httpbin.org/post", data={"username": "admin"})
# print(r2.status_code)
# print(r2.json())

def test_get():
    r3 = s.get("https://httpbin.org/get")
    print(r3.status_code)
    print(r3.json())

def test_get_params():
    params = {
        "q": "test",
        "page": "1"
    }
    headers = {
        "User-Agent": "curl-requests-test/1.0",
        "X-Test-Header": "my-value"
    }
    r = s.get('https://httpbin.org/get', params=params, headers=headers, )
    print(r.status_code)
    print(r.json())
    print(r.content)

def test_get_timeout():
    try:
        r = s.get('https://httpbin.org/delay/5', timeout=1)
    except ReadTimeout:
        print("Server took too long to respond (read timeout)")
    except ConnectTimeout:
        print("Couldn't connect to server (connect timeout)")
    except Timeout:
        print("General timeout error")
    print(r.status_code)
    print(r.json())
    print(r.content)
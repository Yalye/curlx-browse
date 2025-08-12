from curl_requests.session import CurlSession
from curl_requests.exceptions import ReadTimeout, ConnectTimeout, Timeout

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
    except ReadTimeout as e:
        print("Server took too long to respond (read timeout)")
    except ConnectTimeout:
        print("Couldn't connect to server (connect timeout)")
    except Timeout:
        print("General timeout error")
    except Exception as e:
        print(f"Caught exception type: {type(e)} - {e}")
    # print(r.status_code)
    # print(r.json())
    # print(r.content)

def test_get_headers():
    # 仅使用默认 headers
    r1 = s.get("https://httpbin.org/headers")
    print("=== Default Headers ===")
    print(r1.text)

    # 添加自定义 headers（部分覆盖）
    r2 = s.get("https://httpbin.org/headers", headers={
        "User-Agent": "Custom-UA/2.0",
        "X-Test": "yes"
    })
    print("\n=== Custom Headers ===")
    print(r2.text)

def test_get_cookies():
    resp1 = s.get('https://httpbin.org/cookies/set?testcookie=value123')
    print("Cookies after first request:", resp1.cookies)

    resp2 = s.get('https://httpbin.org/cookies')
    print("Second response content:", resp2.content.decode())

    s.close()

def test_redirection():
    resp = s.get("https://httpbin.org/redirect/2", allow_redirects=True)
    print(resp.status_code)  # 200
    print(resp.content[:200])

    resp_no_redirect = s.get("https://httpbin.org/redirect/2", allow_redirects=False)
    print(resp_no_redirect.status_code)  # 302

if __name__ == '__main__':
    test_get_timeout()
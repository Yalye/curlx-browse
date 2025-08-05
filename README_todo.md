# curl-requests

## Purpose

The `curl-requests` library provides an easy-to-use interface for making HTTP requests using `libcurl` in Python. It is designed as a performance-oriented alternative to `requests` and offers flexibility for advanced users who need to control the HTTP request process at a low level. The library allows you to make HTTP GET, POST, and other types of requests directly using the curl library, which is widely used for its speed and robustness in handling web requests.

The project aims to:
- Provide a Python wrapper around `libcurl` using the `cffi` library for low-level HTTP operations.
- Offer fine-grained control over HTTP request parameters, headers, cookies, and more.
- Support various HTTP methods and features, including custom headers, SSL configurations, and POST data handling.
- Be a flexible tool for those who need advanced capabilities like bypassing security measures and customizing HTTP headers.

## Current Status

The project is in an **early development stage** and currently supports the following:

- **GET Requests**: Standard GET requests to retrieve resources.
- **POST Requests**: Sending POST requests with form-encoded data.
- **Custom Headers**: Ability to add custom headers to requests.
- **Basic SSL Handling**: Optional SSL verification bypass.
- **Response Handling**: Captures status codes, response content, and raw response data.

### Known Issues:
- Header parsing is currently a placeholder (headers returned as an empty dictionary).
- No cookie management functionality yet.
- No advanced features like redirects or file uploads (multipart/form-data) have been implemented.
  
## Installation

### Prerequisites

- **Python** (>=3.7)
- **libcurl**: Make sure the `libcurl` shared library (`libcurl.dll`, `libcurl.so`, `libcurl.dylib`) is available on your system.
  - On **Windows**, `libcurl` may need to be installed using tools like `vcpkg` or manually downloaded from [curl's official website](https://curl.se/download.html).
  - On **Linux**, install using `apt-get install libcurl4-openssl-dev` or equivalent for your distribution.
  - On **macOS**, use `brew install curl`.

### Installation Steps

```bash
git clone https://github.com/yourusername/curl-requests.git
cd curl-requests
pip install .

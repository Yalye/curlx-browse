# curl_requests/exceptions.py

class CurlRequestException(Exception):
    """Base exception for curl_requests"""
    pass

class Timeout(CurlRequestException):
    """General timeout exception"""
    pass

class ConnectTimeout(Timeout):
    """Raised when the connection times out"""
    pass

class ReadTimeout(Timeout):
    """Raised when reading the response times out"""
    pass

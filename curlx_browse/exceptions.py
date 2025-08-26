# curlx_browse/exceptions.py

class CurlRequestException(Exception):
    """Base exception for curlx_browse"""
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

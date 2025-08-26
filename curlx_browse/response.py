import json

class CurlResponse:
    def __init__(self, status_code, content, headers=None, url=None, cookies=None, raw=None):
        """
        Initializes the Response object with necessary fields.

        Args:
        status_code (int): HTTP response status code (e.g., 200, 404).
        content (bytes): Raw response body (can be a string or binary).
        headers (dict, optional): Response headers (default is an empty dictionary).
        url (str, optional): Final requested URL, considering any redirects.
        cookies (dict, optional): Extracted cookies from the response (default is an empty dictionary).
        raw (any, optional): Raw underlying data object (like the curl handle).

        """
        self.status_code = status_code              # HTTP status code
        self.content = content                      # Raw bytes of the response content
        self.text = content.decode(errors="replace") if isinstance(content, bytes) else str(content)
        self.headers = headers or {}                # Response headers as a dictionary
        self.url = url                              # Final URL after any redirects
        self.cookies = cookies or {}                # Cookies as a dictionary
        self.raw = raw                              # Raw underlying data (like curl handle)

    def json(self):
        """
        Parses the response content as JSON if applicable.

        Returns:
        dict: Parsed JSON response content
        """
        import json
        return json.loads(self.text)

    def __repr__(self):
        """Returns a string representation of the Response object."""
        return f"<Response [{self.status_code}]>"

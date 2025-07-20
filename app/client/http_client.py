"""
Author: nikhil.anand
Created at: 19/07/25
"""

from typing import Dict, Optional, Union
import backoff
import requests
from requests import Response
from fastapi.logger import logger


class HttpClient:
    """
    HTTP client wrapper with retry logic and standardized headers.

    This class provides a robust HTTP client with automatic retry functionality
    using exponential backoff for handling transient network failures. It includes
    standardized headers and error handling for reliable web requests.

    Features:
        - Automatic retry with exponential backoff
        - Standardized headers for all requests
        - Comprehensive error handling and logging
        - Support for GET, POST, and PUT methods
    """

    def __init__(self) -> None:
        """
        Initialize the HttpClient.

        Currently, no initialization parameters are required as the client
        uses static configuration and method-specific parameters.
        """
        pass

    @staticmethod
    def __get_standard_headers() -> Dict[str, str]:
        """
        Get the standard headers for HTTP requests.

        Returns:
            Dict[str, str]: Dictionary containing standard HTTP headers
                - Accept: Specifies accepted content types
                - Content-Type: Specifies the content type for request body
        """
        return {"Accept": "*/*", "Content-Type": "application/json"}

    def __get_headers(self, headers: Optional[Dict[str, str]]) -> Dict[str, str]:
        """
        Merge custom headers with standard headers.

        This method combines the standard headers with any custom headers
        provided for a specific request, with custom headers taking precedence.

        Args:
            headers (Optional[Dict[str, str]]): Custom headers to merge with standard headers

        Returns:
            Dict[str, str]: Combined headers dictionary
        """
        standard_headers = self.__get_standard_headers()
        if headers is not None:
            standard_headers.update(headers)
        return standard_headers

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_tries=6)
    def __execute(
        self, http_method: str, url: str, payload: str, headers: Dict[str, str], timeout: Optional[Union[float, int]]
    ) -> Response:
        """
        Execute HTTP request with retry logic and error handling.

        This method performs the actual HTTP request with automatic retry using
        exponential backoff for handling transient failures. It validates response
        status codes and provides comprehensive error logging.

        Args:
            http_method (str): HTTP method (GET, POST, PUT, etc.)
            url (str): Target URL for the request
            payload (str): Request body data
            headers (Dict[str, str]): HTTP headers for the request
            timeout (Optional[Union[float, int]]): Request timeout in seconds

        Returns:
            Response: The HTTP response object

        Raises:
            requests.exceptions.RequestException: For any HTTP request failures
        """
        try:
            response = requests.request(http_method, url, headers=headers, data=payload, timeout=timeout)
            if response.status_code < 200 or response.status_code >= 300:
                logger.error("Http request unsuccessful on url {} due to {}".format(url, response.reason))
                raise requests.exceptions.RequestException
            return response
        except Exception as e:
            logger.error(msg="Failed to execute http request on url {} ".format(url), exception=e)
            raise requests.exceptions.RequestException

    def get(
        self,
        url: str,
        payload: str = "",
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[Union[float, int]] = None,
    ) -> Response:
        """
        Perform HTTP GET request.

        Args:
            url (str): Target URL for the GET request
            payload (str, optional): Request body data. Defaults to ""
            headers (Optional[Dict[str, str]], optional): Custom headers. Defaults to None
            timeout (Optional[Union[float, int]], optional): Request timeout. Defaults to None

        Returns:
            Response: The HTTP response object
        """
        headers = self.__get_headers(headers=headers)
        return self.__execute(http_method="GET", url=url, payload=payload, headers=headers, timeout=timeout)

    def post(
        self,
        url: str,
        payload: str = "",
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[Union[float, int]] = None,
    ) -> Response:
        """
        Perform HTTP POST request.

        Args:
            url (str): Target URL for the POST request
            payload (str, optional): Request body data. Defaults to ""
            headers (Optional[Dict[str, str]], optional): Custom headers. Defaults to None
            timeout (Optional[Union[float, int]], optional): Request timeout. Defaults to None

        Returns:
            Response: The HTTP response object
        """
        headers = self.__get_headers(headers=headers)
        return self.__execute(http_method="POST", url=url, payload=payload, headers=headers, timeout=timeout)

    def put(
        self,
        url: str,
        payload: str = "",
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[Union[float, int]] = None,
    ) -> Response:
        """
        Perform HTTP PUT request.

        Args:
            url (str): Target URL for the PUT request
            payload (str, optional): Request body data. Defaults to ""
            headers (Optional[Dict[str, str]], optional): Custom headers. Defaults to None
            timeout (Optional[Union[float, int]], optional): Request timeout. Defaults to None

        Returns:
            Response: The HTTP response object
        """
        headers = self.__get_headers(headers=headers)
        return self.__execute(http_method="PUT", url=url, payload=payload, headers=headers, timeout=timeout)

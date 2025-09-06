# src/common/api.py
import logging
import requests
from typing import Optional
from requests.exceptions import RequestException, HTTPError, ConnectionError, Timeout

logger = logging.getLogger(__name__)


class ApiError(Exception):
    """Custom exception for API errors"""
    pass


class ApiClient:
    """Base API client with error handling and logging"""
   
    ApiError = ApiError

    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.session = requests.Session()
   
    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Make HTTP request with error handling and logging"""       
        logger.debug(f"Making {method.upper()} request to {url}")
        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs
            )
            logger.debug(f"Response status: {response.status_code}")
            response.raise_for_status()
            return response
            
        except ConnectionError as e:
            logger.error(f"Connection failed to {url}: {e}", exc_info=True)
            raise ApiError(f"Failed to connect to API: {e}") from e
            
        except Timeout as e:
            logger.error(f"Request timeout to {url}: {e}", exc_info=True)
            raise ApiError(f"Request timed out: {e}") from e
            
        except HTTPError as e:
            logger.error(f"HTTP error {e.response.status_code} for {url}: {e}", exc_info=True)
            raise ApiError(f"API request failed with status {e.response.status_code}: {e}") from e
            
        except RequestException as e:
            logger.error(f"Request failed to {url}: {e}", exc_info=True)
            raise ApiError(f"Request failed: {e}") from e
    
    def get(self, url: str, params: Optional[dict] = None, **kwargs) -> requests.Response:
        return self._make_request("GET", url, params=params, **kwargs)
    
    def post(self, url: str, data: Optional[dict] = None, json: Optional[dict | list] = None, **kwargs) -> requests.Response:
        return self._make_request("POST", url, data=data, json=json, **kwargs)
    
    def put(self, url: str, data: Optional[dict] = None, json: Optional[dict | list] = None, **kwargs) -> requests.Response:
        return self._make_request("PUT", url, data=data, json=json, **kwargs)
    
    def delete(self, url: str, **kwargs) -> requests.Response:
        return self._make_request("DELETE", url, **kwargs)

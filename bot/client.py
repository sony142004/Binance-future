import hmac
import hashlib
import time
import requests
from urllib.parse import urlencode
from bot.logging_config import logger

class BinanceFuturesClient:
    BASE_URL = "https://testnet.binancefuture.com"

    def __init__(self, api_key: str, api_secret: str):
        if not api_key or not api_secret:
            raise ValueError("API Key and Secret must be provided")
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key
        })

    def _generate_signature(self, query_string: str) -> str:
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def _request(self, method: str, endpoint: str, params: dict = None):
        if params is None:
            params = {}
        
        # Add timestamp
        params['timestamp'] = int(time.time() * 1000)
        
        query_string = urlencode(params)
        signature = self._generate_signature(query_string)
        
        url = f"{self.BASE_URL}{endpoint}?{query_string}&signature={signature}"
        
        logger.debug(f"API Request: {method} {url.replace(self.api_secret, '***')}")
        
        try:
            response = self.session.request(method, url)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"API Response: {data}")
            return data
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error: {e.response.status_code} - {e.response.text}")
            raise Exception(f"API Error: {e.response.text}") from e
        except requests.exceptions.RequestException as e:
            logger.error(f"Network Error: {e}")
            raise Exception(f"Network Error: {e}") from e

    def ping(self):
        url = f"{self.BASE_URL}/fapi/v1/ping"
        response = self.session.get(url)
        return response.json()

from datetime import datetime, timedelta

class GeckoTerminalPool:
    """Mock the data from geckoterminal API
    """
    def __init__(self, address: str, hours: int, minutes: int) -> None:
        self.address = address
        self.time_created = datetime.now() - timedelta(hours=hours, minutes=minutes)

    def get(self) -> dict:
        """Return the mock data

        Returns:
            dict: A summarized object representing geckoterminal API schema
        """
        return {
            "attributes": {
                "base_token_price_usd": "1.0",
                "base_token_price_native_currency": "0.000075059997023997",
                "quote_token_price_usd": "1.001",
                "quote_token_price_native_currency": "1.0",
                "address": "0x001",
                "name": "Token / WETH",
                "reserve_in_usd": "100000",
                "pool_created_at": datetime.strftime(self.time_created, '%Y-%m-%dT%H:%M:%SZ')
            }
        }

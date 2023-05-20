class DexScreenerPair:
    """Mock the data from dexscreener API
    """
    def __init__(self, address: str, base_symbol: str, has_liq: bool, has_fdv: bool, liq: float, fdv: float) -> None:
        self.address = address
        self.base_symbol = base_symbol
        self.has_liq = has_liq
        self.has_fdv = has_fdv
        self.liq = liq
        self.fdv = fdv

    def get(self):
        """Return the mock data

        Returns:
            dict: A full object representing dexscreener API pair schema
        """
        obj = {
            "chainId": "ethereum",
            "dexId": "uniswap",
            "url": f"https://dexscreener.com/ethereum/{self.address}",
            "pairAddress": self.address,
            "labels": [
                "v3"
            ],
            "baseToken": {
                "address": "",
                "name": "Pepe",
                "symbol": self.base_symbol
            },
            "quoteToken": {
                "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                "name": "Wrapped Ether",
                "symbol": "WETH"
            },
            "priceNative": "0.0000000008361",
            "priceUsd": "0.000001518",
            "txns": {
                "h24": {
                    "buys": 937,
                    "sells": 1422
                },
                "h6": {
                    "buys": 119,
                    "sells": 210
                },
                "h1": {
                    "buys": 16,
                    "sells": 25
                },
                "m5": {
                    "buys": 2,
                    "sells": 2
                }
            },
            "volume": {
                "h24": 17025890.11,
                "h6": 2578608.53,
                "h1": 218802.23,
                "m5": 20005.24
            },
            "priceChange": {
                "h24": -5.02,
                "h6": -0.33,
                "h1": -0.6,
                "m5": -0.15
            },
            "pairCreatedAt": 1681942955000
        }

        if self.has_liq:
            obj['liquidity'] = {
                "usd": self.liq,
                "base": 3803744557424,
                "quote": 1140
            }
        if self.has_fdv:
            obj['fdv'] = self.fdv

        return obj

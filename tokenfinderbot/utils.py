import requests
from datetime import datetime, timedelta


def get_new_pools() -> list:
    """Get new pools from geckoterminal API

    Raises:
        Exception: Connection Error

    Returns:
        list: new pools recently created
    """
    try:
        url = "https://api.geckoterminal.com/api/v2/networks/eth/new_pools"
        response = requests.get(url)
        data = response.json()
        return data['data']
    except Exception as e:
        raise ConnectionError(f"geckoterminal API Error: {e}")


def filter_pools_by_time(pools: list, hours: int = 1, minutes: int = 0) -> list:
    """Filter pools by the time they have been created less than x hours, y minutes ago

    Args:
        pools (list): pools list from geckoterminal API
        hours (int, optional): how many hours ago. Defaults to 1.
        minutes (int, optional): how many minutes ago. Defaults to 0.

    Returns:
        list: filtered pools
    """
    address_list = []
    time_diff = timedelta(hours=hours, minutes=minutes)
    for pool in pools:
        pool_created_at = datetime.strptime(pool['attributes']['pool_created_at'], '%Y-%m-%dT%H:%M:%SZ')
        if datetime.now() - pool_created_at < time_diff:
            address_list.append(pool['attributes']['address'])
    return address_list

def get_pools_details(address_list: list) -> list:
    """Get pools info from dexscreener api

    Args:
        address_list (list): list of pool addresses

    Raises:
        Exception: Connection Error

    Returns:
        list: detailed info for each pool
    """
    if len(address_list) == 0:
        return []
    try:
        url = f"https://api.dexscreener.com/latest/dex/pairs/ethereum/{','.join(address_list)}"
        response = requests.get(url)
        data = response.json()
        return data['pairs']
    except Exception as e:
        raise ConnectionError(f"dexscreener API Error: {e}")


def filter_pools_by_liq_mc(pairs: list, liq_mc_ratio: float = 1.5, min_mc: float = 100000, min_liq: float = 0) -> list:
    """Filter pools by liquidity and market cap

    Args:
        pairs (list): list of pairs from dexscreener API
        liq_mc_ratio (float, optional): minimum amount of accepted liquidity/market cap ratio. Defaults to 1.5.
        min_mc (int, optional): minimum accepted market cap. Defaults to 100000.
        min_liq (int, optional): minimum accepted liquidity. Defaults to 0.

    Returns:
        list: filtered list of accepted pools
    """
    filtered_pools = []
    for pair in pairs:
        if 'liquidity' not in pair or 'usd' not in pair['liquidity']:
            continue
        liquidity_usd = pair['liquidity']['usd']
        if 'fdv' in pair and pair['fdv'] >= liq_mc_ratio * liquidity_usd and pair['fdv'] >= min_mc and liquidity_usd >= min_liq:
            filtered_pools.append(pair)
    
    return filtered_pools
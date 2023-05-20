from tokenfinderbot.utils import get_pools_details, filter_pools_by_liq_mc
from .dexscreener_api import DexScreenerPair
import pytest


@pytest.fixture
def pairs():
    """Fetches pairs data from dexscreener API

    Returns:
        list: pairs data for PEPE/WETH and HEX/WETH
    """
    address_list = ['0x11950d141ecb863f01007add7d1a342041227b58',
                    '0x55d5c232d921b9eaa6b37b5845e439acd04b4dba']
    return get_pools_details(address_list)


def test_get_pools_details(pairs):
    """Test if dexscreener API responds correctly

    Args:
        pairs (list): pairs data from dexscreener API
    """
    assert len(pairs) == 2


def test_dexscreener_api_integrity(pairs):
    """Check if dexscreener API schema is still working as supposed

    Args:
        pairs (list): pairs data from dexscreener API
    """
    assert 'baseToken' in pairs[0] and 'quoteToken' in pairs[0] and 'baseToken' in pairs[1] and 'quoteToken' in pairs[1]


def test_filter_pools_by_liq_mc():
    """Test filtering pools by liquidity and market cap
    """
    mock_pairs = [
        # everything ok -> ok
        DexScreenerPair("0x001", "T1", True, True, 100000, 100000*1.6).get(),
        # no liquidity -> not ok
        DexScreenerPair("0x002", "T1", False, True, 100000, 100000*1.6).get(),
        # no fdv -> not ok
        DexScreenerPair("0x003", "T1", True, False, 100000, 100000*1.6).get(),
        # fdv < 1.5* liquidity -> not ok
        DexScreenerPair("0x004", "T1", True, True, 100000, 100000*1.4).get(),
        # fdv < min_mc -> not ok
        DexScreenerPair("0x005", "T1", True, True, 10, 10*1.6).get(),
        # liquidity < min_liq -> not ok
        DexScreenerPair("0x005", "T1", True, True, 0, 100000).get(),
    ]

    filtered_pairs = filter_pools_by_liq_mc(
        mock_pairs, liq_mc_ratio=1.5, min_mc=100000, min_liq=1)

    assert len(
        filtered_pairs) == 1 and "0x001" in filtered_pairs[0]['pairAddress']

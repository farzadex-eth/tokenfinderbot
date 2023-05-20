from .geckoterminal_api import GeckoTerminalPool
from tokenfinderbot.utils import get_new_pools, filter_pools_by_time
import pytest


@pytest.fixture
def pools():
    """Fetches new pools from geckoterminal API

    Returns:
        list: list of new pools from geckoterminal API
    """
    return get_new_pools()


def test_get_new_pools(pools):
    """Test if geckoterminal API responds with new pools data

    Args:
        pools (list): list of new pools from geckoterminal API
    """
    assert len(pools) > 0


def test_geckoterminal_api_integrity(pools):
    """Check if geckoterminal API schema is still working as supposed

    Args:
        pools (list): list of new pools from geckoterminal API
    """
    assert 'attributes' in pools[0] and 'address' in pools[0]['attributes']


def test_filter_pools_by_time():
    """Test filtering new pools by the time created
        default time diff is 1 hour
    """
    mock_pools = [GeckoTerminalPool("0x001", 0, 59).get(
    ), GeckoTerminalPool("0x002", 1, 0).get()]

    address_list = filter_pools_by_time(mock_pools, hours=1, minutes=0)
    assert "0x001" in address_list and "0x002" not in address_list

from .dexscreener_api import DexScreenerPair
from tokenfinderbot.db import PoolDB
import pytest

@pytest.fixture
def pooldb() -> PoolDB:
    """Create a db for test

    Returns:
        PoolDB: a db instance
    """
    db_instance = PoolDB("test_db")
    db_instance.delete_table()
    return db_instance


def test_pool_insert(pooldb: PoolDB) -> None:
    """Test inserting new pool into db

    Args:
        pooldb (PoolDB): a db instance
    """
    pool = DexScreenerPair("0x001", "T1", True, True, 100000, 100000*1.6).get()
    pooldb.insert_pool(pool)

    assert pooldb.pool_exists(pool)


def test_duplicate_pool_insert(pooldb: PoolDB) -> None:
    """Test duplicate pool insert

    Args:
        pooldb (PoolDB): a db instance
    """
    pool = DexScreenerPair("0x001", "T1", True, True, 100000, 100000*1.6).get()
    pooldb.insert_pool(pool)

    with pytest.raises(ValueError, match='Pool already exists'):
        pooldb.insert_pool(pool)


def test_get_pool(pooldb: PoolDB) -> None:
    """Test getting a pool data from db

    Args:
        pooldb (PoolDB): a db instance
    """
    pool = DexScreenerPair("0x001", "T1", True, True, 100000, 100000*1.6).get()
    pooldb.insert_pool(pool)

    retrieved_pool = pooldb.get_pool("0x001")

    assert retrieved_pool['pairAddress'] == "0x001"


def test_pool_string(pooldb: PoolDB) -> None:
    """Test pool info string

    Args:
        pooldb (PoolDB): a db instance
    """
    pool = DexScreenerPair("0x001", "T1", True, True, 100000, 100000*1.6).get()
    pooldb.insert_pool(pool)
    print(pooldb.get_pool_str("0x001"))
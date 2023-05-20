from tinydb import TinyDB, Query
from datetime import datetime, timedelta, timezone


class PoolDB:
    """A JSON database using tinydb
    """

    def __init__(self, name: str = "db") -> None:
        self.db = TinyDB(f"{name}.json")
        self.pools_table = self.db.table("pools")

    def pool_exists(self, pool: dict) -> bool:
        """Check if a pool with a specific address exists in the db

        Args:
            pool (dict): pool

        Returns:
            bool: True if it already exist
        """
        Pool = Query()
        return len(self.pools_table.search(Pool.pairAddress == pool['pairAddress'])) > 0

    def insert_pool(self, pool: dict) -> None:
        """Insert pool data into db

        Args:
            pool (dict): pool

        Raises:
            Exception: Pool already exists
        """
        if self.pool_exists(pool):
            raise ValueError('Pool already exists')
        self.pools_table.insert(pool)

    def delete_table(self) -> None:
        """Delete table
        """
        self.db.drop_table("pools")

    def get_pool(self, address: str) -> dict:
        """Retrieve a pool

        Args:
            address (str): pool pair address

        Returns:
            dict: pool data
        """
        Pool = Query()
        return self.pools_table.search(Pool.pairAddress == address)[0]

    def get_pool_str(self, address: str) -> str:
        """Returns a string of summarized pool info

        Args:
            address (str): pool pair address

        Returns:
            str: pool info
        """
        class bcolors:
            HEADER = '\033[95m'
            OKBLUE = '\033[94m'
            OKCYAN = '\033[96m'
            OKGREEN = '\033[92m'
            WARNING = '\033[93m'
            FAIL = '\033[91m'
            ENDC = '\033[0m'
            BOLD = '\033[1m'
            UNDERLINE = '\033[4m'

        pool = self.get_pool(address)
        info_str = f"""\n--------------------------------------------------------------\n{bcolors.HEADER}{pool['baseToken']['symbol']} / {pool['quoteToken']['symbol']}:
  {bcolors.OKBLUE}Pair Address: {bcolors.OKCYAN}{address}
  {bcolors.OKBLUE}URL: {bcolors.OKCYAN}{pool['url']}
  {bcolors.OKBLUE}Price: 
    {bcolors.ENDC}{pool['priceNative']} {pool['quoteToken']['symbol']}
    {pool['priceUsd']} USD
  {bcolors.OKBLUE}Liquidity: {bcolors.ENDC}{pool['liquidity']['usd']}
  {bcolors.OKBLUE}Market Cap: {bcolors.ENDC}{pool['fdv']}
  {bcolors.OKBLUE}Created at: {bcolors.ENDC}{datetime.utcfromtimestamp(int(pool['pairCreatedAt']/1000)).strftime('%Y-%m-%d %H:%M:%S')} UTC [{(datetime.now(tz=timezone.utc) - timedelta(seconds=pool['pairCreatedAt']/1000)).strftime('%H hour(s), %M minute(s) ago')}]
--------------------------------------------------------------
        """
        return info_str

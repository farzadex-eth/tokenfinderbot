from .db import PoolDB
from .utils import *
from dotmap import DotMap
from datetime import datetime
from schedule import repeat, every, run_pending

class TokenBot:
    """TokenBot class
    This class creates an instance of token bot with default settings.
    Settings can be changed by calling set_settings method.
    """
    def __init__(self) -> None:
        default_settings = {
            'time_filter': {
                'hours': 12,
                'minutes': 0
            },
            'liq_mc_filter': {
                'mc_liq_ratio': 1.5,
                'min_liq': 1000,
                'min_mc': 100000
            },
            'update_interval': 15,
            'db_name': 'db'
        }
        self._settings = DotMap(default_settings)

    def get_settings(self) -> DotMap:
        """Returns current bot settings

        Returns:
            DotMap: current bot settings
        """
        return self._settings

    def set_settings(self, settings: DotMap) -> None:
        """Set new settings

        Args:
            settings (DotMap): a settings object similar to return value of get_settings
        """

        # Check if the setting dict includes all the keys
        if {'time_filter', 'liq_mc_filter', 'update_interval', 'db_name'} <= set(settings.toDict()) and {'hours', 'minutes'} <= set(settings.time_filter.toDict()) and {'mc_liq_ratio', 'min_liq', 'min_mc'} <= set(settings.liq_mc_filter.toDict()):
            self._settings = settings
        else:
            raise (KeyError("Invalid settings dict"))

    
    def single_run(self) -> None:
        """Main function of the bot to fetch and filter new pools based on the filters
        """
        print("************************************************")
        try:
            print(f"*** New run started at {(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')}")
            # init database
            pooldb = PoolDB(self._settings.db_name)

            # get new pools
            new_pools = get_new_pools()
            print("*** Fetched new pools from geckoterminal")

            # filter new pools by time filter
            address_list = filter_pools_by_time(
                new_pools, hours=self._settings.time_filter.hours, minutes=self._settings.time_filter.minutes)
            print("*** Filtered new pools by creation time")

            # get filtered pools info
            pairs = get_pools_details(address_list)
            print("*** Fetched details from dexscreener")

            # filter pools by liquidity and market cap
            filtered_pairs = filter_pools_by_liq_mc(pairs,
                                                    mc_liq_ratio=self._settings.liq_mc_filter.mc_liq_ratio, min_mc=self._settings.liq_mc_filter.min_mc, 
                                                    min_liq=self._settings.liq_mc_filter.min_liq)
            print("*** Filtered pools by liquidity and market cap")

            # write filtered pools to database and print in terminal
            new_pairs_num = 0
            for pair in filtered_pairs:
                try:
                    pooldb.insert_pool(pair)
                    print(pooldb.get_pool_str(pair['pairAddress']))
                    new_pairs_num += 1
                except:
                    pass
            if new_pairs_num == 0: 
                print("[*** No new results! Wait for the next run! ***]")
        except Exception as e:
            print(e)

        print("************************************************")

    def run(self) -> None:
        """Runs the main function every x minutes
        """
        # run a scheduled periodic task
        @repeat(every(2).minutes)
        def main_job():
            self.single_run()

        # first run
        self.single_run()

        # run the task every x minutes
        while True:
            run_pending()



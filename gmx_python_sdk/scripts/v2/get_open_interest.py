import time
from numerize import numerize

from .base import GetData
from .gmx_utils import execute_threading
from .get_oracle_prices import GetOraclePrices


class OpenInterest(GetData):
    def __init__(self, chain: str):
        super().__init__(chain)

    def _get_data_processing(self):
        """
        Generate the dictionary of open interest data

        Returns
        -------
        funding_apr : dict
            dictionary of open interest data.

        """
        oracle_prices_dict = GetOraclePrices(
            chain=self.chain
        ).get_recent_prices()
        print("GMX v2 Open Interest\n")

        long_oi_output_list = []
        short_oi_output_list = []
        long_pnl_output_list = []
        short_pnl_output_list = []
        mapper = []
        long_precision_list = []

        for market_key in self.markets.info:
            # Skip swap markets
            self._get_token_addresses(market_key)

            index_token_address = self.markets.get_index_token_address(
                market_key
            )

            market = [
                market_key,
                index_token_address,
                self._long_token_address,
                self._short_token_address
            ]

            prices_list = [
                int(
                    oracle_prices_dict[
                        index_token_address
                    ]['minPriceFull']
                ),
                int(
                    oracle_prices_dict[
                        index_token_address
                    ]['maxPriceFull']
                )
            ]

            # If the market is a synthetic one we need to use the decimals
            # from the index token
            try:
                if self.markets.is_synthetic(market_key):
                    decimal_factor = self.markets.get_decimal_factor(
                        market_key,
                    )
                else:
                    decimal_factor = self.markets.get_decimal_factor(
                        market_key,
                        long=True
                    )
            except KeyError:
                pass

            oracle_factor = (30 - decimal_factor)
            precision = 10 ** (decimal_factor + oracle_factor)
            long_precision_list = long_precision_list + [precision]

            long_oi_with_pnl, long_pnl = self.make_query(
                self.reader_contract,
                self.data_store_contract_address,
                market,
                prices_list,
                is_long=True
            )

            short_oi_with_pnl, short_pnl = self.make_query(
                self.reader_contract,
                self.data_store_contract_address,
                market,
                prices_list,
                is_long=False
            )

            long_oi_output_list.append(long_oi_with_pnl)
            short_oi_output_list.append(short_oi_with_pnl)
            long_pnl_output_list.append(long_pnl)
            short_pnl_output_list.append(short_pnl)
            mapper.append(self.markets.get_market_symbol(market_key))

        # TODO - currently just waiting x amount of time to not hit rate limit,
        # but needs a retry
        long_oi_threaded_output = execute_threading(long_oi_output_list)
        time.sleep(0.2)
        short_oi_threaded_output = execute_threading(short_oi_output_list)
        time.sleep(0.2)
        long_pnl_threaded_output = execute_threading(long_pnl_output_list)
        time.sleep(0.2)
        short_pnl_threaded_output = execute_threading(short_pnl_output_list)

        for (
            market_symbol,
            long_oi,
            short_oi,
            long_pnl,
            short_pnl,
            long_precision
        ) in zip(
            mapper,
            long_oi_threaded_output,
            short_oi_threaded_output,
            long_pnl_threaded_output,
            short_pnl_threaded_output,
            long_precision_list
        ):
            print("{} Long: ${}".format(
                market_symbol,
                numerize.numerize(
                    (long_oi - long_pnl) / long_precision)
                )
            )

            self.output['long'][market_symbol] = (
                long_oi - long_pnl
            ) / long_precision

            precision = 10 ** 30

            print("{} Short: ${}".format(
                market_symbol,
                numerize.numerize(
                    ((short_oi - short_pnl) / precision))
                )
            )
            self.output['short'][market_symbol] = (
                short_oi - short_pnl
            ) / precision

        return self.output

    def make_query(
        self,
        reader_contract,
        data_store_contract_address: str,
        market: str,
        prices_list: list,
        is_long: bool,
        maximize: bool = False
    ):
        """
        Make query to reader contract to get open interest with pnl and the
        pnl for a given market and direction (set with is_long)

        Parameters
        ----------
        reader_contract : web3._utils.datatypes.Contract
            web3 object of the reader contract.
        data_store_contract_address : str
            address of the datastore contract.
        market : str
            address of the GMX market.
        prices_list : list
            list of min/max short, long, and index fast prices.
        is_long : bool
            is long or short.
        maximize : bool, optional
            either use min or max price. The default is False.

        Returns
        -------
        oi_with_pnl
            uncalled web3 query.
        pnl
            uncalled web3 query.
        """
        oi_with_pnl = reader_contract.functions.getOpenInterestWithPnl(
            data_store_contract_address,
            market,
            prices_list,
            is_long,
            maximize
        )
        pnl = reader_contract.functions.getPnl(
            data_store_contract_address,
            market,
            prices_list,
            is_long,
            maximize
        )

        return oi_with_pnl, pnl


if __name__ == '__main__':
    data = OpenInterest(chain="arbitrum").get_data(to_csv=False)

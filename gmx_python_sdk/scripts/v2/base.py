import logging

from .get_markets import Markets
from .get_oracle_prices import GetOraclePrices


class GetData:
    def __init__(self, chain: str, use_local_datastore: bool = False):
        self.chain = chain
        self.use_local_datastore = use_local_datastore

        self.log = logging.getLogger(self.__class__.__name__)
        self._markets = Markets(self.chain)
        self._long_token_address = None
        self._short_token_address = None

    def get_data(self, to_json: bool = False, to_csv: bool = False):
        data = self._get_data_processing()

        if to_json:
            self._save_json_file_to_datastore(
                "{}_data.json".format(self.chain),
                data
            )

        if to_csv:
            self._save_csv_to_datastore(
                "{}_data.csv".format(self.chain),
                data
            )

        return data

    def _get_data_processing(self):
        pass

    def _get_token_addresses(self, market_key: str):
        self._long_token_address = (
            self.markets.info[market_key]['long_token_address']
        )
        self._short_token_address = (
            self.markets.info[market_key]['short_token_address']
        )
        self.log.info(
            "Long Token Address: {}\nShort Token Address: {}".format(
                self._long_token_address, self._short_token_address
            )
        )

    def _filter_swap_markets(self, market_key: str):
        market_symbol = self._markets[market_key]['market_symbol']
        if 'swap' in market_symbol:
            # Remove swap markets from dict
            self.markets.info.pop(market_key)
            return True
        return False

    def _get_oracle_prices(
        self,
        market_key: str,
        index_token_address: str,
    ):
        """
        For a given market get the marketInfo from the reader contract

        Parameters
        ----------
        market_key : str
            address of GMX market.
        index_token_address : str
            address of index token.
        long_token_address : str
            address of long collateral token.
        short_token_address : str
            address of short collateral token.

        Returns
        -------
        reader_contract object
            unexecuted reader contract object.

        """
        oracle_prices_dict = GetOraclePrices(self.chain).get_recent_prices()

        try:
            prices = (
                (
                    int(
                        (
                            oracle_prices_dict[index_token_address]
                            ['minPriceFull']
                        )
                    ),
                    int(
                        (
                            oracle_prices_dict[index_token_address]
                            ['maxPriceFull']
                        )
                    )
                ),
                (
                    int(
                        (
                            oracle_prices_dict[self._long_token_address]
                            ['minPriceFull']
                        )
                    ),
                    int(
                        (
                            oracle_prices_dict[self._long_token_address]
                            ['maxPriceFull']
                        )
                    )
                ),
                (
                    int(
                        (
                            oracle_prices_dict[self._short_token_address]
                            ['minPriceFull']
                        )
                    ),
                    int(
                        (
                            oracle_prices_dict[self._short_token_address]
                            ['maxPriceFull']
                        )
                    )
                ))

        # TODO - this needs to be here until GMX add stables to signed price
        # API
        except KeyError:
            prices = (
                (
                    int(
                        oracle_prices_dict[index_token_address]['minPriceFull']
                    ),
                    int(
                        oracle_prices_dict[index_token_address]['maxPriceFull']
                    )
                ),
                (
                    int(
                        (
                            oracle_prices_dict[self._long_token_address]
                            ['minPriceFull']
                        )
                    ),
                    int(
                        (
                            oracle_prices_dict[self._long_token_address]
                            ['maxPriceFull']
                        )
                    )
                ),
                (
                    int(1000000000000000000000000),
                    int(1000000000000000000000000)
                ))

        return self.reader_contract.functions.getMarketInfo(
            self.data_store_contract_address,
            prices,
            market_key
        )


if __name__ == "__main__":
    markets = Markets(chain='arbitrum').get_available_markets()
    print('markets')
    from pprint import pprint
    pprint(markets)

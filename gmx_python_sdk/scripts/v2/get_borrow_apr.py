from .base import GetData
from .get_oracle_prices import GetOraclePrices
from .get_markets import GetMarkets
from .gmx_utils import (
    get_reader_contract, contract_map, execute_threading,
    save_json_file_to_datastore, save_csv_to_datastore,
    make_timestamped_dataframe
)


class GetBorrowAPR(GetData):
    def __init__(self, chain: str):
        self.reader_contract = None
        self.data_store_contract_address = None
        self.chain = chain

    def _get_data_processing(self):
        """
        Generate the dictionary of borrow APR data

        Returns
        -------
        funding_apr : dict
            dictionary of borrow data.

        """
        self.data_store_contract_address = (
            contract_map[self.chain]['datastore']['contract_address']
        )

        output_list = []
        mapper = []
        for market_key in self._markets.info:
            index_token_address = self._markets.get_index_token_address(
                market_key
            )

            if (
                index_token_address ==
                "0x0000000000000000000000000000000000000000"
            ):
                continue

            self._get_token_addresses(market_key)
            output = self._get_oracle_prices(
                market_key,
                index_token_address,
            )

            output_list.append([output])
            mapper.append(self._markets.get_market_symbol(market_key))

        threaded_output = execute_threading(output_list)

        borrow_apr_dict = {
            "long": {
            },
            "short": {
            }
        }

        for key, output in zip(mapper, threaded_output):
            borrow_apr_dict["long"][key] = (
                output[1] / 10 ** 28
            ) * 3600
            borrow_apr_dict["short"][key] = (
                output[2] / 10 ** 28
            ) * 3600

            self.log.info(
                (
                    "{}\nLong Borrow Hourly Rate: -{:.5f}%\n"
                    "Short Borrow Hourly Rate: -{:.5f}%\n"
                ).format(
                    key,
                    borrow_apr_dict["long"][key],
                    borrow_apr_dict["short"][key]
                )
            )
        return borrow_apr_dict


if __name__ == "__main__":
    data = GetBorrowAPR(chain='arbitrum').get_borrow_apr(to_csv=False)

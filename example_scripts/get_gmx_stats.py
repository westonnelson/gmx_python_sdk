from utils import _set_paths

_set_paths()

from gmx_python_sdk.scripts.v2.get.get_available_liquidity import (
    GetAvailableLiquidity
)
from gmx_python_sdk.scripts.v2.get.get_borrow_apr import GetBorrowAPR
from gmx_python_sdk.scripts.v2.get.get_claimable_fees import GetClaimableFees
from gmx_python_sdk.scripts.v2.get.get_contract_balance import (
    GetPoolTVL as ContractTVL
)
from gmx_python_sdk.scripts.v2.get.get_funding_apr import GetFundingFee
from gmx_python_sdk.scripts.v2.get.get_gm_prices import GMPrices
from gmx_python_sdk.scripts.v2.get.get_markets import Markets
from gmx_python_sdk.scripts.v2.get.get_open_interest import OpenInterest
from gmx_python_sdk.scripts.v2.get.get_oracle_prices import OraclePrices
from gmx_python_sdk.scripts.v2.get.get_pool_tvl import GetPoolTVL


class GetGMXv2Stats:

    def __init__(self, to_json, to_csv):

        self.to_json = to_json
        self.to_csv = to_csv

    def get_available_liquidity(self, chain):

        return GetAvailableLiquidity(
            chain=chain
        ).get_data(
            to_csv=self.to_csv,
            to_json=self.to_json
        )

    def get_borrow_apr(self, chain):

        return GetBorrowAPR(
            chain=chain
        ).get_data(
            to_csv=self.to_csv,
            to_json=self.to_json
        )

    def get_claimable_fees(self, chain):

        return GetClaimableFees(
            chain=chain
        ).get_data(
            to_csv=self.to_csv,
            to_json=self.to_json
        )

    def get_contract_tvl(self, chain):

        return ContractTVL(
            chain=chain
        ).get_pool_balances(
            to_json=self.to_json
        )

    def get_funding_apr(self, chain):

        return GetFundingFee(
            chain=chain
        ).get_funding_apr(
            to_csv=self.to_csv,
            to_json=self.to_json
        )

    def get_gm_price(self, chain):

        return GMPrices(
            chain=chain
        ).get_price_traders(
            to_csv=self.to_csv,
            to_json=self.to_json
        )

    def get_available_markets(self, chain):

        return Markets(
            chain=chain
        ).get_available_markets()

    def get_open_interest(self, chain):

        return OpenInterest(
            chain=chain
        ).get_data(
            to_csv=self.to_csv,
            to_json=self.to_json
        )

    def get_oracle_prices(self, chain):

        return OraclePrices(
            chain=chain
        ).get_recent_prices()

    def get_pool_tvl(self, chain):

        return GetPoolTVL(
            chain=chain
        ).get_pool_balances(
            to_csv=self.to_csv,
            to_json=self.to_json
        )


if __name__ == "__main__":

    to_json = False
    to_csv = False
    chain = "arbitrum"

    stats_object = GetGMXv2Stats(
        to_json=to_json,
        to_csv=to_csv
    )

    liquidity = stats_object.get_available_liquidity(chain=chain)
    borrow_apr = stats_object.get_borrow_apr(chain=chain)
    claimable_fees = stats_object.get_claimable_fees(chain=chain)
    contract_tvl = stats_object.get_contract_tvl(chain=chain)
    funding_apr = stats_object.get_funding_apr(chain=chain)
    gm_prices = stats_object.get_gm_price(chain=chain)
    markets = stats_object.get_available_markets(chain=chain)
    open_interest = stats_object.get_open_interest(chain=chain)
    oracle_prices = stats_object.get_oracle_prices(chain=chain)
    pool_tvl = stats_object.get_pool_tvl(chain=chain)

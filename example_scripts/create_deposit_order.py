from utils import _set_paths

_set_paths()

from gmx_python_sdk.scripts.v2.order.create_deposit_order import DepositOrder
from gmx_python_sdk.scripts.v2.liquidity_argument_parser import LiquidityArgumentParser


parameters = {
    "chain": "arbitrum",
    "market_token_symbol": "BTC",
    "long_token_symbol": "BTC",
    "short_token_symbol": "USDC",
    "long_token_usd": 18,
    "short_token_usd": 0
}

output = LiquidityArgumentParser(is_deposit=True).process_parameters_dictionary(parameters)

DepositOrder(
    chain=output["chain"],
    market_key=output["market_key"],
    initial_long_token=output["long_token_address"],
    initial_short_token=output["short_token_address"],
    long_token_amount=output["long_token_amount"],
    short_token_amount=output["short_token_amount"]
)

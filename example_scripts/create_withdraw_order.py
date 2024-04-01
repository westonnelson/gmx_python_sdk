from utils import _set_paths

_set_paths()

from gmx_python_sdk.scripts.v2.order.create_withdrawal_order import (
    WithdrawOrder
)
from gmx_python_sdk.scripts.v2.liquidity_argument_parser import (
    LiquidityArgumentParser
)


parameters = {
    "chain": "arbitrum",
    "market_token_symbol": "BTC",
    "out_token_symbol": "USDC",
    "gm_amount": 12.42
}

output = LiquidityArgumentParser(
    is_withdrawal=True
).process_parameters_dictionary(
    parameters
)

WithdrawOrder(
    chain=output["chain"],
    market_key=output["market_key"],
    out_token=output["out_token_address"],
    gm_amount=output["gm_amount"]
)

from utils import _set_paths

_set_paths()

from gmx_python_sdk_2.v2.order_argument_parser import OrderArgumentParser
from gmx_python_sdk_2.v2.create_increase_order import IncreaseOrder

from gmx_python_sdk_2.v2.gmx_utils import Config

# or omit argument to save/load config in base directory
config_obj = Config()

# Try load config, will create base template if it doesnt exist
new_config_dict = config_obj.load_config()
new_config_dict['private_key'] = "set_private_key_here"
new_config_dict['user_wallet_address'] = "set_wallet_address_here"

# Set config file
config_obj.set_config(new_config_dict)


parameters = {
    "chain": 'arbitrum',

    # the market you want to trade on
    "index_token_symbol": "ETH",

    # token to use as collateral. Start token swaps into collateral token
    # if different
    "collateral_token_symbol": "ETH",

    # the token to start with - WETH not supported yet
    "start_token_symbol": "ETH",

    # True for long, False for short
    "is_long": False,

    # Position size in in USD
    "size_delta_usd": 10,

    # if leverage is passed, will calculate number of tokens in
    # start_token_symbol amount
    "leverage": 1,

    # as a decimal ie 0.003 == 0.3%
    "slippage_percent": 0.003
}


order_parameters = OrderArgumentParser(
    is_increase=True
).process_parameters_dictionary(
    parameters
)

order = IncreaseOrder(
    chain=order_parameters['chain'],
    market_key=order_parameters['market_key'],
    collateral_address=order_parameters['start_token_address'],
    index_token_address=order_parameters['index_token_address'],
    is_long=order_parameters['is_long'],
    size_delta=order_parameters['size_delta'],
    initial_collateral_delta_amount=(
        order_parameters['initial_collateral_delta']
    ),
    slippage_percent=order_parameters['slippage_percent'],
    swap_path=order_parameters['swap_path']
)


# After we are done with operations, set private_key and
# user_wallet_address to None so they are not saved locally
new_config_dict['private_key'] = None
new_config_dict['user_wallet_address'] = None

# set config file
config_obj.set_config(new_config_dict)

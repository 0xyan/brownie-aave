from brownie import config, network, interface
from scripts.helpful_scripts import get_account
from scripts.get_weth import get_weth
from web3 import Web3

AMOUNT = Web3.toWei(0.1, "ether")


def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in ["mainnet-fork"]:
        # depositing eth to weth contract
        get_weth()
    print("got some weth")

    lending_pool = get_lending_pool()
    print(lending_pool)

    approve_tx = approve_erc20(AMOUNT, lending_pool.address, erc20_address, account)

    tx = lending_pool.deposit(
        erc20_address, AMOUNT, account.address, 0, {"from": account}
    )
    tx.wait(1)
    print("deposited")


def approve_erc20(amount, spender, erc20_address, account):
    print("approving erc20")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("approved!")


def get_lending_pool():
    lending_pool_address = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    # calling function to get lending pool address
    lending_pool_address = lending_pool_address.getLendingPool({"from": get_account()})
    # getting the contract
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool

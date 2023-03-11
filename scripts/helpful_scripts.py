from brownie import accounts, network, config

LOCAL_NETWORKS = ["development", "ganache-local", "mainnet-fork"]


def get_account():
    if network.show_active() in LOCAL_NETWORKS:
        account = accounts[0]
    else:
        account = accounts.add(config["wallets"]["from_key"])
    return account

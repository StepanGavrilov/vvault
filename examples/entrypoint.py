from pathlib import Path

from vvault.vault import VaultMaster


def first_start():
    # 1. creating vvault instance,
    # check connection to vault service.

    vvault = VaultMaster(
        url="http://localhost:8200", auth_methods=("approle", "userpass")
    )

    # 2. starting VaultMaster
    # checks on this step
    # init and sealed statuses
    keys = vvault.start(
        root_token=None, unseal_keys=None, config_file=Path("services.yaml")
    )
    print(f"keys: {keys}")


def ordinary_start():
    # 1. creating vvault instance,
    # check connection to vault service.

    vvault = VaultMaster(
        url="http://localhost:8200", auth_methods=("approle", "userpass")
    )

    # 2. starting VaultMaster
    # checks on this step
    # init and sealed statuses
    keys = vvault.start(
        root_token="hvs.c3Ijt6ahSSSmg0AGBA2pze5C",
        unseal_keys=(
            "51a46125d0462d796057a33f96d8787fc90d0003c82b4954431f112e494b43b9a5",
            "402d43f17048954c55213df52bae04630a24930d504e79d3eabce79e996fc0e006",
            "4edefc25ec69f786a5bd678af63f8f00e80064de426739ec974b7322cd441ec46a",
        ),
        config_file=Path("services.yaml"),
        update=True,
    )


if __name__ == "__main__":
    ordinary_start()

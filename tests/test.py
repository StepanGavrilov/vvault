from pathlib import Path
from unittest import TestCase

from vvault.vault import VaultMaster


class VaultTest(TestCase):
    vault_master: VaultMaster
    secure_data: dict

    @classmethod
    def setUpClass(cls) -> None:
        import time

        time.sleep(6)
        cls.secure_data = {}
        cls.vault_master = VaultMaster(
            url="http://vault:8200", auth_methods=("approle", "userpass")
        )

    def test_01_start_no_config(self):
        with self.assertRaises(
            FileNotFoundError, msg="Config file exists (check for negative)"
        ):
            self.vault_master.start(config_file=Path("no-file.yaml"))

    def test_02_start_no_valid_config_file(self):
        with self.assertRaises(AttributeError, msg="Must be not correct yaml file."):
            self.vault_master.start(config_file=Path("tests/services_no_valid.yaml"))

    def test_03_first_start(self):
        self.secure_data.update(
            self.vault_master.start(
                config_file=Path("tests/services2test.yaml"), root_token=None
            )
        )
        self.assertIsInstance(
            self.vault_master.config,
            dict,
            f"Parsed config must be dict: {type(self.vault_master.config)}",
        )
        required_keys = ["environments", "policy", "acl"]
        self.assertListEqual(
            sorted(required_keys),
            sorted(list(self.vault_master.config.keys())),
            f"Structure of config file not correct, required: {required_keys},"
            f" in config: {list(self.vault_master.config.keys())}",
        )

        self.assertTrue(self.vault_master.initialized, "Must be initialized.")
        self.assertFalse(self.vault_master.sealed, "Must be unsealed.")
        required_auth_methods = {"approle/", "userpass/"}
        actual_auth_methods = set(self.vault_master.auth_methods)
        self.assertTrue(
            required_auth_methods.issubset(actual_auth_methods),
            f"Required auth methods: {required_auth_methods} actual: {actual_auth_methods}",
        )
        correct_policy_response = {
            "keys": ["default", "prod/db_access", "dev/db_access", "root"],
            "policies": ["default", "prod/db_access", "dev/db_access", "root"],
            "lease_id": "",
            "renewable": False,
            "lease_duration": 0,
            "data": {
                "keys": ["default", "prod/db_access", "dev/db_access", "root"],
                "policies": ["default", "prod/db_access", "dev/db_access", "root"],
            },
            "wrap_info": None,
            "warnings": None,
            "auth": None,
        }
        vault_polices = self.vault_master.polices
        vault_polices.pop("request_id")
        self.assertDictEqual(
            correct_policy_response, vault_polices, "Policies not correct"
        )

        secret = self.vault_master.read_secret(area="dev", context="db/config")
        self.assertDictEqual(
            {
                "POSTGRES_USER": "postgres",
                "POSTGRES_BD": "postgres",
                "POSTGRES_PASSWORD": "1",
            },
            secret,
            "Current secrets don't match",
        )
        list_of_secrets = self.vault_master.list_secrets(area="dev", context=None)
        self.assertListEqual(["db/"], list_of_secrets, "List of Secrets don't match")

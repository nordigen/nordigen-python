from unittest import mock
from unittest.mock import patch

import pytest

from nordigen.api import AccountApi


class TestAccountApi:
    """Test Account api"""

    account_id = "1d2b827b-9ca2-4adb-b4c3-0deb76a0ac50"
    iban = "LT213250024324970797"

    @pytest.fixture(scope="class")
    def account(self, client) -> AccountApi:
        """
        Create Account api instance.

        Args:
            client (NordigenClient): return NordigenClient instance

        Returns:
            AccountApi: return AccountApi instance
        """
        return AccountApi(client=client, id=self.account_id)

    def test_get_account_metadata(self, account: AccountApi):
        """
        Test get account metadata.

        Args:
            account (AccountApi): AccountApi instance
        """
        with patch("requests.get") as mock_request:
            mock_request.return_value.json.return_value = {
                "id": self.account_id,
                "created": "2022-02-22T10:37:34.556Z",
                "last_accessed": "2022-02-22T10:37:34.556Z",
                "iban": self.iban,
            }
            response = account.get_metadata()
            assert response["id"] == self.account_id

    def test_get_balances(self, account: AccountApi):
        """
        Test get balances of an account.

        Args:
            account (AccountApi): AccountApi instance
        """
        with patch("requests.get") as mock_request:
            mock_request.return_value.json.return_value = {
                "balances": [
                    {
                        "balanceAmount": {
                            "amount": "657.49",
                            "currency": "EUR",
                        },
                        "balanceType": "EUR",
                    }
                ]
            }
            response = account.get_balances()
            print(response)
            assert response["balances"][0]["balanceType"] == "EUR"

    def test_get_details(self, account: AccountApi):
        """
        Test get account details.

        Args:
            account (AccountApi): AccountApi instance
        """
        with patch("requests.get") as mock_request:
            mock_request.return_value.json.return_value = {
                "account": {
                    "resourceId": "534252452",
                    "iban": self.iban,
                    "currency": "EUR",
                }
            }
            response = account.get_details()
            assert response["account"]["iban"] == self.iban

    def test_get_transactions(self, account: AccountApi, client):
        """
        Test get account transactions.

        Args:
            account (AccountApi): [description]
        """
        with patch("requests.get") as mock_request:
            mock_request.return_value.json.return_value = {
                "trx": {
                    "booked": [
                        {
                            "trxAmount": {
                                "currency": "EUR",
                                "amount": "328.18",
                            },
                        }
                    ]
                }
            }
            response = account.get_transactions()
            assert (
                response["trx"]["booked"][0]["trxAmount"]["currency"] == "EUR"
            )
            assert (
                mock.call(
                    url=f"{client.base_url}/accounts/{self.account_id}/transactions/",
                    headers=client._headers,
                    params=None,
                )
                in mock_request.call_args_list
            )

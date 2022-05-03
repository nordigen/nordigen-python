from unittest import mock
from unittest.mock import patch

import pytest

from nordigen.api import PremiumAccountApi


class TestPremiumAccountApi:
    """Test Account api"""

    account_id = "1d2b827b-9ca2-4adb-b4c3-0deb76a0ac50"
    iban = "LT213250024324970797"

    @pytest.fixture(scope="class")
    def account(self, client) -> PremiumAccountApi:
        """
        Create Account api instance.

        Args:
            client (NordigenClient): return NordigenClient instance

        Returns:
            PremiumAccountApi: return PremiumAccountApi instance
        """
        return PremiumAccountApi(client=client, id=self.account_id)

    def test_get_account_metadata(self, account: PremiumAccountApi):
        """
        Test get account metadata.

        Args:
            account (PremiumAccountApi): PremiumAccountApi instance
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

    def test_get_balances(self, account: PremiumAccountApi):
        """
        Test get balances of an account.

        Args:
            account (PremiumAccountApi): PremiumAccountApi instance
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
            assert response["balances"][0]["balanceType"] == "EUR"

    def test_get_details(self, account: PremiumAccountApi, client):
        """
        Test get account details.

        Args:
            account (PremiumAccountApi): PremiumAccountApi instance
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

            mock_request.assert_called_with(
                url=f"{client.base_url}/accounts/premium/{self.account_id}/details/",
                headers=client._headers,
                params={},
            )

    def test_get_transactions(self, account: PremiumAccountApi, client):
        """
        Test get account transactions.

        Args:
            account (PremiumAccountApi): [description]
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
            mock_request.assert_called_with(
                url=f"{client.base_url}/accounts/premium/{self.account_id}/transactions/",
                headers=client._headers,
                params={},
            )

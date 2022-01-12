import os
import pytest

from nordigen.api import AccountApi


class TestAccountApi:
    """Test Account api"""

    @pytest.fixture(scope="class")
    def account(self, client) -> AccountApi:
        """
        Create Account api instance.

        Args:
            client (NordigenClient): return NordigenClient instance

        Returns:
            AccountApi: return AccountApi instance
        """
        return AccountApi(client=client, id=os.getenv("ACCOUNT_ID"))

    def test_get_account_metadata(self, account: AccountApi):
        """
        Test get account metadata.

        Args:
            account (AccountApi): [description]
        """
        response = account.get_metadata()
        assert response["id"] == os.getenv("ACCOUNT_ID")

    def test_get_balances(self, account: AccountApi):
        """
        Test get balances of an account.

        Args:
            account (AccountApi): [description]
        """
        response = account.get_balances()
        assert "balances" in response

    def test_get_details(self, account: AccountApi):
        """
        Test get account details.

        Args:
            account (AccountApi): [description]
        """
        response = account.get_details()
        assert response["account"]["iban"] == "LT213250024324970797"

    def test_get_transactions(self, account: AccountApi):
        """
        Test get account transactions.

        Args:
            account (AccountApi): [description]
        """
        response = account.get_transactions()
        assert "transactions" in response

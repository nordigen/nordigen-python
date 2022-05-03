from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Final, Optional

from nordigen.types import AccountBalances
from nordigen.types.http_enums import HTTPMethod
from nordigen.types.types import AccountData, AccountDetails

if TYPE_CHECKING:
    from nordigen import NordigenClient


class AccountApi:
    """
    Account API endpoints to fetch accounts, details, balances and transactions.

    Attributes
    ---------
    client (NordigenClient):
        Injectable NordigenClient object to make an http requests
    id (str):
        account id retrieved from request get_requisition_by_id()

    Returns: None
    """

    __ENDPOINT: Final = "accounts"

    def __init__(self, client: NordigenClient, id: str) -> None:
        self._request = client.request
        self._id: str = id

    def _get(self, endpoint: str, parameters: Optional[Dict] = None):
        """
        Construct get request.

        Args:
            endpoint (str): endpoint

        Returns:
            [type]: [description]
        """
        url = f"{self.__ENDPOINT}/{self._id}/{endpoint}/"
        return self._request(HTTPMethod.GET, f"{url}", parameters)

    def get_metadata(self) -> AccountData:
        """
        Access account metadata.
        Information about the account record, such as the processing status and IBAN.
        Account status is recalculated based on the error count in the latest req.

        Returns:
            AccountData: account metadata
        """
        return self._request(HTTPMethod.GET, f"{self.__ENDPOINT}/{self._id}/")

    def get_balances(self) -> AccountBalances:
        """
        Access account balances.
        Balances will be returned in Berlin Group PSD2 format.

        Returns:
            AccountBalances: account balance data
        """
        return self._get("balances")

    def get_details(self) -> AccountDetails:
        """
        Access account details.
        Account details will be returned in Berlin Group PSD2 format.

        Returns:
            AccountDetails: account details data
        """
        return self._get("details")

    def get_transactions(
        self, date_from: Optional[str] = None, date_to: Optional[str] = None
    ) -> Dict:
        """
        Access account transactions.
        Transactions will be returned in Berlin Group PSD2 format.


        Returns:
            Dict: account transactions details
        """
        date_range = {"date_from": date_from, "date_to": date_to}
        return self._get("transactions", date_range)


class PremiumAccountApi(AccountApi):
    """
    Account API endpoints to fetch accounts, details, balances and transactions.
    Uses premium endpoints.

    Attributes
    ---------
    client (NordigenClient):
        Injectable NordigenClient object to make an http requests
    id (str):
        account id retrieved from request get_requisition_by_id()

    Returns: None
    """

    __PREMIUM_ENDPOINT: Final = "accounts/premium"

    def _get(self, endpoint: str, parameters: Optional[Dict] = None):
        """
        Construct get request.

        Args:
            endpoint (str): endpoint

        Returns:
            [type]: [description]
        """
        url = f"{self.__PREMIUM_ENDPOINT}/{self._id}/{endpoint}/"
        return self._request(HTTPMethod.GET, f"{url}", parameters)

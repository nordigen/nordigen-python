from __future__ import annotations

from typing import TYPE_CHECKING, Final, Optional

from nordigen.types.http_enums import HTTPMethod

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
        self.__request = client.request
        self.__id: str = id

    def __get(self, endpoint: str, parameters: dict = {}):
        """
        Construct get request.

        Args:
            endpoint (str): endpoint

        Returns:
            [type]: [description]
        """
        url = f"{self.__ENDPOINT}/{self.__id}/{endpoint}/"
        return self.__request(HTTPMethod.GET, f"{url}", parameters)


    def __getPremium(self, path, parameters: dict = {}):
        """
        Construct get request for premium endpoints

        Args:
            path (_type_): _description_
            parameters (dict, optional): _description_. Defaults to {}.

        Returns:
            _type_: _description_
        """
        url = f'{self.__ENDPOINT}/premium/{self.__id}/{path}'
        return self.__request(HTTPMethod.GET, f"{url}", parameters)

    def get_metadata(self) -> dict:
        """
        Access account metadata.
        Information about the account record, such as the processing status and IBAN.
        Account status is recalculated based on the error count in the latest req.

        Returns:
            AccountData: account metadata
        """
        return self.__request(
            HTTPMethod.GET, f"{self.__ENDPOINT}/{self.__id}/"
        )

    def get_balances(self) -> dict:
        """
        Access account balances.
        Balances will be returned in Berlin Group PSD2 format.

        Returns:
            dict: dictionary with balances
        """
        return self.__get("balances")

    def get_details(self) -> dict:
        """
        Access account details.
        Account details will be returned in Berlin Group PSD2 format.

        Returns:
            dict: dictionary with account details
        """
        return self.__get("details")

    def get_transactions(
        self,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None
    ) -> dict:
        """
        Access account transactions.
        Transactions will be returned in Berlin Group PSD2 format.


        Returns:
            Dict: account transactions details
        """
        date_range = {
            "date_from": date_from,
            "date_to": date_to
        }
        return self.__get("transactions", date_range)


    def get_premium_details(self, country: str = "") -> dict:
        """
        Get premium details

        Args:
            country (str, optional): _description_. Defaults to "".

        Returns:
            dict: _description_
        """
        parameters = {
            "country": country
        }
        return self.__getPremium("details", parameters)

    def get_premium_balances(self) -> dict:
        """
        Get premium balances

        Returns:
            dict: balances data
        """
        return self.__getPremium("balances")

    def get_premium_transactions(
        self,
        country: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None
    )  -> dict:
        """
        Get premium transactions

        Args:
            country (Optional[str], optional): country in iso format. Defaults to None.
            date_from (Optional[str], optional): date_from. Defaults to None.
            date_to (Optional[str], optional): date_to. Defaults to None.

        Returns:
            dict: dict with premium transactions
        """
        parameters = {
            "date_from": date_from,
            "date_to": date_to,
            "country": country or "",
        }
        return self.__getPremium("transactions", parameters)

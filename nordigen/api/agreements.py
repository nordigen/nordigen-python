from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Final, List, Union

from nordigen.types.http_enums import HTTPMethod
from nordigen.types.types import AgreementsList, EnduserAgreement

if TYPE_CHECKING:
    from nordigen.client import NordigenClient


class AgreementsApi:
    """
    Agreements api class.

    Attributes
    -------
    client (NordigenClient): Injectable NordigenClient object to make an http requests
    institution_id (str): institution_id (bank id) from institutions response.
        e.g {"id": "MONZO_MONZGB2L"}

    Returns: None
    """

    __ENDPOINT: Final = "agreements/enduser"

    def __init__(self, client: NordigenClient) -> None:
        self.__client = client

    def create_agreement(
        self,
        institution_id: str,
        max_historical_days: int = 90,
        access_valid_for_days: int = 90,
        access_scope: Union[None, List[str]] = None,
    ) -> EnduserAgreement:
        """
        Create end user agreement.

        Args:
            institution (str): Institution id.
            max_historical_days (int, optional): Length of the transaction history. Defaults to 90.
            access_valid_for_days (int, optional): access valid for days.
            access_scope (List[str], optional):
                access scope for account, by default provides access to balances, details, transactions.
                Defaults to [ "balances", "details", "transactions" ].

        Returns:
            EnduserAgreement: Enduser agreement json object
        """
        access_scope = access_scope or ["balances", "details", "transactions"]
        payload = {
            "max_historical_days": max_historical_days,
            "access_valid_for_days": access_valid_for_days,
            "access_scope": access_scope,
            "institution_id": institution_id,
        }

        return self.__client.request(
            HTTPMethod.POST, f"{self.__ENDPOINT}/", payload
        )

    def get_agreements(
        self, limit: int = 100, offset: int = 0
    ) -> AgreementsList:
        """
        Get list of agreements.

        Args:
                 a unique end-user ID of someone who's using your services, it has to be unique within your solution.
                 Usually, it's UUID
            limit (int, optional): number of results to return per page. Defaults to 100.
            offset (int, optional): the initial index from which to return the results. Defaults to 0.

        Returns:
            AgreementsList: json object with enduser agreements
        """
        params = {"limit": limit, "offset": offset}
        return self.__client.request(
            HTTPMethod.GET, f"{self.__ENDPOINT}/", params
        )

    def get_agreement_by_id(self, agreement_id: str) -> EnduserAgreement:
        """
        Get agreement by agreement id.

        Args:
            agreement_id (str): id id from create_agreement response
        Returns:
            EnduserAgreement: JSON object with specific enduser agreements
        """
        return self.__client.request(
            HTTPMethod.GET, f"{self.__ENDPOINT}/{agreement_id}"
        )

    def delete_agreement(self, agreement_id: str) -> Dict:
        """
        Delete End User Agreement by id.

        Args:
            agreement_id (str): A UUID string identifying this end user agreement.

        Returns:
            Dict: Dictionary with deleted agreement
        """
        return self.__client.request(
            HTTPMethod.DELETE, f"{self.__ENDPOINT}/{agreement_id}"
        )

    def accept_agreement(
        self, agreement_id: str, ip: str, user_agent: str
    ) -> Dict:
        """
        Accept an end-user agreement via the API.

        Args:
            agreement_id (str): A UUID string identifying this end user agreement.
            ip (str): IP address of the client
            user_agent (str): [User Agent of the browser
        Returns:
            Dict: Dict with information on accepted agreement
        """
        payload = {"user_agent": user_agent, "ip_address": ip}
        return self.__client.request(
            HTTPMethod.PUT,
            f"{self.__ENDPOINT}/{agreement_id}/accept/",
            payload,
        )

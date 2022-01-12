from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Final, List

from nordigen.types.http_enums import HTTPMethod
from nordigen.types.types import Requisition

if TYPE_CHECKING:
    from nordigen import NordigenClient


class RequisitionsApi:
    """
    Requsition API class related to requisitions.

    Attributes
    ---------
    client(NordigenClient): Injectable NordigenClient object to make an http requests

    Returns: None
    """

    ENDPOINT: Final = "requisitions"

    def __init__(self, client: NordigenClient) -> None:
        self.__client = client

    def get_requisitions(
        self, limit: int = 100, offset: int = 0
    ) -> Requisition:
        """
        Get list of requisitions.

        Args:
            limit (int, optional): number of results to return per page. Defaults to 100.
            offset (int, optional): the initial index from which to return the results. Defaults to 0.

        Returns:
            Requisition: json response with requisition details
        """
        payload = {"limit": limit, "offset": offset}
        return self.__client.request(
            HTTPMethod.GET, f"{self.ENDPOINT}/", payload
        )

    def create_requisition(
        self,
        redirect_uri: str,
        reference_id: str,
        institution_id: str = None,
        agreement: List[str] = None,
        user_language: str = None,
    ) -> Requisition:
        """
        Create requisition for creating links and retrieving accounts.

        Args:
            redirect_uri (str): application redirect url
            reference_id (str): additional layer of unique ID defined by you
            enduser_id (str): a unique end-user ID of someone who's using your services, usually it's a UUID
            agreements (List[str] or str optional): agreement is provided as a string.
            user_language (str, optional): to enforce a language for all end user steps hosted
                by Nordigen passed as a two-letter country code. Defaults to None

        Returns:
            Requisition: [description]
        """
        payload = {
            "redirect": redirect_uri,
            "reference": reference_id,
            "institution_id": institution_id,
        }

        if user_language:
            payload["user_language"] = user_language

        if agreement:
            payload["agreement"] = agreement

        return self.__client.request(
            HTTPMethod.POST, f"{self.ENDPOINT}/", payload
        )

    def get_requisition_by_id(self, requisition_id: str) -> Requisition:
        """
        Get list of requisitions.

        Args:
            requisition_id (str): A UUID string identifying this requisition.
        Returns:
            Requisition: account details
        """
        return self.__client.request(
            HTTPMethod.GET, f"{self.ENDPOINT}/{requisition_id}/"
        )

    def delete_requisition(self, requisition_id: str) -> Dict:
        """
        Delete requisition by id.

        Args:
            requisition_id (str): A UUID string identifying this requisition.

        Returns: Dict that consist confirmation message that requisition has been deleted
        """
        return self.__client.request(
            HTTPMethod.DELETE, f"{self.ENDPOINT}/{requisition_id}"
        )

from __future__ import annotations

from typing import TYPE_CHECKING, Final, List, Optional

from nordigen.types import Institutions
from nordigen.types.http_enums import HTTPMethod

if TYPE_CHECKING:
    from nordigen import NordigenClient


class InstitutionsApi:
    """
    Institution API class. Used to fetch information about bank.

    Attributes
    ---------
    client(NordigenClient): Injectable NordigenClient object to make an http requests

    Returns: None
    """

    ENDPOINT: Final = "aspsps"

    def __init__(self, client: NordigenClient) -> None:
        self.__request = client.request
        self.ENDPOINT = "institutions"

    def get_institutions(self, country: Optional[str] = None) -> List[Institutions]:
        """
        Get all available Institutions (banks) in a given country or for all countries if
        country isn't specified.

        Args:
            country (str, optional): Two-character country code

        Returns:
            List[Institutions]: List of institutions in a given country
        """
        url = self.ENDPOINT
        if country:
            url = f"{self.ENDPOINT}/?country={country}"

        return self.__request(
            HTTPMethod.GET, url
        )

    def get_institution_by_id(self, id: str) -> Institutions:
        """
        Get details about specific institution by its id.

        Args:
            id (str): institution id (bank id)

        Returns:
            Institutions: Institutions json object
        """
        return self.__request(HTTPMethod.GET, f"{self.ENDPOINT}/{id}/")

    def get_institution_id_by_name(
        self, country: str, institution: str
    ) -> str:
        """
        Get institution id by institution name.

        Args:
            country (str): Two-character country code
            institution (str): Institution name (ex: Revolut)

        Raises:
            ValueError: If institution with given name is not found

        Returns:
            str: Institution id
        """
        institutions = self.get_institutions(country)

        for bank in institutions:
            if institution.lower() in bank["name"].lower():
                return bank["id"]

        raise ValueError(f"Institution: {institution} is not found")

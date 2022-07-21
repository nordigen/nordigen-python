import json
from typing import Dict, Final, Optional

import requests
from requests.models import HTTPError, Response

from nordigen.api import (
    AccountApi,
    AgreementsApi,
    InstitutionsApi,
    RequisitionsApi,
)
from nordigen.utils.filter import DataFilter
from nordigen.types.http_enums import HTTPMethod
from nordigen.types.types import RequisitionDto, TokenType


class NordigenClient:
    """
    Class to initialize new Client.

    Attributes
    ---------
    secret_key (str): Generated secret_key
    secret_id (str): Generated secret_id
    """

    __ENDPOINT: Final = "token"

    def __init__(
        self,
        secret_key: str,
        secret_id: str,
        timeout: int = 10,
    ) -> None:
        self.secret_key = secret_key
        self.secret_id = secret_id
        self.base_url = "https://ob.nordigen.com/api/v2"
        self._headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Nordigen-Python-v2",
        }
        self._token: Optional[str] = None
        self.institution = InstitutionsApi(client=self)
        self.requisition = RequisitionsApi(client=self)
        self.agreement = AgreementsApi(client=self)
        self.data_filter = DataFilter()
        self._timeout = timeout

    def account_api(self, id: str) -> AccountApi:
        """
        Create Account api instance.

        Args:
            id (str): account id

        Returns:
            AccountApi: Account instance
        """
        return AccountApi(client=self, id=id)

    @property
    def token(self):
        """
        Get token.

        Returns:
            str: return token
        """
        return self._token

    @token.setter
    def token(self, value: str):
        """
        Set token.

        Args:
            value (str): token
        """
        self._token = value
        self._headers["Authorization"] = f"Bearer {value}"

    def generate_token(self) -> TokenType:
        """
        Generate new access token.

        Returns:
            TokenType: Dict that contains access and refresh token
        """
        payload = {"secret_key": self.secret_key, "secret_id": self.secret_id}
        response = self.request(
            HTTPMethod.POST,
            f"{self.__ENDPOINT}/new/",
            payload,
            self._headers,
        )

        self.token = response["access"]
        return response

    def exchange_token(self, refresh_token: str) -> TokenType:
        """
        Exchange refresh token for access token.

        Args:
            refresh_token (str): refresh token

        Returns:
            TokenType: Dict that contains access and refresh token
        """
        payload = {"refresh": refresh_token}
        response = self.request(
            HTTPMethod.POST,
            f"{self.__ENDPOINT}/refresh/",
            payload,
            self._headers,
        )

        self.token = response["access"]
        return response

    def request(
        self,
        method: HTTPMethod,
        endpoint: str,
        data: Dict = None,
        headers: Dict = None,
    ) -> Response:
        """
        Request wrapper for Nordigen library.

        Args:
            method (HTTPMethod): Supports GET, POST, PUT, DELETE
            endpoint (str): [endpoint url
            data (Dict, optional): body or parameters that need to be sent alongside with the request.
                Defaults to {}.

        Raises:
            Exception: HTTP method is not supported
            HTTPError: HTTP error with status code

        Returns:
            Response: JSON Response object
        """
        request_meta = {
            "url": f"{self.base_url}/{endpoint}",
            "headers": headers if headers else self._headers,
        }

        data = self.data_filter.filter_payload(data)

        if method == HTTPMethod.GET:
            response = requests.get(**request_meta, params=data, timeout=self._timeout)
        elif method == HTTPMethod.POST:
            response = requests.post(**request_meta, data=json.dumps(data), timeout=self._timeout)
        elif method == HTTPMethod.PUT:
            response = requests.put(**request_meta, data=json.dumps(data), timeout=self._timeout)
        elif method == HTTPMethod.DELETE:
            response = requests.delete(**request_meta, params=data, timeout=self._timeout)
        else:
            raise Exception(f'Method "{method}" is not supported')

        if response.ok:
            return response.json()

        raise HTTPError(
            {"response": response.json(), "status": response.status_code}
        )

    def initialize_session(
        self,
        redirect_uri: str,
        institution_id: str,
        reference_id: str,
        max_historical_days: int = 90,
        access_valid_for_days: int = 90,
    ) -> RequisitionDto:
        """
        Factory method that creates authorization in a specific institution
        and are responsible for the following steps:
            * Creates agreement
            * Creates requisition

        Returns:
            Dict[str]: link to initiate authorization with bank and requisition_id
        """
        # Create agreement
        agreement = self.agreement.create_agreement(
            max_historical_days=max_historical_days,
            access_valid_for_days=access_valid_for_days,
            institution_id=institution_id,
        )

        requisition_dict = {
            "redirect_uri": redirect_uri,
            "reference_id": reference_id,
            "institution_id": institution_id,
            "agreement": agreement["id"],
        }

        # Create requisition
        requisition = self.requisition.create_requisition(**requisition_dict)

        return RequisitionDto(
            link=requisition["link"], requisition_id=requisition["id"]
        )

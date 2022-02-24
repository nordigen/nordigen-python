import json
from unittest import mock
from unittest.mock import patch

import pytest

from nordigen.api import AgreementsApi
from nordigen.nordigen import NordigenClient

from .mocks import generate_mock


class TestAgreementApi:

    enduser_id = "1234567"
    institution_id = "REVOLUT_REVOGB21"
    agreement_id = "4bbf9b01-6c9e-431d-bfc6-11242429e991"

    @pytest.fixture(scope="class")
    def agreement(self, client) -> AgreementsApi:
        """Returns Agreement instance."""
        return AgreementsApi(client=client)

    def test_get_agreement_by_id(self, agreement: AgreementsApi):
        """
        Test get list of agreements by id.

        Args:
            agreement (AgreementsApi): AgreementsApi instance
        """
        with patch("requests.get") as mocked_request:
            mocked_request.return_value.json.return_value = generate_mock(
                self.agreement_id
            )
            response = agreement.get_agreement_by_id(
                agreement_id=self.agreement_id
            )
            assert response["results"][1]["id"] == self.agreement_id

    def test_delete_agreement(self, agreement: AgreementsApi):
        """
        Test delete agreement by id.

        Args:
            agreement (AgreementsApi): AgreementsApi instance
        """
        with patch("requests.delete") as mock_request:
            mock_request.return_value.json.return_value = {
                "summary": "End User Agreement deleted"
            }
            response = agreement.delete_agreement(
                agreement_id=self.agreement_id
            )
            assert response["summary"] == "End User Agreement deleted"

    def test_accept_agreement(self, agreement: AgreementsApi):
        """
        Test accept end user agreement.

        Args:
            agreemen (AgreementsApi): AgreementsApi instance
        """
        with patch("requests.put") as mock_request:
            mock_request.return_value.json.return_value = {
                "id": self.agreement_id,
                "accepted": True,
            }
            response = agreement.accept_agreement(
                user_agent="Chrome",
                ip="127.0.0.1",
                agreement_id=self.agreement_id,
            )
            assert response["id"] == self.agreement_id

    def test_create_agreement(
        self, agreement: AgreementsApi, client: NordigenClient
    ):
        """
        Test create agreement.

        Args:
            agreement (AgreementsApi): Agreement instance
            client: (NordigenClient): NordigenClient instance
        """
        payload = {
            "max_historical_days": 90,
            "access_valid_for_days": 90,
            "access_scope": ["balances", "details", "transactions"],
            "institution_id": self.institution_id,
        }
        with patch("requests.post") as mock_request:
            mock_request.return_value.json.return_value = {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "created": "2022-02-22T10:20:10.977Z",
                "max_historical_days": 90,
                "access_valid_for_days": 90,
                "institution_id": self.institution_id,
            }
            response = agreement.create_agreement(self.institution_id)
            assert response["institution_id"] == self.institution_id
            assert "enduser_id" not in response
            assert (
                mock.call(
                    url=f"{client.base_url}/agreements/enduser/",
                    headers=client._headers,
                    data=json.dumps(payload),
                )
                in mock_request.call_args_list
            )

    def test_get_agreements(
        self, agreement: AgreementsApi, client: NordigenClient
    ):
        """
        Test get agreements.

        Args:
            agreement (AgreementsApi): Agreement instance
            client: (NordigenClient): NordigenClient instance
        """
        with patch("requests.get") as mock_request:
            mock_request.return_value.json.return_value = generate_mock(
                self.agreement_id
            )
            response = agreement.get_agreements()
            assert response["results"][1]["id"] == self.agreement_id
            assert mock.call(
                url=f"{client.base_url}/agreements/enduser/",
                headers=client._headers,
                params={"limit": 100, "offset": 0},
            )

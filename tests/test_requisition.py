from unittest import mock
from unittest.mock import patch

import pytest

from nordigen.api import RequisitionsApi
from nordigen.nordigen import NordigenClient

from .mocks import generate_mock


class TestRequisitionApi:
    """Test Requisition api."""

    enduser_id = "1234567"
    redirect_uri = "https://ob.nordigen.com"
    institution_id = "REVOLUT_REVOGB21"
    requisition_id = "d49dffbb-01dc-498c-a674-8cb725aad14a"

    @pytest.fixture(scope="class")
    def requisition(self, client) -> RequisitionsApi:
        """Returns Agreement instance."""
        return RequisitionsApi(client=client)

    def test_get_requisitions(
        self, requisition: RequisitionsApi, client: NordigenClient
    ):
        """
        Test get requisition.

        Args:
            requisition (RequisitionsApi): Requisition instance
            client (NordigenClient): NordigenClient instance
        """
        with patch("requests.get") as mock_request:
            mock_request.return_value.json.return_value = generate_mock(
                self.requisition_id
            )
            response = requisition.get_requisitions()

            assert len(response["results"]) == 2
            assert (
                response["results"][0]["id"]
                == "3fa85f64-5717-4562-b3fc-2c963f66afa6"
            )
            assert (
                mock.call(
                    url=f"{client.base_url}/requisitions/",
                    headers=client._headers,
                    params={"limit": 100, "offset": 0},
                )
                in mock_request.call_args_list
            )

    def test_delete_requisition(self, requisition: RequisitionsApi):
        """
        Test delete requisition by id.

        Args:
            requisition (RequisitionsApi): Requisition instance
        """
        with patch("requests.delete") as mock_request:
            mock_request.return_value.json.return_value = {
                "summary": "Requisition deleted"
            }
            response = requisition.delete_requisition(
                requisition_id=self.requisition_id
            )
            assert response["summary"] == "Requisition deleted"

    def test_get_requisition_by_id(self, requisition: RequisitionsApi):
        """
        Test get requisition by id for api v2.

        Args:
            requisition (RequisitionsApi): Requisition instance
        """
        with patch("requests.get") as mock_request:
            mock_request.return_value.json.return_value = generate_mock(
                self.requisition_id
            )
            response = requisition.get_requisition_by_id(
                requisition_id=self.requisition_id
            )
            assert response["results"][1]["id"] == self.requisition_id

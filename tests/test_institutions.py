import unittest
from unittest.mock import MagicMock, Mock, patch

from nordigen.api import InstitutionsApi
from nordigen import NordigenClient


class TestInstitutionsAPI(unittest.TestCase):
    """Test Institution API."""

    def setUp(self) -> None:
        self.client = NordigenClient(
            secret_id="my_secret_id", secret_key="my_secret_key"
        )
        self.mock_client = MagicMock(autospec=self.client)
        self.mock_institution = InstitutionsApi(client=self.mock_client)

    @patch.object(InstitutionsApi, "get_institutions")
    def test_get_institutions(self, mock_response: Mock):
        """
        Test get institutions list.

        Args:
            mock_response (Mock): mocked institution object
        """
        mock_response.return_value = [
            {
                "id": "CITADELE_PARXLV22",
                "logo": "https://cdn.nordigen.com/ais/CITADELE_PARXLV22.png",
                "name": "Citadele",
                "transaction_total_days": "730",
            },
            {
                "id": "REVOLUT_REVOGB21",
                "name": "Revolut",
                "bic": "REVOGB21",
                "transaction_total_days": "730",
                "countries": ["GB"],
                "logo": "https://cdn.nordigen.com/ais/REVOLUT_REVOGB21.png",
            },
        ]
        response = self.mock_institution.get_institutions(country="LV")

        assert response[0]["id"] == "CITADELE_PARXLV22"
        assert response[1]["id"] == "REVOLUT_REVOGB21"

    @patch.object(InstitutionsApi, "get_institution_by_id")
    def test_get_institution_by_id(self, mock_response: Mock):
        """
        Test get institution by id.

        Args:
            mock_response (Mock): [description]
        """
        mock_response.return_value = {
            "id": "CITADELE_PARXLV22",
            "logo": "https://cdn.nordigen.com/ais/CITADELE_PARXLV22.png",
            "name": "Citadele",
            "transaction_total_days": "730",
        }

        response = self.mock_institution.get_institution_by_id(
            id="CITADELE_PARXLV22"
        )

        assert response["id"] == "CITADELE_PARXLV22"
        assert response["name"] == "Citadele"

    @patch.object(InstitutionsApi, "get_institution_id_by_name")
    def test_get_institution_id_by_name(self, mock_response: Mock):
        """
        Test get institution id by institution name.

        Args:
            mock_response (Mock): mocked method 'get_institution_id_by_name'
        """
        mock_response.return_value = "REVOLUT_REVOGB21"
        response = self.mock_institution.get_institution_id_by_name(
            institution="Revolut", country="LV"
        )

        assert response == "REVOLUT_REVOGB21"

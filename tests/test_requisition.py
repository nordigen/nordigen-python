import pytest
from uuid import uuid4

from nordigen.api import RequisitionsApi


class TestRequisitionApi:
    """Test Requisition api."""

    enduser_id = "1234567"
    redirect_uri = "https://ob.nordigen.com"
    institution_id = "REVOLUT_REVOGB21"

    @pytest.fixture(scope="class")
    def requisition(self, client) -> RequisitionsApi:
        """Returns Agreement instance."""
        return RequisitionsApi(client=client)

    @pytest.fixture
    def requisition_id(self, requisition: RequisitionsApi):
        """
        Test create requisition.

        Args:
            requisition (RequisitionsApi): Requisition instance
        """
        reference_id = str(uuid4())

        response = requisition.create_requisition(
            redirect_uri=self.redirect_uri,
            reference_id=reference_id,
            institution_id=self.institution_id,
        )
        assert response["institution_id"] == self.institution_id
        assert "link" in response
        yield response["id"]

    def test_get_requisitions(self, requisition: RequisitionsApi):
        """
        Test get requisition.

        Args:
            requisition (RequisitionsApi): Requisition instance
        """
        response = requisition.get_requisitions()
        for requisition in response["results"]:
            if requisition["id"] == self.enduser_id:
                assert requisition["id"] == self.enduser_id
                assert "institution_id" not in requisition

    def test_delete_requisition(
        self, requisition: RequisitionsApi, requisition_id: str
    ):
        """
        Test delete requisition by id.

        Args:
            requisition (RequisitionsApi): Requisition instance
            requisition_id (str): requsition id
        """
        response = requisition.delete_requisition(
            requisition_id=requisition_id
        )
        assert response["summary"] == "Requisition deleted"

    def test_get_requisition_by_id(
        self, requisition: RequisitionsApi, requisition_id: str
    ):
        """
        Test get requisition by id for api v2.

        Args:
            requisition (RequisitionsApi): Requisition instance
            requisition_id (str): requisition id
        """
        response = requisition.get_requisition_by_id(
            requisition_id=requisition_id
        )
        assert response["id"] == requisition_id
        assert "link" in response

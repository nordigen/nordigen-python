import pytest

from nordigen.api import AgreementsApi


class TestAgreementApi:

    enduser_id = "1234567"
    institution_id = "REVOLUT_REVOGB21"

    @pytest.fixture(scope="class")
    def agreement(self, client) -> AgreementsApi:
        """Returns Agreement instance."""
        return AgreementsApi(client=client)

    @pytest.fixture(scope="class")
    def agreement_id(self, agreement: AgreementsApi):
        """
        Test creating agreement and reuse agreement_id accross tests.

        Args:
            agreement (AgreementsApi): AgreementsApi instance
        """
        response = agreement.create_agreement(
            institution_id=self.institution_id
        )
        # assert "institution_id" not in response
        yield response["id"]

    def test_get_agreement_by_id(self, agreement: AgreementsApi, agreement_id):
        """
        Test get list of agreements by id.

        Args:
            agreement (AgreementsApi): AgreementsApi instance
            agreement_id ([type]): agreement id
        """
        response = agreement.get_agreement_by_id(agreement_id=agreement_id)
        assert response["id"] == agreement_id

    def test_delete_agreement(self, agreement: AgreementsApi, agreement_id):
        """
        Test delete agreement by id.

        Args:
            agreement (AgreementsApi): AgreementsApi instance
            agreement_id (str): agreement id
        """
        response = agreement.delete_agreement(agreement_id=agreement_id)
        assert response["summary"] == "End User Agreement deleted"

    @pytest.mark.skip(reason="available only for premium users")
    def test_accept_agreement(self, agreement: AgreementsApi, agreement_id):
        """
        Test accept end user agreement.

        Args:
            agreemen (AgreementsApi): AgreementsApi instance
            agreement_id ([type]): agreement id
        """
        response = agreement.accept_agreement(
            user_agent="Chrome", ip="127.0.0.1", agreement_id=agreement_id
        )
        assert response["id"] == agreement_id

    def test_create_agreement(self, agreement: AgreementsApi):
        """
        Test create agreement.

        Args:
            agreement (AgreementsApi): Agreement instance
        """
        response = agreement.create_agreement(self.institution_id)
        assert response["institution_id"] == self.institution_id
        assert "enduser_id" not in response

    def test_get_agreements(self, agreement: AgreementsApi):
        """
        Test get agreement.

        Args:
            agreement (AgreementsApi): Agreement instance
        """
        response = agreement.get_agreements()["results"]
        for agreement in response:
            if agreement["institution_id"] == self.institution_id:
                assert agreement["institution_id"] == self.institution_id

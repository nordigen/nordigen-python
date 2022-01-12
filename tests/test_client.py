import unittest
from unittest.mock import Mock, patch

from nordigen import NordigenClient


class TestClient(unittest.TestCase):
    """Test Nordigen client."""

    def setUp(self) -> None:
        self.client = NordigenClient(
            secret_id="my_secret_id", secret_key="my_secret_key"
        )

    @patch.object(NordigenClient, "generate_token")
    def test_generate_token(self, mock_generate_token: Mock):
        """Test token generation."""
        payload = {
            "secret_key": self.client.secret_key,
            "secret_id": self.client.secret_id,
        }

        mock_generate_token.return_value = {
            "access": "access token",
            "access_expires": 86400,
            "refresh": "refresh token",
            "refresh_expires": 2592000,
        }
        response = self.client.generate_token(**payload)

        self.assertEqual(86400, response["access_expires"])
        self.assertEqual("access token", response["access"])

    @patch.object(NordigenClient, "exchange_token")
    def test_exchange_token(self, mock_exchange_token: Mock):
        """
        Test token exchange.

        Args:
            mock_exchange_token (Mock): mock exchange token
        """
        mock_exchange_token.return_value = {
            "access": "access token",
            "access_expires": 86400,
        }

        response = self.client.exchange_token(refresh_token="refresh_token")
        self.assertEqual("access token", response["access"])

import json
import unittest
from unittest import mock
from unittest.mock import patch

from nordigen import NordigenClient
from nordigen.types.http_enums import HTTPMethod

from tests.mocks import mocked_token


class TestClient(unittest.TestCase):
    """Test Nordigen client."""

    def setUp(self) -> None:
        """setUp."""
        self.client = NordigenClient(
            secret_id="SECRET_ID",
            secret_key="SECRET_KEY",
        )
        self.url = self.client.base_url

    @patch("requests.post")
    def test_generate_token(self, mock_request):
        """Test token generation."""
        payload = {
            "secret_key": self.client.secret_key,
            "secret_id": self.client.secret_id,
        }

        mock_request.return_value.json.return_value = mocked_token
        response = self.client.generate_token()

        mock_request.assert_called_with(
            url=f"{self.url}/token/new/",
            headers=self.client._headers,
            data=json.dumps(payload),
            timeout = 10,
        )

        assert response["access_expires"] == 86400
        assert response["access"] == mocked_token["access"]
        assert self.client.token == "access_token"

    @patch("requests.post")
    def test_exchange_token(self, mock_request):
        """Test token exchange."""
        mock_request.return_value.json.return_value = {
            "access": "new_access_token",
            "access_expires": 86400,
        }

        response = self.client.exchange_token(refresh_token="refresh_token")
        assert self.client.token == "new_access_token"
        assert response["access"] == "new_access_token"

    @patch("requests.get")
    def test_get_request(self, mock_request):
        """
        Test request with GET.

        Args:
            mock_request (Mock): Mock request
        """
        mock_request.return_value.json.return_value = {"status": 200}
        response = self.client.request(HTTPMethod.GET, "sample")
        assert response["status"] == 200
        assert (
            mock.call(
                url=f"{self.url}/sample",
                headers=self.client._headers,
                params={},
                timeout = 10,
            )
            in mock_request.call_args_list
        )

    @patch("requests.post")
    def test_post_request(self, mock_request):
        """
        Test request with POST.

        Args:
            mock_request (Mock): Mock request
        """
        mock_request.return_value.json.return_value = {"status": 201}
        payload = {"data": "Post data"}
        response = self.client.request(HTTPMethod.POST, "sample", payload)
        assert response["status"] == 201
        assert (
            mock.call(
                url=f"{self.url}/sample",
                headers=self.client._headers,
                data=json.dumps(payload),
                timeout = 10,
            )
            in mock_request.call_args_list
        )

    def test_client_raises_exception(self):
        """Test unsupported Http method."""
        with self.assertRaises(Exception) as context:
            self.client.request(HTTPMethod.PATCH, "sample")

        assert str(context.exception) in 'Method "PATCH" is not supported'

    def test_token_setter(self):
        """Test token setter."""
        self.client.token = "Token"
        assert self.client._headers["Authorization"] == "Bearer Token"

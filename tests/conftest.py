from unittest.mock import patch

import pytest

from nordigen import NordigenClient

from .mocks import mocked_token


@pytest.fixture(scope="module")
def client():
    """
    Nordigen client fixture.

    Yields:
        [NordigenClient]: NordigenClient instance
    """
    nordigen = NordigenClient(secret_id="SECRET_ID", secret_key="SECRET_KEY")
    with patch("requests.post") as mock_request:
        mock_request.return_value.json.return_value = mocked_token
        response = nordigen.generate_token()
        nordigen.token = response["access"]
        yield nordigen

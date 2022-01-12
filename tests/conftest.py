import pytest
import os
from dotenv import load_dotenv

from nordigen import NordigenClient

load_dotenv()


@pytest.fixture(scope="module")
def client():
    """
    Nordigen client fixture.

    Yields:
        [NordigenClient]: NordigenClient instance
    """
    nordigen = NordigenClient(
        secret_id=os.getenv("SECRET_ID"), secret_key=os.getenv("SECRET_KEY")
    )
    nordigen.generate_token()
    yield nordigen

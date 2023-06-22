# Nordigen Python

This is official Python client library for [GoCardless Bank Account Data](https://gocardless.com/bank-account-data/) API

For a full list of endpoints and arguments, see the [docs](https://developer.gocardless.com/bank-account-data/quick-start-guide).

Before starting to use API you will need to create a new secret and get your `SECRET_ID` and `SECRET_KEY` from the [GoCardless Bank Account Data Portal](https://bankaccountdata.gocardless.com/user-secrets/).

## Requirements

* Python >= 3.8


## Installation

Install library via pip package manager:

```
pip install nordigen
```

## Example application

Example code can be found in `main.py` file and Flask application can be found in the `example` directory

## Quickstart


```python
from uuid import uuid4

from nordigen import NordigenClient

# initialize Nordigen client and pass SECRET_ID and SECRET_KEY
client = NordigenClient(
    secret_id="SECRET_ID",
    secret_key="SECRET_KEY"
)

# Create new access and refresh token
# Parameters can be loaded from .env or passed as a string
# Note: access_token is automatically injected to other requests after you successfully obtain it
token_data = client.generate_token()

# Use existing token
client.token = "YOUR_TOKEN"

# Exchange refresh token for new access token
new_token = client.exchange_token(token_data["refresh"])

# Get institution id by bank name and country
institution_id = client.institution.get_institution_id_by_name(
    country="LV",
    institution="Revolut"
)

# Get all institution by providing country code in ISO 3166 format
institutions = client.institution.get_institutions("LV")

# Initialize bank session
init = client.initialize_session(
    # institution id
    institution_id=institution_id,
    # redirect url after successful authentication
    redirect_uri="https://gocardless.com",
    # additional layer of unique ID defined by you
    reference_id=str(uuid4())
)

# Get requisition_id and link to initiate authorization process with a bank
link = init.link # bank authorization link
requisition_id = init.requisition_id
```

After successful authorization with a bank you can fetch your data (details, balances, transactions)

---

## Fetching account metadata, balances, details and transactions

```python

# Get account id after you have completed authorization with a bank
# requisition_id can be gathered from initialize_session response
accounts = client.requisition.get_requisition_by_id(
    requisition_id=init.requisition_id
)

# Get account id from the list.
account_id = accounts["accounts"][0]

# Create account instance and provide your account id from previous step
account = client.account_api(id=account_id)

# Fetch account metadata
meta_data = account.get_metadata()
# Fetch details
details = account.get_details()
# Fetch balances
balances = account.get_balances()
# Fetch transactions
transactions = account.get_transactions()
# Filter transactions by specific date range
transactions = account.get_transactions(date_from="2021-12-01", date_to="2022-01-21")
```

## Premium endpoints

```python
# Get premium transactions. Country and date parameters are optional
premium_transactions = account.get_premium_transactions(
    country="LV",
    date_from="2021-12-01",
    date_to="2022-01-21"
)
# Get premium details
premium_details = account.get_premium_details()
```

## Support

For any inquiries please contact support at [bank-account-data-support@gocardless.com](bank-account-data-support@gocardless.com) or create an issue in repository.

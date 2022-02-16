from uuid import uuid4
from nordigen import NordigenClient

def main():
    # Load token from .env file or pass secrets as a string
    client = NordigenClient(
        secret_id="SECRET_ID",
        secret_key="SECRET_KEY"
    )
    # generate access_token
    token_data = client.generate_token()

    # Use existing token
    client.token = "YOUR_TOKEN"

    # Exchange refresh token for new access token
    new_token = client.exchange_token(token_data["refresh"])

    # Get institution_id by country and institution name
    institution_id = client.institution.get_institution_id_by_name(
        country="LV", institution="Revolut"
    )
    # Initialize bank session
    init = client.initialize_session(
        # institution id
        institution_id=institution_id,
        # redirect url after successful authentication
        redirect_uri="https://nordigen.com",
        # additional layer of unique ID defined by you
        reference_id=str(uuid4()),
    )
    print(init.link)

    # Get account id after you have completed authorization with a bank
    accounts = client.requisition.get_requisition_by_id(
        requisition_id=init.requisition_id
    )
    # Get account id from the list.
    try:
        account_id = accounts["accounts"][0]
    except IndexError:
        raise ValueError(
            "Account list is empty. Make sure you have completed authorization with a bank."
        )

    # Create account instance and provide your account id from previous step
    account = client.account_api(id=account_id)

    # Get account data
    meta_data = account.get_metadata()
    balances = account.get_balances()
    details = account.get_details()
    transactions = account.get_transactions()
    # Filter transactions by specific date range
    transactions = account.get_transactions(date_from="2021-12-01", date_to="2022-01-21")

if __name__ == "__main__":
    main()

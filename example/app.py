import os
from uuid import uuid4

from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, render_template, session, url_for

from nordigen import NordigenClient

app = Flask(__name__)
# set Flask secret key
app.config["SECRET_KEY"] = os.urandom(24)

COUNTRY = "LV"
REDIRECT_URI = "http://127.0.0.1:5000/results"

# Load secrets from .env file
load_dotenv()

# Init Nordigen client pass secret_id and secret_key generated from OB portal
# In this example we will load secrets from .env file
client = NordigenClient(
    secret_id=os.getenv("SECRET_ID"),
    secret_key=os.getenv("SECRET_KEY")
)

# Generate access & refresh token
client.generate_token()


@app.route("/", methods=["GET"])
def home():
    # Get list of institutions
    institution_list = client.institution.get_institutions(country=COUNTRY)
    return render_template("index.html", institutions=institution_list)


@app.route("/agreements/<institution_id>", methods=["GET"])
def agreements(institution_id):

    if institution_id:

        init = client.initialize_session(
            institution_id=institution_id,
            redirect_uri=REDIRECT_URI,
            reference_id=str(uuid4()),
        )

        redirect_url = init.link
        # save requisiton id to a session
        session["req_id"] = init.requisition_id
        return redirect(redirect_url)

    return redirect(url_for("home"))


@app.route("/results", methods=["GET"])
def results():

    if "req_id" in session:

        accounts = client.requisition.get_requisition_by_id(
            requisition_id=session["req_id"]
        )["accounts"]

        accounts_data = []
        for id in accounts:
            account = client.account_api(id)
            metadata = account.get_metadata()
            transactions = account.get_transactions()
            details = account.get_details()
            balances = account.get_balances()

            accounts_data.append(
                {
                    "metadata": metadata,
                    "details": details,
                    "balances": balances,
                    "transactions": transactions,
                }
            )

        return jsonify(accounts_data)

    raise Exception(
        "Requisition ID is not found. Please complete authorization with your bank"
    )


if __name__ == "__main__":
    app.run(debug=True)

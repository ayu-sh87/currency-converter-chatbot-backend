from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "fca_live_f2h8ArWCLoCgwGT9y1sU3fDUFXe3nOF2lJ5rNCCg"

@app.route("/", methods=["POST"])
def index():
    data = request.get_json()

    source_currency = data["queryResult"]["parameters"]["unit-currency"]["currency"]
    amount = data["queryResult"]["parameters"]["unit-currency"]["amount"]
    target_currency = data["queryResult"]["parameters"]["currency-name"]

    if isinstance(target_currency, list):
        target_currency = target_currency[0]

    rate = fetch_conversion_factor(source_currency, target_currency)
    final_amount = round(float(amount) * float(rate), 2)

    response = {
        "fulfillmentText": f"{amount} {source_currency} is {final_amount} {target_currency}"
    }
    return jsonify(response)


def fetch_conversion_factor(source, target):
    url = (
        "https://api.freecurrencyapi.com/v1/latest"
        f"?apikey={API_KEY}"
        f"&base_currency={source}"
        f"&currencies={target}"
    )

    r = requests.get(url)
    data = r.json()

    return data["data"][target]


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

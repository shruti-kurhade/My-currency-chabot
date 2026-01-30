from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Just for browser testing
@app.route('/', methods=['GET'])
def home():
    return "Currency Converter Webhook is Running."

# Dialogflow webhook
@app.route('/', methods=['POST'])
def index():
    data = request.get_json()

    try:
        source_currency = data['queryResult']['parameters']['unit-currency']['currency']
        amount = data['queryResult']['parameters']['unit-currency']['amount']
        target_currency = data['queryResult']['parameters']['currency-name']

        cf = fetch_conversion_factor(source_currency, target_currency)
        final_amount = round(amount * cf, 2)

        response = {
            "fulfillmentText": f"{amount} {source_currency} is {final_amount} {target_currency}"
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({
            "fulfillmentText": "Sorry, I couldn't process that conversion."
        })


def fetch_conversion_factor(source, target):
    url = f"https://api.exchangerate-api.com/v4/latest/{source}"
    res = requests.get(url)
    data = res.json()
    return data['rates'][target]


if __name__ == "__main__":
    app.run(debug=True)
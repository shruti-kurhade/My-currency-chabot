from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Currency Converter Webhook is Running."

@app.route('/', methods=['POST'])
def index():
    data = request.get_json()

    intent_name = data['queryResult']['intent']['displayName']

    
    if intent_name == "supported-currency":
        return jsonify({
            "fulfillmentText": "I support most international currencies including US Dollar (USD), Indian Rupee (INR), Euro (EUR), British Pound (GBP), Japanese Yen (JPY), Australian Dollar (AUD), Canadian Dollar (CAD) and many others."
            })
    
    try:
        source_currency = data['queryResult']['parameters']['unit-currency']['currency']
        amount = data['queryResult']['parameters']['unit-currency']['amount']
        target_currency = data['queryResult']['parameters']['currency-name']

        cf = fetch_conversion_factor(source_currency, target_currency)
        final_amount = round(amount * cf, 2)

        return jsonify({
            "fulfillmentText": f"{amount} {source_currency} is {final_amount} {target_currency}"
        })

    except Exception:
        return jsonify({
            "fulfillmentText": "Please enter a valid currency conversion. Example: Convert 10 USD to INR."
        })


def fetch_conversion_factor(source, target):
    url = f"https://api.exchangerate-api.com/v4/latest/{source}"
    res = requests.get(url)
    data = res.json()
    return data['rates'][target]


if __name__ == "__main__":
    app.run(debug=True)

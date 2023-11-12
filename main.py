from functools import reduce

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

capitalize_currency = lambda currency: currency.upper()


def convert_all_and_sum(amounts, conversion_function):
    converted_amounts = map(conversion_function, amounts)
    return reduce(lambda x, y: x + y, converted_amounts)


def get_exchange_rate(from_currency, to_currency):
    api_key = 'ee4cd4fcf90316edf094a734'

    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{from_currency}"

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Fehler beim Abrufen des Wechselkurses")

    data = response.json()

    if to_currency not in data['conversion_rates']:
        raise ValueError(f"Umrechnung von {from_currency} zu {to_currency} nicht unterstützt.")

    return data['conversion_rates'][to_currency]


def convert(amount, from_currency, to_currency):
    if from_currency == to_currency:
        return amount
    try:
        rate = get_exchange_rate(from_currency, to_currency)
        return amount * rate
    except Exception as e:
        raise e


# Umrechnungsfunktion basierend auf die Währungen mit aktuellem Kurs
@app.route('/convert', methods=['POST'])
def convert_handler():
    data = request.get_json()
    amounts = data.get('amounts', [])
    from_currency = capitalize_currency(data.get('from_currency', ''))
    to_currency = capitalize_currency(data.get('to_currency', ''))

    try:
        total_converted = convert_all_and_sum(amounts, lambda x: convert(x, from_currency, to_currency))
        return jsonify({f"Der totale Betrag nach der Umrechnung von {from_currency} zu {to_currency} ist": round(
            total_converted, 2)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)

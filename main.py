from functools import reduce

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Lambda Funktion, um die erhaltene Währung in Grossbuchstaben umzuwandeln.
capitalize_currency = lambda currency: currency.upper()


# Map und reduce damit man die summierte Liste der Amounts umwandeln kann
def convert_all_and_sum(amounts, conversion_function):
    converted_amounts = map(conversion_function, amounts)
    return reduce(lambda x, y: x + y, converted_amounts)


def get_exchange_rate(from_currency, to_currency):
    # Hier wird der API-Schlüssel festgelegt, der für den Zugriff auf die Wechselkurs-API benötigt wird.
    api_key = 'ee4cd4fcf90316edf094a734'

    # Die URL für die API-Anfrage wird erstellt. Dabei wird die Basiswährung in den URL-Pfad eingefügt.
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{from_currency}"

    response = requests.get(url)

    # Wenn die Antwort der API nicht den Statuscode 200 hat (was OK bedeutet), wird eine Ausnahme ausgelöst.
    if response.status_code != 200:
        raise Exception("Fehler beim Abrufen des Wechselkurses")

    data = response.json()

    # Überprüfung, ob die Zielwährung in den Umrechnungskursen vorhanden ist.
    # Wenn sie nicht vorhanden ist, wird eine ValueError-Ausnahme mit einer Nachricht ausgelöst.
    if to_currency not in data['conversion_rates']:
        raise ValueError(f"Umrechnung von {from_currency} zu {to_currency} nicht unterstützt.")

    # Der Umrechnungskurs von der Basiswährung zur Zielwährung wird aus der JSON-Antwort extrahiert und zurückgegeben.
    return data['conversion_rates'][to_currency]


# Umrechnung der Amounts in dem man den Amount mit dem Wechselkurs (wird von get_exchange_rate Funktion geholt)
def convert(amount, from_currency, to_currency):
    if from_currency == to_currency:
        # Keine Umrechnung notwendig da es die selbe Währung ist.
        return amount
    try:
        # Umrechnen basierend auf den aktuellen Umrechnungskursen von der API
        rate = get_exchange_rate(from_currency, to_currency)
        return amount * rate
    except Exception as e:
        # Ausnahme behandeln, z.B. wenn die API nicht erreichbar ist
        raise e


# Die Funktion konvertiert dann jeden Betrag mit dem aktuellen Wechselkurs, summiert alle konvertierten Beträge und
# gibt das Gesamtergebnis zurück.
@app.route('/convert', methods=['POST'])
def convert_handler():
    data = request.get_json()
    amounts = data.get('amounts', [])
    from_currency = capitalize_currency(data.get('from_currency', ''))
    to_currency = capitalize_currency(data.get('to_currency', ''))

    try:
        # Umrechnungsfunktion basierend auf den Währungen mit aktuellem Kurs
        total_converted = convert_all_and_sum(amounts, lambda x: convert(x, from_currency, to_currency))
        return jsonify({f"Der totale Betrag nach der Umrechnung von {from_currency} zu {to_currency} ist": round(
            total_converted, 2)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)

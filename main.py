from functools import reduce

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Lambda Funktion, um die erhaltene
capitalize_currency = lambda currency: currency.upper()


# Map und reduce damit man die summierte Liste der Amounts umwandeln kann
def convert_all_and_sum(amounts, conversion_function):
    converted_amounts = map(conversion_function, amounts)
    return reduce(lambda x, y: x + y, converted_amounts)

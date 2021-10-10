import requests
import json
from config import EXCHANGE_API_KEY

currency_dict = {
    "рубль": "RUB",
    "доллар": "USD",
    "евро": "EUR"
}


class APIException(Exception):
    pass


class Currency:
    @staticmethod
    def get_price(base, query, amount):
        response = requests.get(
            f"https://free.currconv.com/api/v7/convert?q={base}_{query}&compact=ultra&apiKey={EXCHANGE_API_KEY}")
        info = json.loads(response.content)

        return info[f'{base}_{query}'] * amount

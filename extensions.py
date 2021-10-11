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
        try:
            amount_float = float(amount)
        except Exception:
            raise APIException("Третьим параметром должно быть число.")

        if base == query:
            raise APIException(f'Нельзя переводить одинаковые валюты {base} в {query}.')

        try:
            base_ticker = currency_dict[base.lower()]
        except KeyError:
            raise APIException(f'Валюта {base} не обнаружена.')

        try:
            query_ticker = currency_dict[query.lower()]
        except KeyError:
            raise APIException(f'Валюта {query} не обнаружена.')

        try:
            query = f'{base_ticker}_{query_ticker}&compact=ultra&apiKey={EXCHANGE_API_KEY}'
            response = requests.get(
                f"https://free.currconv.com/api/v7/convert?q={query}")
            info = json.loads(response.content)
            result = info[f'{base_ticker}_{query_ticker}'] * amount_float
        except Exception:
            raise APIException("Не удалось получить курсы валют.")

        return f'Цена {amount} {base_ticker} = {result:.2f} {query_ticker}'

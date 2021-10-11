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
    def get_price(message):
        try:
            base_name, query_name, amount_text = message.text.split()
        except ValueError:
            raise APIException("Неверный формат ввода. /help - инструкция по использованию.")

        try:
            amount = float(amount_text)
        except Exception:
            raise APIException("Третьим параметром должно быть число.")

        try:
            base = currency_dict[base_name.lower()]
        except KeyError:
            raise APIException(f'Валюта {base_name} не обнаружена.')

        try:
            query = currency_dict[query_name.lower()]
        except KeyError:
            raise APIException(f'Валюта {query_name} не обнаружена.')

        if base == query:
            raise APIException(f'Нельзя переводить {base} в {query}.')

        try:
            response = requests.get(
                f"https://free.currconv.com/api/v7/convert?q={base}_{query}&compact=ultra&apiKey={EXCHANGE_API_KEY}")
            info = json.loads(response.content)
            result = info[f'{base}_{query}'] * amount
        except Exception:
            raise APIException("Не удалось получить курсы валют.")

        return f'Цена {amount} {base} = {result:.2f} {query}'

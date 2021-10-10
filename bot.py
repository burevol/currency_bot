import telebot
from extensions import APIException, Currency
from config import TELEGRAM_API_KEY

bot = telebot.TeleBot(TELEGRAM_API_KEY)

currency = {
    "рубль": "RUB",
    "доллар": "USD",
    "евро": "EUR"
}


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(commands=['values'])
def send_values(message):
    l_mess = ["Доступные виды валют:"]
    for i, j in currency.items():
        l_mess.append(f'{i} - {j}')
    bot.send_message(message.chat.id, '\n'.join(l_mess))


@bot.message_handler(content_types=["text"])
def main_handler(message):
    try:
        try:
            base_name, query_name, amount_text = message.text.split()
        except ValueError:
            raise APIException("Неверный формат ввода.")

        if not amount_text.isdigit():
            raise APIException("Третьим параметром должно быть число.")

        try:
            base = currency[base_name]
        except Exception:
            raise APIException(f'Валюта {base_name} не обнаружена')

        try:
            query = currency[query_name]
        except Exception:
            raise APIException(f'Валюта {query_name} не обнаружена')
    except APIException as ex:
        bot.reply_to(message, str(ex))
    else:
        bot.reply_to(message, Currency.get_price(base, query, int(amount_text)))


bot.infinity_polling()

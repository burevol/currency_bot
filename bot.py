import telebot
from extensions import APIException, Currency, currency_dict
from config import TELEGRAM_API_KEY

bot = telebot.TeleBot(TELEGRAM_API_KEY)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Это бот для пересчета валют. \n Использование: \n "
                          "/help - это сообщение \n /values - список доступных валют \n "
                          "<название базовой валюты> <название валюты пересчета> <количество> "
                          "- пересчет валюты из базовой\n"
                          "Пример: доллар рубль 15")


@bot.message_handler(commands=['values'])
def send_values(message):
    l_mess = ["Доступные виды валют:"]
    for i, j in currency_dict.items():
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
            base = currency_dict[base_name]
        except Exception:
            raise APIException(f'Валюта {base_name} не обнаружена')

        try:
            query = currency_dict[query_name]
        except Exception:
            raise APIException(f'Валюта {query_name} не обнаружена')

        try:
            result = Currency.get_price(base, query, int(amount_text))
        except Exception:
            raise APIException("Ошибка при получении курсов валют")

    except APIException as ex:
        bot.reply_to(message, str(ex))
    else:
        bot.reply_to(message, result)


bot.infinity_polling()

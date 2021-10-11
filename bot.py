import telebot
from extensions import APIException, Currency, currency_dict
from config import TELEGRAM_API_KEY

bot = telebot.TeleBot(TELEGRAM_API_KEY)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Это бот для пересчета валют. \n Использование:\n "
                          "/help - это сообщение.\n /values - список доступных валют.\n "
                          "<название базовой валюты> <в какую валюту перевести> <количество переводимой валюты>\n"
                          "- пересчет валюты из базовой.\n"
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
        values = message.text.split()
        if len(values) != 3:
            raise APIException("Неверный формат ввода. /help - инструкция по использованию.")
        base, query, amount = values
        result = Currency.get_price(base, query, amount)
    except APIException as ex:
        bot.reply_to(message, f'Ошибка пользователя.\n{ex}')
    except Exception:
        bot.reply_to(message, "Не удалось обработать команду.")
    else:
        bot.reply_to(message, result)


bot.infinity_polling()

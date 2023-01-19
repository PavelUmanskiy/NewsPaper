# A simple currency converter bot made by Pavel Umanskiy on December, 13th 2022.
import telebot
from config import currency_info, translated_currencies, valid_characters
from extensions import InputException, APIException, BotAbilities


file = open('SF_HOMEWORK\TELEGRAM_BOT\my_tokens.txt', 'r', encoding='utf8')
info = file.readlines()
TOKEN = info[0][:-1]
API_KEY = info[1]
file.close()


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def command_start_help(message: telebot.types.Message):
    bot.reply_to(message, f"Здравствуйте, {message.chat.username}!\
\nЯ - бот-конвертер валют! Я могу помочь Вам с задачей по конверсии одной валюты в другую. \
Просто напишите мне следующее сообщение, и я сделаю всю математику за вас:\
\n<base> <amount> <quote>\nГде «base» — это валюта, которая у вас есть, «amount» — это количество \
валюты, которую вы хотите конвертировать, а «quote» — это валюта, в которую вы хотите конвертировать, \
\nВы можете просмотреть все доступные валюты, отправив команду /values. Эта команда предоставит большой список\
всех возможных конверсий.")


@bot.message_handler(commands=['values'])
def command_values(message: telebot.types.Message):
    try:
        text = BotAbilities.api_ask_list(translated_currencies, API_KEY)
    except APIException as api_error:
        bot.reply_to(message, api_error)
    except Exception as server_error:
        bot.reply_to(message, f'Не удалось обработать команду по причине ошибки на сервере.\nКод ошибки: {server_error}')
    else:
        bot.reply_to(message, 'Можно переводить:\n' + text)   


@bot.message_handler(content_types=['text'])
def convert(message):
    try:
        base_ticker, quote_ticker, base, amount, quote = BotAbilities.check_input(message, currency_info, valid_characters)   
    except InputException as input_error:
        bot.reply_to(message, input_error)
    except Exception as server_error:
        bot.reply_to(message, f'Не удалось обработать команду по причине ошибки на сервере.\nКод ошибки: {server_error}')

    try:
        pair = base_ticker + quote_ticker
    except UnboundLocalError:
        bot.reply_to(message, 'Не удалось обработать введённые валюты. Проверьте соответствие вашей формы ввода \
с формой ввода, представленной в /start')
    except Exception as server_error:
        bot.reply_to(message, f'Не удалось обработать команду по причине ошибки на сервере.\nКод ошибки: {server_error}')
    else:
        try:
            api_response = BotAbilities.api_ask_rates(pair, API_KEY)
        except APIException as api_error:
            bot.reply_to(message, api_error)
        except Exception as server_error:
            bot.reply_to(message, f'Не удалось обработать команду по причине ошибки на сервере.\nКод ошибки: {server_error}')
        else:
            amount = amount if amount % 1 else int(amount)
            text = f'{amount} {base} в {quote} - это: {round((amount * api_response), 2)}'
            bot.reply_to(message, text)
    

bot.polling(none_stop=True)

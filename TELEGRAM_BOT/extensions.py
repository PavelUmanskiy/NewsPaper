import requests as req
import json
from telebot import types

class InputException(Exception):
    pass


class APIException(Exception):
    pass


class BotAbilities():
    @staticmethod
    def check_input(message: types.Message, currency_info: dict, valid_characters: tuple) -> tuple:
        amount_started = False
        for current_index in range(len(message.text)):
            if not amount_started and message.text[current_index] in valid_characters:
                start_index = current_index
                amount_started = True
            if amount_started and not message.text[current_index] in valid_characters:
                finish_index = current_index
                break
            
        base, amount, quote = message.text.partition(message.text[start_index: finish_index])
            
            
        base = base.strip().lower()
        amount = amount.strip()
        quote = quote.strip().lower()
                        
        if quote == base:
            raise InputException(f"Невозможно конвертировать валюту {base} саму в себя.")
            
            
        try:
            base_ticker = currency_info[base]
        except KeyError:
            raise InputException(f"Не удалось обработать первую валюту {base}")
            
        try:
            quote_ticker = currency_info[quote]
        except KeyError:
            raise InputException(f"Не удалось обработать вторую валюту {quote}")
            
        try:
            amount = float(amount)
        except ValueError:
            raise InputException(f"Не удалось обработать количество {amount}.\nЕсли Вы написали дробное число через запятую, \
попробуйте ещё раз, но на этот раз запишите его через точку.")
            
        return (base_ticker, quote_ticker, base, amount, quote)

    
    @staticmethod
    def api_ask_rates(pair: str, API_KEY: str) -> float:
        r = req.get(f'https://currate.ru/api/?get=rates&pairs={pair}&key={API_KEY}')
        
        if int(json.loads(r.content)['status']) // 100 != 2:
            raise APIException("Вы ввелли недействительный перевод. Проверьте, есть ли ваш перевод в списке /values.\n\
Если Ваш запрос есть в списке, значит на стороне представителя курса валют неполадки. В таком случае попробуйте повторить запрос позже.")
        
        api_response = float(json.loads(r.content)['data'][pair])
        return api_response

    @staticmethod
    def api_ask_list(translated_currencies: dict, API_KEY: str) -> str:
        text = ''
        r = req.get(f'https://currate.ru/api/?get=currency_list&key={API_KEY}')
        
        if int(json.loads(r.content)['status']) // 100 != 2:
            raise APIException("Вы ввелли недействительный перевод. Проверьте, есть ли ваш перевод в списке /values.\n\
Если Ваш запрос есть в списке, значит на стороне представителя курса валют неполадки. В таком случае попробуйте повторить запрос позже.")
        
        api_response = json.loads(r.content)['data']
        for pair in api_response:
            ticker1, ticker2 = pair[:3], pair[3:]
            if ticker1 in translated_currencies.keys() and ticker2 in translated_currencies.keys():
                text += f'{translated_currencies[ticker1]} в {translated_currencies[ticker2]} и обратно\n'

        return text
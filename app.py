from config import *
import telebot
from TOKEN import TOKEN


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!\n'
                                      f'Рад тебя приветствовать. Я - Бот-калькулятор валюты.\n'
                                      f'Я могу сообщить стоимость валютной пары на текущий '
                                      f'момент с учетом торгов на бирже.\n'
                                      f'Для того чтобы узнать с какими валютами я могу работать, '
                                      f'введи команду /value\n'
                                      f'Для получения расчёта конвертации валюты пришли мне сообщение:\n'
                                      f'\n<Валюта1><пробел><валюта2><пробел><Количество>\n'
                                      f'\nВалюта1 - это валюта, которую хочешь купить.\n'
                                      f'Валюта2 - это валюта, за которую собираешься покупать.\n'
                                      f'Количество - количество валюты, которую хочешь купить.>')


@bot.message_handler(commands=['value'])
def handle_start_help(message: telebot.types.Message):
    text = f'Я знаю все существующие валютные тикеры, но, если тебе лень' \
           ' их вспоминать, можешь использовать названия самых популярных валют в россии:\n\n'
    for key in KEYS_OFTEN_USED.keys():
        text = text + key + '\n'
    text = text + f'\n\nХочешь использовать тикеры? Могу напомнить 5 тикеров по команде /tikers'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['tikers'])
def handle_start_help(message: telebot.types.Message):
    text = random_tikers()
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['voice'])
def handle_voice(message: telebot.types.Message):
    bot.reply_to(message, 'Я не могу прослушать аудио, я сейчас в общественном месте, без наушников. '
                          'Пришли сообщение текстом.')


@bot.message_handler(content_types=['photo'])
def handle_photo(message: telebot.types.Message):
    bot.reply_to(message, 'Красивая картинка, но зачем это мне?')


@bot.message_handler(content_types=['audio', 'document', 'video'])
def handle_audio_document_video(message: telebot.types.Message):
    bot.reply_to(message, f'{message.from_user.first_name}, ты серьезно пытаешся отправить мне файлы?!')


@bot.message_handler(content_types=['text'])
def handle_text(message: telebot.types.Message):
    e, base, quote, amount, value = Convertator.get_price(message.text)
    if not e:
        bot.send_message(message.chat.id, f'Для покупки {amount} {base} надо {value} {quote}')
    else:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}\nНужна помощь? Введите /help')


bot.polling(none_stop=True)

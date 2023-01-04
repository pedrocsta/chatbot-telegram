import telebot

from constants import API_KEY
from queries import cancel_reservation, check_availability, make_reservation
from responses import mag_day_shift, msg_help, msg_reserve, msg_schedule

bot = telebot.TeleBot(API_KEY, parse_mode=None)


@bot.message_handler(commands=['start'])
def start(message) -> None:
    bot.send_message(
        message.chat.id,
        f"Olá {message.chat.first_name} {message.chat.last_name}, bem vindo ao atendimento do NUARTE. 🤩"
        "Digite /help caso precise de ajuda."
    )


@bot.message_handler(commands=['help'])
def help(message) -> None:
    bot.send_message(
        message.chat.id,
        msg_help
    )


@bot.message_handler(commands=['reservar'])
def reserve(message) -> None:
    bot.send_message(
        message.chat.id,
        msg_reserve
    )


@bot.message_handler(commands=['sala', 'camarim'])
def day_shift(message) -> None:
    global room
    txt = f'{message.text}'.replace('/', '')
    room = 1 if txt == 'sala' else 2

    bot.send_message(
        message.chat.id,
        mag_day_shift
    )


@bot.message_handler(commands=['manha', 'tarde', 'noite'])
def schedule(message) -> None:
    global shift
    txt = f'{message.text}'.replace('/', '')

    if txt == 'manha':
        shift = 1
    elif txt == 'tarde':
        shift = 2
    else:
        shift = 3

    # current_date = message.date - 86400

    bot.send_message(
        message.chat.id,
        msg_schedule
    )


@bot.message_handler(commands=['primeiro', 'segundo', 'terceiro', 'quarto', 'quinto', 'sexto'])
def time_booked(message) -> None:
    global time
    time = f'{message.text}'.replace('/', '')

    if check_availability(time, shift, room):
        make_reservation(time, shift, room)
        bot.send_message(
            message.chat.id,
            'Horário reservado com sucesso!'
        )
    else:
        bot.send_message(
            message.chat.id,
            'Desculpe, mas o horário já foi reservado!'
        )


bot.infinity_polling()

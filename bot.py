import telebot

from constants import API_KEY
from queries import (cancel_reserve, check_availability, check_user,
                     make_reservation)
from responses import (msg_cancel_reservation, msg_day_shift_cancel_reserve,
                       msg_day_shift_reserve, msg_help, msg_reserve,
                       msg_schedule_cancel_reserve, msg_schedule_reserve)

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
    global operation
    operation = f'{message.text}'.replace('/', '')
    bot.send_message(
        message.chat.id,
        msg_reserve
    )


@bot.message_handler(commands=['cancelar'])
def cancel_reservation(message) -> None:
    global operation
    operation = f'{message.text}'.replace('/', '')
    bot.send_message(
        message.chat.id,
        msg_cancel_reservation
    )


@bot.message_handler(commands=['sala', 'camarim'])
def day_shift(message) -> None:
    global room
    txt = f'{message.text}'.replace('/', '')
    room = 1 if txt == 'sala' else 2

    if operation == 'reservar':
        bot.send_message(
            message.chat.id,
            msg_day_shift_reserve
        )
    else:
        bot.send_message(
            message.chat.id,
            msg_day_shift_cancel_reserve
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

    if operation == 'reservar':
        bot.send_message(
            message.chat.id,
            msg_schedule_reserve
        )
    else:
        bot.send_message(
            message.chat.id,
            msg_schedule_cancel_reserve
        )


@bot.message_handler(commands=['primeiro', 'segundo', 'terceiro', 'quarto', 'quinto', 'sexto'])
def time_booked(message) -> None:
    global time
    time = f'{message.text}'.replace('/', '')
    associate = message.from_user.username

    if check_user(associate):
        if operation == 'reservar':
            if check_availability(time, shift, room)[0]:
                make_reservation(time, shift, room, associate)
                bot.send_message(
                    message.chat.id,
                    'Horário reservado com sucesso!'
                )
            else:
                bot.send_message(
                    message.chat.id,
                    'Desculpe, mas o horário já foi reservado!'
                )
        else:
            disponivel, booked_by = check_availability(time, shift, room)
            if not disponivel and booked_by == associate:
                cancel_reserve(time, shift, room)
                bot.send_message(
                    message.chat.id,
                    'Reserva cancelada com sucesso!'
                )
            elif not disponivel and booked_by != associate:
                bot.send_message(
                    message.chat.id,
                    'Desculpe, mas o horário não foi reservado por você!'
                )
            else:
                bot.send_message(
                    message.chat.id,
                    'Desculpe, mas o horário não foi reservado!'
                )
    else:
        bot.send_message(
            message.chat.id,
            'Desculpe, mas você não tem permissão para isso!'
        )


bot.infinity_polling()

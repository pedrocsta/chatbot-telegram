import telebot

from constants import API_KEY

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
        "Posso ajudá-lo a reservar salas do NUARTE.\n"
        "\n"
        "Você pode me controlar enviando estes comandos:\n"
        "\n"
        "/reservar - reserva uma sala\n"
        "/cancelar - cancela uma reserva"
    )


@bot.message_handler(commands=['reservar'])
def reserve(message) -> None:
    bot.send_message(
        message.chat.id,
        "Qual das salas abaixo deseja reservar?\n"
        "\n"
        "/sala - reserva a sala normal\n"
        "/camarim - reserva o camarim"
    )


@bot.message_handler(commands=['sala', 'camarim'])
def type_room(message) -> None:
    # text = f'{message.text}'.replace('/', '')
    bot.send_message(
        message.chat.id,
        "Em qual turno vai querer reservar?\n"
        "\n"
        "/manha - vê os horários da manhã"
        "/tarde - vê os horários da tarde"
        "/noite - vê os horários da noite"
    )


@bot.message_handler(commands=['manha', 'tarde', 'noite'])
def type_room(message) -> None:
    # current_date = message.date - 86400

    bot.send_message(
        message.chat.id,
        "Qual dos horários abaixo deseja realizar a reserva?\n"
        "\n"
        "/primeiros - Reserva o primeiro e segundo horário"
        "/intermediarios - Reserva o terceiro e quarto horário"
        "/ultimos - Reserva o quinto e sexto horário"
    )


def schedules(room) -> str:
    pass


bot.infinity_polling()

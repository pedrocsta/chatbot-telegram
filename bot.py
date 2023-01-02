from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

import responses
from constants import API_KEY


def start_command(update, context):
    update.message.reply_text(
        f"""Olá {update.message.from_user['first_name']} {update.message.from_user['last_name']}. Seja bem vindo!
Digite "/help" caso precise de ajuda."""
    )


def help_command(update, context):
    update.message.reply_text('"Oi" ou "Olá" -> Retorna uma saudação.')


def handle_message(update, context):
    txt = str(update.message.text).lower()
    response = responses.sample_response(txt)

    update.message.reply_text(response)


def error(update, context):
    print(f"Update: {update} caused error: {context.error}")


def main():
    updater = Updater(API_KEY, use_context=True)
    application = updater.dispatcher

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(Filters.text, handle_message))
    application.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

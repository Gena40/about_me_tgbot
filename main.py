import os
import logging

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    filters,
    MessageHandler,
    ApplicationBuilder,
    ContextTypes,
    CommandHandler
)


load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
LOGLEVEL = getattr(logging, os.environ.get('LOGLEVEL', 'INFO'))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# os.path.dirname(os.path.dirname(os.path.dirname(
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=LOGLEVEL
)


def check_tokens() -> bool:
    """
    Checks for the necessary environment variables.
    """
    return all([TELEGRAM_TOKEN])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


async def hobby(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Sends text to the bot with description of my hobby.
    """
    text = (
        'Главное моё увлечение - приборный поиск.⛏\n'
        'Это когда ты ходишь с лопатой и металлоискателем по местам старинных поселений и ищешь клад. '
        'Конечно, найти настоящий клад - это большая редкость и всерьез рассчитывать на это не стоит💰.\n'
        'Однако, во все времена люди что-нибудь теряли.🪙💍 '
        'Например монетки, крестики и кольца попадаются чаще всего. '
        'Но чтобы найти такую "потеряшку", тоже надо постараться. '
        'Бывает за целый день поисков не находишь вообще ничего подобного. '
        'А вот бутылочные крышки попадаются чаще всего🚯, без них ни один выезд не обходится 😅\n'
        'Самое интересное в таком увлечении для меня - это сам процесс, '
        'потому что никогда заранее не знаешь что ты сейчас выкопаешь. '
        'Иногда попадаются действительно очень интересные и старинные вещи.👑🎖⚱️ '
        'И в момент, когда из ломтя сырой земли тебе в ладонь выпадает кусочек далекой эпохи, '
        'испытываешь просто неповторимые эмоции, '
        'которые однозначно стоят потраченных сил и времени💪⌛️.'
    )
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open(f'{BASE_DIR}/data/old_coin.jpg', 'rb'),
        caption=text
    )


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


def main() -> None:
    """
    The main logic of the bot.
    """
    if not check_tokens():
        message = (
            'The required environment variable is missing!'
            'The program is forced to stop.'
        )
        logging.critical(message)
        return

    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    hobby_handler = CommandHandler('hobby', hobby)
    application.add_handler(hobby_handler)

    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    application.run_polling()


if __name__ == '__main__':
    main()

    # start_handler = CommandHandler('start', start)
    # echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    # application.add_handler(start_handler)
    # application.add_handler(echo_handler)



import os
import logging

from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    filters,
    MessageHandler,
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    ConversationHandler
)


load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
LOGLEVEL = getattr(logging, os.environ.get('LOGLEVEL', 'INFO'))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=LOGLEVEL
)

reply_keyboard = [
    ["что такое GPT", "разница между SQL и NoSQL", "история первой ❤️"],
    ["Выйти из этого меню"]
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)



def check_token() -> bool:
    """
    Checks for the necessary environment variables.
    """
    return all([TELEGRAM_TOKEN])


async def my_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Start of a dialog with a voice message choice.
    """
    await update.message.reply_text(
        "Выберите тему, про которую хотите послушать",
        reply_markup=markup
    )
    return CHOOSING


async def voice_gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Sends a voice message about GPT to the bot.
    """
    await context.bot.send_voice(
        chat_id=update.effective_chat.id,
        voice=open(f'{BASE_DIR}/data/audio.ogg', 'rb')
    )


async def hobby(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Sends text to the bot with description of my hobby.
    """
    text = (
        'Главное моё увлечение - приборный поиск\n'
        'Это когда ты ходишь с лопатой и металлоискателем по местам старинных поселений и ищешь клад⛏ '
        'Конечно, найти настоящий клад - это большая редкость и всерьез рассчитывать на это не стоит✖️💰.\n'
        'Однако, во все времена люди что-нибудь теряли.🪙💍 '
        'Например монетки, крестики и кольца попадаются чаще всего. '
        'Но чтобы найти такую "потеряшку", тоже надо постараться. '
        'Бывает за целый день поисков не находишь вообще ничего подобного. '
        'А вот бутылочные крышки попадаются чаще всего, без них ни один выезд не обходится 😅\n'
        'Самое интересное в таком увлечении для меня - это сам процесс, '
        'потому что никогда заранее не знаешь что ты сейчас выкопаешь. '
        'Иногда попадаются действительно очень интересные и старинные вещи.👑🎖⚱️ '
        'И в момент, когда из ломтя сырой земли тебе в ладонь выпадает кусочек далекой эпохи, '
        'испытываешь просто неповторимые эмоции, '
        'которые однозначно стоят потраченных сил и времени.'
    )
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open(f'{BASE_DIR}/data/old_coin.jpg', 'rb'),
        caption=text
    )


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler function for an unknown command.
    """
    text = update.message.text
    if text == 'my_voice':
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="The voice message selection menu is already open."
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Sorry, I didn't understand that command."
        )


async def voice_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Function - handler for choosing a voice message to listen."""
    text = update.message.text
    if text == "что такое GPT":
        await update.message.reply_voice(
            voice=open(f'{BASE_DIR}/data/audio.ogg', 'rb'),
            reply_markup=markup
        )
    elif text == "разница между SQL и NoSQL":
        await update.message.reply_text("Voice aboute SQL/NoSQL", reply_markup=markup)
    elif text == "история первой ❤️":
        await update.message.reply_text("Voice aboute ❤️", reply_markup=markup)
    else:
        await update.message.reply_text("Неизвестная команда")


async def exit_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Exit the voice message chooser menu.
    """
    await update.message.reply_text(
        "Ожидаю следующей команды...",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def main() -> None:
    """
    The main logic of the bot.
    """
    if not check_token():
        message = (
            'The required environment variable is missing!'
            'The program is forced to stop.'
        )
        logging.critical(message)
        return

    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    hobby_handler = CommandHandler('hobby', hobby)
    application.add_handler(hobby_handler)

    gpt_handler = CommandHandler('gpt', voice_gpt)
    application.add_handler(gpt_handler)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("my_voice", my_voice)],
        states={
            CHOOSING: [
                MessageHandler(
                    filters.Regex(
                        "^(что такое GPT|разница между SQL и NoSQL|история первой ❤️)$"
                    ),
                    voice_choice
                ),
                MessageHandler(filters.Regex("^Выйти из этого меню$"), exit_menu),
            ]
        },
        fallbacks=[MessageHandler(filters.Regex("^Выйти из этого меню$"), exit_menu)]
    )

    application.add_handler(conv_handler)

    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    application.run_polling()


if __name__ == '__main__':
    main()

    # echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    # application.add_handler(start_handler)

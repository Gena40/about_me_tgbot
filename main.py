"""Main module of telegram bot AboutMeSimpleBot."""
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


# pylint: disable=unused-argument, consider-using-with
# mypy: disable-error-code="union-attr"

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
LOGLEVEL = getattr(logging, os.environ.get('LOGLEVEL', 'INFO'))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CHOOSING = 0

BOT_DESCRIPTION = (
    'Здравствуйте!\n'
    'Данный бот предназначен для знакомства со мной - Геннадием Романовым (t.me/Gena40).\n'
    'Здесь Вы можете посмотреть как я сейчас выгляжу (/my_selfie), '
    'как я выглядел в старшей школе (/me_at_school), '
    'почитать про моё любимое увлечение (/hobby), ознакомиться с моим кодом '
    'на примере исходников этого бота (/sorce_code) и прослушать несколько '
    'голосовых сообщений в моём исполнении (/my_voice).\n'
    'Для удобства ввода команд предусмотрено меню. Давайте знакомиться!'
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=LOGLEVEL
)

logger = logging.getLogger(__name__)

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


async def selfie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Sends my selfie photo to the bot.
    """
    logger.info('requested selfie')
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open(f'{BASE_DIR}/data/selfie.jpg', 'rb')
    )


async def school_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Sends my school photo to the bot.
    """
    logger.info('requested school_photo')
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open(f'{BASE_DIR}/data/school_photo.jpg', 'rb')
    )


async def source_repo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Send link to the repository with code of this bot.
    """
    logger.info('requested source_repo')
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='https://github.com/Gena40/about_me_tgbot'
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Sends text with description of the bot's functionality.
    """
    logger.info('Get command %s, send bot description', update.message.text)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=BOT_DESCRIPTION
    )


async def hobby(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Sends text to the bot with description of my hobby.
    """
    logger.info('requested info about hobby')
    text = (
        'Главное моё увлечение - приборный поиск.\n'
        'Это когда ты ходишь с лопатой и металлоискателем по местам '
        'старинных поселений и ищешь клад ⛏\n '
        'Конечно, найти настоящий клад - это большая редкость и всерьез '
        'рассчитывать на это не стоит ✖️💰\n'
        'Однако, во все времена люди что-нибудь теряли🪙💍\n '
        'Например монетки, крестики и кольца попадаются чаще всего. '
        'Но чтобы найти такую "потеряшку", тоже надо постараться. '
        'Бывает за целый день поисков не находишь вообще ничего подобного. '
        'А вот бутылочные крышки - другое дело, без них ни один выезд не обходится 😅\n'
        'Самое интересное в таком увлечении для меня - это сам процесс, '
        'потому что никогда заранее не знаешь что ты сейчас выкопаешь. '
        'Иногда попадаются действительно очень интересные и старинные вещи 👑🎖⚱️ '
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
    if text == '/my_voice':
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Меню выбора голосового сообщения уже открыто."
        )
    else:
        logger.info('requested unknow command: %s', text)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Извините, но я не понимаю такую команду."
        )


async def voice_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Function - handler for choosing a voice message to listen."""
    text = update.message.text
    logger.info('requested voice: %s', text)
    if text == "что такое GPT":
        await update.message.reply_voice(
            voice=open(f'{BASE_DIR}/data/audio_gpt.ogg', 'rb'),
            caption='про GPT',
            reply_markup=markup
        )
    elif text == "разница между SQL и NoSQL":
        await update.message.reply_voice(
            voice=open(f'{BASE_DIR}/data/audio_sql.ogg', 'rb'),
            caption='про разницу между SQL и NoSQL',
            reply_markup=markup
        )
    elif text == "история первой ❤️":
        await update.message.reply_voice(
            voice=open(f'{BASE_DIR}/data/audio_love.ogg', 'rb'),
            caption='про первую любовь',
            reply_markup=markup
        )
    else:
        await update.message.reply_text("Неизвестная команда")


async def exit_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Exit the voice message chooser menu.
    """
    logger.info('received command to close audio selection menu')
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

    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()  # type: ignore

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    help_handler = CommandHandler('help', start)
    application.add_handler(help_handler)

    hobby_handler = CommandHandler('hobby', hobby)
    application.add_handler(hobby_handler)

    selfie_handler = CommandHandler('my_selfie', selfie)
    application.add_handler(selfie_handler)

    school_photo_handler = CommandHandler('me_at_school', school_photo)
    application.add_handler(school_photo_handler)

    source_repo_handler = CommandHandler('source_repo', source_repo)
    application.add_handler(source_repo_handler)

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

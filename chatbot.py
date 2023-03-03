import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.constants import ParseMode


from chatgpt import ChatGPT, CHAT_MODES

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

chat_bot = ChatGPT()

CURRENT_MODE = "assistant"

HELP_MESSAGE = """Commands:
⚪ /clear – reset dialog
⚪ /eng_mode – learn English
⚪ /assist_mode – assistant
⚪ /help – Show help
"""


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(HELP_MESSAGE, parse_mode=ParseMode.HTML)


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.chat.send_action(action="typing")
    res = chat_bot.send_message(message=update.message.text, chat_mode=CURRENT_MODE)
    await update.message.reply_text(res, parse_mode=ParseMode.HTML)


async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.chat.send_action(action="typing")
    chat_bot.clear()
    await update.message.reply_text("clear!")


async def assistant_mode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.chat.send_action(action="typing")
    chat_bot.clear()
    global CURRENT_MODE
    CURRENT_MODE = "assistant"
    await update.message.reply_text(CHAT_MODES[CURRENT_MODE]["welcome_message"], parse_mode=ParseMode.HTML)


async def eng_mode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.chat.send_action(action="typing")
    chat_bot.clear()
    global CURRENT_MODE
    CURRENT_MODE = "eng_teacher"
    await update.message.reply_text(CHAT_MODES[CURRENT_MODE]["welcome_message"], parse_mode=ParseMode.HTML)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.

    user_filter = filters.User(username="xxx")

    token = os.environ.get("TELEGRAM_TOKEN")
    application = Application.builder().token(token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("help", help_command, filters=user_filter))
    application.add_handler(CommandHandler("clear", clear_command, filters=user_filter))
    application.add_handler(CommandHandler("assist_mode", assistant_mode, filters=user_filter))
    application.add_handler(CommandHandler("eng_mode", eng_mode, filters=user_filter))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & user_filter, message))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
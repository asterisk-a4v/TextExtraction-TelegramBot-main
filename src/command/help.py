from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("This bot runs automatically. There are no commands.")


helpCommand_handler = CommandHandler('start', help)
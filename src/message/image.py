from os import remove

from PIL import Image
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from ..action.extract import image_to_text
from ..action.format import format_input
from ..action.parse import parse_geometry


async def image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Extracts text from image."""

    reference = update.effective_message.photo[-1].file_id
    hook = await context.bot.get_file(reference)

    file_path = f"storage/{hook.file_unique_id}.jpg"
    await hook.download_to_drive(file_path)

    output = image_to_text(file_path)

    image = Image.open(file_path)
    width, height = image.size

    await update.message.reply_text(
        str(
            format_input(
                parse_geometry(
                    width, 
                    height,
                    output
                )
            )
        )
    )
    image.close()
    remove(file_path)



imageMessage_handler = MessageHandler(filters.PHOTO & (~filters.CAPTION), image)

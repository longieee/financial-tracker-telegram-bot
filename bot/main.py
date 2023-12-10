import logging
import traceback

from chat_utils import must_have_args, restricted
from const import START_MESSAGE, TELEGRAM_BOT_TOKEN
from gsheet import Sheet
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from utils import breakdown_expense_tracking_string, breakdown_income_tracking_string

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

sheet = Sheet()


@restricted
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=START_MESSAGE)


@restricted
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I didn't understand that command.",
    )


@restricted
@must_have_args
async def spend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        sheet.append_row(breakdown_expense_tracking_string(context.args))
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="I added the row to your Expense Tracker sheet",
        )
    except Exception:
        logger.warning(traceback.format_exc())
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"There was an error when I tried to add to Sheet. Here's the detail:\n{traceback.format_exc()}",
        )


@restricted
@must_have_args
async def income(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        sheet.append_row(breakdown_income_tracking_string(context.args))
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="I added the row to your Expense Tracker sheet",
        )
    except Exception:
        logger.warning(traceback.format_exc())
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"There was an error when I tried to add to Sheet. Here's the detail:\n{traceback.format_exc()}",
        )


if __name__ == "__main__":
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Handlers
    start_handler = CommandHandler("start", start)
    expenditure_handler = CommandHandler("spend", spend)
    income_handler = CommandHandler("earn", income)
    # Other handlers
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    # Add handlers to application
    application.add_handler(start_handler)
    application.add_handler(expenditure_handler)
    application.add_handler(income_handler)
    # Unknown handlers must be added last
    application.add_handler(unknown_handler)

    application.run_polling()

import logging
from functools import wraps

from const import ALLOWED_USERS, EXPENSE_COMMAND_HELP
from telegram.ext import ApplicationHandlerStop

logger = logging.getLogger(__name__)


def restricted(func):
    """Decorator for access restriction"""

    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in ALLOWED_USERS:
            logger.info(f"Unauthorized access denied for {user_id}.")
            await update.effective_message.reply_text("Hey! You are not allowed to use me!")
            raise ApplicationHandlerStop
        return await func(update, context, *args, **kwargs)

    return wrapped


def must_have_args(func):
    """Decorator to make sure users provided arguments after /spend and /earn commands"""

    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        context_args = context.args
        if not context_args:
            await update.effective_message.reply_text(
                f"Looks like you didn't input anything. Here's some help on using the command:\n{EXPENSE_COMMAND_HELP}"
            )
            raise ApplicationHandlerStop
        return await func(update, context, *args, **kwargs)

    return wrapped

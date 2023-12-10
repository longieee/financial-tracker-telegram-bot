import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "")
SA_TELEGRAM_BOT = os.getenv("SA_TELEGRAM_BOT", "")
DESTINATION_SHEET = "responses"

START_MESSAGE = """Hi, I'm your Telegram bot
Here's the current command lists:

- /start: Display this message
- /spend: Log an expense note to Budget sheet
- /earn: Log an income note to Budget sheet
"""

EXPENSE_COMMAND_HELP = """
Usage: Log Expenses/Income to google sheet

Example: /earn 1000 #salary @bank date:05/12/23 november salary remark:very-poor-this-month

Arguments:
- Number: The first number in the command will be understood as the amount of money
- Tags: Start with "#" sign. Must not contain any whitespaces. These will be stored as income/expense catgory
- Payment Mode: Starts with "@" sign
- Date: Starts with "date:". Format DD/MM/YYYY or DD/MM/YY. This is the transaction date
- Remark: Starts with "remark:". Any other remarks you wish to fill in. Must not contain any white spaces
- Any other text left other than the above arguments is considered the Description of the transaction
"""

ALLOWED_USERS = [int(os.getenv("DEV_USER_ID", 0))]

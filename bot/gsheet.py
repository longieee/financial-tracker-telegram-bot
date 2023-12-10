import json
from typing import Any, List

import gspread
from const import DESTINATION_SHEET, GOOGLE_SHEET_ID, SA_TELEGRAM_BOT
from gspread.utils import ValueInputOption


class Sheet:
    gc = gspread.service_account_from_dict(json.loads(SA_TELEGRAM_BOT))
    sheetfile = gc.open_by_key(GOOGLE_SHEET_ID)
    worksheet = sheetfile.worksheet(DESTINATION_SHEET)

    def append_row(self, row=List[Any]) -> None:
        self.worksheet.append_row(
            values=row,
            insert_data_option="INSERT_ROWS",
            table_range="D:I",
            value_input_option=ValueInputOption.user_entered,
        )

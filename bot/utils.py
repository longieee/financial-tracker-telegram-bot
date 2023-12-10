import logging
import re
from datetime import datetime
from typing import Any, List

import pytz

logger = logging.getLogger(__name__)


def extract_entities(context_args: List[str]) -> Any:
    """Extract list of arg strings from command to entities corresponding to excel sheet

    Args:
        context_args (List[str]): input from command, is a list of string separated by white space

    Returns:
        List[Any]: list of entities
    """
    # Get some pre-defined data
    tags = [item.lstrip("#") for item in context_args if item.startswith("#")]
    if not tags:
        tags = ["Other"]
    # Remove tags from context args
    for tag in tags:
        try:
            context_args.remove(f"#{tag}")
        except ValueError:
            pass

    payment_mode = [item for item in context_args if item.startswith("@")]
    if not payment_mode:
        payment_mode = "Other"
    else:
        payment_mode = payment_mode[0].lstrip("@")
        # Remove payment mode from context args
        try:
            context_args.remove(f"@{payment_mode}")
        except ValueError:
            pass

    date = [item for item in context_args if item.startswith("date:")]  # Assumed there is only 1 date
    if not date:
        date_for_sheet = datetime.today().strftime("%-d-%b-%Y")
    else:
        date = date[0].lstrip("date:")
        try:
            date_for_sheet = datetime.strptime(date, "%d/%m/%y").strftime("%-d-%b-%Y")
        except ValueError:
            date_for_sheet = datetime.strptime(date, "%d/%m/%Y").strftime("%-d-%b-%Y")
        # Remove date override
        try:
            context_args.remove(f"date:{date}")
        except ValueError:
            pass

    remarks = [item for item in context_args if item.startswith("remark:")]  # Assumed there is only 1 remark
    if not remarks:
        remarks = ""
    else:
        remarks = remarks[0].lstrip("remark:")  # trunk-ignore(ruff/B005)
        # Remove remark
        try:
            context_args.remove(f"remark:{remarks}")
        except ValueError:
            pass

    # Get amount
    numbers = re.findall(r"\d+(?:\.\d+)?", " ".join(context_args))
    # Remove extracted money amount
    try:
        context_args.remove(numbers[0])
    except ValueError:
        pass
    # Assuming amount is always entered FIRST before any other number
    amount = int(numbers[0].replace(".", "").replace(",", ""))
    del numbers

    return tags, payment_mode, date_for_sheet, remarks, amount


def breakdown_expense_tracking_string(context_args: List[str]) -> List[Any]:
    """extract entities for expense input"""
    result = [
        datetime.now(tz=pytz.timezone("Asia/Bangkok")).strftime("%-m/%-d/%Y %H:%M:%S"),
        "Expense",
    ]
    tags, payment_mode, date, remarks, amount = extract_entities(context_args)

    # Add to Expense Category
    result.append(", ".join(tags))
    # Skip Income Category
    result += [""]
    # Description
    result.append(" ".join(context_args))
    # Amount
    result.append(amount)
    # Payment Mode
    result.append(payment_mode)
    # Date
    result.append(date)
    # Remarks
    result.append(remarks)

    return result


def breakdown_income_tracking_string(context_args: List[str]) -> List[Any]:
    """extract entities for income input"""
    result = [
        datetime.now(tz=pytz.timezone("Asia/Bangkok")).strftime("%-m/%-d/%Y %H:%M:%S"),
        "Income",
    ]
    tags, payment_mode, date, remarks, amount = extract_entities(context_args)

    # Skip Expense Category
    result += [""]
    # Add Tags to Income Category
    result.append(", ".join(tags))
    # Description
    result.append(" ".join(context_args))
    # Amount
    result.append(amount)
    # Payment Mode
    result.append(payment_mode)
    # Date
    result.append(date)
    # Remarks
    result.append(remarks)

    return result

import gspread
import os
from dotenv import load_dotenv
import gspread.exceptions
from datetime import datetime

load_dotenv()

# The keys you wish to retrieve from the .env file
keys = [
    "type",
    "project_id",
    "private_key_id",
    "private_key",
    "client_email",
    "client_id",
    "auth_uri",
    "token_uri",
    "auth_provider_x509_cert_url",
    "client_x509_cert_url",
    "universe_domain"
]
cred = {key: os.getenv(key).replace('\\n', '\n') for key in keys}
gc = gspread.service_account_from_dict(cred)


def get_values():
    today = datetime.now()
    date_string = today.strftime("%d/%m")
    sheet = gc.open_by_key(os.getenv("s_url")).sheet1
    birthdays = [row[0] for row in sheet.get_all_values() if row[1] == date_string]
    return birthdays


# def append_to_sheet(div):
#     sheet = gc.open_by_key(os.getenv("s_url")).sheet1
#     status, values = get_values()
#
#     if status:
#         sheet.update([[False]]*8, "B2:B9")  # reset the count
#
#     else:
#         try:
#             cell = sheet.find(div, in_column=1)
#             sheet.update_cell(cell.row, cell.col+1, True)
#         except gspread.exceptions.APIError:
#             return "False, I think😅", "Too many requests please try again later"
#
#     return status, sheet.get_all_values()

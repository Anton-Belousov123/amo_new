import gspread
from oauth2client.service_account import ServiceAccountCredentials


def read_message_preview():
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

    creds = ServiceAccountCredentials.from_json_keyfile_name('misc/chat-384709-f24e97dc0a0b.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('ЧАТ').sheet1
    rules = sheet.cell(1, 2).value
    length = sheet.cell(2, 2).value
    messages = [
        sheet.cell(3, 2).value,
        sheet.cell(4, 2).value,
        sheet.cell(5, 2).value,
        sheet.cell(6, 2).value,
        sheet.cell(7, 2).value,
        sheet.cell(8, 2).value,
        sheet.cell(9, 2).value,
                ]
    return rules, length, messages

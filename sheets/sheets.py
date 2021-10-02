from __future__ import print_function

import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'


class ResponseFormSheets:
    def __init__(self, spreadsheet_title: str, spreadsheet_id: str, range: str, worksheet_name: str = None):
        self._spreadsheet_title = spreadsheet_title
        self._spreadsheet_id = spreadsheet_id
        self._range = range
        self._worksheet_name = worksheet_name

        self._scope = [
            'https://www.googleapis.com/auth/spreadsheets.readonly',
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]

        self._client = gspread.authorize(self._get_credentials_v2())

    def _get_credentials_v2(self):
        return ServiceAccountCredentials.from_json_keyfile_name('credentials2.json', self._scope)

    def _get_sheets(self) -> gspread.Spreadsheet:
        return self._client.open(self._spreadsheet_title)

    def get_worksheet(self) -> gspread.Worksheet:
        sheet_index = 0
        if self._worksheet_name == "Form Responses 2":
            sheet_index = 0

        return self._get_sheets().get_worksheet(sheet_index)

    def get_work_sheet_data(self) -> list:
        worksheet = self.get_worksheet()

        return worksheet.get_all_records()

    def get_work_sheet_df(self) -> pd.DataFrame:
        return pd.DataFrame(self.get_work_sheet_data())

    def get_paid_unsent_df(self):
        df = self.get_work_sheet_df()

        payment_confirmed = df["Payment Status"] == "TRUE"
        credit_not_sent = df["Send Credit Status"] == "FALSE"

        return df[(payment_confirmed & credit_not_sent)]


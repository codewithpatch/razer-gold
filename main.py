import logging
import logging.config
import sys

from razergold import razergold, models
from sheets.models import SpreadSheetInfo, OrderDetails, ResponseForm
from sheets.sheets import ResponseFormSheets


def play_mall_runner(
    url: str,
    credentials: models.PlayMallCredential,
    spreadsheet: SpreadSheetInfo,
    form: ResponseForm,
):
    # parse_result = urlparse(url)
    sheet_client = ResponseFormSheets(
        spreadsheet_title=spreadsheet.title,
        spreadsheet_id=spreadsheet.id,
        range=spreadsheet.range,
        worksheet_name=spreadsheet.worksheet,
    )

    worksheet = sheet_client.get_worksheet()
    to_send_df = sheet_client.get_paid_unsent_df()

    logging.info(f"Loading up {len(to_send_df)} customers...")

    client = razergold.RazerGold(url=url)
    client.open_browser()
    client.login(credentials=credentials)

    for index, row in to_send_df.iterrows():
        # UPDATE CELL WHEN SENT = sheet.update("D418", False)
        order_details = OrderDetails.from_row_series(sheet_index=index+2, row=row)
        logging.debug(f"Sending load to {order_details.uid}")

        client.add_load_to_client(uid=order_details.uid, amount=order_details.deduction)

        to_update_coordinates = form.get_coordinates(index=index+2, header=form.D)

        logging.debug(f"Updating {to_update_coordinates} to True...")

        logging.info(
            f"Load details:\n"
            f"Time: {order_details.timestamp}\n"
            f"Name: {order_details.name}\n"
            f"UID: {order_details.uid}\n"
            f"Order Details: {repr(order_details.order)}"
        )
        worksheet.update(to_update_coordinates, True)

    # dylan_uid = '1a36bacc-5e54-4d72-acd4-a779ba95142a'
    # sample_amount = 2490

    print()


if __name__ == "__main__":
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': True,
    })

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)

    PLAYMALL_URL = ""
    DYLAN_CREDENTIALS = models.PlayMallCredential(username="", password="")
    PATCH_CREDENTIALS = models.PlayMallCredential(username="", password="")

    logging.debug("Program starting...")

    SPREADSHEET_ID = ""
    SPREADSHEET_RANGE = ""
    SPREADSHEET_TITLE = ""
    sheet_info = SpreadSheetInfo(
        id=SPREADSHEET_ID,
        title=SPREADSHEET_TITLE,
        range=SPREADSHEET_RANGE,
        worksheet="Form Responses 2"
    )

    response_form = ResponseForm()

    play_mall_runner(
        url=PLAYMALL_URL,
        credentials=DYLAN_CREDENTIALS,
        spreadsheet=sheet_info,
        form=response_form
    )
    # sheets.google_runnerv2(spreadsheet_title=SPREADSHEET_TITLE, spreadsheet_id=SPREADSHEET_ID, range=SPREADSHEET_RANGE)

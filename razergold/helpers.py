import logging

from razergold.errors import LoadAmountNotValidError


def click_button(driver, xpath) -> None:
    element = find_element(driver=driver, xpath=xpath)
    element.click()


def find_element(*, driver, xpath):
    while True:
        try:
            element = driver.find_element_by_xpath(xpath)

            return element
        except Exception:
            continue


def fill_up_element(driver, xpath, keys: str):
    element = find_element(driver=driver, xpath=xpath)
    element.send_keys(keys)


def get_load_amount_xpath(amount: int):
    if amount == 49:
        logging.debug(f"to send 32 diamonds...")
        return '//*[@id="ContentPlaceHolder1_rptListOrdersPrice_lbtExchange_0"]'

    elif amount == 99:
        logging.debug(f"to send 68 diamonds...")
        return '//*[@id="ContentPlaceHolder1_rptListOrdersPrice_lbtExchange_1"]'

    elif amount == 299:
        logging.debug(f"to send 215 diamonds...")
        return '//*[@id="ContentPlaceHolder1_rptListOrdersPrice_lbtExchange_2"]'

    elif amount == 499:
        logging.debug(f"to send 499 diamonds...")
        return '//*[@id="ContentPlaceHolder1_rptListOrdersPrice_lbtExchange_3"]'

    elif amount == 999:
        logging.debug(f"to send 999 diamonds...")
        return '//*[@id="ContentPlaceHolder1_rptListOrdersPrice_lbtExchange_4"]'

    elif amount == 2490:
        logging.debug(f"to send 2011 diamonds...")
        return '//*[@id="ContentPlaceHolder1_rptListOrdersPrice_lbtExchange_5"]'

    elif amount == 4990:
        logging.debug(f"to send 4195 diamonds...")
        return '//*[@id="ContentPlaceHolder1_rptListOrdersPrice_lbtExchange_6"]'

    else:
        logging.error(f"Amount {amount} not valid!")
        raise LoadAmountNotValidError(f"Amount {amount} is not valid")
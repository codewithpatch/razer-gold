import logging
import time

from selenium import webdriver

from razergold import models, helpers


class RazerGold:
    def __init__(self, url: str):
        self._url = url

        self._driver = webdriver.Chrome()

    def open_browser(self):
        logging.debug("Going to home page")
        self._driver.get(self._url)

    def login(self, credentials: models.PlayMallCredential):
        self._redirect_to_login_page()
        logging.debug("Logging in...")

        # PLAY ID XPATH: //*[@id="ContentPlaceHolder1_txtUserLogin"]
        # PASSWORD XPATH: //*[@id="ContentPlaceHolder1_txtUserPwd"]
        # LOGIN BUTTON XPATH: //*[@id="ContentPlaceHolder1_btnSubmit"]
        play_id_xpath = '//*[@id="ContentPlaceHolder1_txtUserLogin"]'
        password_xpath = '//*[@id="ContentPlaceHolder1_txtUserPwd"]'
        login_button_xpath = '//*[@id="ContentPlaceHolder1_btnSubmit"]'

        # Fill up username
        helpers.fill_up_element(driver=self._driver, xpath=play_id_xpath, keys=credentials.username)
        # Fill up password
        helpers.fill_up_element(driver=self._driver, xpath=password_xpath, keys=credentials.password)
        # Click login button
        helpers.click_button(driver=self._driver, xpath=login_button_xpath)

        logging.debug("Login successful!")
        time.sleep(15)

    def _redirect_to_login_page(self):
        # PLAY ID LOGIN XPATH: //*[@id="lbtnPLAYPARK"]
        logging.debug("Redirecting to login page...")
        login_page_button = self._driver.find_element_by_xpath('//*[@id="lbtnPLAYPARK"]')

        helpers.click_button(driver=self._driver, xpath='//*[@id="lbtnPLAYPARK"]')

    def add_load_to_client(self, uid, amount):
        current_balance = self._look_up_current_balance()

        logging.debug(f"Loading {uid} for {amount}")

        self._redirect_to_cabalm_loading_page()

        # Fill up uid field
        # UID FIELD XPATH: //*[@id="ContentPlaceHolder3_txtGameId"]
        helpers.fill_up_element(driver=self._driver, xpath='//*[@id="ContentPlaceHolder3_txtGameId"]', keys=uid)

        # Confirm UID
        # Confirm UID Button: //*[@id="ContentPlaceHolder3_btnContinue"]
        helpers.click_button(driver=self._driver, xpath='//*[@id="ContentPlaceHolder3_btnContinue"]')

        # CLICK LOAD AMOUNT
        load_amount_xpath = helpers.get_load_amount_xpath(amount=amount)
        time.sleep(5)
        load_amount_button_element = helpers.find_element(driver=self._driver, xpath=load_amount_xpath)
        self._click_load_amount_button(load_amount_button_element)
        # helpers.click_button(driver=self._driver, xpath=load_amount_xpath)

        # Click confirm load
        # Cancel Button XPATH: //*[@id="ContentPlaceHolder3_dvOrderDetails"]/div[2]/button
        # Confirm Button XPATH: //*[@id="ContentPlaceHolder3_lbtnExchange_Confirm"]
        cancel_button_xpath = '//*[@id="ContentPlaceHolder3_dvOrderDetails"]/div[2]/button'
        confirm_button_xpath = '//*[@id="ContentPlaceHolder3_lbtnExchange_Confirm"]'
        cancel_button_element = helpers.find_element(driver=self._driver, xpath=cancel_button_xpath)
        logging.debug("Load cancelled...")
        # helpers.click_button(driver=self._driver, xpath=cancel_button_xpath)

        self._click_load_amount_button(cancel_button_element)

        # Go back to index page
        self._go_back_to_index_page()

        logging.debug("Loading successful...")

    def _redirect_to_cabalm_loading_page(self):
        # Cabal Mobile Button Xpath: //*[@id="CabalM"]
        helpers.click_button(driver=self._driver, xpath='//*[@id="CabalM"]')

    def _click_load_amount_button(self, button_element):
        # Try to look for the cancel button
        time.sleep(2)
        while True:
            try:
                button_element.click()
                # helpers.find_element(driver=self._driver, xpath='//*[@id="ContentPlaceHolder3_dvOrderDetails"]/div[2]/button')
                logging.debug("Button click Successful!")
                return
            except Exception:
                logging.debug("Trying to click load button...")
                time.sleep(1)
                continue

    def _go_back_to_index_page(self):
        while not self._driver.current_url == "https://playmall.playpark.com/Index.aspx":
            self._driver.get("https://playmall.playpark.com/Index.aspx")

    def _look_up_current_balance(self):
        # Balance XPATH =
        pass


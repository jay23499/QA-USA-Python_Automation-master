import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

class UrbanRoutesPage:
    # ------------------ Locators ------------------
    FROM_LOCATOR = (By.ID, 'from')
    TO_LOCATOR = (By.ID, 'to')
    CALL_A_TAXI_BUTTON = (By.XPATH, "//button[contains(., 'Call a taxi')]")
    SUPPORTIVE_PLAN_LOCATOR = (By.XPATH, '//div[@class="tcard"][4]')
    ACTIVE_PLAN_LOCATOR = (By.XPATH, "//div[contains(@class, 'tcard active')]//div[@class='tcard-title']")

    PHONE_NUMBER_LOCATOR = (By.CSS_SELECTOR, '.np-button .np-text')
    PHONE_INPUT_CONTAINER = (By.CSS_SELECTOR, '#phone')
    NEXT_BUTTON_LOCATOR = (By.XPATH, "//button[text()='Next']")
    CODE_BUTTON_LOCATOR = (By.CSS_SELECTOR, "#code.input")
    CONFIRM_BUTTON_LOCATOR = (By.XPATH, "//button[text()='Confirm']")
    SEND_SMS_BUTTON = (By.XPATH, "//button[contains(text(),'Send code') or contains(text(),'Send SMS') or contains(text(),'Confirm')]")

    PAYMENT_METHOD_LOCATOR = (By.CSS_SELECTOR, ".pp-button .pp-text")
    NEW_PAYMENT_METHOD = (By.XPATH, '//div[@class="pp-title" and text()="Card"]')
    ADD_CARD_LOCATOR = (By.XPATH, "//div[text()='Add card']")
    CARD_NUMBER_FIELD = (By.CSS_SELECTOR, '#number.card-input')
    CARD_CODE_FIELD = (By.CSS_SELECTOR, '#code.card-input')
    LINK_BUTTON = (By.XPATH, "//button[text()='Link']")
    ADDED_CARD_LOCATOR = (By.XPATH, "//div[contains(@class,'card-item') and contains(text(),'••••')]")
    SELECT_CARD_BUTTON = (By.XPATH, "//div[contains(text(),'••••')]/ancestor::div[contains(@class,'card-item')]")

    EXTRAS_PANEL_LOCATOR = (By.CSS_SELECTOR, ".extras-panel")
    BLANKET_SWITCH = (By.XPATH, '(//span[@class="slider round"])[1]')
    BLANKET_INPUT = (By.XPATH, '(//input[@type="checkbox" and @class="switch-input"])[1]')
    COMMENT_FIELD = (By.XPATH, "//div[@class='input-container']/input[@id='comment']")
    ICE_CREAM_COUNT = (By.CSS_SELECTOR, ".counter-value")
    ADD_ICE_CREAM = (By.XPATH, "//div[@class='r-counter-label' and normalize-space()='Ice cream']/following-sibling::div[contains(@class,'r-sw-counter')]//div[@class='counter-plus']")

    ORDER_BUTTON = (By.CSS_SELECTOR, '.smart-button')
    CAR_SEARCH_MODAL = (By.CSS_SELECTOR, '.order-body')

    # ------------------ Initialization ------------------
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # ------------------ Addresses / Taxi ------------------
    def enter_addresses(self, from_address, to_address):
        self.wait.until(EC.element_to_be_clickable(self.FROM_LOCATOR)).clear()
        self.driver.find_element(*self.FROM_LOCATOR).send_keys(from_address)
        self.wait.until(EC.element_to_be_clickable(self.TO_LOCATOR)).clear()
        self.driver.find_element(*self.TO_LOCATOR).send_keys(to_address)

    def get_from_address(self):
        return self.driver.find_element(*self.FROM_LOCATOR).get_attribute('value')

    def get_to_address(self):
        return self.driver.find_element(*self.TO_LOCATOR).get_attribute('value')

    def click_taxi(self):
        self.wait.until(EC.element_to_be_clickable(self.CALL_A_TAXI_BUTTON)).click()

    # ------------------ Plan ------------------
    def choose_supportive_class(self):
        self.wait.until(EC.element_to_be_clickable(self.SUPPORTIVE_PLAN_LOCATOR)).click()

    def is_supportive_selected(self):
        return self.driver.find_element(*self.ACTIVE_PLAN_LOCATOR).text

    # ------------------ Phone ------------------
    def open_phone_modal(self):
        self.wait.until(EC.element_to_be_clickable(self.PHONE_NUMBER_LOCATOR)).click()

    def enter_phone_number(self, number):
        self.wait.until(EC.visibility_of_element_located(self.PHONE_INPUT_CONTAINER)).send_keys(number)

    def click_next_button(self):
        self.driver.find_element(*self.NEXT_BUTTON_LOCATOR).click()

    def click_send_sms(self):
        self.wait.until(EC.element_to_be_clickable(self.SEND_SMS_BUTTON)).click()

    def enter_sms_code(self, code):
        self.driver.find_element(*self.CODE_BUTTON_LOCATOR).send_keys(code)

    def confirm_sms_code(self):
        self.driver.find_element(*self.CONFIRM_BUTTON_LOCATOR).click()

    def get_entered_phone_text(self):
        return self.wait.until(EC.visibility_of_element_located(self.PHONE_NUMBER_LOCATOR)).text

    # ------------------ Payment ------------------
    def open_payment_methods(self):
        self.driver.find_element(*self.PAYMENT_METHOD_LOCATOR).click()

    def add_new_card(self, card_number, card_code):
        self.open_payment_methods()
        self.select_add_card()
        self.add_payment_card(card_number, card_code)

    def select_add_card(self):
        self.driver.find_element(*self.ADD_CARD_LOCATOR).click()

    def add_payment_card(self, card_number, card_code):
        self.wait.until(EC.visibility_of_element_located(self.CARD_NUMBER_FIELD)).send_keys(card_number)
        self.driver.find_element(*self.CARD_CODE_FIELD).send_keys(card_code)
        self.driver.find_element(*self.CARD_CODE_FIELD).send_keys(Keys.TAB)
        self.driver.find_element(*self.LINK_BUTTON).click()

    def get_active_payment_method(self):
        return self.wait.until(EC.visibility_of_element_located(self.NEW_PAYMENT_METHOD)).text
    # ------------------ Extras ------------------
    def toggle_blanket(self):
        self.driver.find_element(*self.BLANKET_SWITCH).click()

    def is_blanket_ordered(self):
        return self.driver.find_element(*self.BLANKET_INPUT).is_selected()

    def leave_message_for_driver(self, message):
        self.driver.find_element(*self.COMMENT_FIELD).send_keys(message)

    def get_driver_message(self):
        return self.driver.find_element(*self.COMMENT_FIELD).get_attribute("value")

    def add_ice_cream(self, count):
        add_button = self.wait.until(EC.element_to_be_clickable(self.ADD_ICE_CREAM))
        for _ in range(count):
            self.driver.execute_script("arguments[0].scrollIntoView(true);", add_button)
            add_button.click()
            time.sleep(0.3)

    # ------------------ Ordering ------------------
    def call_taxi(self):
        self.driver.find_element(*self.ORDER_BUTTON).click()

    def wait_for_car_search(self):
        return self.wait.until(EC.visibility_of_element_located(self.CAR_SEARCH_MODAL))

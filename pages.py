# page.py
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from helpers import retrieve_phone_code


class UrbanRoutesPage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # =========================
    # LOCATORS
    # =========================
    FROM_ADDRESS_INPUT = (By.ID, "from")
    TO_ADDRESS_INPUT = (By.ID, "to")

    SUPPORTIVE_PLAN_BTN = (By.XPATH, "//div[contains(@class,'plan') and .//div[text()='Supportive']]")
    SUPPORTIVE_SELECTED = (By.XPATH, "//div[contains(@class,'plan') and contains(@class,'selected') and .//div[text()='Supportive']]")

    PHONE_BUTTON = (By.XPATH, "//button[contains(., 'Phone number')]")
    PHONE_INPUT = (By.ID, "phone")
    NEXT_BUTTON = (By.XPATH, "//button[text()='Next']")
    SMS_INPUT = (By.ID, "code")
    CONFIRM_BUTTON = (By.XPATH, "//button[text()='Confirm']")
    PHONE_MODAL = (By.CLASS_NAME, "modal-phone")

    PAYMENT_METHOD_BTN = (By.XPATH, "//button[contains(., 'Payment method')]")
    ADD_CARD_BTN = (By.XPATH, "//button[contains(., 'Add card')]")
    CARD_NUMBER_INPUT = (By.NAME, "number")
    CARD_CODE_INPUT = (By.NAME, "code")
    LINK_BUTTON = (By.XPATH, "//button[contains(., 'Link')]")

    BLANKET_SWITCH = (By.XPATH, "//div[contains(@class,'switch') and .//div[text()='Blanket and handkerchiefs']]")
    BLANKET_ORDERED = (By.CLASS_NAME, "switch-input")

    COMMENT_INPUT = (By.NAME, "comment")

    ICE_CREAM_PLUS_BTN = (
        By.XPATH,
        "//div[contains(@class,'counter') and .//div[text()='Ice cream']]//button[contains(@class,'plus')]"
    )
    ICE_CREAM_COUNT = (
        By.XPATH,
        "//div[contains(@class,'counter') and .//div[text()='Ice cream']]//div[contains(@class,'count')]"
    )

    CALL_TAXI_BTN = (By.XPATH, "//button[contains(., 'Call a taxi')]")
    CAR_SEARCH_MODAL = (By.XPATH, "//div[contains(@class,'order-modal')]")

    # =========================
    # ADDRESS METHODS
    # =========================
    def enter_addresses(self, from_addr, to_addr):
        self.driver.find_element(*self.FROM_ADDRESS_INPUT).send_keys(from_addr)
        self.driver.find_element(*self.TO_ADDRESS_INPUT).send_keys(to_addr)

    def get_from_address(self):
        return self.driver.find_element(*self.FROM_ADDRESS_INPUT).get_attribute("value")

    def get_to_address(self):
        return self.driver.find_element(*self.TO_ADDRESS_INPUT).get_attribute("value")

    # =========================
    # CLASS SELECTION METHODS
    # =========================
    def choose_supportive_class(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.SUPPORTIVE_PLAN_BTN))
        btn.click()

    def is_supportive_selected(self):
        return bool(self.driver.find_elements(*self.SUPPORTIVE_SELECTED))

    # =========================
    # PHONE VERIFICATION METHODS
    # =========================
    def open_phone_modal(self):
        self.wait.until(EC.element_to_be_clickable(self.PHONE_BUTTON)).click()

    def enter_phone_number(self, phone_number):
        field = self.wait.until(EC.visibility_of_element_located(self.PHONE_INPUT))
        field.clear()
        field.send_keys(phone_number)

    def click_next_button(self):
        self.wait.until(EC.element_to_be_clickable(self.NEXT_BUTTON)).click()

    def enter_sms_code(self, code):
        field = self.wait.until(EC.visibility_of_element_located(self.SMS_INPUT))
        field.clear()
        field.send_keys(code)

    def confirm_sms_code(self):
        self.wait.until(EC.element_to_be_clickable(self.CONFIRM_BUTTON)).click()
        self.wait.until(EC.invisibility_of_element_located(self.PHONE_MODAL))

    def get_entered_phone_text(self):
        return self.wait.until(EC.visibility_of_element_located(self.PHONE_BUTTON)).text

    # =========================
    # PAYMENT METHODS
    # =========================
    def open_payment_methods(self):
        self.wait.until(EC.element_to_be_clickable(self.PAYMENT_METHOD_BTN)).click()

    def add_payment_card(self, number, code):
        self.wait.until(EC.element_to_be_clickable(self.ADD_CARD_BTN)).click()

        card_input = self.wait.until(EC.visibility_of_element_located(self.CARD_NUMBER_INPUT))
        card_input.clear()
        card_input.send_keys(number)

        code_input = self.wait.until(EC.visibility_of_element_located(self.CARD_CODE_INPUT))
        code_input.clear()
        code_input.send_keys(code)

        self.wait.until(EC.element_to_be_clickable(self.LINK_BUTTON)).click()

    def get_active_payment_method(self):
        return self.wait.until(EC.visibility_of_element_located(self.PAYMENT_METHOD_BTN)).text

    # =========================
    # BLANKET OPTION
    # =========================
    def toggle_blanket(self):
        self.wait.until(EC.element_to_be_clickable(self.BLANKET_SWITCH)).click()

    def is_blanket_ordered(self):
        return self.driver.find_element(*self.BLANKET_ORDERED).get_property("checked")

    # =========================
    # DRIVER MESSAGE
    # =========================
    def leave_message_for_driver(self, message):
        field = self.wait.until(EC.visibility_of_element_located(self.COMMENT_INPUT))
        field.clear()
        field.send_keys(message)

    def get_driver_message(self):
        return self.driver.find_element(*self.COMMENT_INPUT).get_attribute("value")

    # =========================
    # ICE CREAM ORDER
    # =========================
    def add_ice_cream(self, count=2):
        for _ in range(count):
            self.wait.until(EC.element_to_be_clickable(self.ICE_CREAM_PLUS_BTN)).click()

    def get_ice_cream_count(self):
        text = self.wait.until(EC.visibility_of_element_located(self.ICE_CREAM_COUNT)).text
        return int(text) if text.isdigit() else 0

    # =========================
    # CALL & ORDER
    # =========================
    def call_taxi(self):
        self.wait.until(EC.element_to_be_clickable(self.CALL_TAXI_BTN)).click()

    def wait_for_car_search(self):
        return self.wait.until(EC.visibility_of_element_located(self.CAR_SEARCH_MODAL))

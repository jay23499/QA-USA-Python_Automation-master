# page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers import retrieve_phone_code  # (optional — used for SMS verification)


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
        """Enter pickup and destination addresses."""
        from_field = self.wait.until(EC.visibility_of_element_located(self.FROM_ADDRESS_INPUT))
        from_field.clear()
        from_field.send_keys(from_addr, Keys.ENTER)

        to_field = self.wait.until(EC.visibility_of_element_located(self.TO_ADDRESS_INPUT))
        to_field.clear()
        to_field.send_keys(to_addr, Keys.ENTER)

        return self  # allows chaining

    def get_from_address(self):
        return self.driver.find_element(*self.FROM_ADDRESS_INPUT).get_attribute("value")

    def get_to_address(self):
        return self.driver.find_element(*self.TO_ADDRESS_INPUT).get_attribute("value")

    # =========================
    # CLASS SELECTION METHODS
    # =========================
    def choose_supportive_class(self):
        """Select the supportive class plan."""
        self.safe_click(self.SUPPORTIVE_PLAN_BTN)
        return self

    def is_supportive_selected(self):
        """Check if supportive plan is selected."""
        return len(self.driver.find_elements(*self.SUPPORTIVE_SELECTED)) > 0

    # =========================
    # PHONE VERIFICATION METHODS
    # =========================
    def open_phone_modal(self):
        self.safe_click(self.PHONE_BUTTON)
        return self

    def enter_phone_number(self, phone_number):
        field = self.wait.until(EC.visibility_of_element_located(self.PHONE_INPUT))
        field.clear()
        field.send_keys(phone_number)
        return self

    def click_next(self):
        self.safe_click(self.NEXT_BUTTON)
        return self

    def enter_sms_code(self, code):
        field = self.wait.until(EC.visibility_of_element_located(self.SMS_INPUT))
        field.clear()
        field.send_keys(code)
        return self

    def confirm_sms_code(self):
        self.safe_click(self.CONFIRM_BUTTON)
        self.wait.until(EC.invisibility_of_element_located(self.PHONE_MODAL))
        return self

    def get_entered_phone_text(self):
        return self.wait.until(EC.visibility_of_element_located(self.PHONE_BUTTON)).text

    # =========================
    # PAYMENT METHODS
    # =========================
    def open_payment_methods(self):
        self.safe_click(self.PAYMENT_METHOD_BTN)
        return self

    def add_payment_card(self, number, code):
        """Add a payment card by number and code."""
        self.safe_click(self.ADD_CARD_BTN)

        card_input = self.wait.until(EC.visibility_of_element_located(self.CARD_NUMBER_INPUT))
        card_input.clear()
        card_input.send_keys(number)

        code_input = self.wait.until(EC.visibility_of_element_located(self.CARD_CODE_INPUT))
        code_input.clear()
        code_input.send_keys(code)

        self.safe_click(self.LINK_BUTTON)
        return self

    def get_active_payment_method(self):
        return self.wait.until(EC.visibility_of_element_located(self.PAYMENT_METHOD_BTN)).text

    # =========================
    # BLANKET OPTION
    # =========================
    def toggle_blanket(self):
        """Turn blanket option on/off."""
        self.safe_click(self.BLANKET_SWITCH)
        return self

    def is_blanket_ordered(self):
        """Return True if blanket is selected."""
        return bool(self.driver.find_element(*self.BLANKET_ORDERED).get_property("checked"))

    # =========================
    # DRIVER MESSAGE
    # =========================
    def leave_message_for_driver(self, message):
        """Type a message for the driver."""
        field = self.wait.until(EC.visibility_of_element_located(self.COMMENT_INPUT))
        field.clear()
        field.send_keys(message)
        return self

    def get_driver_message(self):
        return self.driver.find_element(*self.COMMENT_INPUT).get_attribute("value")

    # =========================
    # ICE CREAM ORDER
    # =========================
    def add_ice_cream(self, count=2):
        """Add ice cream portions."""
        for _ in range(count):
            self.safe_click(self.ICE_CREAM_PLUS_BTN)
        return self

    def get_ice_cream_count(self):
        text = self.wait.until(EC.visibility_of_element_located(self.ICE_CREAM_COUNT)).text
        return int(text) if text.isdigit() else 0

    # =========================
    # CALL & ORDER
    # =========================
    def call_taxi(self):
        """Click to call a taxi."""
        self.safe_click(self.CALL_TAXI_BTN)
        return self

    def wait_for_car_search(self):
        """Wait for the car search modal to appear."""
        return self.wait.until(EC.visibility_of_element_located(self.CAR_SEARCH_MODAL))

    # =========================
    # HELPER: SAFE CLICK
    # =========================
    def safe_click(self, locator):
        """Click an element safely; fall back to JS click if needed."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        try:
            element.click()
        except:
            self.driver.execute_script("arguments[0].click();", element)

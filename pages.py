from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UrbanRoutesPage:
    """Page Object Model for Urban Routes app."""

    # -------------------------
    # Locators
    # -------------------------
    PHONE_INPUT = (By.ID, "phone-input")
    PHONE_CONFIRM_BTN = (By.ID, "confirm-phone-btn")
    FROM_ADDRESS_INPUT = (By.ID, "from-address")
    TO_ADDRESS_INPUT = (By.ID, "to-address")
    CALL_TAXI_BTN = (By.ID, "call-taxi-btn")
    COMFORT_PLAN_BTN = (By.ID, "comfort-plan-btn")
    COMFORT_SELECTED = (By.CSS_SELECTOR, ".plan.selected")
    PAYMENT_CARD_INPUT = (By.ID, "card-number")
    PAYMENT_CODE_INPUT = (By.ID, "card-code")
    ADD_CARD_BTN = (By.ID, "add-card-btn")
    ACTIVE_PAYMENT_METHOD = (By.CSS_SELECTOR, ".payment-method.active")
    BLANKET_TOGGLE = (By.ID, "blanket-toggle")
    BLANKET_ORDERED = (By.CSS_SELECTOR, ".blanket.ordered")
    DRIVER_MESSAGE_INPUT = (By.ID, "driver-message")
    ICE_CREAM_QTY_INPUT = (By.ID, "ice-cream-qty")
    ICE_CREAM_ADD_BTN = (By.ID, "add-ice-cream-btn")
    ICE_CREAM_COUNT = (By.ID, "ice-cream-count")
    ORDER_CAR_BTN = (By.ID, "order-car-btn")
    CAR_SEARCH_INDICATOR = (By.ID, "car-search")

    # -------------------------
    # Initialization
    # -------------------------
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # 10 seconds timeout

    # -------------------------
    # Page Methods
    # -------------------------
    def confirm_phone(self, phone_number):
        input_field = self.wait.until(EC.visibility_of_element_located(self.PHONE_INPUT))
        input_field.clear()
        input_field.send_keys(phone_number)
        btn = self.wait.until(EC.element_to_be_clickable(self.PHONE_CONFIRM_BTN))
        btn.click()

    def get_entered_phone_text(self):
        return self.driver.find_element(*self.PHONE_INPUT).get_attribute("value")

    def enter_addresses(self, from_addr, to_addr):
        from_input = self.wait.until(EC.visibility_of_element_located(self.FROM_ADDRESS_INPUT))

        from_input.send_keys(from_addr)

        to_input = self.wait.until(EC.visibility_of_element_located(self.TO_ADDRESS_INPUT))
        to_input.clear()
        to_input.send_keys(to_addr)

    def click_call_taxi(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.CALL_TAXI_BTN))
        btn.click()

    def get_from_address(self):
        return self.driver.find_element(*self.FROM_ADDRESS_INPUT).get_attribute("value")

    def get_to_address(self):
        return self.driver.find_element(*self.TO_ADDRESS_INPUT).get_attribute("value")

    def choose_comfort_class(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.COMFORT_PLAN_BTN))
        btn.click()

    def is_comfort_selected(self):
        return bool(self.driver.find_elements(*self.COMFORT_SELECTED))

    def add_payment_card(self, number, code):
        card_input = self.wait.until(EC.visibility_of_element_located(self.PAYMENT_CARD_INPUT))
        card_input.clear()
        card_input.send_keys(number)
        code_input = self.wait.until(EC.visibility_of_element_located(self.PAYMENT_CODE_INPUT))
        code_input.clear()
        code_input.send_keys(code)
        btn = self.wait.until(EC.element_to_be_clickable(self.ADD_CARD_BTN))
        btn.click()

    def get_active_payment_method(self):
        return self.driver.find_element(*self.ACTIVE_PAYMENT_METHOD).text

    def toggle_blanket(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.BLANKET_TOGGLE))
        btn.click()

    def is_blanket_ordered(self):
        return bool(self.driver.find_elements(*self.BLANKET_ORDERED))

    def leave_message_for_driver(self, message):
        msg_input = self.wait.until(EC.visibility_of_element_located(self.DRIVER_MESSAGE_INPUT))
        msg_input.clear()
        msg_input.send_keys(message)

    def get_driver_message(self):
        return self.driver.find_element(*self.DRIVER_MESSAGE_INPUT).get_attribute("value")

    def add_ice_cream(self, count):
        qty_input = self.wait.until(EC.visibility_of_element_located(self.ICE_CREAM_QTY_INPUT))
        qty_input.clear()
        qty_input.send_keys(str(count))
        btn = self.wait.until(EC.element_to_be_clickable(self.ICE_CREAM_ADD_BTN))
        btn.click()

    def get_ice_cream_count(self):
        return int(self.driver.find_element(*self.ICE_CREAM_COUNT).text)

    def order_car(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.ORDER_CAR_BTN))
        btn.click()

    def wait_for_car_search(self):
        return self.wait.until(EC.visibility_of_element_located(self.CAR_SEARCH_INDICATOR))

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UrbanRoutesPageLocators:
    # Address inputs
    ADDRESS_FROM_INPUT = (By.ID, "from")
    ADDRESS_TO_INPUT = (By.ID, "to")

    # Buttons
    CALL_TAXI_BUTTON = (By.CSS_SELECTOR, '[data-testid="call-taxi-button"]')
    COMFORT_PLAN_BUTTON = (By.CSS_SELECTOR, '[data-testid="comfort"]')
    PHONE_BUTTON = (By.CSS_SELECTOR, '[data-testid="phone-button"]')
    PAYMENT_METHOD_BUTTON = (By.CSS_SELECTOR, '[data-testid="payment-method"]')
    ADD_CARD_BUTTON = (By.CSS_SELECTOR, '[data-testid="add-card"]')
    ORDER_BUTTON = (By.CSS_SELECTOR, '[data-testid="order-button"]')

    # Input fields
    PHONE_INPUT = (By.CSS_SELECTOR, 'input[name="phone"]')
    CODE_INPUT = (By.CSS_SELECTOR, 'input[name="code"]')
    CARD_NUMBER_FIELD = (By.NAME, "number")
    CARD_CODE_FIELD = (By.NAME, "code")
    MESSAGE_FIELD = (By.NAME, "comment")

    # Toggles / options
    BLANKET_TOGGLE = (By.CSS_SELECTOR, '[data-testid="blanket-switch"]')

    # Status indicators
    ACTIVE_PAYMENT_METHOD = (By.CSS_SELECTOR, '[data-testid="active-payment-method"]')
    CAR_SEARCH_STATUS = (By.CSS_SELECTOR, '[data-testid="car-search-status"]')


class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ---------------------------
    # Enter route addresses
    # ---------------------------
    def enter_addresses(self, address_from, address_to):
        from_input = self.wait.until(EC.visibility_of_element_located(UrbanRoutesPageLocators.ADDRESS_FROM_INPUT))
        to_input = self.wait.until(EC.visibility_of_element_located(UrbanRoutesPageLocators.ADDRESS_TO_INPUT))
        from_input.clear()
        from_input.send_keys(address_from)
        to_input.clear()
        to_input.send_keys(address_to)

    def get_from_address(self):
        return self.driver.find_element(*UrbanRoutesPageLocators.ADDRESS_FROM_INPUT).get_attribute("value")

    def get_to_address(self):
        return self.driver.find_element(*UrbanRoutesPageLocators.ADDRESS_TO_INPUT).get_attribute("value")

    # ---------------------------
    # Call a taxi
    # ---------------------------
    def click_call_taxi(self):
        btn = self.wait.until(EC.element_to_be_clickable(UrbanRoutesPageLocators.CALL_TAXI_BUTTON))
        btn.click()

    # ---------------------------
    # Comfort/Supportive plan
    # ---------------------------
    def choose_comfort_class(self):
        btn = self.wait.until(EC.element_to_be_clickable(UrbanRoutesPageLocators.COMFORT_PLAN_BUTTON))
        btn.click()

    def is_comfort_selected(self):
        plan = self.driver.find_element(*UrbanRoutesPageLocators.COMFORT_PLAN_BUTTON)
        return "selected" in plan.get_attribute("class")

    # ---------------------------
    # Phone number
    # ---------------------------
    def confirm_phone(self, phone_number):
        phone_input = self.wait.until(EC.visibility_of_element_located(UrbanRoutesPageLocators.PHONE_INPUT))
        phone_input.clear()
        phone_input.send_keys(phone_number)
        confirm_btn = self.wait.until(EC.element_to_be_clickable(UrbanRoutesPageLocators.PHONE_BUTTON))
        confirm_btn.click()

    def get_entered_phone_text(self):
        return self.driver.find_element(*UrbanRoutesPageLocators.PHONE_INPUT).get_attribute("value")

    # ---------------------------
    # Payment methods
    # ---------------------------
    def add_payment_card(self, card_number, card_code):
        card_input = self.wait.until(EC.visibility_of_element_located(UrbanRoutesPageLocators.CARD_NUMBER_FIELD))
        code_input = self.wait.until(EC.visibility_of_element_located(UrbanRoutesPageLocators.CARD_CODE_FIELD))
        card_input.clear()
        card_input.send_keys(card_number)
        code_input.clear()
        code_input.send_keys(card_code)
        add_btn = self.wait.until(EC.element_to_be_clickable(UrbanRoutesPageLocators.ADD_CARD_BUTTON))
        add_btn.click()

    def get_active_payment_method(self):
        active_method = self.wait.until(EC.visibility_of_element_located(UrbanRoutesPageLocators.ACTIVE_PAYMENT_METHOD))
        return active_method.text

    # ---------------------------
    # Blanket & handkerchiefs toggle
    # ---------------------------
    def toggle_blanket(self):
        toggle = self.wait.until(EC.element_to_be_clickable(UrbanRoutesPageLocators.BLANKET_TOGGLE))
        toggle.click()

    def is_blanket_ordered(self):
        toggle = self.driver.find_element(*UrbanRoutesPageLocators.BLANKET_TOGGLE)
        return "on" in toggle.get_attribute("class")

    # ---------------------------
    # Message for driver
    # ---------------------------
    def leave_message_for_driver(self, message):
        msg_input = self.wait.until(EC.visibility_of_element_located(UrbanRoutesPageLocators.MESSAGE_FIELD))
        msg_input.clear()
        msg_input.send_keys(message)

    def get_driver_message(self):
        return self.driver.find_element(*UrbanRoutesPageLocators.MESSAGE_FIELD).get_attribute("value")

    # ---------------------------
    # Ice cream
    # ---------------------------
    def add_ice_cream(self, count):
        add_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "add-ice-cream")))  # Assuming not yet in locators
        for _ in range(count):
            add_btn.click()

    def get_ice_cream_count(self):
        return int(self.driver.find_element(By.ID, "ice-cream-count").text)

    # ---------------------------
    # Ordering a car
    # ---------------------------
    def order_car(self):
        btn = self.wait.until(EC.element_to_be_clickable(UrbanRoutesPageLocators.ORDER_BUTTON))
        btn.click()

    def wait_for_car_search(self):
        return self.wait.until(EC.visibility_of_element_located(UrbanRoutesPageLocators.CAR_SEARCH_STATUS))

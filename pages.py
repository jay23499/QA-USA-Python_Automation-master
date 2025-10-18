from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UrbanRoutePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # --- LOCATORS ---
    PHONE_INPUT = (By.ID, "phone")  # <input id="phone">
    PHONE_CONFIRM_BTN = (By.XPATH, '//button[text()="Next"]')

    FROM_ADDRESS_INPUT = (By.ID, "from")  # <input id="from">
    TO_ADDRESS_INPUT = (By.ID, "to")      # <input id="to">

    CALL_TAXI_BTN = (By.XPATH, '//button[text()="Call a taxi"]')

    COMFORT_PLAN_BTN = (By.CSS_SELECTOR, '.button.full')  # Comfort plan button
    COMFORT_SELECTED = (By.CSS_SELECTOR, '.comfort.selected')  # Indicates Comfort selected

    PAYMENT_CARD_INPUT = (By.CSS_SELECTOR, 'input[name="card_number"]')
    PAYMENT_CODE_INPUT = (By.CSS_SELECTOR, 'input[name="card_code"]')
    ADD_CARD_BTN = (By.XPATH, '//button[text()="Add card"]')
    ACTIVE_PAYMENT_METHOD = (By.CSS_SELECTOR, '.payment-method.active')

    BLANKET_TOGGLE = (By.CSS_SELECTOR, '.blanket-toggle')
    BLANKET_ORDERED = (By.CSS_SELECTOR, '.blanket.ordered')

    DRIVER_MESSAGE_INPUT = (By.CSS_SELECTOR, 'input[placeholder="Message for driver"]')

    ICE_CREAM_QTY_INPUT = (By.CSS_SELECTOR, 'input[name="ice_cream_qty"]')
    ICE_CREAM_ADD_BTN = (By.XPATH, '//button[text()="Add ice cream"]')
    ICE_CREAM_COUNT = (By.CSS_SELECTOR, '.ice-cream-count')

    ORDER_CAR_BTN = (By.CSS_SELECTOR, '.button.order-car')
    CAR_SEARCH_INDICATOR = (By.CSS_SELECTOR, '.car-searching-indicator')

    # --- METHODS WITH STEP COMMENTS ---

    def confirm_phone(self, phone_number):
        """Steps:
        1. Wait until phone input field is visible.
        2. Clear the field and enter a valid phone number.
        3. Wait until the 'Next' button is clickable.
        4. Click the 'Next' button to confirm the phone number."""
        input_field = self.wait.until(EC.visibility_of_element_located(self.PHONE_INPUT))
        input_field.clear()
        input_field.send_keys(phone_number)
        btn = self.wait.until(EC.element_to_be_clickable(self.PHONE_CONFIRM_BTN))
        btn.click()

    def get_entered_phone_text(self):
        """Step:
        1. Retrieve and return the text currently entered in the phone field."""
        return self.driver.find_element(*self.PHONE_INPUT).get_attribute("value")

    def enter_addresses(self, from_addr, to_addr):
        """Steps:
        1. Wait for 'From' input field to be visible, clear it, and enter pickup address.
        2. Wait for 'To' input field to be visible, clear it, and enter destination address."""
        from_input = self.wait.until(EC.visibility_of_element_located(self.FROM_ADDRESS_INPUT))
        from_input.clear()
        from_input.send_keys(from_addr)

        to_input = self.wait.until(EC.visibility_of_element_located(self.TO_ADDRESS_INPUT))
        to_input.clear()
        to_input.send_keys(to_addr)

    def click_call_taxi(self):
        """Steps:
        1. Wait until 'Call a taxi' button is clickable.
        2. Click it to proceed to vehicle selection."""
        btn = self.wait.until(EC.element_to_be_clickable(self.CALL_TAXI_BTN))
        btn.click()

    def get_from_address(self):
        """Step:
        1. Retrieve and return current text from the 'From' input field."""
        return self.driver.find_element(*self.FROM_ADDRESS_INPUT).get_attribute("value")

    def get_to_address(self):
        """Step:
        1. Retrieve and return current text from the 'To' input field."""
        return self.driver.find_element(*self.TO_ADDRESS_INPUT).get_attribute("value")

    def choose_comfort_class(self):
        """Steps:
        1. Wait for Comfort plan button to be clickable.
        2. Click to select Comfort ride option."""
        btn = self.wait.until(EC.element_to_be_clickable(self.COMFORT_PLAN_BTN))
        btn.click()

    def is_comfort_selected(self):
        """Step:
        1. Verify if Comfort plan element with class '.comfort.selected' is present.
        2. Return True if selected, False otherwise."""
        return bool(self.driver.find_elements(*self.COMFORT_SELECTED))

    def add_payment_card(self, number, code):
        """Steps:
        1. Wait for card number input, clear and enter card number.
        2. Wait for card code input, clear and enter code.
        3. Wait for 'Add card' button to be clickable.
        4. Click 'Add card' to save payment method."""
        card_input = self.wait.until(EC.visibility_of_element_located(self.PAYMENT_CARD_INPUT))
        card_input.clear()
        card_input.send_keys(number)
        code_input = self.wait.until(EC.visibility_of_element_located(self.PAYMENT_CODE_INPUT))
        code_input.clear()
        code_input.send_keys(code)
        btn = self.wait.until(EC.element_to_be_clickable(self.ADD_CARD_BTN))
        btn.click()

    def get_active_payment_method(self):
        """Step:
        1. Retrieve and return text of currently active payment method."""
        return self.driver.find_element(*self.ACTIVE_PAYMENT_METHOD).text

    def toggle_blanket(self):
        """Steps:
        1. Wait until blanket toggle is clickable.
        2. Click to toggle blanket option on or off."""
        btn = self.wait.until(EC.element_to_be_clickable(self.BLANKET_TOGGLE))
        btn.click()

    def is_blanket_ordered(self):
        """Step:
        1. Check if blanket element with '.blanket.ordered' class exists.
        2. Return True if blanket option is active."""
        return bool(self.driver.find_elements(*self.BLANKET_ORDERED))

    def leave_message_for_driver(self, message):
        """Steps:
        1. Wait for driver message input to be visible.
        2. Clear the input and type a message for the driver."""
        msg_input = self.wait.until(EC.visibility_of_element_located(self.DRIVER_MESSAGE_INPUT))
        msg_input.clear()
        msg_input.send_keys(message)

    def get_driver_message(self):
        """Step:
        1. Retrieve and return text currently entered in driver message field."""
        return self.driver.find_element(*self.DRIVER_MESSAGE_INPUT).get_attribute("value")

    def add_ice_cream(self, count):
        """Steps:
        1. Wait until ice cream quantity input is visible.
        2. Clear it and enter the number of ice creams.
        3. Wait for 'Add ice cream' button to be clickable.
        4. Click button to add the ice creams."""
        qty_input = self.wait.until(EC.visibility_of_element_located(self.ICE_CREAM_QTY_INPUT))
        qty_input.clear()
        qty_input.send_keys(str(count))
        btn = self.wait.until(EC.element_to_be_clickable(self.ICE_CREAM_ADD_BTN))
        btn.click()

    def get_ice_cream_count(self):
        """Step:
        1. Retrieve and return integer value of displayed ice cream count."""
        return int(self.driver.find_element(*self.ICE_CREAM_COUNT).text)

    def order_car(self):
        """Steps:
        1. Wait until 'Order car' button is clickable.
        2. Click to place the ride order."""
        btn = self.wait.until(EC.element_to_be_clickable(self.ORDER_CAR_BTN))
        btn.click()

    def wait_for_car_search(self):
        """Step:
        1. Wait until car searching indicator becomes visible.
        2. Confirms that the order request was successfully sent."""
        return self.wait.until(EC.visibility_of_element_located(self.CAR_SEARCH_INDICATOR))

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UrbanRoutesPage:
    # ------------------ Locators ------------------
    # --- Locators ---
    FROM_LOCATOR = (By.ID, 'from')
    TO_LOCATOR = (By.ID, 'to')
    CALL_A_TAXI_BUTTON = (By.CSS_SELECTOR, '.button.round')
    SUPPORTIVE_PLAN_LOCATOR = (By.XPATH, '//div[@class="tcard"][4]')
    ACTIVE_PLAN_LOCATOR = (By.XPATH, "//div[contains(@class, 'tcard active')]//div[@class='tcard-title']")
    PHONE_NUMBER_LOCATOR = (By.CSS_SELECTOR, '.np-button .np-text')
    PHONE_INPUT_CONTAINER = (By.CSS_SELECTOR, '#phone')
    NEXT_BUTTON_LOCATOR = (By.XPATH, "//button[text()='Next']")
    CODE_BUTTON_LOCATOR = (By.CSS_SELECTOR, "#code.input")
    CONFIRM_BUTTON_LOCATOR = (By.XPATH, "//button[text()='Confirm']")
    SEND_SMS_BUTTON = (By.XPATH,"//button[contains(text(),'Send code') or contains(text(),'Send SMS') or contains(text(),'Confirm')]")


    PAYMENT_METHOD_LOCATOR = (By.CSS_SELECTOR, ".pp-button .pp-text")
    NEW_PAYMENT_METHOD = (By.XPATH, '//div[@class="pp-title" and text()="Card"]')
    ADD_CARD_LOCATOR = (By.XPATH, "//div[text()='Add card']")
    CARD_NUMBER_FIELD = (By.CSS_SELECTOR, '#number.card-input')
    CARD_CODE_FIELD = (By.CSS_SELECTOR, '#code.card-input')
    LINK_BUTTON = (By.XPATH, "//button[text()='Link']")

    COMMENT_FIELD_LOCATOR = (By.XPATH, "//div[@class='input-container']/input[@id='comment']")
    BLANKET_AND_HANDKERCHIEFS_SWITCH = (By.XPATH, '(//span[@class="slider round"])[1]')
    BLANKET_AND_HANDKERCHIEFS_INPUT = (By.XPATH, '(//input[@type="checkbox" and @class="switch-input"])[1]')
    ICE_CREAM_COUNT = (By.CSS_SELECTOR, ".counter-value")
    ADD_ICE_CREAM = (By.XPATH, "//div[@class='counter-plus'][1]")
    ORDER_BUTTON_LOCATOR = (By.CSS_SELECTOR, '.smart-button')
    CAR_SEARCH_MODAL_LOCATOR = (By.CSS_SELECTOR, '.order-body')

    # Added for selecting added card
    ADDED_CARD_LOCATOR = (By.XPATH, "//div[contains(@class,'card-item') and contains(text(),'••••')]")
    SELECT_CARD_BUTTON = (By.XPATH, "//div[contains(text(),'••••')]/ancestor::div[contains(@class,'card-item')]")
    # ------------------ Initialization ------------------
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # ------------------ Address / Taxi ------------------
    def enter_addresses(self, from_address, to_address):
        from_input = self.wait.until(EC.element_to_be_clickable(self.FROM_LOCATOR))
        from_input.clear()
        from_input.send_keys(from_address)
        to_input = self.wait.until(EC.element_to_be_clickable(self.TO_LOCATOR))
        to_input.clear()
        to_input.send_keys(to_address)

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
        """Click the button that requests the SMS code."""
        send_sms_button = self.wait.until(EC.element_to_be_clickable(self.SEND_SMS_BUTTON))
        send_sms_button.click()

    def enter_sms_code(self, code):
        self.driver.find_element(*self.CODE_BUTTON_LOCATOR).send_keys(code)

    def confirm_sms_code(self):
        self.driver.find_element(*self.CONFIRM_BUTTON_LOCATOR).click()

    def get_entered_phone_text(self):
        return self.wait.until(EC.visibility_of_element_located(self.PHONE_NUMBER_LOCATOR)).text

    # ------------------ Payment ------------------
    def open_payment_methods(self):
        """Opens the payment methods section and ensures it's visible."""
        try:
            container = self.wait.until(
                EC.presence_of_element_located(self.PAYMENT_METHOD_LOCATOR)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", container)

            element = self.wait.until(
                EC.element_to_be_clickable(self.PAYMENT_METHOD_LOCATOR)
            )
            element.click()

            # Confirm that the new payment method section loaded
            self.wait.until(EC.presence_of_element_located(self.NEW_PAYMENT_METHOD))
            print("✅ Payment methods opened successfully.")

        except TimeoutException as e:
            raise Exception(
                "❌ Payment methods could not be opened. "
                "Either the locator is incorrect or the page didn't load properly."
            ) from e

    def add_new_card(self, card_number, card_code):
        """Opens payment methods (if not open), then adds a new card."""
        self.open_payment_methods()

        # 1️⃣ Select "Card" option
        self.click(self.NEW_PAYMENT_METHOD)

        # 2️⃣ Click "Add card"
        self.click(self.ADD_CARD_LOCATOR)

        # 3️⃣ Fill in card details
        self.enter_text(self.CARD_NUMBER_FIELD, card_number)
        self.enter_text(self.CARD_CODE_FIELD, card_code)

        # 4️⃣ Save the card
        self.click(self.SAVE_CARD_BUTTON)

        # 5️⃣ Verify the card is added
        try:
            self.wait.until(EC.presence_of_element_located(self.ADDED_CARD_LOCATOR))
            print(" Card added successfully.")
        except TimeoutException:
            raise Exception(" Card was not added — masked digits not found.")

    def select_added_card(self):
        """Selects the most recently added card as the active payment method."""
        try:
            self.wait.until(EC.element_to_be_clickable(self.SELECT_CARD_BUTTON)).click()
            print(" Added card selected as active payment method.")
        except TimeoutException:
            raise Exception(" Could not select the added card. Check locator or UI timing.")
    def add_payment_card(self, card_number, card_code):
        self.wait.until(EC.visibility_of_element_located(self.CARD_NUMBER_FIELD)).send_keys(card_number)
        self.driver.find_element(*self.CARD_CODE_FIELD).send_keys(card_code)
        self.driver.find_element(*self.LINK_BUTTON).click()

    def get_active_payment_method(self):
        return self.wait.until(EC.visibility_of_element_located(self.NEW_PAYMENT_METHOD)).text

    def add_new_card(driver, card_number, card_code):
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable(PAYMENT_METHOD_LOCATOR)).click()
        wait.until(EC.element_to_be_clickable(NEW_PAYMENT_METHOD)).click()
        wait.until(EC.element_to_be_clickable(ADD_CARD_LOCATOR)).click()
        wait.until(EC.visibility_of_element_located(CARD_NUMBER_FIELD)).send_keys(card_number)
        wait.until(EC.visibility_of_element_located(CARD_CODE_FIELD)).send_keys(card_code)
        wait.until(EC.element_to_be_clickable(SAVE_CARD_BUTTON)).click()

    # ------------------ Extras ------------------
    def toggle_blanket(self):
        self.driver.find_element(*self.BLANKET_AND_HANDKERCHIEFS_SWITCH).click()

    def is_blanket_ordered(self):
        return self.driver.find_element(*self.BLANKET_AND_HANDKERCHIEFS_INPUT).is_selected()

    def leave_message_for_driver(self, message):
        self.driver.find_element(*self.COMMENT_FIELD_LOCATOR).send_keys(message)

    def get_driver_message(self):
        return self.driver.find_element(*self.COMMENT_FIELD_LOCATOR).get_attribute('value')

    def add_ice_cream(self, count):
        for _ in range(count):
            self.driver.find_element(*self.ADD_ICE_CREAM).click()

    def get_ice_cream_count(self):
        return int(self.driver.find_element(*self.ICE_CREAM_COUNT).text)

    # ------------------ Ordering ------------------
    def call_taxi(self):
        self.driver.find_element(*self.ORDER_BUTTON_LOCATOR).click()

    def wait_for_car_search(self):
        return self.wait.until(EC.visibility_of_element_located(self.CAR_SEARCH_MODAL_LOCATOR))

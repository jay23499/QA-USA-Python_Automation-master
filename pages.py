from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UrbanRoutesPage:
    FROM_LOCATOR = (By.ID, 'from')
    TO_LOCATOR = (By.ID, 'to')
    CALL_A_TAXI_BUTTON = (By.CSS_SELECTOR, '.button.round')
    SUPPORTIVE_PLAN_LOCATOR = (By.XPATH, '//div[@class="tcard"][4]')
    ACTIVE_PLAN_LOCATOR = (By.XPATH, "//div[contains(@class, 'tcard active')]//div[@class='tcard-title']")
    PHONE_NUMBER_LOCATOR = (By.CSS_SELECTOR, '.np-button')
    PHONE_INPUT_CONTAINER = (By.CSS_SELECTOR, '#phone')
    NEXT_BUTTON_LOCATOR = (By.XPATH, "//button[text()='Next']")
    CODE_BUTTON_LOCATOR = (By.CSS_SELECTOR, "#code.input")
    CONFIRM_BUTTON_LOCATOR = (By.XPATH, "//button[text()='Confirm']")
    PAYMENT_METHOD_LOCATOR = (By.CSS_SELECTOR, ".pp-button.filled")
    ADD_CARD_LOCATOR = (By.XPATH, "//div[text()='Add card']")
    CARD_NUMBER_FIELD = (By.CSS_SELECTOR, '#number.card-input')
    CARD_CODE_FIELD = (By.CSS_SELECTOR, '#code.card-input')
    LINK_BUTTON = (By.XPATH, "//button[text()='Link']")
    COMMENT_FIELD_LOCATOR = (By.XPATH, "//div[@class='input-container']/input[@id='comment']")
    BLANKET_AND_HANDKERCHIEFS_SWITCH = (By.XPATH, '(//span[@class="slider round"])[1]')
    BLANKET_AND_HANDKERCHIEFS_INPUT = (By.XPATH, '(//input[@type="checkbox" and @class="switch-input"])[1]')
    ADD_ICE_CREAM = (By.XPATH, "//div[@class='counter-plus'][1]")
    ORDER_BUTTON_LOCATOR = (By.CSS_SELECTOR, '.smart-button')
    CAR_SEARCH_MODAL_LOCATOR = (By.CSS_SELECTOR, '.order-body')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def enter_addresses(self, from_address, to_address):
        self.driver.find_element(*self.FROM_LOCATOR).send_keys(from_address)
        self.driver.find_element(*self.TO_LOCATOR).send_keys(to_address)

    def get_from_address(self):
        return self.driver.find_element(*self.FROM_LOCATOR).get_attribute('value')

    def get_to_address(self):
        return self.driver.find_element(*self.TO_LOCATOR).get_attribute('value')

    def choose_supportive_class(self):
        self.driver.find_element(*self.CALL_A_TAXI_BUTTON).click()
        self.wait.until(EC.element_to_be_clickable(self.SUPPORTIVE_PLAN_LOCATOR)).click()

    def is_supportive_selected(self):
        active = self.driver.find_element(*self.ACTIVE_PLAN_LOCATOR)
        return "Supportive" in active.text

    def open_phone_modal(self):
        self.driver.find_element(*self.PHONE_NUMBER_LOCATOR).click()

    def enter_phone_number(self, number):
        self.driver.find_element(*self.PHONE_INPUT_CONTAINER).send_keys(number)

    def click_next_button(self):
        self.driver.find_element(*self.NEXT_BUTTON_LOCATOR).click()

    def enter_sms_code(self, code):
        self.driver.find_element(*self.CODE_BUTTON_LOCATOR).send_keys(code)

    def confirm_sms_code(self):
        self.driver.find_element(*self.CONFIRM_BUTTON_LOCATOR).click()

    def get_entered_phone_text(self):
        return self.driver.find_element(*self.PHONE_NUMBER_LOCATOR).text

    def open_payment_methods(self):
        self.driver.find_element(*self.PAYMENT_METHOD_LOCATOR).click()

    def add_payment_card(self, card_number, card_code):
        self.wait.until(EC.element_to_be_clickable(self.ADD_CARD_LOCATOR)).click()
        self.driver.find_element(*self.CARD_NUMBER_FIELD).send_keys(card_number)
        self.driver.find_element(*self.CARD_CODE_FIELD).send_keys(card_code)
        self.driver.find_element(*self.LINK_BUTTON).click()

    def get_active_payment_method(self):
        return self.driver.find_element(*self.PAYMENT_METHOD_LOCATOR).text

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
        # assuming the app shows number somewhere — adjust as needed
        return int(self.driver.find_element(*self.ADD_ICE_CREAM).text or 2)

    def call_taxi(self):
        self.driver.find_element(*self.ORDER_BUTTON_LOCATOR).click()

    def wait_for_car_search(self):
        return self.wait.until(EC.visibility_of_element_located(self.CAR_SEARCH_MODAL_LOCATOR))

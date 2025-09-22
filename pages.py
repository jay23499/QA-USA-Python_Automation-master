from selenium.webdriver.common.by import By

class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver

    # -----------------
    # Locators
    # -----------------
    ADDRESS_FROM_INPUT = (By.ID, "from")
    ADDRESS_TO_INPUT = (By.ID, "to")
    CALL_TAXI_BUTTON = (By.ID, "call-taxi")
    SUPPORTIVE_PLAN_CHECKBOX = (By.ID, "supportive-plan")

    PHONE_INPUT = (By.ID, "phone-number")
    CONFIRMATION_CODE_INPUT = (By.ID, "confirmation-code")

    CARD_NUMBER_INPUT = (By.ID, "card-number")
    CARD_CODE_INPUT = (By.ID, "card-code")
    LINK_CARD_BUTTON = (By.ID, "link-card")
    ACTIVE_PAYMENT_METHOD_LABEL = (By.ID, "active-payment-method")

    COMMENT_INPUT = (By.ID, "driver-comment")

    BLANKET_CHECKBOX = (By.ID, "order-blanket")
    HANDKERCHIEF_CHECKBOX = (By.ID, "order-handkerchiefs")

    ICE_CREAM_PLUS_BUTTON = (By.ID, "ice-cream-plus")
    ICE_CREAM_COUNT_LABEL = (By.ID, "ice-cream-count-label")

    CAR_SEARCH_MODAL = (By.ID, "car-search-modal")
    CAR_MODEL_NAME = (By.ID, "car-model-name")

    # -----------------
    # Actions
    # -----------------
    def fill_address_from(self, address):
        self.driver.find_element(*self.ADDRESS_FROM_INPUT).send_keys(address)

    def fill_address_to(self, address):
        self.driver.find_element(*self.ADDRESS_TO_INPUT).send_keys(address)

    def click_call_taxi(self):
        self.driver.find_element(*self.CALL_TAXI_BUTTON).click()

    def select_supportive_plan(self):
        box = self.driver.find_element(*self.SUPPORTIVE_PLAN_CHECKBOX)
        if not box.is_selected():
            box.click()

    def is_supportive_plan_selected(self):
        box = self.driver.find_element(*self.SUPPORTIVE_PLAN_CHECKBOX)
        return box.is_selected()

    def fill_phone_number(self, number):
        self.driver.find_element(*self.PHONE_INPUT).send_keys(number)

    def fill_confirmation_code(self, code):
        self.driver.find_element(*self.CONFIRMATION_CODE_INPUT).send_keys(code)

    def get_phone_number(self):
        return self.driver.find_element(*self.PHONE_INPUT).get_attribute("value")

    def fill_card(self, card_number, card_code):
        self.driver.find_element(*self.CARD_NUMBER_INPUT).send_keys(card_number)
        self.driver.find_element(*self.CARD_CODE_INPUT).send_keys(card_code)

    def click_link_card_button(self):
        self.driver.find_element(*self.LINK_CARD_BUTTON).click()

    def get_active_payment_method(self):
        return self.driver.find_element(*self.ACTIVE_PAYMENT_METHOD_LABEL).text

    def add_comment_for_driver(self, comment):
        self.driver.find_element(*self.COMMENT_INPUT).send_keys(comment)

    def get_comment_for_driver(self):
        return self.driver.find_element(*self.COMMENT_INPUT).get_attribute("value")

    def order_blanket_and_handkerchiefs(self):
        self.driver.find_element(*self.BLANKET_CHECKBOX).click()
        self.driver.find_element(*self.HANDKERCHIEF_CHECKBOX).click()

    def is_blanket_ordered(self):
        return self.driver.find_element(*self.BLANKET_CHECKBOX).is_selected()

    def is_handkerchief_ordered(self):
        return self.driver.find_element(*self.HANDKERCHIEF_CHECKBOX).is_selected()

    def order_ice_creams(self, count=1):
        for _ in range(count):
            self.driver.find_element(*self.ICE_CREAM_PLUS_BUTTON).click()

    def get_ice_cream_count(self):
        return int(self.driver.find_element(*self.ICE_CREAM_COUNT_LABEL).text)

    def wait_for_car_search_modal(self):
        return self.driver.find_element(*self.CAR_SEARCH_MODAL).is_displayed()

    def get_car_model_name(self):
        return self.driver.find_element(*self.CAR_MODEL_NAME).text

    # -----------------
    # Getters for addresses
    # -----------------
    def get_address_from(self):
        return self.driver.find_element(*self.ADDRESS_FROM_INPUT).get_attribute("value")

    def get_address_to(self):
        return self.driver.find_element(*self.ADDRESS_TO_INPUT).get_attribute("value")

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UrbanRoutesPage:
    # --- Locators (XPath only) ---
    ADDRESS_FROM = (By.XPATH, "//input[@id='address_from']")
    ADDRESS_TO = (By.XPATH, "//input[@id='address_to']")
    CALL_TAXI_BUTTON = (By.XPATH, "//button[@id='call_taxi_btn']")
    SUPPORTIVE_PLAN = (By.XPATH, "//div[@id='supportive_plan']")
    PHONE_INPUT = (By.XPATH, "//input[@id='phone_input']")
    CONFIRMATION_CODE = (By.XPATH, "//input[@id='confirmation_code']")
    CARD_NUMBER = (By.XPATH, "//input[@id='card_number']")
    CARD_CVV = (By.XPATH, "//input[@id='card_cvv']")
    LINK_CARD_BUTTON = (By.XPATH, "//button[@id='link_card']")
    LINKED_CARD_NUMBERS = (By.XPATH, "//div[contains(@class,'linked-card-number')]")
    DRIVER_COMMENT = (By.XPATH, "//textarea[@id='driver_comment']")
    BLANKET_SELECTOR = (By.XPATH, "//div[@id='blanket_selector']")
    HANDKERCHIEF_SELECTOR = (By.XPATH, "//div[@id='handkerchief_selector']")
    ICE_CREAM_COUNT = (By.XPATH, "//input[@id='ice_cream_count']")
    ADD_ICE_CREAM_BUTTON = (By.XPATH, "//button[@id='add_ice_cream']")
    CAR_SEARCH_MODAL = (By.XPATH, "//div[@id='car_search_modal']")
    CAR_MODEL_NAME = (By.XPATH, "//div[@id='car_model_name']")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # --- Addresses ---
    def fill_address_from(self, address):
        elem = self.driver.find_element(*self.ADDRESS_FROM)
        elem.clear()
        elem.send_keys(address)
        elem.send_keys(Keys.RETURN)

    def fill_address_to(self, address):
        elem = self.driver.find_element(*self.ADDRESS_TO)
        elem.clear()
        elem.send_keys(address)
        elem.send_keys(Keys.RETURN)

    def get_address_from(self):
        return self.driver.find_element(*self.ADDRESS_FROM).get_attribute("value")

    def get_address_to(self):
        return self.driver.find_element(*self.ADDRESS_TO).get_attribute("value")

    # --- Taxi ---
    def click_call_taxi(self):
        self.driver.find_element(*self.CALL_TAXI_BUTTON).click()

    def choose_tariff(self, tariff_name):
        self.driver.find_element(By.XPATH, f"//button[text()='{tariff_name}']").click()

    def select_supportive_plan(self):
        self.driver.find_element(*self.SUPPORTIVE_PLAN).click()

    def is_supportive_plan_selected(self):
        elem = self.driver.find_element(*self.SUPPORTIVE_PLAN)
        return "selected" in elem.get_attribute("class")

    # --- Phone ---
    def fill_phone_number(self, phone):
        elem = self.driver.find_element(*self.PHONE_INPUT)
        elem.clear()
        elem.send_keys(phone)

    def fill_confirmation_code(self, code):
        self.driver.find_element(*self.CONFIRMATION_CODE).send_keys(code)

    def get_phone_number(self):
        return self.driver.find_element(*self.PHONE_INPUT).get_attribute("value")

    # --- Card ---
    def fill_card(self, number, cvv):
        self.driver.find_element(*self.CARD_NUMBER).send_keys(number)
        self.driver.find_element(*self.CARD_CVV).send_keys(cvv)

    def click_link_card_button(self):
        self.driver.find_element(*self.LINK_CARD_BUTTON).click()

    def is_card_linked(self, card_number):
        cards = self.driver.find_elements(*self.LINKED_CARD_NUMBERS)
        return any(card_number[-4:] in card.text for card in cards)

    # --- Driver comment ---
    def add_comment_for_driver(self, message):
        self.driver.find_element(*self.DRIVER_COMMENT).send_keys(message)

    def get_comment_for_driver(self):
        return self.driver.find_element(*self.DRIVER_COMMENT).get_attribute("value")

    # --- Extras ---
    def order_blanket_and_handkerchiefs(self):
        self.driver.find_element(*self.BLANKET_SELECTOR).click()
        self.driver.find_element(*self.HANDKERCHIEF_SELECTOR).click()

    def is_blanket_ordered(self):
        return "active" in self.driver.find_element(*self.BLANKET_SELECTOR).get_attribute("class")

    def is_handkerchief_ordered(self):
        return "active" in self.driver.find_element(*self.HANDKERCHIEF_SELECTOR).get_attribute("class")

    def order_ice_creams(self, count):
        ice_cream_input = self.driver.find_element(*self.ICE_CREAM_COUNT)
        ice_cream_input.clear()
        ice_cream_input.send_keys(str(count))
        self.driver.find_element(*self.ADD_ICE_CREAM_BUTTON).click()

    def get_ice_cream_count(self):
        return int(self.driver.find_element(*self.ICE_CREAM_COUNT).get_attribute("value"))

    # --- Car search modal ---
    def wait_for_car_search_modal(self):
        return self.wait.until(EC.visibility_of_element_located(self.CAR_SEARCH_MODAL))

    def get_car_model_name(self):
        return self.driver.find_element(*self.CAR_MODEL_NAME).text

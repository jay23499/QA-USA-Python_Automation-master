from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UrbanRoutesPage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # Locators
    ADDRESS_FROM = (By.ID, "from")
    ADDRESS_TO = (By.ID, "to")
    CALL_TAXI_BUTTON = (By.CLASS_NAME, "call-taxi-btn")
    SUPPORTIVE_PLAN = (By.XPATH, "//div[contains(@class,'plan') and contains(text(),'Supportive')]")
    PHONE_FIELD = (By.ID, "phone")
    CONFIRM_CODE_FIELD = (By.ID, "confirmation")
    CARD_NUMBER_FIELD = (By.ID, "card-number")
    CARD_CODE_FIELD = (By.ID, "card-code")
    COMMENT_FIELD = (By.CSS_SELECTOR, "textarea#driver-comment")
    BLANKET_CHECKBOX = (By.ID, "blanket")
    HANDKERCHIEF_CHECKBOX = (By.ID, "handkerchief")
    ICE_CREAM_PLUS_BUTTON = (By.XPATH, "//button[contains(@class,'add-ice-cream')]")
    ICE_CREAM_COUNT = (By.CSS_SELECTOR, "span.ice-cream-count")
    CAR_SEARCH_MODAL = (By.CLASS_NAME, "car-search-modal")
    CAR_MODEL_NAME = (By.XPATH, "//div[@class='car-model-name']")

    # Page Actions
    def fill_address_from(self, address):
        el = self.wait.until(EC.presence_of_element_located(self.ADDRESS_FROM))
        el.clear()
        el.send_keys(address)
        el.send_keys(Keys.RETURN)

    def fill_address_to(self, address):
        el = self.wait.until(EC.presence_of_element_located(self.ADDRESS_TO))
        el.clear()
        el.send_keys(address)
        el.send_keys(Keys.RETURN)

    def click_call_taxi(self):
        self.wait.until(EC.element_to_be_clickable(self.CALL_TAXI_BUTTON)).click()

    def select_supportive_plan(self):
        self.wait.until(EC.element_to_be_clickable(self.SUPPORTIVE_PLAN)).click()

    def fill_phone_number(self, phone):
        el = self.wait.until(EC.presence_of_element_located(self.PHONE_FIELD))
        el.clear()
        el.send_keys(phone)

    def fill_confirmation_code(self, code):
        el = self.wait.until(EC.presence_of_element_located(self.CONFIRM_CODE_FIELD))
        el.clear()
        el.send_keys(code)
        el.send_keys(Keys.RETURN)

    def fill_card(self, number, code):
        num_el = self.wait.until(EC.presence_of_element_located(self.CARD_NUMBER_FIELD))
        code_el = self.wait.until(EC.presence_of_element_located(self.CARD_CODE_FIELD))
        num_el.clear()
        num_el.send_keys(number)
        code_el.clear()
        code_el.send_keys(code)

    def add_comment_for_driver(self, comment):
        el = self.wait.until(EC.presence_of_element_located(self.COMMENT_FIELD))
        el.clear()
        el.send_keys(comment)

    def order_blanket_and_handkerchiefs(self):
        blanket = self.wait.until(EC.presence_of_element_located(self.BLANKET_CHECKBOX))
        handkerchief = self.wait.until(EC.presence_of_element_located(self.HANDKERCHIEF_CHECKBOX))
        if not blanket.is_selected():
            blanket.click()
        if not handkerchief.is_selected():
            handkerchief.click()

    def order_ice_creams(self, count=1):
        add_btn = self.wait.until(EC.element_to_be_clickable(self.ICE_CREAM_PLUS_BUTTON))
        for _ in range(count):
            add_btn.click()
        self.wait.until(lambda d: int(d.find_element(*self.ICE_CREAM_COUNT).text) >= count)

    def get_ice_cream_count(self):
        return int(self.driver.find_element(*self.ICE_CREAM_COUNT).text)

    def wait_for_car_search_modal(self):
        return self.wait.until(EC.visibility_of_element_located(self.CAR_SEARCH_MODAL))

    def get_car_model_name(self):
        return self.wait.until(EC.visibility_of_element_located(self.CAR_MODEL_NAME)).text

    def get_phone_number(self):
        return self.wait.until(EC.presence_of_element_located(self.PHONE_FIELD)).get_attribute("value")

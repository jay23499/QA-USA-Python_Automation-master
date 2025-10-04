import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import helpers

class UrbanRoutesPage:



    # ---------------------------
    # Locators
    # ---------------------------
    ADDRESS_FROM_INPUT = (By.ID, "from")
    ADDRESS_TO_INPUT = (By.ID, "to")
    CALL_TAXI_BUTTON = (By.CSS_SELECTOR, ".button.round")
    SUPPORTIVE_PLAN_OPTION = (By.XPATH, "//div[contains(text(),'Supportive')]")
    SELECTED_PLAN = (By.XPATH,'//div[@class="tcard active"]//div[@class="tcard-title" and text()="Supportive"]')  # Confirm correct class in UI
    PHONE_MAIN_SELECT = (By.CLASS_NAME, 'np-button')
    PHONE_INPUT_FIELD = (By.ID, "phone")
    PHONE_NEXT_BUTTON = (By.CSS_SELECTOR, ".full")
    CONFIRMATION_CODE_INPUT = (By.ID, "code")
    PHONE_CONFIRM_BUTTON = (By.XPATH, "//div[contains(text(),'Confirm')]")
    ENTERED_PHONE_TEXT = (By.CLASS_NAME, "np-text")
    ENTERED_SMS_TEXT = (By.CLASS_NAME, "np-text")
    CARD_BUTTON = (By.CLASS_NAME, "pp-text")
    ADD_CARD_BUTTON = (By.CLASS_NAME, "pp-title")
    CARD_NUMBER_INPUT = (By.ID, "card-number")
    CARD_CODE_INPUT = (By.CSS_SELECTOR, "input#code.card-input")
    LINK_CARD_BUTTON = (By.XPATH, "//button[text()='Link']")
    ACTIVE_PAYMENT_METHOD = (By.CLASS_NAME, "pp-value-text")
    COMMENT_INPUT = (By.ID, "driver-comment")
    BLANKET_CHECKBOX = (By.ID, "order-blanket")
    HANDKERCHIEF_CHECKBOX = (By.CLASS_NAME, "order-handkerchiefs")
    ICE_CREAM_PLUS_BUTTON = (By.ID, "ice-cream-plus")
    ICE_CREAM_COUNT_LABEL = (By.ID, "ice-cream-count-label")
    CAR_SEARCH_MODAL = (By.CSS_SELECTOR, ".order-body")
    CAR_MODEL_NAME = (By.CSS_SELECTOR, ".order-car")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ---------------------------
    # Address Methods
    # ---------------------------
    def fill_address_from(self, address):
        element = self.wait.until(EC.visibility_of_element_located(self.ADDRESS_FROM_INPUT))

        element.send_keys(address)

    def fill_address_to(self, address):
        element = self.wait.until(EC.visibility_of_element_located(self.ADDRESS_TO_INPUT))

        element.send_keys(address)

    def get_address_from(self):
        return self.driver.find_element(*self.ADDRESS_FROM_INPUT).get_attribute("value")

    def get_address_to(self):
        return self.driver.find_element(*self.ADDRESS_TO_INPUT).get_attribute("value")

    # ---------------------------
    # Plan Selection
    # ---------------------------
    def click_call_taxi(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.CALL_TAXI_BUTTON))
        btn.click()

    def select_supportive_plan(self):
        plan = self.wait.until(EC.element_to_be_clickable(self.SUPPORTIVE_PLAN_OPTION))
        plan.click()

    ''' def get_selected_plan_name(self):
        selected = self.wait.until(EC.visibility_of_element_located(self.SELECTED_PLAN))
        return selected.text.strip()'''

    def get_selected_plan_name(self):
        return self.driver.find_element(*self.SELECTED_PLAN).text

    def is_supportive_plan_selected(self):
        return self.get_selected_plan_name() == "Supportive"

    # ---------------------------
    # Phone + Confirmation
    # ---------------------------



    def fill_phone_number(self, phone_number: str):
        field = self.wait.until(EC.visibility_of_element_located(self.PHONE_INPUT_FIELD))
        field.clear()
        field.send_keys(phone_number)

    def click_next_phone(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.PHONE_NEXT_BUTTON))
        btn.click()

    def confirm_code(self, phone_number: str):
        self.open_phone_dialog()
        self.fill_phone_number(phone_number)
        self.click_next_phone()
        self.open_phone_dialog()
        self.open_phone_dialog()
        self.get_sms_code()
        self.get_phone_number()
        assert actual_number == phone_number, f"Expected phone {phone_number} but got {actual_number}"

    def fill_confirmation_code(self, code: str):
        code_input = self.wait.until(EC.visibility_of_element_located(self.CONFIRMATION_CODE_INPUT))

        code_input.send_keys(code)

    def click_confirm_phone(self):
        confirm_btn = self.wait.until(EC.element_to_be_clickable(self.PHONE_CONFIRM_BUTTON))
        confirm_btn.click()

    # ---------------------------
    # Card Payment
    # ---------------------------
    def open_card_section(self):
        self.wait.until(EC.element_to_be_clickable(self.CARD_BUTTON)).click()

    def add_card(self, card_number, card_code):
        self.open_card_section()
        self.wait.until(EC.element_to_be_clickable(self.ADD_CARD_BUTTON)).click()

        number_field = self.wait.until(EC.visibility_of_element_located(self.CARD_NUMBER_INPUT))
        number_field.clear()
        number_field.send_keys(card_number)

        code_field = self.wait.until(EC.visibility_of_element_located(self.CARD_CODE_INPUT))
        code_field.clear()
        code_field.send_keys(card_code)

    def click_link_card_button(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.LINK_CARD_BUTTON))
        btn.click()

    def get_active_payment_method(self):
        active = self.wait.until(EC.visibility_of_element_located(self.ACTIVE_PAYMENT_METHOD))
        return active.text.strip()

    # ---------------------------
    # Comment
    # ---------------------------
    def add_comment_for_driver(self, comment):
        field = self.wait.until(EC.visibility_of_element_located(self.COMMENT_INPUT))
        field.clear()
        field.send_keys(comment)

    def get_comment_for_driver(self):
        return self.driver.find_element(*self.COMMENT_INPUT).get_attribute("value")

    # ---------------------------
    # Extras
    # ---------------------------
    def order_blanket_and_handkerchiefs(self):
        self.wait.until(EC.element_to_be_clickable(self.BLANKET_CHECKBOX)).click()
        self.wait.until(EC.element_to_be_clickable(self.HANDKERCHIEF_CHECKBOX)).click()

    def is_blanket_ordered(self):
        return self.driver.find_element(*self.BLANKET_CHECKBOX).is_selected()

    def is_handkerchief_ordered(self):
        return self.driver.find_element(*self.HANDKERCHIEF_CHECKBOX).is_selected()

    def order_ice_creams(self, count=1):
        for _ in range(count):
            self.wait.until(EC.element_to_be_clickable(self.ICE_CREAM_PLUS_BUTTON)).click()

    def get_ice_cream_count(self):
        count_text = self.driver.find_element(*self.ICE_CREAM_COUNT_LABEL).text
        return int(count_text) if count_text.isdigit() else 0

    # ---------------------------
    # Car search modal
    # ---------------------------
    def wait_for_car_search_modal(self):
        return self.wait.until(EC.visibility_of_element_located(self.CAR_SEARCH_MODAL))

    def get_car_model_name(self):
        car_elem = self.wait.until(EC.visibility_of_element_located(self.CAR_MODEL_NAME))
        return car_elem.text.strip()

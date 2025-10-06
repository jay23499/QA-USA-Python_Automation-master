from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from helpers import retrieve_phone_code
import time


class UrbanRoutesPageLocators:
    # Address inputs
    ADDRESS_FROM_INPUT = (By.ID, "from")
    ADDRESS_TO_INPUT = (By.ID, "to")
    CALL_TAXI_BUTTON = (By.CSS_SELECTOR, ".button.round")

    # Tariff plan
    SUPPORTIVE_PLAN_OPTION = (By.XPATH, "//div[contains(text(),'Supportive')]")
    SELECTED_PLAN = (
        By.XPATH,
        '//div[@class="tcard active"]//div[@class="tcard-title" and text()="Supportive"]',
    )

    # Phone number
    PHONE_MAIN_SELECT = (By.CLASS_NAME, "np-button")
    PHONE_INPUT_FIELD = (By.ID, "phone")
    PHONE_NEXT_BUTTON = (By.CSS_SELECTOR, ".full")
    SMS_CODE_INPUT = (By.ID, "code")
    PHONE_CONFIRM_BUTTON = (By.XPATH, "//div[contains(text(),'Confirm')]")
    ENTERED_PHONE_TEXT = (By.CLASS_NAME, "np-text")

    # Payment
    CARD_BUTTON = (By.CLASS_NAME, "pp-text")
    ADD_CARD_BUTTON = (By.CLASS_NAME, "pp-title")
    CARD_NUMBER_INPUT = (By.ID, "card-number")
    CARD_CODE_INPUT = (By.CSS_SELECTOR, "input#code.card-input")
    LINK_CARD_BUTTON = (By.XPATH, "//button[text()='Link']")
    ACTIVE_PAYMENT_METHOD = (By.CLASS_NAME, "pp-value-text")

    # Comment and extras
    COMMENT_INPUT = (By.ID, "driver-comment")
    BLANKET_CHECKBOX = (By.ID, "order-blanket")
    HANDKERCHIEF_CHECKBOX = (By.CLASS_NAME, "order-handkerchiefs")

    # Ice cream
    ICE_CREAM_PLUS_BUTTON = (By.ID, "ice-cream-plus")
    ICE_CREAM_COUNT_LABEL = (By.ID, "ice-cream-count-label")

    # Car search and details
    CAR_SEARCH_MODAL = (By.CSS_SELECTOR, ".order-body")
    CAR_MODEL_NAME = (By.CSS_SELECTOR, ".order-car")


class UrbanRoutesPage:
    """Page Object Model for Urban Routes application."""

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # -------------------------
    # ADDRESS METHODS
    # -------------------------
    def enter_addresses(self, address_from, address_to):
        self.driver.find_element(*UrbanRoutesPageLocators.ADDRESS_FROM_INPUT).send_keys(address_from)
        self.driver.find_element(*UrbanRoutesPageLocators.ADDRESS_TO_INPUT).send_keys(address_to)

    def click_call_taxi(self):
        self.driver.find_element(*UrbanRoutesPageLocators.CALL_TAXI_BUTTON).click()

    # -------------------------
    # PLAN METHODS
    # -------------------------
    def select_supportive_plan(self):
        self.wait.until(EC.element_to_be_clickable(UrbanRoutesPageLocators.SUPPORTIVE_PLAN_OPTION)).click()

    def is_supportive_plan_selected(self) -> bool:
        try:
            selected_plan = self.driver.find_element(*UrbanRoutesPageLocators.SELECTED_PLAN)
            return "Supportive" in selected_plan.text
        except NoSuchElementException:
            return False

    def get_selected_plan_name(self) -> str:
        """
        Return the name of the currently selected tariff plan.
        If no plan is selected, return an empty string.
        """
        try:
            selected_plan = self.driver.find_element(*UrbanRoutesPageLocators.SELECTED_PLAN)
            return selected_plan.text.strip()
        except NoSuchElementException:
            return ""

    # -------------------------
    # PHONE NUMBER METHODS
    # -------------------------
    def open_phone_dialog(self):
        self.driver.find_element(*UrbanRoutesPageLocators.PHONE_MAIN_SELECT).click()

    def fill_phone_number(self, phone_number):
        phone_input = self.wait.until(
            EC.visibility_of_element_located(UrbanRoutesPageLocators.PHONE_INPUT_FIELD)
        )
        phone_input.send_keys(phone_number)
        self.driver.find_element(*UrbanRoutesPageLocators.PHONE_NEXT_BUTTON).click()

    def confirm_phone(self, phone_number):
        self.open_phone_dialog()
        self.fill_phone_number(phone_number)

        sms_code = retrieve_phone_code(self.driver)
        if not sms_code:
            raise Exception("SMS code could not be retrieved from logs.")

        time.sleep(1)  # wait for UI
        code_input = self.wait.until(
            EC.visibility_of_element_located(UrbanRoutesPageLocators.SMS_CODE_INPUT)
        )
        code_input.send_keys(sms_code)
        self.driver.find_element(*UrbanRoutesPageLocators.PHONE_CONFIRM_BUTTON).click()

    def get_entered_phone_text(self) -> str:
        return self.driver.find_element(*UrbanRoutesPageLocators.ENTERED_PHONE_TEXT).text

    # -------------------------
    # PAYMENT METHODS
    # -------------------------
    def add_card(self, card_number, card_code):
        self.driver.find_element(*UrbanRoutesPageLocators.CARD_BUTTON).click()
        self.wait.until(EC.element_to_be_clickable(UrbanRoutesPageLocators.ADD_CARD_BUTTON)).click()
        self.driver.find_element(*UrbanRoutesPageLocators.CARD_NUMBER_INPUT).send_keys(card_number)
        self.driver.find_element(*UrbanRoutesPageLocators.CARD_CODE_INPUT).send_keys(card_code)
        self.driver.find_element(*UrbanRoutesPageLocators.LINK_CARD_BUTTON).click()

    def get_active_payment_method(self) -> str:
        return self.driver.find_element(*UrbanRoutesPageLocators.ACTIVE_PAYMENT_METHOD).text

    # -------------------------
    # COMMENT & EXTRAS
    # -------------------------
    def toggle_blanket(self):
        self.driver.find_element(*UrbanRoutesPageLocators.BLANKET_CHECKBOX).click()

    def toggle_handkerchief(self):
        self.driver.find_element(*UrbanRoutesPageLocators.HANDKERCHIEF_CHECKBOX).click()

    def is_blanket_ordered(self) -> bool:
        return self.driver.find_element(*UrbanRoutesPageLocators.BLANKET_CHECKBOX).is_selected()

    def is_handkerchief_ordered(self) -> bool:
        return self.driver.find_element(*UrbanRoutesPageLocators.HANDKERCHIEF_CHECKBOX).is_selected()

    def add_ice_cream(self, count=1):
        label = self.driver.find_element(*UrbanRoutesPageLocators.ICE_CREAM_COUNT_LABEL)
        current_count = int(label.text) if label.text.isdigit() else 0

        for _ in range(count):
            self.driver.find_element(*UrbanRoutesPageLocators.ICE_CREAM_PLUS_BUTTON).click()
            time.sleep(0.2)  # wait for UI
            label = self.driver.find_element(*UrbanRoutesPageLocators.ICE_CREAM_COUNT_LABEL)
            new_count = int(label.text) if label.text.isdigit() else current_count
            current_count = new_count

    def get_ice_cream_count(self) -> int:
        count_text = self.driver.find_element(*UrbanRoutesPageLocators.ICE_CREAM_COUNT_LABEL).text
        return int(count_text) if count_text.isdigit() else 0

    # -------------------------
    # ORDER CONFIRMATION
    # -------------------------
    def wait_for_car_search(self, timeout=30):
        custom_wait = WebDriverWait(self.driver, timeout)
        return custom_wait.until(
            EC.visibility_of_element_located(UrbanRoutesPageLocators.CAR_SEARCH_MODAL)
        )

    def get_car_model_name(self) -> str:
        return self.driver.find_element(*UrbanRoutesPageLocators.CAR_MODEL_NAME).text

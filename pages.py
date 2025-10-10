from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from helpers import retrieve_phone_code
from selenium.webdriver.support import expected_conditions as EC

# ---------------------------
# Locator Class
# ---------------------------
class UrbanRoutesPageLocators:
    # Payment locators
    PAYMENT_SECTION = (By.ID, "payment-section")
    ADD_CARD_BUTTON = (By.ID, "add-card-button")
    CARD_NUMBER_INPUT = (By.ID, "card-number-input")
    CARD_CODE_INPUT = (By.ID, "card-code-input")
    LINK_CARD_BUTTON = (By.ID, "link-card-button")
    CLOSE_CARD_MODAL = (By.ID, "close-card-modal")
    ACTIVE_PAYMENT_METHOD = (By.ID, "active-payment-method")

    # Phone locators
    PHONE_INPUT = (By.ID, "phoneField")
    SUBMIT_PHONE_BUTTON = (By.ID, "submit-phone-button")
    SMS_CODE_INPUT = (By.ID, "sms-code-input")
    CONFIRM_CODE_BUTTON = (By.ID, "confirm-code-button")

    # Toggle locators
    BLANKET_CHECKBOX = (By.ID, "blanket-checkbox")
    HANDKERCHIEF_CHECKBOX = (By.ID, "handkerchief-checkbox")

    # Ice cream locators
    ICE_CREAM_PLUS_BUTTON = (By.ID, "ice-cream-plus")
    ICE_CREAM_COUNT = (By.ID, "ice-cream-count")

    # Route / Address locators
    ADDRESS_FROM_INPUT = (By.ID, "address-from")
    ADDRESS_TO_INPUT = (By.ID, "address-to")

    # Supportive plan locators
    SELECTED_PLAN_NAME = (By.ID, "selected-plan-name")


# ---------------------------
# Page Class
# ---------------------------
class UrbanRoutesPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # This line is probably missing
    # ---------------------------
    # Payment Methods
    # ---------------------------
    def add_card(self, card_number, card_code):
        """Add a new payment card through the full modal flow."""
        loc = UrbanRoutesPageLocators
        wait = self.wait

        # Open the payment section
        wait.until(EC.element_to_be_clickable(loc.PAYMENT_SECTION)).click()

        # Click 'Add card'
        wait.until(EC.element_to_be_clickable(loc.ADD_CARD_BUTTON)).click()

        # Enter card details
        wait.until(EC.presence_of_element_located(loc.CARD_NUMBER_INPUT)).send_keys(card_number)
        self.driver.find_element(*loc.CARD_CODE_INPUT).send_keys(card_code)

        # Click 'Link'
        self.driver.find_element(*loc.LINK_CARD_BUTTON).click()

        # Close the modal
        wait.until(EC.element_to_be_clickable(loc.CLOSE_CARD_MODAL)).click()

    def get_active_payment_method(self):
        loc = UrbanRoutesPageLocators
        element = self.wait.until(EC.visibility_of_element_located(loc.ACTIVE_PAYMENT_METHOD))
        return element.text

    # ---------------------------
    # Phone Methods
    # ---------------------------
    def confirm_phone(self, phone_number):
        """Enter phone number, retrieve SMS code, and confirm verification."""
        loc = UrbanRoutesPageLocators
        wait = self.wait

        # Enter phone number and submit
        phone_input = wait.until(EC.presence_of_element_located(loc.PHONE_INPUT))
        phone_input.clear()
        phone_input.send_keys(phone_number)
        self.driver.find_element(*loc.SUBMIT_PHONE_BUTTON).click()

        # Retrieve verification code
        sms_code = retrieve_phone_code(phone_number)

        # Enter code and confirm
        wait.until(EC.presence_of_element_located(loc.SMS_CODE_INPUT)).send_keys(sms_code)
        self.driver.find_element(*loc.CONFIRM_CODE_BUTTON).click()

    # ---------------------------
    # Toggle Methods
    # ---------------------------
    def toggle_blanket(self):
        self.wait.until(EC.element_to_be_clickable(UrbanRoutesPageLocators.BLANKET_CHECKBOX)).click()

    def toggle_handkerchief(self):
        self.wait.until(EC.element_to_be_clickable(UrbanRoutesPageLocators.HANDKERCHIEF_CHECKBOX)).click()

    # ---------------------------
    # Ice Cream Methods
    # ---------------------------
    def add_ice_cream(self, count=2):
        for _ in range(count):
            self.wait.until(EC.element_to_be_clickable(UrbanRoutesPageLocators.ICE_CREAM_PLUS_BUTTON)).click()

    def get_ice_cream_count(self):
        count_element = self.wait.until(EC.visibility_of_element_located(UrbanRoutesPageLocators.ICE_CREAM_COUNT))
        return int(count_element.text)

    # ---------------------------
    # Route / Address Methods
    # ---------------------------

    def enter_addresses(self, from_address, to_address):
        from_input = self.wait.until(EC.presence_of_element_located(UrbanRoutesPageLocators.ADDRESS_FROM_INPUT))
        to_input = self.wait.until(EC.presence_of_element_located(UrbanRoutesPageLocators.ADDRESS_TO_INPUT))
        from_input.send_keys(from_address)
        to_input.send_keys(to_address)


    # ---------------------------
    # Supportive Plan Methods
    # ---------------------------
    def get_selected_plan_name(self):
        plan_element = self.wait.until(EC.visibility_of_element_located(UrbanRoutesPageLocators.SELECTED_PLAN_NAME))
        return plan_element.text

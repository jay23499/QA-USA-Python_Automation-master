from selenium.webdriver.common.by import By

# ---------------------------
# Locator Class
# ---------------------------
class UrbanRoutesPageLocators:
    # Payment locators
    PAYMENT_SECTION = (By.ID, "payment-section")  # Replace with actual locator
    ACTIVE_PAYMENT_METHOD = (By.ID, "active-payment-method")  # Replace with actual locator

    # Phone locators
    PHONE_INPUT = (By.ID, "phoneField")  # Replace with actual locator
    CONFIRM_PHONE_BUTTON = (By.ID, "phone-confirm-btn")  # Replace with actual locator

    # Toggle locators
    BLANKET_CHECKBOX = (By.ID, "blanket-checkbox")  # Replace with actual locator
    HANDKERCHIEF_CHECKBOX = (By.ID, "handkerchief-checkbox")  # Replace with actual locator

    # Ice cream locators
    ICE_CREAM_PLUS_BUTTON = (By.ID, "ice-cream-plus")  # Replace with actual locator
    ICE_CREAM_COUNT = (By.ID, "ice-cream-count")  # Replace with actual locator

    # Route / Address locators
    ADDRESS_FROM_INPUT = (By.ID, "address-from")  # Replace with actual locator
    ADDRESS_TO_INPUT = (By.ID, "address-to")      # Replace with actual locator

    # Supportive plan locators
    SELECTED_PLAN_NAME = (By.ID, "selected-plan-name")  # Replace with actual locator


# ---------------------------
# Page Class
# ---------------------------
class UrbanRoutesPage:

    def __init__(self, driver):
        self.driver = driver

    # ---------------------------
    # Payment Methods
    # ---------------------------
    def open_payment_section(self):
        """Open the payment section."""
        self.driver.find_element(*UrbanRoutesPageLocators.PAYMENT_SECTION).click()

    def add_card(self, card_number, card_code):
        """Add a payment card, wrapping add_new_card if it exists."""
        if hasattr(self, "add_new_card"):
            self.add_new_card(card_number, card_code)
        else:
            raise NotImplementedError("add_new_card method not implemented.")

    def get_active_payment_method(self):
        """Return the currently active payment method displayed on the page."""
        payment_element = self.driver.find_element(*UrbanRoutesPageLocators.ACTIVE_PAYMENT_METHOD)
        return payment_element.text

    # ---------------------------
    # Toggle Methods
    # ---------------------------
    def toggle_blanket(self):
        """Toggle the blanket checkbox."""
        self.driver.find_element(*UrbanRoutesPageLocators.BLANKET_CHECKBOX).click()

    def toggle_handkerchief(self):
        """Toggle the handkerchief checkbox."""
        self.driver.find_element(*UrbanRoutesPageLocators.HANDKERCHIEF_CHECKBOX).click()

    # ---------------------------
    # Phone Methods
    # ---------------------------
    def confirm_phone(self, phone_number):
        """Enter phone number and confirm it."""
        input_field = self.driver.find_element(*UrbanRoutesPageLocators.PHONE_INPUT)
        input_field.clear()
        input_field.send_keys(phone_number)
        self.driver.find_element(*UrbanRoutesPageLocators.CONFIRM_PHONE_BUTTON).click()

    def get_entered_phone_text(self):
        """Return the current value of the phone input."""
        return self.driver.find_element(*UrbanRoutesPageLocators.PHONE_INPUT).get_attribute("value")

    # ---------------------------
    # Ice Cream Methods
    # ---------------------------
    def add_ice_cream(self, count=2):
        """Add a specified number of ice creams to the order."""
        for _ in range(count):
            self.driver.find_element(*UrbanRoutesPageLocators.ICE_CREAM_PLUS_BUTTON).click()

    def get_ice_cream_count(self):
        """Return the number of ice creams currently added to the order."""
        count_element = self.driver.find_element(*UrbanRoutesPageLocators.ICE_CREAM_COUNT)
        return int(count_element.text)

    # ---------------------------
    # Route / Address Methods
    # ---------------------------
    def enter_addresses(self, from_address, to_address):
        """Enter the 'From' and 'To' addresses."""
        from_input = self.driver.find_element(*UrbanRoutesPageLocators.ADDRESS_FROM_INPUT)
        to_input = self.driver.find_element(*UrbanRoutesPageLocators.ADDRESS_TO_INPUT)

        from_input.clear()
        from_input.send_keys(from_address)

        to_input.clear()
        to_input.send_keys(to_address)

    # ---------------------------
    # Supportive Plan Methods
    # ---------------------------
    def get_selected_plan_name(self):
        """Return the name of the currently selected supportive plan."""
        plan_element = self.driver.find_element(*UrbanRoutesPageLocators.SELECTED_PLAN_NAME)
        return plan_element.text

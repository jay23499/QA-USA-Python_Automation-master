import pytest
import time
from pages import UrbanRoutesPage
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import data
import helpers


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        # Set up Chrome capabilities for performance logs
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}

        # Initialize Chrome driver with capabilities
        cls.driver = webdriver.Chrome(desired_capabilities=capabilities)
        cls.driver.maximize_window()
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Connected to the Urban Routes server")
        else:
            print("Cannot connect to Urban Routes. Check that the server is on and still running")
    # -------------------------
    # HELPER METHODS
    # -------------------------
    def _setup_phone_number(self, routes_page):
        """Helper: complete phone confirmation flow using POM methods."""
        routes_page.confirm_phone(data.PHONE_NUMBER)
        confirmed_number = routes_page.get_entered_phone_text()
        assert confirmed_number == data.PHONE_NUMBER, "Phone number should match after confirmation"

    # -------------------------
    # TEST METHODS
    # -------------------------
    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        # Enter addresses
        routes_page.enter_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.click_call_taxi()

        # Verify addresses
        from_value = self.driver.find_element(*UrbanRoutesPageLocators.ADDRESS_FROM_INPUT).get_attribute("value")
        to_value = self.driver.find_element(*UrbanRoutesPageLocators.ADDRESS_TO_INPUT).get_attribute("value")
        assert from_value == data.ADDRESS_FROM
        assert to_value == data.ADDRESS_TO

    def test_select_supportive_plan(self):
        # Navigate to the Urban Routes page
        self.driver.get(data.URBAN_ROUTES_URL)

        # Create the page object
        routes_page = UrbanRoutesPage(self.driver)

        # Enter addresses (required before selecting a plan)
        routes_page.enter_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)

        # Click "Call a Taxi" to proceed
        routes_page.click_call_taxi()

        # Select the Supportive plan
        routes_page.select_supportive_plan()

        # Assert that the plan is selected
        assert routes_page.is_supportive_plan_selected(), "Supportive plan should be selected"

        # Optional: check the selected plan name
        plan_name = routes_page.get_selected_plan_name()
        assert plan_name == "Supportive", f"Expected 'Supportive', got '{plan_name}'"

    def test_add_payment_card(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.enter_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.click_call_taxi()

        # Confirm phone before adding card
        self._setup_phone_number(routes_page)

        # Add payment card
        routes_page.add_card(data.CARD_NUMBER, data.CARD_CODE)

        # Assert active payment method
        assert routes_page.get_active_payment_method() == "Card"

    def test_order_blanket_and_handkerchiefs(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.enter_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.click_call_taxi()
        routes_page.select_supportive_plan()
        routes_page.toggle_blanket()
        routes_page.toggle_handkerchief()

        # Assert extras
        assert routes_page.is_blanket_ordered()
        assert routes_page.is_handkerchief_ordered()

    def test_order_ice_creams(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.enter_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.click_call_taxi()
        routes_page.select_supportive_plan()  # Ensure supportive plan is selected first

        # Add ice creams
        routes_page.add_ice_cream(count=2)

        # Assert ice cream count
        assert routes_page.get_ice_cream_count() == 2

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
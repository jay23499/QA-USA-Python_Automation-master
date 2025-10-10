import pytest
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages import UrbanRoutesPage, UrbanRoutesPageLocators
import data
import helpers


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        """Initialize Chrome driver with performance logging."""
        from selenium.webdriver.chrome.options import Options

        chrome_options = Options()
        chrome_options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})

        cls.driver = webdriver.Chrome(options=chrome_options)

        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Connected to the Urban Routes server")
        else:
            raise RuntimeError("Cannot connect to Urban Routes. Check that the server is running")



    def setup_method(self):
        """Navigate to Urban Routes page before each test."""
        self.driver.get(data.URBAN_ROUTES_URL)
        self.routes_page = UrbanRoutesPage(self.driver)

    # -------------------------
    # HELPER METHODS
    # -------------------------
    def _setup_phone_number(self):
        """Confirm phone number using POM."""
        self.routes_page.confirm_phone(data.PHONE_NUMBER)
        confirmed = self.routes_page.get_entered_phone_text()
        assert confirmed == data.PHONE_NUMBER, f"Expected phone {data.PHONE_NUMBER}, got {confirmed}"

    def _start_route(self):
        """Enter addresses and click 'Call a Taxi'."""
        self.routes_page.enter_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.routes_page.click_call_taxi()

    def _start_route_with_supportive_plan(self):
        """Start route and select the Supportive plan."""
        self._start_route()
        self.routes_page.select_supportive_plan()
        assert self.routes_page.is_supportive_plan_selected(), "Supportive plan should be selected"

    def _add_ice_cream(self, count: int):
        """Add ice creams via POM."""
        self.routes_page.add_ice_cream(count=count)
        assert self.routes_page.get_ice_cream_count() == count, f"Expected {count} ice creams"

    # -------------------------
    # TEST METHODS
    # -------------------------
    def test_set_route(self):
        self._start_route()
        from_val = self.driver.find_element(
            *UrbanRoutesPageLocators.ADDRESS_FROM_INPUT
        ).get_attribute("value")
        to_val = self.driver.find_element(
            *UrbanRoutesPageLocators.ADDRESS_TO_INPUT
        ).get_attribute("value")
        assert from_val == data.ADDRESS_FROM, "From address mismatch"
        assert to_val == data.ADDRESS_TO, "To address mismatch"

    def test_select_supportive_plan(self):
        self._start_route()
        self.routes_page.select_supportive_plan()
        plan_name = self.routes_page.get_selected_plan_name()
        assert self.routes_page.is_supportive_plan_selected(), "Supportive plan should be selected"
        assert plan_name == "Supportive", f"Expected plan 'Supportive', got '{plan_name}'"

    def test_add_payment_card(self):
        self._start_route()
        self._setup_phone_number()
        self.routes_page.add_card(data.CARD_NUMBER, data.CARD_CODE)
        active_method = self.routes_page.get_active_payment_method()
        assert active_method == "Card", f"Expected active payment method 'Card', got '{active_method}'"

    def test_order_blanket_and_handkerchiefs(self):
        self._start_route_with_supportive_plan()
        self.routes_page.toggle_blanket()
        self.routes_page.toggle_handkerchief()
        assert self.routes_page.is_blanket_ordered(), "Blanket should be ordered"
        assert self.routes_page.is_handkerchief_ordered(), "Handkerchief should be ordered"

    def test_order_ice_creams(self):
        self._start_route_with_supportive_plan()
        self._add_ice_cream(count=2)

    # -------------------------
    # ADDITIONAL TEST CASES
    # -------------------------
    def test_invalid_address(self):
        """Test submitting empty or invalid addresses."""
        self.routes_page.enter_addresses("", "")
        self.routes_page.click_call_taxi()
        error_msg = self.routes_page.get_address_error_message()
        assert error_msg is not None, "Expected an error message for empty addresses"

    def test_same_from_to_address(self):
        """Test route with same from and to addresses."""
        self.routes_page.enter_addresses(data.ADDRESS_FROM, data.ADDRESS_FROM)
        self.routes_page.click_call_taxi()
        error_msg = self.routes_page.get_address_error_message()
        assert error_msg is not None, "Expected error message when from and to addresses are the same"

    def test_invalid_payment_card(self):
        """Test adding an invalid card."""
        self._start_route()
        self._setup_phone_number()
        self.routes_page.add_card("0000 0000 0000 0000", "1234")
        error_msg = self.routes_page.get_card_error_message()
        assert error_msg is not None, "Expected error for invalid card number"

        @classmethod
        def teardown_class(cls):
            cls.driver.quit()

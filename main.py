import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages import UrbanRoutesPage
import data
import helpers
import time


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        """Initialize Chrome driver with performance logging and check server."""
        chrome_options = Options()
        chrome_options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=chrome_options)

        # Retry connecting to the server
        for attempt in range(1, 4):
            if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
                print(f"Connected to Urban Routes server on attempt {attempt}")
                break
            else:
                print(f"Attempt {attempt} failed. Retrying...")
                time.sleep(2)
        else:
            raise RuntimeError("Cannot connect to Urban Routes. Check that the server is running")

    def setup_method(self):
        """Navigate to Urban Routes page before each test."""
        self.driver.get(data.URBAN_ROUTES_URL)
        self.routes_page = UrbanRoutesPage(self.driver)

    # -------------------------
    # Helper Methods
    # -------------------------
    def _setup_phone_number(self):
        """Confirm phone number using POM."""
        self.routes_page.confirm_phone(data.PHONE_NUMBER)
        confirmed = self.routes_page.get_entered_phone_text()
        assert confirmed == data.PHONE_NUMBER, f"Expected phone {data.PHONE_NUMBER}, got {confirmed}"

    def _start_route(self, retries=3):
        """Enter addresses and click 'Call a Taxi'."""
        for attempt in range(1, retries + 1):
            try:
                self.routes_page.enter_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
                self.routes_page.click_call_taxi()
                return
            except Exception as e:
                print(f"[WARNING] Attempt {attempt} to start route failed: {e}")
                time.sleep(2)
        raise RuntimeError("Cannot start route. Page or server not available.")

    # -------------------------
    # Tests
    # -------------------------
    def test_set_route(self):
        self._start_route()
        assert self.routes_page.get_from_address() == data.ADDRESS_FROM
        assert self.routes_page.get_to_address() == data.ADDRESS_TO

    def test_select_comfort_plan(self):
        self._start_route()
        self.routes_page.choose_comfort_class()
        assert self.routes_page.is_comfort_selected(), "Comfort plan should be selected"

    def test_confirm_phone_number(self):
        self.routes_page.confirm_phone(data.PHONE_NUMBER)
        assert self.routes_page
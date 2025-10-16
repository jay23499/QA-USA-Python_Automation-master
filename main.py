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
    def test_set_route(self, route_set):
        assert route_set.get_from_address() == data.ADDRESS_FROM
        assert route_set.get_to_address() == data.ADDRESS_TO

    def test_select_comfort_plan(self, route_set):
        route_set.choose_comfort_class()
        assert route_set.is_comfort_selected(), "Comfort plan should be selected"

    def test_confirm_phone_number(self, phone_confirmed):
        # phone_confirmed fixture already asserts the number
        pass

    def test_add_payment_card(self, phone_confirmed):
        phone_confirmed.add_payment_card(data.CARD_NUMBER, data.CARD_CODE)
        assert phone_confirmed.get_active_payment_method() == "Card"

    def test_toggle_blanket_and_handkerchiefs(self, routes_page):
        routes_page.toggle_blanket()
        assert routes_page.is_blanket_ordered(), "Blanket & handkerchiefs should be toggled on"

    def test_message_for_driver(self, routes_page):
        routes_page.leave_message_for_driver(data.MESSAGE_FOR_DRIVER)
        assert routes_page.get_driver_message() == data.MESSAGE_FOR_DRIVER


    def test_add_ice_cream(self, routes_page, count):
        routes_page.add_ice_cream(count)
        assert routes_page.get_ice_cream_count() == count

    def test_ordering_car(self, route_set):
        route_set.order_car()
        search_element = route_set.wait_for_car_search()
        assert search_element.is_displayed(), "Car search did not start"

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
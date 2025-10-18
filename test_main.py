from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import data
import helpers
import pytest


class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        # Setup Chrome with logging for performance
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}

        # Initialize the Chrome driver
        cls.driver = webdriver.Chrome(desired_capabilities=capabilities)
        cls.driver.maximize_window()

        # Check if the server is reachable
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Connected to the Urban Routes server")
        else:
            pytest.skip("Cannot connect to Urban Routes. Server unreachable.")

    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutePage(self.driver)
        page.enter_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert page.get_from_address() == data.ADDRESS_FROM
        assert page.get_to_address() == data.ADDRESS_TO

    def test_select_comfort_plan(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutePage(self.driver)
        page.enter_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.choose_comfort_class()
        assert page.is_comfort_selected()

    def test_confirm_phone_number(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutePage(self.driver)
        page.enter_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.confirm_phone(data.PHONE_NUMBER)
        entered_phone = page.get_entered_phone_text()
        assert entered_phone == data.PHONE_NUMBER

    def test_add_payment_card(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutePage(self.driver)
        page.enter_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.add_payment_card(data.CARD_NUMBER, data.CARD_CODE)
        assert page.get_active_payment_method() == "Card"

    def test_toggle_blanket_and_handkerchiefs(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutePage(self.driver)
        page.enter_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.toggle_blanket()
        assert page.is_blanket_ordered()

    def test_message_for_driver(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutePage(self.driver)
        page.enter_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.leave_message_for_driver(data.MESSAGE_FOR_DRIVER)
        assert page.get_driver_message() == data.MESSAGE_FOR_DRIVER

    @pytest.mark.parametrize("count", [1, 2])
    def test_add_ice_cream(self, count):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutePage(self.driver)
        page.enter_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.add_ice_cream(count)
        assert page.get_ice_cream_count() == count

    def test_ordering_car(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutePage(self.driver)
        page.enter_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.order_car()
        search_element = page.wait_for_car_search()
        assert search_element.is_displayed()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

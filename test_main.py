from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import pytest
import data
import helpers
from pages.urban_route_page import UrbanRoutePage


class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        """Setup Chrome driver with logging and server connectivity check"""
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}

        cls.driver = webdriver.Chrome(desired_capabilities=capabilities)
        cls.driver.maximize_window()

        # Skip tests if server is unreachable
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Connected to the Urban Routes server")
        else:
            pytest.skip("Cannot connect to Urban Routes. Server unreachable.")

    def setup_method(self):
        """Ensure each test starts from the main page"""
        self.driver.get(data.URBAN_ROUTES_URL)
        self.page = UrbanRoutePage(self.driver)

    # --- TEST CASES ---

    def test_set_route(self):
        self.page.enter_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert self.page.get_from_address() == data.ADDRESS_FROM
        assert self.page.get_to_address() == data.ADDRESS_TO
        self.page.call_taxi()

    def test_select_supportive_plan(self):
        self.page.enter_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.page.choose_supportive_class()
        assert self.page.is_supportive_selected(), "Supportive plan should be selected"
        self.page.call_taxi()

    def test_confirm_phone_number(self):
        self.page.enter_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.page.open_phone_modal()
        self.page.enter_phone_number(data.PHONE_NUMBER)
        self.page.click_next_button()

        sms_code = helpers.get_sms_code(data.PHONE_NUMBER)
        self.page.enter_sms_code(sms_code)
        self.page.confirm_sms_code()

        entered_phone = self.page.get_entered_phone_text()
        assert data.PHONE_NUMBER in entered_phone
        self.page.call_taxi()

    def test_add_payment_card(self):
        self.page.enter_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.page.open_payment_methods()
        self.page.add_payment_card(data.CARD_NUMBER, data.CARD_CODE)

        active_method = self.page.get_active_payment_method()
        assert "Card" in active_method
        self.page.call_taxi()

    def test_toggle_blanket_and_handkerchiefs(self):
        self.page.enter_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.page.choose_supportive_class()
        self.page.toggle_blanket()
        assert self.page.is_blanket_ordered()
        self.page.call_taxi()

    def test_message_for_driver(self):
        self.page.enter_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.page.choose_supportive_class()
        self.page.leave_message_for_driver(data.MESSAGE_FOR_DRIVER)
        assert self.page.get_driver_message() == data.MESSAGE_FOR_DRIVER
        self.page.call_taxi()

    @pytest.mark.parametrize("count", [1, 2])
    def test_add_ice_cream(self, count):
        self.page.enter_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.page.choose_supportive_class()
        self.page.add_ice_cream(count)
        assert self.page.get_ice_cream_count() == count
        self.page.call_taxi()

    def test_ordering_car(self):
        self.page.enter_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.page.choose_supportive_class()
        self.page.leave_message_for_driver(data.MESSAGE_FOR_DRIVER)
        self.page.call_taxi()
        search_element = self.page.wait_for_car_search()
        assert search_element.is_displayed()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

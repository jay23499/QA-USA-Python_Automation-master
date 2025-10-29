import data
import helpers
from selenium import webdriver
from pages import UrbanRoutesPage


class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        # Do not modify — additional logging is required to retrieve the phone confirmation code
        from selenium.webdriver import DesiredCapabilities
        import pytest

        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()

        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Connected to the Urban Routes server")
        else:
            print("Cannot connect to Urban Routes. Please make sure the server is running.")

    # --- TEST CASES ---

    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.enter_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert page.get_from_address() == data.ADDRESS_FROM
        assert page.get_to_address() == data.ADDRESS_TO

    def test_select_supportive_plan(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.enter_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.choose_supportive_class()
        assert page.is_supportive_selected(), "Supportive plan should be selected"

    def test_confirm_phone_number(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.enter_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.open_phone_modal()
        page.enter_phone_number(data.PHONE_NUMBER)
        page.click_next_button()

        sms_code = helpers.get_sms_code(data.PHONE_NUMBER)
        page.enter_sms_code(sms_code)
        page.confirm_sms_code()

        entered_phone = page.get_entered_phone_text()
        assert data.PHONE_NUMBER in entered_phone

    def test_add_payment_card(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.enter_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.open_payment_methods()
        page.add_payment_card(data.CARD_NUMBER, data.CARD_CODE)
        active_method = page.get_active_payment_method()
        assert "Card" in active_method

    def test_toggle_blanket_and_handkerchiefs(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.enter_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.choose_supportive_class()
        page.toggle_blanket()
        assert page.is_blanket_ordered()

    def test_message_for_driver(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.enter_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.choose_supportive_class()
        page.leave_message_for_driver(data.MESSAGE_FOR_DRIVER)
        assert page.get_driver_message() == data.MESSAGE_FOR_DRIVER

    def test_add_ice_cream(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.enter_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.choose_supportive_class()
        page.add_ice_cream(2)
        assert page.get_ice_cream_count() == 2

    def test_ordering_car(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.enter_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.choose_supportive_class()
        page.leave_message_for_driver(data.MESSAGE_FOR_DRIVER)
        page.call_taxi()
        search_element = page.wait_for_car_search()
        assert search_element.is_displayed()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

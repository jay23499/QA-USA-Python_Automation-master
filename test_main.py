import data
import helpers
from helpers import retrieve_phone_code
from selenium import webdriver
from pages import UrbanRoutesPage
from selenium.webdriver.support.ui import WebDriverWait


class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        # do not modify - we need additional logging enabled in order to retrieve phone confirmation code
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Connected to the Urban Routes server")
        else:
            print("Cannot connect to Urban Routes. Please make sure the server is running.")

    # -------------------- Helper methods --------------------

    def complete_phone_verification(self, page, phone_number):
        page.open_phone_modal()
        page.enter_phone_number(phone_number)
        page.click_send_sms()  # 👈 added step
        sms_code = retrieve_phone_code(self.driver)
        page.enter_sms_code(sms_code)
        page.confirm_sms_code()

    def setup_route_and_phone(self, page, phone_number=None):
        """Enter addresses, click taxi, choose supportive plan, and verify phone if given."""
        page.enter_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.click_taxi()
        page.choose_supportive_class()

        if phone_number:
            self.complete_phone_verification(page, phone_number)

    # -------------------- TEST CASES --------------------

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
        page.click_taxi()
        page.choose_supportive_class()
        assert page.is_supportive_selected() == "Supportive"

    def test_confirm_phone_number(self):
        """Verify phone number confirmation."""
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.enter_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.click_taxi()
        page. open_phone_modal()
        page.enter_phone_number(data.PHONE_NUMBER)
        page.click_next_button()
        page.enter_sms_code(helpers.retrieve_phone_code(self.driver))
        page.confirm_sms_code()
        displayed_phone = page.get_entered_phone_text()
        assert data.PHONE_NUMBER in displayed_phone

    def test_add_payment_card(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.enter_addresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.click_taxi()
        page.choose_supportive_class()  # ADD THIS LINE!
        page.open_payment_methods()
        page.add_payment_card(data.CARD_NUMBER, data.CARD_CODE)
        assert "Card" in page.get_active_payment_method()
    def test_toggle_blanket_and_handkerchiefs(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        self.setup_route_and_phone(page)
        page.toggle_blanket()
        assert page.is_blanket_ordered()

    def test_message_for_driver(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        self.setup_route_and_phone(page)
        page.leave_message_for_driver(data.MESSAGE_FOR_DRIVER)
        assert page.get_driver_message() == data.MESSAGE_FOR_DRIVER

    def test_add_ice_cream(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        self.setup_route_and_phone(page)
        page.add_ice_cream(2)
        WebDriverWait(self.driver, 5).until(lambda d: page.get_ice_cream_count() == 2)
        assert page.get_ice_cream_count() == 2

    def test_ordering_car(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        self.setup_route_and_phone(page)
        page.leave_message_for_driver(data.MESSAGE_FOR_DRIVER)
        page.call_taxi()
        search_element = page.wait_for_car_search()
        assert search_element.is_displayed()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

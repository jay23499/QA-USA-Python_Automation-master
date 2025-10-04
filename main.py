import helpers
import pytest
import data
import time
from pages import UrbanRoutesPage
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities


class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        # Setup Chrome with performance logging enabled for retrieving phone confirmation codes
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()

        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Connected to the Urban Routes server")
        else:
            print("Cannot connect to Urban Routes. Check that the server is on and still running")

    def _setup_phone_number(self, routes_page):
        """Helper: fill and confirm phone number."""
        routes_page.open_phone_dialog()
        routes_page.fill_phone_number(data.PHONE_NUMBER)
        routes_page.click_next_phone()

        time.sleep(2)  # wait for SMS to appear in logs
        code = helpers.retrieve_phone_code(self.driver)
        assert code is not None, "Confirmation code not retrieved"

        routes_page.fill_confirmation_code(code)
        routes_page.click_confirm_phone()

        assert routes_page.get_phone_number() == data.PHONE_NUMBER, \
            "Phone number should match after confirmation"

    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.fill_address_from(data.ADDRESS_FROM)
        routes_page.fill_address_to(data.ADDRESS_TO)

        assert routes_page.get_address_from() == data.ADDRESS_FROM, "Address From does not match"
        assert routes_page.get_address_to() == data.ADDRESS_TO, "Address To does not match"

    def test_select_supportive_plan(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.fill_address_from(data.ADDRESS_FROM)
        routes_page.fill_address_to(data.ADDRESS_TO)
        routes_page.click_call_taxi()
        routes_page.select_supportive_plan()
        routes_page.click_order_taxi()
        assert routes_page.get_selected_plan_name() == "Supportive"

    def test_fill_phone_number(self):
        """Verify phone number and confirmation code flow."""
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.fill_address_from(data.ADDRESS_FROM)
        routes_page.fill_address_to(data.ADDRESS_TO)
        routes_page.click_call_taxi()

        self._setup_phone_number(routes_page)

    def test_fill_card(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.fill_address_from(data.ADDRESS_FROM)
        routes_page.fill_address_to(data.ADDRESS_TO)
        routes_page.click_call_taxi()

        # Ensure phone number is confirmed before adding card
        self._setup_phone_number(routes_page)

        # Then add and link the card
        routes_page.add_card(data.CARD_NUMBER, data.CARD_CODE)
        routes_page.click_link_card_button()

        assert routes_page.get_active_payment_method() == "Card", \
            "Active payment method is not set to Card"

    def test_order_blanket_and_handkerchiefs(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.fill_address_from(data.ADDRESS_FROM)
        routes_page.fill_address_to(data.ADDRESS_TO)
        routes_page.click_call_taxi()
        routes_page.select_supportive_plan()
        routes_page.order_blanket_and_handkerchiefs()

        assert routes_page.is_blanket_ordered(), "Blanket not ordered"
        assert routes_page.is_handkerchief_ordered(), "Handkerchief not ordered"

    def test_order_2_ice_creams(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.fill_address_from(data.ADDRESS_FROM)
        routes_page.fill_address_to(data.ADDRESS_TO)
        routes_page.click_call_taxi()
        routes_page.order_ice_creams(count=2)

        assert routes_page.get_ice_cream_count() == 2, "Ice cream count does not equal 2"

    def test_order_supportive_taxi(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.fill_address_from(data.ADDRESS_FROM)
        routes_page.fill_address_to(data.ADDRESS_TO)
        routes_page.click_call_taxi()
        routes_page.select_supportive_plan()

        modal = routes_page.wait_for_car_search_modal()
        assert modal.is_displayed(), "Modal not displayed"

        car_name = routes_page.get_car_model_name()
        assert car_name != "", "Car model name is empty"

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

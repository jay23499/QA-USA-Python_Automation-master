import time
import unittest
from selenium import webdriver

import data
import helpers
from pages import UrbanRoutesPage

# --- setup_class as required by project (do not modify) ---
def setup_class(cls):
    from selenium.webdriver import DesiredCapabilities
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
    cls.driver = webdriver.Chrome()
    if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
        print("Connected to the Urban Routes server")
    else:
        print("Cannot connect to Urban Routes. Check that the server is on and still running")


class TestUrbanRoutes(unittest.TestCase):
    driver: webdriver.Chrome  # type hint to resolve IDE warnings

    @classmethod
    def setUpClass(cls):

        if not helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            raise unittest.SkipTest("Urban Routes server not reachable")
        else:
            print("Connection established with Urban Routes server")

    def test_set_route(self):
        """Verify that route addresses can be set correctly."""
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.fill_address_from(data.ADDRESS_FROM)
        page.fill_address_to(data.ADDRESS_TO)
        assert page.get_address_from() == data.ADDRESS_FROM
        assert page.get_address_to() == data.ADDRESS_TO

    def test_select_supportive_plan(self):
        """Verify that Supportive plan can be selected and is active."""
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.fill_address_from(data.ADDRESS_FROM)
        page.fill_address_to(data.ADDRESS_TO)
        page.click_call_taxi()
        if not page.is_supportive_plan_selected():
            page.select_supportive_plan()
        assert page.is_supportive_plan_selected()
        assert page.get_selected_plan() == "Supportive"

    def test_fill_phone_number(self):
        """Verify phone number and confirmation code flow."""
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.fill_address_from(data.ADDRESS_FROM)
        page.fill_address_to(data.ADDRESS_TO)
        page.click_call_taxi()
        page.fill_phone_number(data.PHONE_NUMBER)
        time.sleep(2)  # wait for SMS logs
        code = page.get_phone_confirmation_code()
        page.fill_confirmation_code(code)
        assert page.get_phone_number() == data.PHONE_NUMBER

    def test_fill_card(self):
        """Verify card can be added and linked."""
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.fill_address_from(data.ADDRESS_FROM)
        page.fill_address_to(data.ADDRESS_TO)
        page.click_call_taxi()
        page.fill_card(data.CARD_NUMBER, data.CARD_CODE)
        page.press_tab()
        page.click_link_card_button()
        assert page.get_active_payment_method() == "Card"

    def test_comment_for_driver_flow(self):
        """Verify adding a comment for the driver."""
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.fill_address_from(data.ADDRESS_FROM)
        page.fill_address_to(data.ADDRESS_TO)
        page.click_call_taxi()
        page.add_comment_for_driver(data.MESSAGE_FOR_DRIVER)
        assert page.get_comment_for_driver() == data.MESSAGE_FOR_DRIVER

    def test_order_blanket_and_handkerchiefs(self):
        """Verify ordering blanket and handkerchiefs."""
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.fill_address_from(data.ADDRESS_FROM)
        page.fill_address_to(data.ADDRESS_TO)
        page.click_call_taxi()
        if not page.is_supportive_plan_selected():
            page.select_supportive_plan()
        page.order_blanket_and_handkerchiefs()
        assert page.is_blanket_ordered()
        assert page.is_handkerchief_ordered()

    def test_order_2_ice_creams(self):
        """Verify ordering 2 ice creams."""
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.fill_address_from(data.ADDRESS_FROM)
        page.fill_address_to(data.ADDRESS_TO)
        page.click_call_taxi()
        page.order_ice_creams(count=2)
        assert page.get_ice_cream_count() == 2

    def test_order_supportive_taxi(self):
        """Verify supportive taxi can be ordered."""
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.fill_address_from(data.ADDRESS_FROM)
        page.fill_address_to(data.ADDRESS_TO)
        if not page.is_supportive_plan_selected():
            page.select_supportive_plan()
        page.click_call_taxi()
        modal = page.wait_for_car_search_modal()
        assert modal.is_displayed()
        assert page.get_car_model_name() != ""

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

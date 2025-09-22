import time
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import data
import helpers
from pages import UrbanRoutesPage


class TestUrbanRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # do not modify - we need additional logging enabled in order to retrieve phone confirmation code
        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=options)

        # Skip if server not reachable
        if not helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            raise unittest.SkipTest("Urban Routes server not reachable")
        else:
            print("Connection established with Urban Routes server")

    def test_set_route(self):
        """Verify that route addresses can be set correctly."""
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.fill_address_from(data.ADDRESS_FROM)
        routes_page.fill_address_to(data.ADDRESS_TO)

        assert routes_page.get_address_from() == data.ADDRESS_FROM
        assert routes_page.get_address_to() == data.ADDRESS_TO

    def test_select_supportive_plan(self):
        """Verify that supportive plan can be selected."""
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.fill_address_from(data.ADDRESS_FROM)
        routes_page.fill_address_to(data.ADDRESS_TO)
        routes_page.select_supportive_plan()
        routes_page.click_call_taxi()

        assert routes_page.get_selected_plan() == "Supportive"

    def test_fill_phone_number(self):
        """Verify phone number and confirmation code flow."""
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.fill_address_from(data.ADDRESS_FROM)
        routes_page.fill_address_to(data.ADDRESS_TO)
        routes_page.click_call_taxi()

        routes_page.fill_phone_number(data.PHONE_NUMBER)
        time.sleep(2)  # wait for SMS log

        code = routes_page.get_phone_confirmation_code()
        routes_page.fill_confirmation_code(code)

        assert routes_page.get_phone_number() == data.PHONE_NUMBER

    def test_fill_card(self):
        """Verify card can be added and linked."""
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.fill_address_from(data.ADDRESS_FROM)
        routes_page.fill_address_to(data.ADDRESS_TO)
        routes_page.click_call_taxi()

        routes_page.fill_card(data.CARD_NUMBER, data.CARD_CODE)
        routes_page.press_tab()
        routes_page.click_link_card_button()

        assert routes_page.get_active_payment_method() == "Card"

    def test_comment_for_driver_flow(self):
        """Verify adding a comment for the driver."""
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.fill_address_from(data.ADDRESS_FROM)
        routes_page.fill_address_to(data.ADDRESS_TO)
        routes_page.click_call_taxi()

        routes_page.add_comment_for_driver(data.MESSAGE_FOR_DRIVER)

        assert routes_page.get_comment_for_driver() == data.MESSAGE_FOR_DRIVER

    def test_order_blanket_and_handkerchiefs(self):
        """Verify ordering blanket and handkerchiefs."""
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.fill_address_from(data.ADDRESS_FROM)
        routes_page.fill_address_to(data.ADDRESS_TO)
        routes_page.select_supportive_plan()
        routes_page.click_call_taxi()
        routes_page.order_blanket_and_handkerchiefs()

        assert routes_page.is_blanket_ordered()
        assert routes_page.is_handkerchief_ordered()

    def test_order_2_ice_creams(self):
        """Verify ordering 2 ice creams."""
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.fill_address_from(data.ADDRESS_FROM)
        routes_page.fill_address_to(data.ADDRESS_TO)
        routes_page.click_call_taxi()
        routes_page.order_ice_creams(count=2)

        assert routes_page.get_ice_cream_count() == 2

    def test_order_supportive_taxi(self):
        """Verify supportive taxi can be ordered."""
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.fill_address_from(data.ADDRESS_FROM)
        routes_page.fill_address_to(data.ADDRESS_TO)
        routes_page.select_supportive_plan()
        routes_page.click_call_taxi()

        modal = routes_page.wait_for_car_search_modal()
        assert modal.is_displayed()

        car_name = routes_page.get_car_model_name()
        assert car_name != ""

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

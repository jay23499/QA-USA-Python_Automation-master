import unittest
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import data
import helpers
from pages import UrbanRoutesPage
from selenium.webdriver.chrome.options import Options

class TestUrbanRoutes(unittest.TestCase):

    @classmethod
    def setup_class(cls):
        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=options)
        # Skip all tests in this class if the server is not reachable
        if not helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            pytest.skip("Urban Routes server not reachable")

    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.fill_address_from(data.ADDRESS_FROM)
        routes_page.fill_address_to(data.ADDRESS_TO)

        assert routes_page.get_address_from() == data.ADDRESS_FROM
        assert routes_page.get_address_to() == data.ADDRESS_TO

    def test_select_supportive_plan(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page= UrbanRoutesPage(self.driver)
        routes_page.fill_address_from(data.ADDRESS_FROM)
        routes_page.fill_address_to(data.ADDRESS_TO)
        routes_page.click_call_taxi()
        if not routes_page.is_supportive_plan_selected():
            routes_page.select_supportive_plan()
        assert routes_page.is_supportive_plan_selected()
    def test_fill_phone_number(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.fill_address_from(data.ADDRESS_FROM)
        routes_page.fill_address_to(data.ADDRESS_TO)
        routes_page.click_call_taxi()

        routes_page.fill_phone_number(data.PHONE_NUMBER)
        time.sleep(2)  # Wait for SMS log
        code = helpers.retrieve_phone_code(self.driver)
        assert code is not None, "Confirmation code not retrieved"

        routes_page.fill_confirmation_code(code)
        assert routes_page.get_phone_number() == data.PHONE_NUMBER

    def test_fill_card(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.fill_address_from(data.ADDRESS_FROM)
        routes_page.fill_address_to(data.ADDRESS_TO)
        routes_page.click_call_taxi()

        routes_page.fill_card(data.CARD_NUMBER, data.CARD_CODE)
        ActionChains(self.driver).send_keys(Keys.TAB).perform()
        routes_page.click_link_card_button()

        assert routes_page.is_card_linked(data.CARD_NUMBER)

    def test_comment_for_driver_flow(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.fill_address_from(data.ADDRESS_FROM)
        routes_page.fill_address_to(data.ADDRESS_TO)
        routes_page.click_call_taxi()
        routes_page.choose_tariff("Basic")
        routes_page.add_comment_for_driver(data.MESSAGE_FOR_DRIVER)

        assert routes_page.get_comment_for_driver() == data.MESSAGE_FOR_DRIVER

    def test_order_blanket_and_handkerchiefs(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.fill_address_from(data.ADDRESS_FROM)
        routes_page.fill_address_to(data.ADDRESS_TO)
        routes_page.click_call_taxi()
        routes_page.order_blanket_and_handkerchiefs()

        assert routes_page.is_blanket_ordered()
        assert routes_page.is_handkerchief_ordered()

    def test_order_2_ice_creams(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.fill_address_from(data.ADDRESS_FROM)
        routes_page.fill_address_to(data.ADDRESS_TO)
        routes_page.click_call_taxi()
        routes_page.order_ice_creams(count=2)

        assert routes_page.get_ice_cream_count() == 2

    def test_order_supportive_taxi(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.fill_address_from(data.ADDRESS_FROM)
        routes_page.fill_address_to(data.ADDRESS_TO)
        routes_page.select_supportive_plan()
        routes_page.add_comment_for_driver(data.MESSAGE_FOR_DRIVER)
        routes_page.click_call_taxi()

        modal = routes_page.wait_for_car_search_modal()
        assert modal.is_displayed()

        car_name = routes_page.get_car_model_name()
        assert car_name != ""

    @classmethod
    def tearDownClass(cls):
      cls.driver.quit()

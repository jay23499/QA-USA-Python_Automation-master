import pytest
import time
import data
import helpers
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys



class TestUrbanRoutes:

    def __init__(self):
        self.routes_page = None



    @classmethod
    def setup_class(cls):
        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=options)
     # Skip all tests in this class if the server is not reachable
        if not helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            pytest.skip("Urban Routes server not reachable")

    def test_set_route(self):
        self.routes_page.fill_address_from(data.ADDRESS_FROM)
        self.routes_page.fill_address_to(data.ADDRESS_TO)
        self.routes_page.click_call_taxi()

        assert self.routes_page.get_address_from() == data.ADDRESS_FROM
        assert self.routes_page.get_address_to() == data.ADDRESS_TO

    def test_select_supportive_plan(self):
        if not self.routes_page.is_supportive_plan_selected():
            self.routes_page.select_supportive_plan()
        assert self.routes_page.is_supportive_plan_selected()

    def test_fill_phone_number(self):
        self.routes_page.fill_phone_number(data.PHONE_NUMBER)
        time.sleep(2)  # Wait for SMS log to be populated
        code = helpers.retrieve_phone_code(self.driver)
        assert code is not None, "Confirmation code not retrieved"

        self.routes_page.fill_confirmation_code(code)
        assert self.routes_page.get_phone_number() == data.PHONE_NUMBER

    def test_fill_card(self):
        self.routes_page.fill_card(data.CARD_NUMBER, data.CARD_CODE)
        ActionChains(self.driver).send_keys(Keys.TAB).perform()  # simulate focus change
        self.routes_page.click_link_card_button()

        assert self.routes_page.is_card_linked(data.CARD_NUMBER)

    def test_comment_for_driver_flow(self):
        self.routes_page.fill_address_from(data.ADDRESS_FROM)
        self.routes_page.fill_address_to(data.ADDRESS_TO)
        self.routes_page.click_call_taxi()
        self.routes_page.choose_tariff("Basic")
        self.routes_page.add_comment_for_driver(data.MESSAGE_FOR_DRIVER)

        assert self.routes_page.get_comment_for_driver() == data.MESSAGE_FOR_DRIVER

    def test_order_blanket_and_handkerchiefs(self):
        self.routes_page.order_blanket_and_handkerchiefs()

        assert self.routes_page.is_blanket_ordered()
        assert self.routes_page.is_handkerchief_ordered()

    def test_order_2_ice_creams(self):
        self.routes_page.order_ice_creams(count=2)
        assert self.routes_page.get_ice_cream_count() == 2

    def test_order_supportive_taxi(self):
        self.routes_page.fill_address_from(data.ADDRESS_FROM)
        self.routes_page.fill_address_to(data.ADDRESS_TO)
        self.routes_page.select_supportive_plan()
        self.routes_page.add_comment_for_driver(data.MESSAGE_FOR_DRIVER)
        self.routes_page.click_call_taxi()

        modal = self.routes_page.wait_for_car_search_modal()
        assert modal.is_displayed()

        car_name = self.routes_page.get_car_model_name()
        assert car_name != ""

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

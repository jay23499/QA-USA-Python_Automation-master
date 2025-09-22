import time
import unittest

from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import data
import helpers
from pages import UrbanRoutesPage


class TestUrbanRoutes(unittest.TestCase):

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
            print("Cannot connect to Urban Routes. Check that the server is on and still running")
    def test_set_route(self):
        """Verify that route addresses can be set correctly."""
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        # Wait until the 'From' input is present
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(routes_page.ADDRESS_FROM_INPUT)
        )

        # Fill in addresses
        routes_page.fill_address_from(data.ADDRESS_FROM)
        routes_page.fill_address_to(data.ADDRESS_TO)

        # Assertions
        self.assertEqual(routes_page.get_address_from(), data.ADDRESS_FROM,
                         "The 'From' address was not set correctly.")
        self.assertEqual(routes_page.get_address_to(), data.ADDRESS_TO,
                         "The 'To' address was not set correctly.")

    def test_select_supportive_plan(self):
        """Verify that supportive plan can be selected."""
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.fill_address_from(data.ADDRESS_FROM)
        routes_page.fill_address_to(data.ADDRESS_TO)
        routes_page.click_call_taxi()

        routes_page.select_supportive_plan()
        self.assertTrue(routes_page.is_supportive_plan_selected(),
                        "Supportive plan was not selected.")

    def test_fill_phone_number(self):
        """Verify phone number and confirmation code flow."""
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.fill_address_from(data.ADDRESS_FROM)
        routes_page.fill_address_to(data.ADDRESS_TO)
        routes_page.click_call_taxi()

        routes_page.fill_phone_number(data.PHONE_NUMBER)
        time.sleep(2)  # wait for SMS log
        code = helpers.retrieve_phone_code(self.driver)
        self.assertIsNotNone(code, "Confirmation code not retrieved.")

        routes_page.fill_confirmation_code(code)
        self.assertEqual(routes_page.get_phone_number(), data.PHONE_NUMBER)

    def test_fill_card(self):
        """Verify card can be added and linked."""
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.fill_address_from(data.ADDRESS_FROM)
        routes_page.fill_address_to(data.ADDRESS_TO)
        routes_page.click_call_taxi()

        routes_page.fill_card(data.CARD_NUMBER, data.CARD_CODE)
        routes_page.click_link_card_button()

        self.assertEqual(routes_page.get_active_payment_method(), "Card",
                         "Card was not set as the active payment method.")

    def test_comment_for_driver_flow(self):
        """Verify adding a comment for the driver."""
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.fill_address_from(data.ADDRESS_FROM)
        routes_page.fill_address_to(data.ADDRESS_TO)
        routes_page.click_call_taxi()

        routes_page.add_comment_for_driver(data.MESSAGE_FOR_DRIVER)
        self.assertEqual(routes_page.get_comment_for_driver(), data.MESSAGE_FOR_DRIVER,
                         "Driver comment was not set correctly.")

    def test_order_blanket_and_handkerchiefs(self):
        """Verify ordering blanket and handkerchiefs."""
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.fill_address_from(data.ADDRESS_FROM)
        routes_page.fill_address_to(data.ADDRESS_TO)
        routes_page.click_call_taxi()
        routes_page.select_supportive_plan()  # must select before ordering
        routes_page.order_blanket_and_handkerchiefs()

        self.assertTrue(routes_page.is_blanket_ordered(),
                        "Blanket was not ordered successfully.")
        self.assertTrue(routes_page.is_handkerchief_ordered(),
                        "Handkerchiefs were not ordered successfully.")

    def test_order_2_ice_creams(self):
        """Verify ordering 2 ice creams."""
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.fill_address_from(data.ADDRESS_FROM)
        routes_page.fill_address_to(data.ADDRESS_TO)
        routes_page.click_call_taxi()
        routes_page.order_ice_creams(count=2)

        self.assertEqual(routes_page.get_ice_cream_count(), 2,
                         "Ice cream count does not match the ordered quantity.")

    def test_order_supportive_taxi(self):
        """Verify supportive taxi can be ordered."""
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.fill_address_from(data.ADDRESS_FROM)
        routes_page.fill_address_to(data.ADDRESS_TO)
        routes_page.select_supportive_plan()
        routes_page.click_call_taxi()

        modal_displayed = routes_page.wait_for_car_search_modal()
        self.assertTrue(modal_displayed, "Car search modal did not appear.")

        car_name = routes_page.get_car_model_name()
        self.assertNotEqual(car_name, "", "Car model name is empty.")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

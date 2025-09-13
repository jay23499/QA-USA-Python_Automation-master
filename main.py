import data
import helpers
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages import UrbanRoutesPage


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        # do not modify - we need additional logging enabled in order to retrieve phone confirmation code
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()

    def setup_method(self, method):
        if not helpers.is_url_reachable(data.URBAN_ROUTES_URL, timeout=10):
            pytest.skip("Urban Routes server not reachable")
        self.page = UrbanRoutesPage(self.driver)
        self.page.driver.get(data.URBAN_ROUTES_URL)

    def test_set_route(self):
        """Set From and To addresses"""
        page.fill_address_from(data.ADDRESS_FROM)
        page.fill_address_to(data.ADDRESS_TO)
        page.click_call_taxi()
        assert self.page.get_address_from() == data.ADDRESS_FROM
        assert self.page.get_address_to() == data.ADDRESS_TO

    def test_select_supportive_plan(self):
        """Select supportive tariff only if not already selected"""
        if not self.page.is_supportive_plan_selected():
            self.page.select_supportive_plan()
        assert self.page.is_supportive_plan_selected()

    def test_fill_phone_number(self):
        """Fill phone number and retrieve SMS code"""
        self.page.fill_phone_number(data.PHONE_NUMBER)
        time.sleep(2)  # Wait for SMS network traffic
        code = helpers.retrieve_phone_code(self.driver)
        assert code is not None, "Confirmation code not retrieved"
        self.page.fill_confirmation_code(code)
        assert self.page.get_phone_number() == data.PHONE_NUMBER

    def test_fill_card(self):
        """Add credit card and handle focus issue on CVV"""
        self.page.fill_card(data.CARD_NUMBER, data.CARD_CODE)
        # Simulate focus change (TAB) to trigger 'Link' button activation
        ActionChains(self.driver).send_keys(Keys.TAB).perform()
        self.page.click_link_card_button()
        assert self.page.is_card_linked(data.CARD_NUMBER)

    def test_comment_for_driver_flow(self):
        """Add a comment for the driver"""
        page.fill_address_from(data.ADDRESS_FROM)
        page.fill_address_to(data.ADDRESS_TO)
        page.click_call_taxi()
        page.choose_tariff("Basic")
        page.add_comment_for_driver(data.MESSAGE_FOR_DRIVER)
        assert self.page.get_comment_for_driver() == data.MESSAGE_FOR_DRIVER

    def test_order_blanket_and_handkerchiefs(self):
        """Order blanket and handkerchiefs"""
        self.page.order_blanket_and_handkerchiefs()
        assert self.page.is_blanket_ordered()
        assert self.page.is_handkerchief_ordered()

    def test_order_2_ice_creams(self):
        """Order ice creams"""
        self.page.order_ice_creams(count=2)
        assert self.page.get_ice_cream_count() == 2

    def test_order_supportive_taxi(self):
        """Order taxi with Supportive tariff and verify car search modal"""
        page.fill_address_from(data.ADDRESS_FROM)
        page.fill_address_to(data.ADDRESS_TO)
        page.select_supportive_plan()
        page.add_comment_for_driver(data.MESSAGE_FOR_DRIVER)
        page.click_call_taxi()
        modal = self.page.wait_for_car_search_modal()
        assert modal.is_displayed()
        car_name = self.page.get_car_model_name()
        assert car_name != ""

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

import data
import helpers


class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.maximize_window()
        if not helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            raise Exception("Cannot connect to Urban Routes server")

    def test_set_route(self):
        page = UrbanRoutesPage(self.driver)
        self.driver.get(data.URBAN_ROUTES_URL)
        page.fill_address_from(data.ADDRESS_FROM)
        page.fill_address_to(data.ADDRESS_TO)
        page.click_call_taxi()

    def test_select_plan(self):
        page = UrbanRoutesPage(self.driver)
        page.select_supportive_plan()

    def test_fill_phone_number(self):
        page = UrbanRoutesPage(self.driver)
        page.fill_phone_number(data.PHONE_NUMBER)
        code = helpers.retrieve_phone_code(self.driver)
        page.fill_confirmation_code(code)
        assert page.get_phone_number() == data.PHONE_NUMBER

    def test_fill_card(self):
        page = UrbanRoutesPage(self.driver)
        page.fill_card(data.CARD_NUMBER, data.CARD_CODE)

    def test_comment_for_driver(self):
        page = UrbanRoutesPage(self.driver)
        page.add_comment_for_driver(data.MESSAGE_FOR_DRIVER)

    def test_order_blanket_and_handkerchiefs(self):
        page = UrbanRoutesPage(self.driver)
        page.order_blanket_and_handkerchiefs()

    def test_order_2_ice_creams(self):
        page = UrbanRoutesPage(self.driver)
        page.order_ice_creams(count=2)
        assert page.get_ice_cream_count() == 2

    def test_car_search_model_appears(self):
        page = UrbanRoutesPage(self.driver)
        modal = page.wait_for_car_search_modal()
        assert modal.is_displayed()
        car_name = page.get_car_model_name()
        assert car_name != ""

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

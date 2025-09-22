from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UrbanRoutesPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # --- Address fields ---
    def fill_address_from(self, address: str) -> None:
        from_input = self.driver.find_element(By.ID, "address-from")
        from_input.clear()
        from_input.send_keys(address)

    def fill_address_to(self, address: str) -> None:
        to_input = self.driver.find_element(By.ID, "address-to")
        to_input.clear()
        to_input.send_keys(address)

    def get_address_from(self) -> str:
        return self.driver.find_element(By.ID, "address-from").get_attribute("value")

    def get_address_to(self) -> str:
        return self.driver.find_element(By.ID, "address-to").get_attribute("value")

    # --- Call taxi ---
    def click_call_taxi(self) -> None:
        self.driver.find_element(By.ID, "call-taxi-button").click()

    # --- Tariff / plan selection ---
    def select_supportive_plan(self) -> None:
        self.driver.find_element(By.ID, "plan-supportive").click()

    def is_supportive_plan_selected(self) -> bool:
        return self.driver.find_element(By.ID, "plan-supportive").is_selected()

    def get_selected_plan(self) -> str:
        selected = self.driver.find_element(By.CSS_SELECTOR, ".plan.selected")
        return selected.text

    # --- Phone number flow ---
    def fill_phone_number(self, phone_number: str) -> None:
        phone_input = self.driver.find_element(By.ID, "phone-number")
        phone_input.clear()
        phone_input.send_keys(phone_number)

    def get_phone_number(self) -> str:
        return self.driver.find_element(By.ID, "phone-number").get_attribute("value")

    def get_phone_confirmation_code(self) -> str:
        """Retrieve confirmation code from Chrome performance logs."""
        logs = self.driver.get_log("performance")
        for entry in logs:
            if "SMS_CODE" in entry["message"]:
                # Example: "SMS_CODE=1234"
                return entry["message"].split("SMS_CODE=")[1][:4]
        return None

    def fill_confirmation_code(self, code: str) -> None:
        code_input = self.driver.find_element(By.ID, "confirmation-code")
        code_input.clear()
        code_input.send_keys(code)

    # --- Card flow ---
    def fill_card(self, number: str, code: str) -> None:
        self.driver.find_element(By.ID, "card-number").send_keys(number)
        self.driver.find_element(By.ID, "card-code").send_keys(code)

    def press_tab(self) -> None:
        ActionChains(self.driver).send_keys(Keys.TAB).perform()

    def click_link_card_button(self) -> None:
        self.driver.find_element(By.ID, "link-card-button").click()

    def get_active_payment_method(self) -> str:
        active = self.driver.find_element(By.CSS_SELECTOR, ".payment-method.active")
        return active.text

    # --- Comment for driver ---
    def add_comment_for_driver(self, message: str) -> None:
        comment_box = self.driver.find_element(By.ID, "driver-comment")
        comment_box.clear()
        comment_box.send_keys(message)

    def get_comment_for_driver(self) -> str:
        return self.driver.find_element(By.ID, "driver-comment").get_attribute("value")

    # --- Extras (blanket, handkerchiefs, ice cream) ---
    def order_blanket_and_handkerchiefs(self) -> None:
        self.driver.find_element(By.ID, "order-blanket").click()
        self.driver.find_element(By.ID, "order-handkerchief").click()

    def is_blanket_ordered(self) -> bool:
        return self.driver.find_element(By.ID, "order-blanket").is_selected()

    def is_handkerchief_ordered(self) -> bool:
        return self.driver.find_element(By.ID, "order-handkerchief").is_selected()

    def order_ice_creams(self, count: int) -> None:
        ice_input = self.driver.find_element(By.ID, "ice-cream-count")
        ice_input.clear()
        ice_input.send_keys(str(count))

    def get_ice_cream_count(self) -> int:
        val = self.driver.find_element(By.ID, "ice-cream-count").get_attribute("value")
        return int(val)

    # --- Supportive taxi ordering ---
    def wait_for_car_search_modal(self):
        modal = self.wait.until(
            EC.visibility_of_element_located((By.ID, "car-search-modal"))
        )
        return modal

    def get_car_model_name(self) -> str:
        return self.driver.find_element(By.ID, "car-model").text

# helpers.py
import json
import time
import ssl
import urllib.request
import logging
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common import WebDriverException

# Configure a basic logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ---------------------------
# Retrieves Phone code. Do not change main logic
# ---------------------------
def retrieve_phone_code(driver: WebDriver) -> str:
    """Retrieve the phone confirmation code from browser network logs.

    This function parses the Chrome DevTools performance logs to extract
    the phone verification code after it has been requested in the app.

    Args:
        driver (WebDriver): Selenium WebDriver instance with performance logging enabled.

    Returns:
        str: Extracted numeric confirmation code.

    Raises:
        Exception: If no phone confirmation code was found within 10 attempts.
    """
    code = None
    for i in range(10):
        try:
            logs = [
                log["message"]
                for log in driver.get_log('performance')
                if log.get("message") and 'api/v1/number?number' in log.get("message")
            ]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd(
                    'Network.getResponseBody',
                    {'requestId': message_data["params"]["requestId"]}
                )
                code = ''.join(filter(str.isdigit, body['body']))  # cleaner extraction

            if code:
                logger.info(f"Phone confirmation code found: {code}")
                return code

        except WebDriverException as e:
            logger.debug(f"WebDriverException encountered: {e}")
            time.sleep(1)
            continue

        logger.debug(f"Attempt {i+1}: code not found, retrying...")
        time.sleep(1)

    # If code was never found
    raise Exception(
        "No phone confirmation code found.\n"
        "Please use retrieve_phone_code only after the code was requested in your application."
    )


# ---------------------------
# Checks if Routes is up and running
# ---------------------------
def is_url_reachable(url: str, timeout: int = 5) -> bool:
    """Check if a given URL is reachable (status code 200).

    This helper is primarily used to verify that the Urban Routes
    application server is up before running tests.

    Args:
        url (str): The target URL to check.
        timeout (int): Optional timeout in seconds for the request (default 5).

    Returns:
        bool: True if reachable, False otherwise.
    """
    try:
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE

        with urllib.request.urlopen(url, context=ssl_ctx, timeout=timeout) as response:
            reachable = response.status == 200
            if reachable:
                logger.info(f"URL reachable: {url}")
            else:
                logger.warning(f"URL responded but status code not 200: {response.status}")
            return reachable

    except Exception as e:
        logger.warning(f"URL not reachable: {e}")
        return False

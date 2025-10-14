# helpers.py

# ---------------------------
# Retrieves Phone code. Do not change main logic
# ---------------------------
def retrieve_phone_code(driver) -> str:
    """This code retrieves phone confirmation number and returns it as a string.
    Use it when application waits for the confirmation code to pass it into your tests.
    The phone confirmation code can only be obtained after it was requested in application."""

    import json
    import time
    from selenium.common import WebDriverException

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
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue

        if code:
            return code
        else:
            time.sleep(1)  # wait before retrying

    # If code was never found
    raise Exception(
        "No phone confirmation code found.\n"
        "Please use retrieve_phone_code only after the code was requested in your application."
    )


# ---------------------------
# Checks if Routes is up and running
# ---------------------------
def is_url_reachable(url) -> bool:
    """Check if the URL can be reached. Returns True if reachable, False otherwise."""

    import ssl
    import urllib.request

    try:
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE

        with urllib.request.urlopen(url, context=ssl_ctx) as response:
            return response.status == 200
    except Exception as e:
        print(f"[WARNING] URL not reachable: {e}")
        return False

import os
import time

from scrape.config import Config
from scrape.interface import Interface

BASE_URL = "https://easyweb.td.com/"

# TODO (jfdoming): refactor
DATA_DIR = "data"


def scrape_latest(config: Config):
    print("Username: ", config.username)
    print("Password: ", config.password or "<missing>")

    with Interface.create(engine="selenium") as browser:
        browser.url = BASE_URL
        time.sleep(4)

        browser.select(id="username").send_keys(config.username)
        time.sleep(1)
        browser.select(id="uapPassword").send_keys(
            config.password.get_secret_value() if config.password else ""
        )
        time.sleep(1)
        browser.click(query=".login-form button.td-button-secondary")

        time.sleep(10)
        browser._SeleniumInterface__driver.save_screenshot(
            "/var/task/screenshot.png"
        )
        raise Exception(browser.url)
        browser.click(query=".otp-section button.td-button-secondary")
        input("Please press enter to continue once 2FA is complete.")

        iterations = 0
        while not browser.url.startswith(BASE_URL) and iterations < 10:
            iterations += 1
            time.sleep(1)
        if not browser.url.startswith(BASE_URL):
            print("Failed to log in, aborting...")
            print(browser.url)
            return

        print("Successfully logged in!")
        time.sleep(4)  # Let the page load.

        _log_accounts_in_frame(browser._SeleniumInterface__driver, config)
        print(
            f"Finished reading account data. The data has been logged under `{DATA_DIR}{os.sep}`."
        )

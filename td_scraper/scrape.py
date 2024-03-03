import os
import sys
import time

from td_scraper.config import Config
from scrape.interface import Interface
from td_scraper.otp import await_otp

BASE_URL = "https://easyweb.td.com/"

# TODO (jfdoming): refactor
DATA_DIR = "data"


def scrape_latest(config: Config):
    print("Username: ", config.username)
    print("Password: ", config.password or "<missing>")

    with Interface.create(engine="selenium") as browser:
        if config.verbosity > 1:
            print("Navigating to TD EasyWeb...")

        browser.url = BASE_URL
        time.sleep(4)

        if config.verbosity > 1:
            print("Logging in...")

        browser.type(config.username, id="username")
        browser.type(
            config.password.get_secret_value() if config.password else "",
            id="uapPassword",
        )
        browser.click(query=".login-form button.td-button-secondary")
        time.sleep(2)

        if config.verbosity > 1:
            print("Sending OTP...")

        otp_button = browser.select(
            query=".otp-section button.td-button-secondary",
            index=0,
            text="Text me",
        )
        if otp_button:
            otp_button.click()
            browser.type(await_otp(config), id="code")
            browser.click(
                query="form .td-button.td-button-secondary",
                text="Enter",
            )
        else:
            # No OTP was requested, so we can assume we're already logging in.
            pass

        if config.verbosity > 1:
            print("Waiting for login to complete...")

        iterations = 0
        while not browser.url.startswith(BASE_URL) and iterations < 10:
            iterations += 1
            time.sleep(1)
        if not browser.url.startswith(BASE_URL):
            print("Failed to log in, aborting...", file=sys.stderr)
            print(browser.url, file=sys.stderr)
            browser.screenshot()
            return

        print("Successfully logged in!")
        time.sleep(4)  # Let the page load.

        if config.verbosity > 1:
            print("Navigating to accounts...")

        _log_accounts_in_frame(browser._SeleniumInterface__driver, config)
        print(
            f"Finished reading account data. The data has been logged under `{DATA_DIR}{os.sep}`."
        )

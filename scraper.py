import logging
import os
import re
import time

from account_details import ACCOUNT_TYPES
from selenium import webdriver
from selenium.webdriver.common.by import By

DATA_DIR = "data"
PRINTABLE_RE = re.compile("[^a-zA-Z0-9_ ]+")


class MatSelect:
    def __init__(self, driver, el):
        self.driver = driver
        self.el = el
        self.options = None

        self.select_by_index(0)

    def select_by_index(self, i):
        self.el.click()

        # Refresh options?
        self.options = self.driver.find_elements(By.TAG_NAME, "mat-option")
        if i < 0 or i >= len(self.options):
            raise ValueError(f"Index {i} out of range")
        self.options[i].click()


def _click(driver, selector, index=0):
    els = driver.find_elements(By.CSS_SELECTOR, selector)
    text = ""
    if index < len(els):
        text = els[index].text
        els[index].click()
    return len(els), text


def _go_frame(driver, name="tddetails"):
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.NAME, name))


def _go_home(driver):
    n, _ = _click(
        driver, '.td-nav-left-label [data-analytics-click="Accounts"]'
    )
    if n < 1:
        _click(driver, '.td-nav-left-label [analytics-click="Accounts"]')


def _get_plain_title(text):
    title = text.split("-")[0].strip()
    title = PRINTABLE_RE.sub("", title)
    return title


def _get_file_path(text):
    title = _get_plain_title(text)
    return os.path.join(DATA_DIR, "{title}.{{ext}}".format(title=title))


def _log_accounts_in_frame(driver, log):
    link_index = 0
    all_data = None  # TODO
    while True:
        print("Opening next account...")
        _go_frame(driver)

        count, text = _click(
            driver, "table a.td-link-standalone-secondary", link_index
        )
        time.sleep(6)

        title = _get_plain_title(text)
        if title not in ACCOUNT_TYPES:
            print(f"Warning: Account type not recognized: {title}")
        elif "credit" in ACCOUNT_TYPES.get(title).lower():
            select = MatSelect(
                driver,
                driver.find_element(By.ID, "matselect-paymentPlanCycleSelect"),
            )
            for i in range(0, len(select.options)):
                select.select_by_index(i)
                time.sleep(4)

                selector = (
                    "#paymentPlanPostedTransactionSubHeading + * .mat-table"
                )
                if not driver.find_elements(By.CSS_SELECTOR, selector):
                    selector = ".mat-table"
                df = _table_to_dataframe(driver, selector, title)
                if df is not None:
                    all_data = all_data.append(df)
        else:
            _click(
                driver, "#transSearchLink[aria-expanded=false]"
            )  # Expand date options.
            time.sleep(2)
            _click(driver, "#searchFromRadio")  # Select date range.
            time.sleep(1)
            _click(
                driver, "#searchRangeRow input[value='Search']"
            )  # View past year.
            time.sleep(8)

            df = _table_to_dataframe(
                driver, ".td-table.td-table-border-row", title
            )
            if df is not None:
                all_data = all_data.append(df)

        print("Read data for account: ", text)
        _go_home(driver)
        time.sleep(4)

        link_index += 1
        if link_index >= count:
            break

    if log:
        all_data.sort_values("Date", kind="mergesort", inplace=True)
        all_data.reset_index(drop=True, inplace=True)
        os.makedirs(DATA_DIR, exist_ok=True)
        file = _get_file_path("combined")
        all_data.to_csv(file.format(ext="csv"))
        all_data.to_pickle(file.format(ext="pickle"))
    else:
        print(all_data)


def scrape_latest(log=True):
    login_url = "https://easyweb.td.com/"

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    with open(".config", "r") as config:
        contents = config.read().splitlines()
        username = contents[0]
        password = contents[1]
        print("Username: ", username)
        print("Password: ", "***" if password.strip() else "<missing>")

        driver = webdriver.Chrome(options=options)

        try:
            driver.get(login_url)
            time.sleep(4)

            driver.find_element(By.ID, "username").send_keys(username)
            time.sleep(1)
            driver.find_element(By.ID, "uapPassword").send_keys(password)
            time.sleep(1)
            _click(driver, ".login-form button.td-button-secondary")

            input("Please press enter to continue once 2FA is complete.")

            iterations = 0
            while (
                not driver.current_url.startswith("https://easyweb.td.com")
                and iterations < 10
            ):
                iterations += 1
                time.sleep(1)

            if not driver.current_url.startswith("https://easyweb.td.com"):
                print("Failed to log in, aborting...")
                print(driver.current_url)
                return

            print("Successfully logged in!")
            time.sleep(4)  # Let the page load.

            _log_accounts_in_frame(driver, log)
            print(
                f"Finished reading account data. The data has been logged under `{DATA_DIR}{os.sep}`."
            )
        finally:
            driver.close()


if __name__ == "__main__":
    try:
        scrape_latest()
    except Exception as e:
        logging.exception(e)
    input("Press Enter to exit")

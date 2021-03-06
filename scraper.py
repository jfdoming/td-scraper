import os
import time
import re
import pandas as pd
from account_details import ACCOUNT_TYPES
from selenium import webdriver
from selenium.webdriver.support.ui import Select

printable_re = re.compile('[^a-zA-Z0-9_ ]+')

def _click(driver, selector, index=0):
    els = driver.find_elements_by_css_selector(selector)
    text = ""
    if index < len(els):
        text = els[index].text
        els[index].click()
    return len(els), text

def _go_frame(driver, name="tddetails"):
    driver.switch_to.frame(driver.find_element_by_name(name))

def _go_home(driver):
    _click(driver, "[data-analytics-click=\"Accounts\"]")

def _get_plain_title(text):
    title = text.split('-')[0].strip()
    title = printable_re.sub('', title)
    return title

def _get_file_path(text):
    title = _get_plain_title(text)
    file = "data/{title}.{{ext}}".format(title=title)
    return file

def _clean_df(df, account_type):
    if df is None:
        return df

    # Standardize column names.
    df.columns = ["Date", "Description", "Debit", "Credit", "Balance"]

    # Keep only posted transactions.
    drop_index = df[df["Date"].str.startswith("Posted Transactions", na=False)].index.values
    if len(drop_index):
        df = df.drop(df.index[:drop_index[-1]])

    # Descriptions should appear at the start of the string and be followed by "  ".
    df["Description"] = df["Description"].str.extract("(.+?)(?:(?=  ).+)?$")

    # Dates should appear at the start of the string and be followed by "  ".
    df["Date"] = df["Date"].str.extract("(.+?)(?:(?=  ).+)?$")

    # Format dates nicely and drop non-date rows.
    df["Date"] = pd.to_datetime(df["Date"], format="%b %d, %Y", errors="coerce")
    df.dropna(subset=["Date"], inplace=True)

    # We'll calculate the balance manually.
    df.drop(["Balance"], axis=1, inplace=True)

    # Merge the "Debit" and "Credit" columns.
    df["Debit"] = df["Debit"].str.extract("([\d,]+\.\d+)", expand=False).map(lambda val: val.replace(",", "") if type(val) == str else val).fillna("x")
    df["Credit"] = df["Credit"].str.extract("([\d,]+\.\d+)", expand=False).map(lambda val: val.replace(",", "") if type(val) == str else val).fillna("x")
    df["Amount"] = ((df["Debit"] != "x") * ("-" + df["Debit"]) + (df["Credit"] != "x") * df["Credit"]).astype(float)
    df.drop(["Debit", "Credit"], axis=1, inplace=True)

    df["Account"] = ACCOUNT_TYPES.get(account_type, "MISSING")
    df["Expense Type"] = ""

    return df

def _table_to_dataframe(driver, table_selector, account_type):
    table = driver.find_elements_by_css_selector(table_selector)
    result_df = None
    if len(table) != 0:
        result_df = pd.read_html(table[0].get_attribute("outerHTML"))
    result_df = result_df[0] if result_df is not None and len(result_df) else None
    return _clean_df(result_df, account_type)

def _log_accounts_in_frame(driver, log):
    link_index = 0
    all_data = pd.DataFrame()
    while True:
        print("Opening next account...")
        count, text = _click(driver, "table a.td-link-standalone-secondary", link_index)
        time.sleep(4)

        title = _get_plain_title(text)
        if ACCOUNT_TYPES.get(title) == "CREDIT":
            select = Select(driver.find_element_by_id("cycles"))
            for i in range(0, len(select.options)):
                select.select_by_index(i)
                time.sleep(2)

                df = _table_to_dataframe(driver, ".td-table.td-table-border-row", title)
                if df is not None:
                    all_data = all_data.append(df)
        else:
            _click(driver, "#ql4") # View 120 days.
            time.sleep(4)

            df = _table_to_dataframe(driver, ".td-table.td-table-border-row", title)
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

        file = _get_file_path("combined")
        all_data.to_csv(file.format(ext="csv"))
        all_data.to_pickle(file.format(ext="pickle"))
    else:
        print(all_data)

def scrape_latest(log=True):
    login_url = "https://easyweb.td.com/"

    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")
    with open(".config", "r") as config:
        contents = config.read().splitlines()
        username = contents[0]
        password = contents[1]
        print("Username: ", username)
        print("Password: ", password)

        driver = webdriver.Chrome(options=options)

        try:
            driver.get(login_url)
            time.sleep(2)

            driver.find_element_by_id("username100").send_keys(username)
            time.sleep(1)
            driver.find_element_by_id("password").send_keys(password)
            time.sleep(1)
            _click(driver, ".otp-login > .td-container button")

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
            time.sleep(2) # Let the page load.

            _go_frame(driver)

            _log_accounts_in_frame(driver, log)
            print("Finished reading account data. The data has been logged under `data/`.")
        finally:
            driver.close()

def get_scraped_data():
    files = os.listdir("data") if os.path.exists("data") else []
    files = [file for file in files if file.endswith(".pickle")]
    if len(files):
        return [pd.read_pickle("data/" + file) for file in files]

    scrape_latest()
    get_scraped_data()

if __name__ == '__main__':
    scrape_latest()

from tempfile import mkdtemp
from typing import Any

from selenium import webdriver
from selenium.webdriver.common.by import By

from scrape.interface import Interface


class SeleniumInterface(Interface):
    def __get_options(self):
        return {
            "headless": "new",
            "no-sandbox": True,
            "no-zygote": True,
            "single-process": True,
            "disable-dev-shm-usage": True,
            "disable-dev-tools": True,
            "disable-gpu": True,
            "remote-debugging-port": 9222,
            "window-size": "1920,1080",
            "user-data-dir": mkdtemp(),
            "data-path": mkdtemp(),
            "disk-cache-dir": mkdtemp(),
            "user-agent": " ".join(
                [
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                    "AppleWebKit/537.36 (KHTML, like Gecko)",
                    "Chrome/79.0.3945.79 Safari/537.36",
                ]
            ),
        }

    @staticmethod
    def __create_options(options_dict: dict[str, Any]):
        options = webdriver.ChromeOptions()
        options.binary_location = "/opt/chrome/chrome"
        for key, value in options_dict.items():
            if isinstance(value, bool):
                if value:
                    options.add_argument(f"--{key}")
            else:
                options.add_argument(f"--{key}={value}")

        return options

    def __init__(self):
        self.__options = SeleniumInterface.__create_options(
            self.__get_options()
        )
        self.__driver = None

    def __enter__(self):
        self.__driver = webdriver.Chrome(options=self.__options)
        return self

    def __exit__(self, *_):
        self.__driver.quit()

    @property
    def url(self):
        return self.__driver.current_url

    @url.setter
    def url(self, url: str):
        self.__driver.get(url)

    def select(self, id: str = None, query: str = None, index: int = None):
        if id is not None:
            return self.__driver.find_element(By.ID, id)
        if query is not None:
            els = self.__driver.find_elements(By.CSS_SELECTOR, query)
            if index is None:
                return els
            return els[index]

        raise ValueError("No selector specified")

    def __select_for_action(self, *args, **kwargs):
        el = self.select(*args, **kwargs)
        if isinstance(el, list):
            if len(el) != 1:
                raise ValueError(
                    "Ambiguous element selection, please specify an index"
                )
            el = el[0]
        return el

    def click(self, *args, **kwargs):
        el = self.__select_for_action(*args, **kwargs)
        el.click()
        return el

    def type(self, *args, **kwargs):
        el = self.__select_for_action(*args, **kwargs)
        el.send_keys()
        return el

    def screenshot(self, path: str = "/var/task/scrape/screenshot.png"):
        self.__driver.save_screenshot(path)

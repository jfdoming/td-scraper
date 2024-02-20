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
                if len(els) > 1:
                    raise ValueError(f"Ambiguous query {query}")
                elif not els:
                    raise ValueError(
                        f"No elements found matching query {query}"
                    )
                return els[0]
            if index >= len(els):
                raise StopIteration()
            return els[index]

        raise ValueError("No selector specified")

    def click(self, *args, **kwargs):
        el = self.select(*args, **kwargs)
        el.click()
        return el

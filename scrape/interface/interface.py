from abc import ABC, abstractmethod
from typing import TypedDict


class SelectOptions(TypedDict):
    id: str | None
    query: str | None


class Interface(ABC):
    @staticmethod
    def create(engine: str, *args, **kwargs):
        if engine == "selenium":
            from scrape.interface.selenium import (
                SeleniumInterface as EngineInterface,
            )
        else:
            raise TypeError(f"'{engine}' is not a valid engine")

        return EngineInterface(*args, **kwargs)

    @property
    @abstractmethod
    def url(self, url: str):
        pass

    @abstractmethod
    def select(self, **kwargs: SelectOptions):
        pass

    @abstractmethod
    def click(self, **kwargs: SelectOptions):
        pass

    @abstractmethod
    def type(
        self,
        text: str,
        **kwargs: SelectOptions,
    ):
        pass

    @abstractmethod
    def screenshot(self, path: str | None = None):
        pass

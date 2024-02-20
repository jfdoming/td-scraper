from abc import ABC, abstractmethod


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
    def select(self, id: str = None):
        pass

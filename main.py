import json
import sys

from scrape import scrape_latest
from scrape.config import Config


def read_config_file():
    with open("config.json", "r") as config:
        return json.load(config)


def main():
    if len(sys.argv) > 1:
        config = json.loads(sys.argv[1])
    else:
        config = read_config_file()
    scrape_latest(Config(**config))


if __name__ == "__main__":
    main()

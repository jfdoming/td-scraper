.PHONY: run update scrape save help

run: update scrape save

update:
	@. env/bin/activate; bash scripts/update_cd.sh

scrape:
	@. env/bin/activate; PATH="${PATH}:." python3 scraper.py

save:
	@. env/bin/activate; PATH="${PATH}:." python3 sheets.py

help:
	@echo "Usage: make [run | update | scrape | save | help]"

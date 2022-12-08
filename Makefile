.PHONY: run update scrape save

run: update scrape save

update:
	@bash scripts/update_cd.sh

scrape:
	@PATH="${PATH}:." python3 scraper.py

save:
	@PATH="${PATH}:." python3 sheets.py

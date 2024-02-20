ROOT_DIR := $(dir $(realpath $(lastword $(MAKEFILE_LIST))))
OPTS := -p 80:8080 --rm -e IS_DEV=1 --env-file <(echo "ACCOUNT_TYPES='$$(cat account_types.json)'") \
	    --volume ${ROOT_DIR}/scrape:/var/task/scrape \
	    --volume ${ROOT_DIR}/main.py:/var/task/main.py \
		--volume ${ROOT_DIR}/.otp:/var/task/.otp \
		td-scraper

.PHONY: build@amd64 build@arm64 run run@arm64 run@amd64 otp help

run: run@arm64

run@amd64: .otp build@amd64
	@exec bash -c "docker run --platform linux/amd64 ${OPTS}"

run@arm64: .otp build@arm64
	@exec bash -c "docker run --platform linux/arm64 ${OPTS}"

build@amd64:
	@docker build --platform linux/amd64 . -t td-scraper

build@arm64:
	@docker build --platform linux/arm64 -f Dockerfile.arm64.dev . -t td-scraper

test:
	@curl localhost/2015-03-31/functions/function/invocations -d "$$(cat account_credentials.json)" 2>/dev/null | python3 local/pretty_output.py

otp:
	@python3 -c "from pathlib import Path; otp=input('Enter OTP: '); Path('.otp').write_text(otp)"

.otp:
	@touch .otp

help:
	@echo "Usage: make [build | run | test | otp | help]"

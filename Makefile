ROOT_DIR := $(dir $(realpath $(lastword $(MAKEFILE_LIST))))
OPTS := -p 80:8080 --rm --env-file <(echo "ACCOUNT_TYPES='$$(cat account_types.json)'") \
	    --volume ${ROOT_DIR}/scraper.py:/var/task/main.py \
		td-scraper

.PHONY: build run run@arm64 run@amd64 help

run: run@amd64

run@amd64: build
	@exec bash -c "docker run --platform linux/amd64 ${OPTS}"

run@arm64: build
	@exec bash -c "docker run --platform linux/arm64 ${OPTS}"

build:
	@docker build . -t td-scraper

test:
	@curl localhost/2015-03-31/functions/function/invocations -d "$$(cat account_credentials.json)" 2>/dev/null | python3 local/pretty_output.py

help:
	@echo "Usage: make [build | run | help]"

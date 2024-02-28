ROOT_DIR := $(dir $(realpath $(lastword $(MAKEFILE_LIST))))
BASE_OPTS := -p 80:8080 --rm -e IS_DEV=1 \
		--env-file <(echo "ACCOUNT_TYPES='$$(cat account_types.json)'") \
		--name td-scraper td-scraper
EXTRA_OPTS := --volume ${ROOT_DIR}/scrape:/var/task/scrape \
	    --volume ${ROOT_DIR}/main.py:/var/task/main.py \
		--volume ${ROOT_DIR}/.otp:/var/task/.otp \
		--volume ${ROOT_DIR}/layers:/var/task/layers

.PHONY: build@amd64 build@arm64 build-otp run run@arm64 run@amd64 otp help

run: run@arm64

run@amd64: .otp build@amd64
	@exec bash -c "docker run --platform linux/amd64 ${EXTRA_OPTS} ${BASE_OPTS}"

run@arm64: .otp build@arm64
	@exec bash -c "docker run --platform linux/arm64 ${EXTRA_OPTS} ${BASE_OPTS}"

run@layers: build@layers
	@exec bash -c "docker run --platform linux/amd64 ${EXTRA_OPTS} ${BASE_OPTS}"

build@amd64:
	@docker build --platform linux/amd64 . -t td-scraper

build@arm64:
	@docker build --platform linux/arm64 -f Dockerfile.arm64.dev . -t td-scraper

build@layers: layers
	@docker build --platform linux/amd64 -f Dockerfile.layers . -t td-scraper


build-otp:
	@tempdir="$$(mktemp -d)" && mkdir -p "$$tempdir/otp" && mkdir -p "$$tempdir/scrape/utils" && cp -r otp/* "$$tempdir/otp/" && cp scrape/utils/otp.py "$$tempdir/scrape/utils/" && pushd "$$tempdir" && touch scrape/__init__.py && zip -r otp-lambda.zip * && popd && mv "$$tempdir/otp-lambda.zip" . && rm -rd "$$tempdir"

layers: layers/py_deps_layer.zip layers/chrome_layer.zip layers/scraper_layer.zip layers/chromedriver_local_libs_layer.zip

layers/py_deps_layer.zip: scripts/build_py_deps_layer.sh requirements-scraper.txt
	@scripts/build_py_deps_layer.sh

layers/chrome_layer.zip: scripts/build_chromium_layer.sh scripts/update_cd.sh
	@scripts/build_chromium_layer.sh

layers/chromedriver_local_libs_layer.zip: scripts/build_chromedriver_local_libs_layer.sh lib/*
	@scripts/build_chromedriver_local_libs_layer.sh

layers/scraper_layer.zip: scripts/build_scraper_layer.sh *.py scrape/* scrape/*/* scrape/*/*/*
	@scripts/build_scraper_layer.sh

test:
	@curl localhost/2015-03-31/functions/function/invocations -d "$$(cat config.json)" 2>/dev/null | python3 local/pretty_output.py

otp:
	@python3 -c "from pathlib import Path; otp=input('Enter OTP: '); Path('.otp').write_text(otp)"

.otp:
	@touch .otp

help:
	@echo "Usage: make [build | run | test | otp | help]"

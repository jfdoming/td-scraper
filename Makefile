ROOT_DIR := $(dir $(realpath $(lastword $(MAKEFILE_LIST))))

.PHONY: build-otp run run@arm64 run@amd64 layers test otp setup-symlinks help

run: run@arm64

run@amd64: .otp
	@scripts/run_target.sh "${ROOT_DIR}" "$@"

run@arm64: .otp
	@scripts/run_target.sh "${ROOT_DIR}" "$@"

run@layers:
	@scripts/run_target.sh "${ROOT_DIR}" "$@"

layers:
	@scripts/run_target.sh "${ROOT_DIR}" "$@"

test:
	@scripts/run_target.sh "${ROOT_DIR}" "$@"


build-otp:
	@tempdir="$$(mktemp -d)" && mkdir -p "$$tempdir/otp" && mkdir -p "$$tempdir/scrape/utils" && cp -r otp/* "$$tempdir/otp/" && cp scrape/utils/otp.py "$$tempdir/scrape/utils/" && pushd "$$tempdir" && touch scrape/__init__.py && zip -r otp-lambda.zip * && popd && mv "$$tempdir/otp-lambda.zip" . && rm -rd "$$tempdir"

test-otp:
	@python3 -c "from pathlib import Path; otp=input('Enter OTP: '); Path('.otp').write_text(otp)"

.otp:
	@touch .otp

call:
	@scripts/run_lambda.sh scraper_arn

call-otp:
	@scripts/run_lambda.sh otp_arn

setup-symlinks:
	@scripts/run_target.sh "${ROOT_DIR}" "$@"

help:
	@echo "Usage: make [build | run | test | otp | help]"

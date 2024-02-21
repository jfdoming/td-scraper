import os
import sys
import time
from datetime import datetime, timedelta, timezone
from functools import cache
from pathlib import Path
from typing import Callable

import boto3

from scrape.config import Config
from scrape.utils.otp import unpack_otp

OTP_OBJ_KEY = None
if "IS_DEV" not in os.environ:
    OTP_OBJ_KEY = os.environ["OTP_OBJ_KEY"]


def __utcnow():
    return datetime.now(tz=timezone.utc)


def __poll(
    poll_fn: Callable[[datetime, Config], str | None],
    freq_seconds: int = None,
    timeout_seconds: int = None,
) -> Callable[
    [datetime, Config],
    str,
]:
    def loop(otp_request_time: datetime, config: Config):
        while __utcnow() < otp_request_time + timedelta(
            seconds=timeout_seconds
        ):
            otp = poll_fn(otp_request_time, config)
            if otp:
                return otp
            time.sleep(freq_seconds)

        raise TimeoutError("Timed out waiting for OTP")

    return loop


def __poll_otp_local(otp_request_time: datetime, _):
    file = Path(".otp")
    mtime = file.stat().st_mtime
    if mtime > otp_request_time.timestamp():
        return file.read_text()
    return None


@cache
def __s3_client() -> boto3.client:
    return boto3.client("s3")


def __poll_otp_s3(otp_request_time: datetime, config: Config) -> str | None:
    client = __s3_client()
    bucket = config.otp_bucket

    try:
        response = client.get_object(
            Bucket=bucket, Key=OTP_OBJ_KEY, IfModifiedSince=otp_request_time
        )
        return unpack_otp(response["Body"].read())
    except client.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "NotModified":
            return None
        raise e


def await_otp(config: Config):
    otp_request_time = __utcnow()

    if "IS_DEV" in os.environ:
        print(
            "Please run `make otp` to complete the 2FA process.",
            file=sys.stderr,
        )
        poll = __poll(__poll_otp_local, freq_seconds=1, timeout_seconds=60)
    else:
        poll = __poll(__poll_otp_s3, freq_seconds=5, timeout_seconds=60)

    return poll(otp_request_time, config)

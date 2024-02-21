import os
from functools import cache

import boto3

from scrape.utils.otp import pack_otp

S3_BUCKET = os.environ["S3_BUCKET"]
OTP_OBJ_KEY = os.environ["OTP_OBJ_KEY"]


@cache
def __s3_resource() -> boto3.resource:
    return boto3.resource("s3")


# NOTE: This lambda can logically write to any S3 bucket. Be sure to
#       configure the appropriate IAM permissions so that it can only
#       write to the intended bucket.
def lambda_handler(event, _):
    otp = pack_otp(event["otp"])

    s3 = __s3_resource()
    dest = s3.Object(bucket_name=S3_BUCKET, key=OTP_OBJ_KEY)
    dest.put(Body=otp)

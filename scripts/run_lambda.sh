#!/bin/bash
set -euo pipefail

OUTFILE="$(mktemp)"
cleanup() {
    CODE=$?
    rm "$OUTFILE"
    exit $CODE
}
trap cleanup EXIT

if [ -z "$1" ]; then
    echo "Lambda ARN required"
    exit 1
fi

# Config goes in aws.json
fn_arn="$(jq ."$1" aws.json)"

cp out.json "$OUTFILE"
#aws lambda invoke --function-name "$fn_arn" --payload file://config.json --cli-binary-format raw-in-base64-out --no-cli-pager --cli-read-timeout 0 "$OUTFILE"

echo "Status: $(jq -r .status "$OUTFILE")"
echo "Standard output:"
jq -r .stdout "$OUTFILE"
echo "Standard error:"
jq -r .stderr "$OUTFILE"

import sys
import json

resp = json.load(sys.stdin)
if "errorType" in resp:
    print("Traceback (most recent call last):", file=sys.stderr)
    print("".join(resp['stackTrace']), file=sys.stderr)
    print(f"{resp['errorType']}: {resp['errorMessage']}", file=sys.stderr)
    sys.exit(1)
else:
    print(resp)

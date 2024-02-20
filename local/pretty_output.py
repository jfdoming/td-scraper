import json
import sys

resp = json.load(sys.stdin)
print("---")
if "errorType" in resp:
    print(resp["errorMessage"], file=sys.stderr)
    sys.exit(1)
else:
    print(resp)

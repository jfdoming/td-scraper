import json
import sys

resp = json.load(sys.stdin)
print("---")
if "errorType" in resp:
    print(resp["errorMessage"], file=sys.stderr)
    sys.exit(1)
elif "status" in resp:
    print(resp["stdout"])
    print(resp["stderr"], file=sys.stderr)
    if resp["status"] == "error":
        sys.exit(1)

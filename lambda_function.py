import json
import subprocess


def lambda_handler(event, _):
    result = subprocess.run(
        ["python", "main.py", json.dumps(event)], capture_output=True
    )
    if result.returncode != 0:
        raise AssertionError(result.stderr.decode("utf-8"))

    try:
        return json.loads(result.stdout.decode("utf-8"))
    except json.JSONDecodeError:
        return {"error": result.stdout.decode("utf-8")}


if __name__ == "__main__":
    raise AssertionError(
        "Function should be called from a lambda docker image"
    )

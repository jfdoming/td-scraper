import json
import os
import subprocess
import sys
from io import FileIO
from tempfile import TemporaryFile


def get_env():
    env = os.environ.copy()

    # Keep the PYTHONPATH from the lambda environment
    env["PYTHONPATH"] = ":".join(sys.path)

    # Don't buffer stdout/stderr
    env["PYTHONUNBUFFERED"] = "1"

    # Disable dbus
    env["DBUS_SESSION_BUS_ADDRESS"] = "/dev/null"

    return env


def TempFile():
    return TemporaryFile(mode="w+b")


def read_file(file: FileIO):
    file.seek(0)
    return file.read().decode("utf-8")


def lambda_handler(event, _):
    with TempFile() as stdout, TempFile() as stderr:
        try:
            subprocess.run(
                ["python", "main.py", json.dumps(event)],
                stdout=stdout,
                stderr=stderr,
                check=True,
                env=get_env(),
                timeout=30,
            )
            return json.loads(read_file(stdout))
        except subprocess.TimeoutExpired as e:
            error_message = str(
                subprocess.TimeoutExpired(
                    ["python", "main.py", "..."],
                    e.timeout,
                )
            )
        except (
            json.JSONDecodeError,
            subprocess.CalledProcessError,
        ) as e:
            error_message = str(e)

        return {
            "status": "error",
            "stdout": read_file(stdout),
            "stderr": read_file(stderr) + "\n---\n" + error_message,
        }


if __name__ == "__main__":
    raise AssertionError(
        "Function should be called from a lambda docker image"
    )

#!/usr/bin/env python3
"""Test one-backend failure, traffic availability, and recovery."""

import json
import subprocess
import sys
import time
import urllib.error
import urllib.request

BASE_URL = "http://localhost:8080"
TARGET = "app-01"
REQUEST_TIMEOUT = 3
FAILURE_SAMPLES = 20
RECOVERY_WAIT_SECONDS = 45

passed = 0
failed = 0


def report(name, condition, detail=""):
    global passed, failed
    if condition:
        print(f"PASS: {name}")
        passed += 1
    else:
        print(f"FAIL: {name}" + (f" — {detail}" if detail else ""))
        failed += 1


def compose(action, service):
    try:
        return subprocess.run(
            ["docker", "compose", action, service],
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f"ERROR: docker compose {action} {service}: {exc}")
        return None


def request(path):
    req = urllib.request.Request(BASE_URL + path, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as response:
            raw = response.read().decode("utf-8")
            try:
                body = json.loads(raw)
            except json.JSONDecodeError:
                body = {}
            return response.status, body
    except urllib.error.HTTPError as exc:
        return exc.code, {}
    except Exception:
        return None, {}


def wait_for_instance(instance_id):
    deadline = time.monotonic() + RECOVERY_WAIT_SECONDS

    while time.monotonic() < deadline:
        status, body = request("/instance")
        if status == 200 and body.get("instance_id") == instance_id:
            return True
        time.sleep(1)

    return False


def main():
    print("=== BARQ backend failure and recovery test ===")
    print(f"Target backend: {TARGET}")

    print("\n1. Stop target backend")
    stopped = compose("stop", TARGET)
    if stopped is None or stopped.returncode != 0:
        report(
            "target backend stopped",
            False,
            stopped.stderr.strip() if stopped else "command failed",
        )
        return 1

    report("target backend stopped", True)

    successes = 0
    errors = 0
    observed_instances = set()

    try:
        print(f"\n2. Send {FAILURE_SAMPLES} requests through NGINX")
        for _ in range(FAILURE_SAMPLES):
            status, body = request("/instance")

            if status == 200:
                successes += 1
                instance_id = body.get("instance_id")
                if instance_id:
                    observed_instances.add(instance_id)
            else:
                errors += 1

            time.sleep(0.2)

        total = successes + errors
        availability = (successes / total * 100) if total else 0

        print(f"Requests: {total}")
        print(f"Successful: {successes}")
        print(f"Failed/errors: {errors}")
        print(f"Availability: {availability:.1f}%")
        print(f"Backend instances observed: {sorted(observed_instances)}")

        report(
            "remaining backend served requests during failure",
            "app-02" in observed_instances,
            f"observed: {sorted(observed_instances)}",
        )

    finally:
        print(f"\n3. Restore {TARGET}")
        started = compose("start", TARGET)
        start_ok = started is not None and started.returncode == 0

        report(
            "target backend start command succeeded",
            start_ok,
            started.stderr.strip() if started else "command failed",
        )

        if start_ok:
            recovered = wait_for_instance(TARGET)
            report(
                "target backend recovered and served a request",
                recovered,
                f"{TARGET} not observed within {RECOVERY_WAIT_SECONDS}s",
            )
        else:
            recovered = False
            print("WARNING: Could not start the target backend.")

    print()
    print(f"RESULT: {passed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

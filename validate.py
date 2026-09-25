#!/usr/bin/env python3
"""Validate the BARQ Compose application through its public NGINX endpoint."""

import json
import subprocess
import sys
import time
import urllib.error
import urllib.request

BASE_URL = "http://localhost:8080"
REQUEST_TIMEOUT = 3
READY_WAIT_SECONDS = 45
INSTANCE_SAMPLES = 30

passed = 0
failed = 0


def check(name, condition, detail=""):
    global passed, failed
    if condition:
        print(f"PASS: {name}")
        passed += 1
    else:
        suffix = f" — {detail}" if detail else ""
        print(f"FAIL: {name}{suffix}")
        failed += 1


def request(path, method="GET", body=None):
    data = None
    headers = {}

    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(
        BASE_URL + path,
        data=data,
        headers=headers,
        method=method,
    )

    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as response:
            raw = response.read().decode("utf-8")
            try:
                payload = json.loads(raw)
            except json.JSONDecodeError:
                payload = {}
            return response.status, payload
    except urllib.error.HTTPError as exc:
        try:
            payload = json.loads(exc.read().decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            payload = {}
        return exc.code, payload
    except Exception as exc:
        return None, {"error": str(exc)}


def compose(*args):
    try:
        return subprocess.run(
            ["docker", "compose", *args],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None


def wait_for_ready():
    deadline = time.monotonic() + READY_WAIT_SECONDS
    last_status = None

    while time.monotonic() < deadline:
        status, body = request("/ready")
        last_status = status
        if status == 200 and body.get("status") == "ready":
            return True, ""
        time.sleep(1)

    return False, (
        f"readiness not reached within {READY_WAIT_SECONDS}s; "
        f"last HTTP status: {last_status}"
    )


def container_status(service):
    result = compose("ps", "-q", service)
    if result is None or result.returncode != 0:
        return None, "could not query Docker Compose"

    container_id = result.stdout.strip()
    if not container_id:
        return None, "container is not created"

    try:
        inspect = subprocess.run(
            [
                "docker", "inspect",
                "--format", "{{.State.Status}}",
                container_id,
            ],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None, "docker inspect failed or timed out"

    if inspect.returncode != 0:
        return None, inspect.stderr.strip() or "docker inspect failed"

    return inspect.stdout.strip(), ""


def no_host_port(service, container_port):
    result = compose("ps", "-q", service)
    if result is None or result.returncode != 0:
        return False, "could not query Docker Compose"

    container_id = result.stdout.strip()
    if not container_id:
        return False, "container is not created"

    try:
        inspect = subprocess.run(
            [
                "docker", "inspect",
                "--format",
                "{{json .NetworkSettings.Ports}}",
                container_id,
            ],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False, "docker inspect failed or timed out"

    if inspect.returncode != 0:
        return False, inspect.stderr.strip() or "docker inspect failed"

    try:
        bindings = json.loads(inspect.stdout)
    except json.JSONDecodeError:
        return False, "could not parse container port bindings"

    published = bindings.get(f"{container_port}/tcp")
    if published:
        return False, f"published at {published}"

    return True, ""


print("=== BARQ validation ===")

ready, detail = wait_for_ready()
check("application readiness within bounded wait", ready, detail)

for path in ("/", "/health", "/ready", "/instance"):
    status, _ = request(path)
    check(f"GET {path} returns HTTP 200", status == 200, f"got {status}")

status, _ = request("/records")
check("GET /records returns HTTP 200", status == 200, f"got {status}")

status, _ = request(
    "/records",
    method="POST",
    body={"title": "validate-script-check"},
)
check("POST /records returns HTTP 201", status == 201, f"got {status}")

status, _ = request("/counter")
check("GET /counter returns HTTP 200", status == 200, f"got {status}")

instances = set()
for _ in range(INSTANCE_SAMPLES):
    status, body = request("/instance")
    if status == 200 and isinstance(body, dict):
        instance_id = body.get("instance_id")
        if instance_id:
            instances.add(instance_id)

check(
    "both backend instances observed through NGINX",
    {"app-01", "app-02"}.issubset(instances),
    f"observed {sorted(instances)}",
)

for service in ("app-01", "app-02", "nginx", "postgres", "redis"):
    status, detail = container_status(service)
    check(
        f"{service} container is running",
        status == "running",
        detail or f"state: {status}",
    )

ok, detail = no_host_port("postgres", 5432)
check("PostgreSQL has no published host port", ok, detail)

ok, detail = no_host_port("redis", 6379)
check("Redis has no published host port", ok, detail)

print()
print(f"RESULT: {passed} passed, {failed} failed")
sys.exit(1 if failed else 0)

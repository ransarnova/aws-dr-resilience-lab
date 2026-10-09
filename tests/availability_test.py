import time
import urllib.request
import urllib.error
from datetime import datetime, timezone

URL = "http://localhost:8080/health/live"

success = 0
failure = 0

print("Starting availability test. Press Ctrl+C to stop.")

try:
    while True:
        start = time.monotonic()

        try:
            with urllib.request.urlopen(URL, timeout=2) as response:
                status = response.status

            if status == 200:
                success += 1
                result = "SUCCESS"
            else:
                failure += 1
                result = "FAILURE"

        except (urllib.error.URLError, TimeoutError, OSError):
            failure += 1
            status = "ERROR"
            result = "FAILURE"

        latency = round((time.monotonic() - start) * 1000, 2)

        timestamp = datetime.now(timezone.utc).isoformat()

        print(
            f"{timestamp} | {result} | "
            f"status={status} | latency={latency}ms",
            flush=True,
        )

        time.sleep(0.5)

except KeyboardInterrupt:
    total = success + failure

    print("\n--- Availability Summary ---")
    print(f"Total requests: {total}")
    print(f"Successful: {success}")
    print(f"Failed: {failure}")

    if total:
        print(f"Observed success rate: {success / total * 100:.2f}%")

import argparse
import asyncio
import json
import os
import time

import aiohttp

TIMEOUT = aiohttp.ClientTimeout(total=10)


async def check_target(session, target):
    start_time = time.perf_counter()
    try:
        async with session.get(target["url"]) as response:
            latency = round((time.perf_counter() - start_time) * 1000, 2)
            status = "Online" if response.status == 200 else "Degraded"
            return {"name": target["name"], "url": target["url"], "status": status,
                    "latency_ms": latency, "checked_at": time.time()}
    except (aiohttp.ClientError, asyncio.TimeoutError):
        return {"name": target["name"], "url": target["url"], "status": "Offline",
                "latency_ms": None, "checked_at": time.time()}


def write_status(results, path="status.json"):
    tmp_path = path + ".tmp"
    with open(tmp_path, "w") as f:
        json.dump(results, f, indent=2)
    os.replace(tmp_path, path)  # atomic swap so the page never reads a half-written file


async def run_checks(session, targets):
    results = await asyncio.gather(*(check_target(session, t) for t in targets))
    write_status(results)
    summary = ", ".join(f"{r['name']}: {r['status']}" for r in results)
    print(f"[{time.strftime('%H:%M:%S')}] {summary}")


async def main(interval, once):
    with open("config.json", "r") as f:
        targets = json.load(f)["targets"]

    async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
        while True:
            await run_checks(session, targets)
            if once:
                break
            await asyncio.sleep(interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Async API uptime monitor")
    parser.add_argument("--interval", type=int, default=30, help="seconds between checks")
    parser.add_argument("--once", action="store_true", help="run a single check and exit")
    args = parser.parse_args()
    try:
        asyncio.run(main(args.interval, args.once))
    except KeyboardInterrupt:
        print("Monitor stopped.")

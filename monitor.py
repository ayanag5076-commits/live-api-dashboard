import asyncio
import aiohttp
import json
import time

async def check_target(session, target):
    start_time = time.time()
    try:
        async with session.get(target['url'], timeout=10) as response:
            latency = round((time.time() - start_time) * 1000, 2)
            status = "Online" if response.status == 200 else "Degraded"
            return {"name": target['name'], "url": target['url'], "status": status, "latency_ms": latency}
    except Exception:
        return {"name": target['name'], "url": target['url'], "status": "Offline", "latency_ms": 0}

async def main():
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    async with aiohttp.ClientSession() as session:
        tasks = [check_target(session, t) for t in config['targets']]
        results = await asyncio.gather(*tasks)
        
    with open('status.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("API status update successfully written to status.json")

if __name__ == "__main__":
    asyncio.run(main())

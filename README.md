# Async Live API Status Dashboard

A production-ready Python automation tool that monitors the uptime and response latency of public web APIs asynchronously, presenting the status on a clean frontend dashboard.

## Features
- **Asynchronous Polling:** Uses Python's `asyncio` and `aiohttp` libraries to ping multiple API endpoints concurrently, minimizing execution overhead.
- **Robust Failover:** Features timeout configurations and fallback handling to classify endpoints as Online, Degraded, or Offline.
- **Decoupled Architecture:** The background monitoring engine (`monitor.py`) handles data processing and writes to a state file (`status.json`), keeping backend operations independent from presentation layout (`index.html`).

## Installation & Setup
1. Clone the repository:
   ```bash
   git clone https://github.com
   cd live-api-dashboard
   ```
2. Install the missing dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

## Running the Application
1. Execute the backend data poller to fetch current network statistics:
   ```bash
   python3 monitor.py
   ```
2. Open `index.html` inside any standard browser window to observe the live status layout.

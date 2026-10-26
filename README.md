# Async Live API Status Dashboard

A Python tool that monitors the uptime and response latency of web APIs asynchronously and shows their status on a live-updating dashboard.

## Features
- **Asynchronous polling:** Uses `asyncio` and `aiohttp` to check every endpoint concurrently, so one slow API never holds up the rest.
- **Status classification:** A 10-second timeout and error handling classify each endpoint as Online (HTTP 200), Degraded (any other status), or Offline (timeout or connection error).
- **Continuous monitoring:** Re-checks on a configurable interval (default 30 seconds), or runs a single check with `--once`.
- **Decoupled architecture:** The monitor (`monitor.py`) writes results atomically to `status.json`; the dashboard (`index.html`) polls that file every 10 seconds, keeping the backend independent from presentation.

## Installation
```bash
git clone https://github.com/ayanag5076-commits/live-api-dashboard.git
cd live-api-dashboard
pip3 install -r requirements.txt
```

## Usage
1. Start the monitor:
   ```bash
   python3 monitor.py              # checks every 30 seconds
   python3 monitor.py --interval 10
   python3 monitor.py --once       # single check, then exit
   ```
2. In a second terminal, serve the dashboard (browsers block loading local files directly):
   ```bash
   python3 -m http.server 8000
   ```
3. Open http://localhost:8000 in your browser.

## Configuration
Add or remove endpoints in `config.json`:
```json
{
  "targets": [
    {"name": "GitHub", "url": "https://github.com"}
  ]
}
```

## Tech stack
Python 3, asyncio, aiohttp, HTML, JavaScript, Tailwind CSS

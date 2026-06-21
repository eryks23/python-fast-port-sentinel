# Network Sentinel

![Python][(https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/)
![License](https://img.shields.io/badge/license-MIT-green)
![Dependencies](https://img.shields.io/badge/dependencies-none-lightgrey)

A lightweight, multithreaded TCP port scanner written in pure Python.

**Repository:** [eryks23/python-fast-port-sentinel](https://github.com/eryks23/python-fast-port-sentinel)
**Entry point:** `network_scanner.py`

## Description

Network Sentinel scans a configurable range of TCP ports on a target host and reports which ones accept connections, resolving the standard service name for each open port (e.g., `80` → `http`). It gives developers, students, and system administrators a fast, dependency-free way to check which network services are reachable on a machine, without installing a full scanning suite such as Nmap. The tool runs interactively from the command line and prints a sorted, timestamped summary report once the scan completes.

## Table of Contents

- [Legal Notice](#legal-notice)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author--contact)

## Legal Notice

This tool performs active TCP connection attempts against a target host. Only scan hosts and networks that you own or have explicit written authorization to test. Scanning systems without permission may violate computer-misuse laws (such as the U.S. Computer Fraud and Abuse Act) or local equivalents, and may breach the acceptable-use policy of your network or hosting provider. The maintainer assumes no liability for misuse of this software.

## Key Features

- **Multithreaded scanning** — spawns one thread per port, scanning the full default range (1–1024) in a few seconds instead of sequentially.
- **Service name resolution** — maps open ports to their registered service (e.g., `22` → `ssh`) via the system services database, falling back to `UNKNOWN` when no mapping exists.
- **Zero external dependencies** — runs anywhere Python 3 is installed; no `pip install` required.
- **Colorized CLI output** — ANSI colors highlight the banner, open ports, and summary report.
- **Interactive target selection** — prompts for a target host at startup and defaults to `127.0.0.1` when left blank.
- **Sorted summary report** — prints a timestamped, sorted list of every open port found.

## Tech Stack

| Component | Details |
|---|---|
| Language | Python 3.6+ |
| Concurrency | `threading` — one thread per port |
| Networking | `socket` — TCP connect scan via `connect_ex` |
| Output | ANSI escape codes for terminal colors |
| Dependencies | None — standard library only |

## Requirements

- Python 3.6 or later (the codebase uses f-strings throughout).
- No third-party packages.
- Outbound network access to the target host. No administrator/root privileges are required: the scanner only opens outbound client connections and never binds a local port or uses raw sockets.
- Note: rapid, sequential connection attempts can resemble a port-scan signature. Local firewalls, antivirus, or endpoint-detection software may flag or throttle this behavior.

## Installation

```bash
git clone https://github.com/eryks23/python-fast-port-sentinel.git
cd python-fast-port-sentinel
```

A virtual environment isn't required today (there are no dependencies yet) but is recommended to keep the project isolated as it grows:

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

There is no `.env` file or external configuration file. Two values can currently be changed:

| Setting | How to change | Default |
|---|---|---|
| Target host | Entered interactively at runtime | `127.0.0.1` |
| Port range | Edit the `scanner.run(1, 1024)` call in the `__main__` block | `1`–`1024` |

Exposing these as command-line flags is tracked in [Roadmap](#roadmap).

## Usage

Run the script and follow the prompt:

```bash
python3 network_scanner.py
```

```text
Enter target host (default 127.0.0.1): 127.0.0.1
```

Example session (ANSI colors omitted for readability):

```text
SCIENTIFIC PROJECT
NETWORK SENTINEL v1.0
-----------------------------------------

[*] Initializing scan for: 127.0.0.1
[*] Range: 1 - 1024

 [+] Port 80 (http) is OPEN
 [+] Port 443 (https) is OPEN

========================================
SENTINEL REPORT - 14:32:05
========================================
 > PORT 80    | SERVICE: http
 > PORT 443   | SERVICE: https
========================================
SYSTEM READY. WAITING FOR NEXT COMMAND.
```

## API Reference

### `NetworkScanner`

```python
NetworkScanner(target_host: str)
```

| Parameter | Type | Description |
|---|---|---|
| `target_host` | `str` | Hostname or IP address to scan. |

**Attributes**

- `open_ports: list[tuple[int, str]]` — `(port, service_name)` pairs for every open port found, populated by `scan_port()`.

#### `scan_port(port)`

```python
scan_port(port: int) -> None
```

Attempts a TCP connection to `port` on `target_host` with a 0.5-second timeout. On success, resolves the service name with `socket.getservbyport()` (falling back to `"UNKNOWN"` if unmapped), appends `(port, service)` to `open_ports`, and prints the result. Any exception — timeout, connection refused, unreachable host — is caught and silently ignored.

#### `run(start_port, end_port)`

```python
run(start_port: int, end_port: int) -> None
```

Scans every port in the inclusive range `[start_port, end_port]`. Spawns one thread per port, pausing briefly every 100 threads to soften the burst, waits for every thread to finish, then calls `report()`.

#### `report()`

```python
report() -> None
```

Prints a timestamped summary of `open_ports`, sorted in ascending order, or a "no active services" message if the list is empty.

### `print_banner()`

```python
print_banner() -> None
```

Module-level helper that prints the colored startup banner. Takes no arguments and returns nothing.

## Project Structure

```text
python-fast-port-sentinel/
├── network_scanner.py   # Entry point: NetworkScanner class + CLI prompt
├── requirements.txt     # Dependency list (currently empty — stdlib only)
├── README.md            # Project documentation
└── LICENSE              # MIT license
```

## Testing

No automated test suite is included yet. To verify behavior manually:

1. Start a local listener on a known port:

```bash
python3 -m http.server 8000
```

2. In a separate terminal, run the scanner against `127.0.0.1` and confirm port `8000` is reported as `OPEN`:

```bash
python3 network_scanner.py
```

3. Exercise the public API directly, without the interactive prompt:

```bash
python3 -c "from network_scanner import NetworkScanner; s = NetworkScanner('127.0.0.1'); s.scan_port(8000); print(s.open_ports)"
```

Contributions adding a `pytest` suite (e.g., mocking `socket.socket().connect_ex`) are welcome.

## Roadmap

Suggested directions for future versions — not committed deliverables:

- [ ] Replace the interactive prompt and hardcoded range with CLI arguments (`argparse`).
- [ ] Bound concurrency with `concurrent.futures.ThreadPoolExecutor` instead of one thread per port.
- [ ] Add an automated test suite.
- [ ] Export results to JSON/CSV.
- [ ] Optional UDP scanning.

## Contributing

1. Fork the repository and create a feature branch: `git checkout -b feature/your-feature`.
2. Keep changes focused and follow PEP 8.
3. Open a pull request with a clear description and, for behavioral changes, before/after example output.
4. For larger changes, open an issue first to discuss the approach.

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for the full text.

## Author 

Maintained by [eryks23](https://github.com/eryks23).

- Repository: [python-fast-port-sentinel](https://github.com/eryks23/python-fast-port-sentinel)

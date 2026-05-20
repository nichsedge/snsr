# snsr

A playful Python-based "screensaver" that randomly moves your mouse and simulates key presses to keep your screen active.

## Features

- Moves the mouse to random screen positions.
- Simulates random key presses.
- Keeps your system from going idle (uses `wakepy` when available).
- Auto-selects an input backend per platform (`pynput` on Linux, `pyautogui` elsewhere) with fallback.

## Usage

### Using `uv`

```bash
uvx snsr
```

`snsr` auto-detects your platform/session and picks the best backend (Linux defaults to the `pynput` backend; macOS and Windows use `pyautogui`), with fallback if the preferred backend fails to start.

### Using pip

```bash
pip install snsr
snsr
```

It will:

* Move your mouse to random points (or jiggle relative on Linux)
* Press a random key (default set: `a`, `s`, `d`, `f`, `j`, `k`, `l`)
* Repeat every few seconds

### Options

```
snsr [--interval LOW HIGH] [--keys CHARS] [--backend {auto,pyautogui,pynput}]
     [--no-failsafe] [--dry-run] [-v]
```

* `--interval LOW HIGH` — random sleep range in seconds between actions (default `1 5`).
* `--keys CHARS` — string of single-character keys to choose from (default `asdfjkl`).
* `--backend` — force a specific backend, or leave on `auto`.
* `--no-failsafe` — disable pyautogui's corner-abort failsafe (off by default — moving the mouse to a screen corner aborts).
* `--dry-run` — log what would happen without actually moving the mouse or pressing keys.
* `-v`, `--verbose` — debug logging.

Logs are written to a per-platform user state directory (e.g. `~/.local/state/snsr/snsr.log` on Linux, `%LOCALAPPDATA%\snsr\snsr.log` on Windows, `~/Library/Logs/snsr/snsr.log` on macOS).

### To Stop

Press `Ctrl+C` in the terminal to exit. By default the pyautogui backend also lets you abort by slamming the mouse into a screen corner.

## Notes

* Ensure your OS allows simulated input events from Python scripts.
* Useful for keeping your machine awake during long tasks (e.g., rendering, builds, meetings).

## Disclaimer

This project is intended for educational or personal use only. Use responsibly and respect your organization's policies regarding input automation.

---

MIT License © 2025

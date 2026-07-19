import argparse
import logging
import os
import platform
import sys
import tempfile
from pathlib import Path


DEFAULT_KEYS = "asdfjkl"


def _log_path():
    if xdg := os.environ.get("XDG_STATE_HOME"):
        base = Path(xdg) / "snsr"
    elif sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / "snsr"
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Logs" / "snsr"
    else:
        base = Path.home() / ".local" / "state" / "snsr"

    try:
        base.mkdir(parents=True, exist_ok=True)
        return base / "snsr.log"
    except OSError:
        return Path(tempfile.gettempdir()) / "snsr.log"


def _setup_logging(verbose):
    log_file = _log_path()
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout),
        ],
    )
    logging.info(f"Log file: {log_file}")
    info = platform.system()
    if sys.platform.startswith("linux"):
        info += " (Wayland)" if os.environ.get("WAYLAND_DISPLAY") else " (X11/Other)"
    logging.info(f"Platform: {info}")


def _auto_backend_name():
    return "pynput" if platform.system().lower() == "linux" else "pyautogui"


def _build_backend(name, *, failsafe):
    if name == "pynput":
        from .pynput_backend import PynputBackend
        return PynputBackend()
    if name == "pyautogui":
        from .pyautogui_backend import PyAutoGuiBackend
        return PyAutoGuiBackend(failsafe=failsafe)
    raise ValueError(f"Unknown backend: {name}")


def parse_args(argv=None):
    p = argparse.ArgumentParser(
        prog="snsr",
        description="Randomly move the mouse and press keys to keep the screen active.",
    )
    p.add_argument(
        "--interval",
        type=float,
        nargs=2,
        metavar=("LOW", "HIGH"),
        default=(1.0, 5.0),
        help="Random sleep range between actions, in seconds (default: 1 5).",
    )
    p.add_argument(
        "--keys",
        default=DEFAULT_KEYS,
        help=f"String of single-character keys to choose from (default: {DEFAULT_KEYS!r}).",
    )
    p.add_argument(
        "--backend",
        choices=["auto", "pyautogui", "pynput"],
        default="auto",
        help="Which input backend to use (default: auto).",
    )
    p.add_argument(
        "--no-failsafe",
        action="store_true",
        help="Disable pyautogui's corner-abort failsafe.",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Log what would happen without actually moving the mouse or pressing keys.",
    )
    p.add_argument("-v", "--verbose", action="store_true")

    args = p.parse_args(argv)
    if args.interval[0] < 0 or args.interval[1] < args.interval[0]:
        p.error("--interval requires 0 <= LOW <= HIGH")
    if not args.keys:
        p.error("--keys cannot be empty")
    return args


def run_screensaver(argv=None):
    args = parse_args(argv)
    _setup_logging(args.verbose)

    from .loop import run_loop

    preferred = _auto_backend_name() if args.backend == "auto" else args.backend
    fallback = "pyautogui" if preferred == "pynput" else "pynput"
    candidates = [preferred] if args.backend != "auto" else [preferred, fallback]

    keys = list(args.keys)
    last_error = None
    for name in candidates:
        try:
            backend = _build_backend(name, failsafe=not args.no_failsafe)
        except Exception as e:
            logging.error(f"Backend '{name}' failed to initialize: {e}")
            last_error = e
            continue

        logging.info(f"Using backend: {name}")
        run_loop(
            backend,
            interval_low=args.interval[0],
            interval_high=args.interval[1],
            keys=keys,
            dry_run=args.dry_run,
        )
        return

    logging.error("Both GUI automation backends failed to initialize.")
    logging.error("This is common on Wayland/headless systems when display access is not authorized.")
    logging.error("Troubleshooting tips:")
    logging.error("  * Run 'xhost +local:' in your terminal to allow local GUI connections.")
    logging.error("  * Ensure DISPLAY and XAUTHORITY environment variables are set correctly.")
    logging.info("Attempting to fall back to wakepy-only mode (preventing system sleep via D-Bus)...")

    try:
        from wakepy import keep
        logging.info("wakepy-only mode active. Running... Press Ctrl+C to stop.")
        with keep.presenting():
            import time
            while True:
                time.sleep(10)
    except Exception as wakepy_error:
        logging.critical(f"wakepy-only mode also failed: {wakepy_error}")
        raise SystemExit(f"No usable backend ({last_error})")


if __name__ == "__main__":
    run_screensaver()

#!/usr/bin/env python3
import os
import platform


def _select_backend():
    system = platform.system().lower()

    # Linux desktop sessions often need the pynput-based backend.
    if system == "linux":
        if os.environ.get("WAYLAND_DISPLAY") or os.environ.get("XDG_SESSION_TYPE") in {
            "wayland",
            "x11",
        }:
            return "main_ubuntu"
        return "main_ubuntu"

    # macOS and Windows are best served by the pyautogui backend.
    return "main"


def run_screensaver():
    preferred = _select_backend()
    fallback = "main" if preferred == "main_ubuntu" else "main_ubuntu"

    try:
        module = __import__(preferred, fromlist=["run_screensaver"])
        module.run_screensaver()
        return
    except Exception as preferred_error:
        print(f"[snsr] failed on '{preferred}', trying fallback '{fallback}': {preferred_error}")

    module = __import__(fallback, fromlist=["run_screensaver"])
    module.run_screensaver()


if __name__ == "__main__":
    run_screensaver()

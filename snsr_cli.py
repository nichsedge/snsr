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
        print(f"[snsr] failed on '{preferred}': {preferred_error}")

    print(f"[snsr] trying fallback '{fallback}'...")
    try:
        module = __import__(fallback, fromlist=["run_screensaver"])
        module.run_screensaver()
        return
    except Exception as fallback_error:
        print(f"[snsr] failed on fallback '{fallback}': {fallback_error}")

    # Fallback to wakepy-only mode if GUI automation fails entirely
    print("\n[snsr] Both GUI automation backends failed to initialize.")
    print("[snsr] This is common on Wayland/headless systems when display access is not authorized.")
    print("[snsr] Troubleshooting tips:")
    print("  * Run 'xhost +local:' in your terminal to allow local GUI connections.")
    print("  * Ensure DISPLAY and XAUTHORITY environment variables are set correctly.")
    print("\n[snsr] Attempting to fall back to wakepy-only mode (preventing system sleep via D-Bus)...")

    try:
        from wakepy import keep
        print("[snsr] wakepy-only mode active. Running... Press Ctrl+C to stop.")
        with keep.presenting():
            import time
            while True:
                time.sleep(10)
    except Exception as wakepy_error:
        print(f"[snsr] wakepy-only mode also failed: {wakepy_error}")
        print("[snsr] Exiting.")


if __name__ == "__main__":
    run_screensaver()

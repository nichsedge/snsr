#!/usr/bin/env python3
import os
import random
import time
import platform
import logging
import sys
import contextlib
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController

# Optional dependency for robust screensaver inhibition
try:
    from wakepy import keep
    WAKEPY_AVAILABLE = True
except ImportError:
    WAKEPY_AVAILABLE = False

# Setup logging
log_file = os.path.join(os.getcwd(), "snsr.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

def run_screensaver():
    logging.info("Starting snsr...")
    logging.info(f"Platform: {platform.system()} ({'Wayland' if os.environ.get('WAYLAND_DISPLAY') else 'X11/Other'})")
    logging.info(f"Python Version: {sys.version}")
    logging.info(f"Log file: {log_file}")
    
    if not WAKEPY_AVAILABLE:
        logging.warning("wakepy not found. Idle prevention might be less reliable.")

    mouse = MouseController()
    keyboard = KeyboardController()
    
    logging.info("Running... Press Ctrl+C to stop.")
    
    # Use wakepy to keep the system awake
    keep_awake = keep.presenting() if WAKEPY_AVAILABLE else contextlib.nullcontext()
    
    try:
        with keep_awake:
            if WAKEPY_AVAILABLE:
                logging.info("System-wide idle prevention active via wakepy.")
            else:
                logging.info("Relying solely on input simulation for idle prevention.")

            last_heartbeat = time.time()
            while True:
                # Random mouse movement (relative)
                try:
                    dx = random.randint(-150, 150)
                    dy = random.randint(-150, 150)
                    logging.debug(f"Moving mouse: {dx}, {dy}")
                    mouse.move(dx, dy)
                    time.sleep(0.1)
                    mouse.move(-dx, -dy)
                except Exception as e:
                    logging.error(f"Mouse movement failed: {e}")
                
                # Random key press
                try:
                    key = random.choice(['a', 's', 'd', 'f', 'j', 'k', 'l'])
                    keyboard.press(key)
                    keyboard.release(key)
                    logging.debug(f"Pressed key: {key}")
                except Exception as e:
                    logging.error(f"Key press failed: {e}")
                
                # Periodic heartbeat to log
                if time.time() - last_heartbeat > 60:
                    logging.info("Still active...")
                    last_heartbeat = time.time()

                time.sleep(random.uniform(5, 15))
    except KeyboardInterrupt:
        logging.info("Stopping snsr (received KeyboardInterrupt)...")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    run_screensaver()

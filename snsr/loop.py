import contextlib
import logging
import random
import time

try:
    from wakepy import keep
    WAKEPY_AVAILABLE = True
except ImportError:
    WAKEPY_AVAILABLE = False


def run_loop(backend, *, interval_low, interval_high, keys, dry_run=False):
    keep_awake = keep.presenting() if WAKEPY_AVAILABLE else contextlib.nullcontext()
    last_heartbeat = time.time()

    try:
        with keep_awake:
            if WAKEPY_AVAILABLE:
                logging.info("System-wide idle prevention active via wakepy.")
            else:
                logging.info("wakepy not available; relying on input simulation only.")

            while True:
                try:
                    if dry_run:
                        logging.debug("dry-run: skipping mouse jiggle")
                    else:
                        backend.jiggle_mouse()
                except Exception as e:
                    logging.error(f"Mouse movement failed: {e}")

                try:
                    key = random.choice(keys)
                    if dry_run:
                        logging.debug(f"dry-run: would press {key}")
                    else:
                        backend.tap_key(key)
                        logging.debug(f"Pressed key: {key}")
                except Exception as e:
                    logging.error(f"Key press failed: {e}")

                if time.time() - last_heartbeat > 60:
                    logging.info("Still active...")
                    last_heartbeat = time.time()

                time.sleep(random.uniform(interval_low, interval_high))
    except KeyboardInterrupt:
        logging.info("Stopping snsr (received KeyboardInterrupt).")

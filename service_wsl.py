import json
import os
import signal
import sys
import time

from simulator import Simulator, SimulationConfig


CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
_running = True


def load_config() -> SimulationConfig:
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    except Exception:
        data = {}
    return SimulationConfig(
        clicks_per_minute=int(data.get("cpm", 120)),
        key=str(data.get("key", "space")),
        mouse_enable=bool(data.get("mouse_enable", True)),
        mouse_interval_seconds=float(data.get("mouse_interval", 5.0)),
        randomize_interval=bool(data.get("randomize_interval", False)),
    )


def _handle_signal(signum, frame):  # noqa: ARG001
    global _running
    _running = False


def main() -> int:
    signal.signal(signal.SIGTERM, _handle_signal)
    signal.signal(signal.SIGINT, _handle_signal)

    config = load_config()
    simulator = Simulator(config)
    simulator.start()
    try:
        while _running:
            time.sleep(1.0)
    finally:
        simulator.stop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())



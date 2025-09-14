import threading
import time
import random
from dataclasses import dataclass
from typing import Optional, List

import pyautogui


def jitter_interval(base_seconds: float, enabled: bool, jitter_ratio: float = 0.1) -> float:
    if not enabled:
        return base_seconds
    delta = base_seconds * jitter_ratio
    return max(0.0, random.uniform(base_seconds - delta, base_seconds + delta))


class StoppableWorker(threading.Thread):
    def __init__(self, target, name: str, *args, **kwargs):
        super().__init__(name=name)
        self._stop_event = threading.Event()
        self._target_func = target
        self._args = args
        self._kwargs = kwargs

    def stop(self) -> None:
        self._stop_event.set()

    def stopped(self) -> bool:
        return self._stop_event.is_set()

    def run(self) -> None:
        self._target_func(self._stop_event, *self._args, **self._kwargs)


def keyboard_worker(stop_event: threading.Event, clicks_per_minute: int, key: str, randomize: bool) -> None:
    if clicks_per_minute <= 0:
        return
    seconds_per_click = 60.0 / float(clicks_per_minute)
    while not stop_event.is_set():
        pyautogui.press(key)
        sleep_seconds = jitter_interval(seconds_per_click, randomize)
        stop_event.wait(sleep_seconds)


def mouse_worker(stop_event: threading.Event, interval_seconds: float, randomize: bool) -> None:
    if interval_seconds <= 0:
        return
    screen_width, screen_height = pyautogui.size()
    amplitude_pixels = max(1, min(screen_width, screen_height) // 200)
    while not stop_event.is_set():
        dx = random.randint(-amplitude_pixels, amplitude_pixels)
        dy = random.randint(-amplitude_pixels, amplitude_pixels)
        pyautogui.moveRel(dx, dy, duration=0.1)
        pyautogui.moveRel(-dx, -dy, duration=0.1)
        sleep_seconds = jitter_interval(interval_seconds, randomize)
        stop_event.wait(sleep_seconds)


@dataclass
class SimulationConfig:
    clicks_per_minute: int = 120
    key: str = "space"
    mouse_enable: bool = True
    mouse_interval_seconds: float = 5.0
    randomize_interval: bool = False


class Simulator:
    def __init__(self, config: SimulationConfig):
        self.config = config
        self._workers: List[StoppableWorker] = []
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0

    def start(self) -> None:
        self.stop()  # idempotent
        if self.config.clicks_per_minute > 0:
            self._workers.append(
                StoppableWorker(
                    keyboard_worker,
                    name="keyboard-worker",
                    clicks_per_minute=self.config.clicks_per_minute,
                    key=self.config.key,
                    randomize=self.config.randomize_interval,
                )
            )
        if self.config.mouse_enable and self.config.mouse_interval_seconds > 0:
            self._workers.append(
                StoppableWorker(
                    mouse_worker,
                    name="mouse-worker",
                    interval_seconds=self.config.mouse_interval_seconds,
                    randomize=self.config.randomize_interval,
                )
            )
        for w in self._workers:
            w.daemon = True
            w.start()

    def stop(self, join_timeout: float = 5.0) -> None:
        for w in self._workers:
            w.stop()
        for w in self._workers:
            w.join(timeout=join_timeout)
        self._workers.clear()

    def run_for(self, duration_seconds: Optional[float] = None) -> None:
        self.start()
        try:
            if duration_seconds and duration_seconds > 0:
                time.sleep(duration_seconds)
            else:
                while True:
                    time.sleep(1.0)
        except KeyboardInterrupt:
            pass
        finally:
            self.stop()



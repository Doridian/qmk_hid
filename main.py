#!/usr/bin/env python3
from qmk_hid import set_rgb_brightness, get_rgb_brightness, find_devs, open_device
from time import sleep
from datetime import datetime
from sys import argv

def transition_backlight_to(dev, target: int, total_seconds: float = 1.0, step_size: int = 1) -> None:
    if step_size < 1:
        step_size = 1

    current = get_rgb_brightness(dev)
    if current == target:
        return

    have_warned = False
    step = -step_size if current > target else step_size

    step_count = int(abs((current - target) / step))
    if step_count < 1:
        set_rgb_brightness(dev, target)
        return

    sleept = total_seconds / float(step_count)
    if sleept < 0.01:
        print("WARN: total_seconds too short!", f"sleept={sleept}", "min=0.01")
        sleept = 0.01

    for i in range(current + step, target, step):
        start = datetime.now()
        set_rgb_brightness(dev, i)
        duration = datetime.now() - start
        sleepc = sleept - duration.total_seconds()
        if sleepc > 0:
            sleep(sleepc)
        elif not have_warned:
            print("WARN: No sleep!", sleepc)
            have_warned = True

    set_rgb_brightness(dev, target)

def main():
    devs = find_devs()
    dev = open_device(devs[0])

    trg = int(argv[1])
    transition_backlight_to(dev, trg, total_seconds=1.0, step_size=5)

if __name__ == "__main__":
    main()

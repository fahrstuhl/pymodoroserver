#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import check_output, run, CalledProcessError
from argparse import ArgumentParser

def main():
    parser = ArgumentParser(description="Lock screen if it's time for a break.")
    parser.add_argument("-u", "--user", type=str, default='')
    parser.add_argument("-pw", "--password", type=str, default='')
    args = parser.parse_args()
    state = ["/home/fahrstuhl/.local/bin/pymodoroclient.py", "-u", args.user, "-pw", args.password]
    locked = ["pgrep", "i3lock"]
    lock = ["/usr/bin/i3lock", "-d", "-u", "-c", "000000"]
    is_break = "break" in check_output(state).decode("utf-8")
    try:
        is_locked = len(check_output(locked)) > 0
    except CalledProcessError:
        is_locked = False
    if not is_locked and is_break:
        run(lock)
    print("⏲️")

if __name__ == "__main__":
    main()

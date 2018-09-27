#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer
from argparse import ArgumentParser
from threading import Timer
from time import sleep

class PymodoroServer(object):

    def __init__(self, work_duration, break_duration):
        self.work_duration = 60*work_duration
        self.break_duration = 60*break_duration
        self.work_timer = Timer(work_duration, self.work_finished)
        self.break_timer = Timer(break_duration, self.break_finished)
        self.state = "stopped"
        self.timer_started = datetime.min

    def start(self):
        self.reset()
        self.start_work()

    def toggle(self):
        if self.state == "stopped":
            self.start()
        else:
            self.stop()

    def start_work(self):
        self.state = "working"
        self.timer_started = datetime.now()
        self.work_timer = Timer(self.work_duration, self.work_finished)
        self.work_timer.start()

    def start_break(self):
        self.state = "break"
        self.timer_started = datetime.now()
        self.break_timer = Timer(self.break_duration, self.break_finished)
        self.break_timer.start()

    def reset(self):
        self.stop()

    def stop(self):
        self.work_timer.cancel()
        self.break_timer.cancel()
        self.state = "stopped"

    def work_finished(self):
        self.work_timer.cancel()
        self.start_break()

    def break_finished(self):
        self.break_timer.cancel()
        self.start_work()

    def get_state(self):
        return self.state

    def get_runtime(self):
        if self.state == "stopped":
            return timedelta()
        else:
            return datetime.now() - self.timer_started

class PymodoroHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global TIMER
        if self.path == "/start":
            TIMER.start()
            self.send_response(200)
            self.end_headers()
        elif self.path == "/stop":
            TIMER.stop()
            self.send_response(200)
            self.end_headers()
        elif self.path == "/toggle":
            TIMER.toggle()
            self.send_response(200)
            self.end_headers()
        elif self.path == "/get_state":
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            response = TIMER.get_state().encode('utf-8')
            self.wfile.write(response)
        elif self.path == "/get_runtime":
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            runtime = TIMER.get_runtime()
            hours, remainder = divmod(runtime.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            if hours > 0:
                response = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds).encode('utf-8')
            else:
                response = "{:02d}:{:02d}".format(minutes, seconds).encode('utf-8')
            self.wfile.write(response)
        else:
            self.send_response(404)
            self.end_headers()

def main():
    global TIMER
    parser = ArgumentParser(description="Start pymodoro server.")
    parser.add_argument("-a", "--address", type=str, default="localhost")
    parser.add_argument("-p", "--port", type=int, default=7132)
    parser.add_argument("-w", "--work_duration", type=int, default=25, help="Duration of work timer in minutes.")
    parser.add_argument("-b", "--break_duration", type=int, default=5, help="Duration of break timer in minutes.")
    args = parser.parse_args()
    TIMER = PymodoroServer(args.work_duration, args.break_duration)
    server = HTTPServer((args.address, args.port), PymodoroHTTPRequestHandler)
    server.serve_forever()

if __name__ == "__main__":
    main()

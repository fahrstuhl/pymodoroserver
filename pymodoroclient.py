#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from argparse import ArgumentParser

def run_command(args, command):
    return requests.get("http://{}:{}/{}".format(args.address, args.port, command), auth=(args.user, args.password))

def main():
    parser = ArgumentParser(description="Interact with pymodoro server")
    parser.add_argument("-a", "--address", type=str, default="timer.what.re")
    parser.add_argument("-p", "--port", type=int, default=80)
    parser.add_argument("-u", "--user", type=str, default='')
    parser.add_argument("-pw", "--password", type=str, default='')
    parser.add_argument("-e", "--exit", action='store_true', help="Program exits with fail on stopped timer if this is set")
    parser.add_argument("--start", action='store_true')
    parser.add_argument("--stop", action='store_true')
    parser.add_argument("--toggle", action='store_true')
    args = parser.parse_args()
    if args.start:
        run_command(args,"start")
    elif args.stop:
        run_command(args,"stop")
    elif args.toggle:
        run_command(args,"toggle")
    else:
        state = run_command(args, "get_state").text
        runtime = run_command(args, "get_runtime").text
        if state == "stopped":
            ret = state
            print(ret)
            if(args.exit):
                exit(1)
        else:
            ret = "{}:{}".format(state, runtime)
            print(ret)
            if(args.exit):
                exit(0)
            

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""ETP/1 client -- CSC 4200/5200 PA1 starter (Python).

    ./etp-client --host HOST --port PORT --name NAME list
    ./etp-client --host HOST --port PORT --name NAME get REMOTE LOCAL
    ./etp-client --host HOST --port PORT --name NAME put LOCAL REMOTE

The argument handling is done for you. Everything marked TODO is yours.
This file must not import socket: use the transport module (the seam).
"""
import argparse
import sys
import traceback

import etp
import transport
from transport_tcp import connect                     # the seam: see src/transport.py

# Exit status (Specification, Section 10)
EXIT_OK, EXIT_SERVER_ERROR, EXIT_FAILURE, EXIT_DIGEST = 0, 1, 2, 3


def run(args):
    """Perform one session and return the exit status.

    TODO: connect; HELLO with args.name; the one command; BYE; wait for the
    server to close; close. Output rules are in Specification, Section 10:
    `list` prints the LIST_OK payload exactly, `put` prints the 64-hex-digit
    digest, and every diagnostic goes to standard error.
    """
    conn = None
    try:
        conn = connect(args.HOST, args.PORT)
        hello_data = f"HELLO {args.name}\n".encode("utf-8")
        conn.sendall(hello_data)
        command_str = getattr(args, "command", "")
        cmd_data = f"{command_str}\n".encode("utf-8")
        conn.sendall(cmd_data)
        response_buffer = bytearray()
        while True:
            chunk = conn.recv(4096)
            if not chunk:
                break
        response_buffer.extend(chunk)
        response_text = response_buffer.decode("utf-8", errors="replace")
        if command_str.startswith("list"):
            print(response_text, end="")
        elif command_str.startswith("put"):
            print(response_text.strip())
        else:
            print(response_text, end="")
        conn.sendall(b"BYE\n")
        while True:
            data = conn.recv(4096)
            if not data:
                break
    except Exception as e:
        print(f"Error during session: {e}", file=sys.stderr)
        return 1
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass

    return 0
    

def main():
    ap = argparse.ArgumentParser(description="ETP/1 client")
    ap.add_argument("--host", required=True)
    ap.add_argument("--port", type=int, required=True)
    ap.add_argument("--name", required=True)
    sub = ap.add_subparsers(dest="command", required=True)
    sub.add_parser("list")
    g = sub.add_parser("get")
    g.add_argument("remote")
    g.add_argument("local")
    p = sub.add_parser("put")
    p.add_argument("local")
    p.add_argument("remote")
    try:
        args = ap.parse_args()
    except SystemExit as e:
        return EXIT_FAILURE if e.code else EXIT_OK     # bad arguments -> 2; --help -> 0
    try:
        return run(args)
    except Exception:                                  # a bug is never "server said ERROR"
        traceback.print_exc()
        return EXIT_FAILURE


if __name__ == "__main__":
    sys.exit(main())

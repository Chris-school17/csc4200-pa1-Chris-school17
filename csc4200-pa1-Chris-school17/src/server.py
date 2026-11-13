#!/usr/bin/env python3
"""ETP/1 server -- CSC 4200/5200 PA1 starter (Python).

    ./etp-server --port PORT --root DIR [--bind ADDR]

The argument handling is done for you. Everything marked TODO is yours.
This file must not import socket: use the transport module (the seam).
"""
import argparse
import os
import sys

import etp
import transport                     # the seam: see src/transport.py


def handle_session(conn, peer, root):
    """Serve one client from HELLO to BYE (Specification, Sections 5-8).

    TODO: loop reading requests with etp.read_message, apply the checks in
    Section 8.1 in order, send exactly one response per request, log one line
    per response (Section 9), and close when the session ends -- for any reason.
    A failure here must end THIS session only, never the server.
    """
    
    while True:
        try:
            data = recv_exact(conn, 3056)
            if data == "close":
                close(conn)
        except:
            close(conn)


def main():
    ap = argparse.ArgumentParser(description="ETP/1 server")
    ap.add_argument("--port", type=int, required=True)
    ap.add_argument("--root", required=True)
    ap.add_argument("--bind", default="127.0.0.1")
    args = ap.parse_args()
    if not os.path.isdir(args.root):
        print(f"etp-server: root directory {args.root!r} does not exist", file=sys.stderr)
        return 2

    # TODO: listen through the transport, then accept sessions forever,
    # serving each one so that a stalled client cannot delay the others
    # (Specification, Section 9: Concurrency).

    ls = listen(bind_addr, port)
    while TRUE:
        conn, addr = accept(ls)
        if conn:
            handle_session(conn, addr, args.root)



if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(0)

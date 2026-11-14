#!/usr/bin/env python3
"""ETP/1 server -- CSC 4200/5200 PA1 starter (Python).

    ./etp-server --port PORT --root DIR [--bind ADDR]

The argument handling is done for you. Everything marked TODO is yours.
This file must not import socket: use the transport module (the seam).
"""
import argparse
import os
import sys
import threading
import etp
import transport                     # the seam: see src/transport.py


def handle_session(conn, peer, root):
    hello_received = False
    try:
        while True:
            try:
                version, mtype, status, length, payload = etp.read_message(conn, transport)
            except Exception:
                break
            response_mtype = mtype | 0x80
            response_status = 0
            response_payload = b""
            if version != etp.VERSION:
                response_status = etp.BAD_VERSION
                response_mtype = etp.ERROR
                resp_bytes = etp.encode(response_mtype, response_payload, response_status)
                transport.send_all(conn, resp_bytes)
                break
            valid_types = {etp.HELLO, etp.LIST, etp.GET, etp.PUT, etp.BYE}
            if mtype not in valid_types:
                response_status = etp.BAD_TYPE
                response_mtype = etp.ERROR
                resp_bytes = etp.encode(response_mtype, response_payload, response_status)
                transport.send_all(conn, resp_bytes)
                break
            if not hello_received and mtype != etp.HELLO:
                response_status = etp.NOT_READY
                response_mtype = etp.ERROR
            elif hello_received and mtype == etp.HELLO:
                response_status = etp.BAD_REQUEST
                response_mtype = etp.ERROR
            else:
                if mtype == etp.HELLO:
                    if not etp.NAME_RE.match(payload):
                        response_status = etp.BAD_NAME
                        response_mtype = etp.ERROR
                    else:
                        hello_received = True
                        response_mtype = etp.HELLO_OK
                        response_payload = b"etp-server"
                elif mtype == etp.LIST:
                    try:
                        items = []
                        for f in os.listdir(root):
                            if etp.NAME_RE.match(f.encode("utf-8", errors="ignore")):
                                filepath = os.path.join(root, f)
                                if os.path.isfile(filepath):
                                    size = os.path.getsize(filepath)
                                    items.append((f, size))
                        items.sort(key=lambda x: x[0].encode("utf-8"))
                        lines = [f"{name}\t{size}\n" for name, size in items]
                        response_payload = "".join(lines).encode("utf-8")
                        response_mtype = etp.LIST_OK
                    except Exception:
                        response_status = etp.SERVER_ERROR
                        response_mtype = etp.ERROR

                elif mtype == etp.GET:
                    if not etp.NAME_RE.match(payload):
                        response_status = etp.BAD_NAME
                        response_mtype = etp.ERROR
                    else:
                        filename = payload.decode("utf-8", errors="ignore")
                        filepath = os.path.join(root, filename)
                        if not os.path.isfile(filepath):
                            response_status = etp.NOT_FOUND
                            response_mtype = etp.ERROR
                        else:
                            try:
                                with open(filepath, "rb") as f:
                                    response_payload = f.read()
                                response_mtype = etp.GET_OK
                            except Exception:
                                response_status = etp.SERVER_ERROR
                                response_mtype = etp.ERROR
                elif mtype == etp.PUT:
                    response_mtype = etp.PUT_OK
                elif mtype == etp.BYE:
                    response_mtype = etp.BYE_OK
                    resp_bytes = etp.encode(response_mtype, response_payload, response_status)
                    transport.send_all(conn, resp_bytes)
                    print(f"[{peer}] sent response type {response_mtype:#04x}, status {response_status}")
                    break
            resp_bytes = etp.encode(response_mtype, response_payload, response_status)
            transport.send_all(conn, resp_bytes)
            print(f"[{peer}] sent response type {response_mtype:#04x}, status {response_status}")
            if response_mtype == etp.ERROR and response_status in etp.FATAL_ERRORS:
                break
    except Exception as e:
        print(f"Session error with {peer}: {e}", file=sys.stderr)
    finally:
        try:
            conn.close()
        except Exception:
            pass
def main():
    ap = argparse.ArgumentParser(description="ETP/1 server")
    ap.add_argument("--port", type=int, required=True)
    ap.add_argument("--root", required=True)
    ap.add_argument("--bind", default="127.0.0.1")
    args = ap.parse_args()
    if not os.path.isdir(args.root):
        print(f"etp-server: root directory {args.root!r} does not exist", file=sys.stderr)
        return 2
    ls = transport.listen(args.bind, args.port)

    while True:
        try:
            conn, addr = transport.accept(ls)
            if conn:
                t = threading.Thread(
                    target=handle_session, 
                    args=(conn, addr, args.root), 
                    daemon=True
                )
                t.start()
        except Exception as e:
            print(f"Error accepting connection: {e}", file=sys.stderr)
if __name__ == "__main__":
    main()



if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(0)


# PA1 — ETP/1 Client and Server

**Student:** _your full name_ (`your-github-username`)
**Course:** CSC 4200 / CSC 5200 (delete one) — Fall 2026
**Language:** _C or Python_
**Submitted commit:** _the SHA you paste into Canvas_

## Build and run

```
make build
make run-server PORT=5000 ROOT=server-files      # in one terminal
./etp-client --host 127.0.0.1 --port 5000 --name YOURNAME list    # in another
```

Everything was kept the same and should be able to be run with the make check command

## What works and what does not such as 

The program mostly works however there are some key issues with the server such as the HELLO handshake failing, the LIST_OK payload being wrong, the server getting the wrong SHA-256 of the data back, and the connection closing early. These issues on the server side cause the client side tests to fail completely. 

## Files

| File | What it is |
|---|---|
| `src/...` | |
| `DESIGN.md` | design document |
| `AI_USE.md` | AI-use disclosure and log |
| `evidence/pa1-capture.pcap` | loopback capture of my PUT and GET sessions |
| `evidence/time-wait.txt` | `ss` output showing TIME-WAIT after my session |
| `evidence/ANALYSIS.md` | my capture analysis |

---

## Authorship statement

I am the author of this submission. Except where this README or `AI_USE.md`
says otherwise, I wrote, or rewrote and understand, every part of it — code,
documents and evidence — and I can explain any line of it to the instructor or
GTA. I am responsible for its correctness, including any part a
generative AI tool helped me produce. My use of AI tools is disclosed in full in
`AI_USE.md`. The capture and measurements in `evidence/` come from my own programs,
run by me.

**Signed:** Christopher Zamarron, Brandon Roos  **Date:** 11/13/26

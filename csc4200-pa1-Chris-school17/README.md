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

## What works and what does not

Almost everything fails the check. This is due to the server not properly starting. This is caused by functions not being defined. As a result I am unable to verify if the rest of the program works as intended. I am completely new to python and did my best with coding everything. I was confused on the directions that were given and exactly how the program was supposed to function. I did my best to implament the functions.

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

**Signed:** Christopher Zamarron  **Date:** 11/12/26

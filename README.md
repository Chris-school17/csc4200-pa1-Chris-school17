# PA2 — ETP-T: a Reliable Transport over UDP

**Team:** _each member's full name, GitHub username and course (CSC 4200 or 5200), one per line; a student working alone lists one_
**Language:** _C or Python_
**Our profile:** _one-way delay ___ ms, bottleneck ___ kbit/s — the repository owner's (from `etpt_relay.py --show-profile OWNER`)_
**Submitted commit:** _the SHA you paste into Canvas_

## Build and run

```
make build
./etpt-recv --port 7001 --out scratch/copy.bin                     # terminal 1
python3 ~/csc4200-course/project/pa2/etpt_relay.py --listen 7000 \
        --to 127.0.0.1:7001 --profile OWNER                        # terminal 2
./etpt-send --host 127.0.0.1 --port 7000 --file scratch/small.bin --window 16   # terminal 3
```

Nothing else needed

## What works and what does not

Everything works except Receiver test R07 which fails with the error "malformed datagrams counted and ignored
counted checksum_failures=2 invalid=2; expected 1 and 3 (Specification, Section 6.1)".   

## Who did what

I did everything for PA2. My partner did everything for PA1. 

## Files

| File | What it is |
|---|---|
| `src/...` | |
| `DESIGN.md` | design document |
| `AI_USE.md` | AI-use disclosure and log |
| `evidence/pa2-capture.pcap` | loopback capture of one transfer through the relay |
| `evidence/measurements.csv` | the full measurement sweep for our profile |
| `evidence/throughput.svg` | the plot the sweep produced |
| `evidence/ANALYSIS.md` | our analysis |

---

## Authorship statement

Each of us who signs below is an author of this submission. Except where this
README or `AI_USE.md` says otherwise, we wrote, or rewrote and understand, every
part of it — code, documents and evidence — and each of us can explain any line of
it to the instructor or GTA. Each of us is responsible for its correctness,
including any part a generative AI tool helped us produce. Our use of AI tools is
disclosed in full in `AI_USE.md`. The capture and measurements in `evidence/` come
from our own programs, run by us. _Every member signs on a line of their own;
add a line for each member._

**Signed:** Brandon Roos  **Date:** 11/22/26

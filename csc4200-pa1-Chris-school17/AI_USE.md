# AI Use Disclosure — PA1

_Generative AI is allowed on PA1 as a tutor, reviewer, debugging partner and
helper with tooling. It is not allowed to be the author of your work. See the PA1
brief, "AI, Authorship and You". Fill in every section. "None" is an acceptable
answer only if it is true._

## 1. Did you use generative AI on this assignment?

- [] No. I did not use any generative AI tool for any part of PA1.
- [X] Yes, as described below.

## 2. Statement (the syllabus form)

> The author acknowledges the utilization of Gemini, a language model
> developed by Alphabet, in the preparation of this assignment. Gemini
> was employed in the following manner(s) within this assignment: _[for example:
> explaining socket errors; reviewing my framing code; drafting the Makefile;
> suggesting test cases; editing DESIGN.md for clarity]_.

## 3. Log

_One row per substantive interaction. Summaries are fine; you do not need to paste
whole conversations, but keep them in case you are asked._

| # | What I asked (summary) | What I used from the answer | What I changed or rejected | How I checked it was right |
|---|---|---|---|---|
| 1 | I asked why my def run function was not compiling  | I used most of the generated code since my function was so broken that I couldn't keep it | Nothing | I read the documentation again and made sure the code met the specifications and ran etp_selfcheck.py |
| 2 | I asked why my def encode function wouldn't raise the length error correctly | I used the code that generated the length error and kept the rest untouched | Nothing | I read the documentation again and made sure the code met the specifications and ran etp_selfcheck.py | 
| 3 | I asked why my def read_message function was not compiling | I used most of the generated code since my function was so broken that I couldn't keep it | Nothing | I read the documentation again and made sure the code met the specifications and ran etp_selfcheck.py |
| 4 | I asked why my def handle_session function was not compiling | I used most of the generated code since my function was so broken that I couldn't keep it | Nothing | I read the documentation again and made sure the code met the specifications and ran etp_selfcheck.py |
| 5 | I asked why my while loop wasn't working properly and causing the program to hang after fixing the other major errors |  I rewrote the while loop using the layout of the generated code | Nothing | I read the documentation again and made sure the code met the specifications and ran etp_selfcheck.py |
## 4. Where AI-produced material remains

def run, def encode, def read_message, def handle_session, def main

## 5. One thing the AI got wrong — or how you checked it

One thing that AI got wrong was how it left the response_payload as an empty b"" instead of populating it with a proper server identifier. I checked it by looking at the output of etp_selftest.py and looking at the documentation again which allowed me to notice the error and fix it 

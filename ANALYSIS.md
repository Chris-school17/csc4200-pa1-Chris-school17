# PA2 Analysis

_Your evidence is `evidence/measurements.csv` and `evidence/throughput.svg` (from
`make measure`) and `evidence/pa2-capture.pcap`. Every number below comes from
those files and from your own profile. Formulas and their symbols are in the
PA2 brief, Section 4.3._

## Our profile and how we measured

python3 ~/csc4200-course/project/pa2/etpt_relay.py --show-profile brandon583
Profile brandon583: delay_ms=25, rate_kbps=3000, queue=100, size=262144
Commit SHA: ed94912ac351c9b565531c5419cf457555092046

## Facts

_Fill in every value. Use your profile for the first five and your
measurements.csv for the last three. Decimal numbers to at least two decimal
places; units as named. Do not change the key names or the `etpt-facts` label:
a script reads this block._

```etpt-facts
profile_delay_ms: 25.00 ms         # one-way delay d from your profile, ms
profile_rate_kbps: 3000.00 kbit/s        # bottleneck rate R from your profile, kbit/s
d_trans_ms: 2.73 ms                # transmission delay of one full segment, L/R, ms
sw_predicted_kbps: 145.45 kbps         # predicted stop-and-wait goodput, kbit/s
w_fill_segments: 19.23           # window that just fills the link, segments
sw_measured_kbps: 151.00 kbps          # median goodput at W = 1, loss 0, from your CSV
plateau_kbps: 2752.90 kbps              # highest median goodput at loss 0, from your CSV
plateau_window: 32            # the W at which it occurred (on a tie, the smaller W)
```

## Q1. Your segments on the wire

_From your capture, decode the header of the SYN, of the ACK that answers it,
and of the first data segment, field by field (give the frame numbers). 

SYN (Frame 1): Source(client), Destination(7000), Sequence Number(0), Flags(SYN), Window Size
SYN-ACK (Frame 2): Source(7000), Destination(client), Sequence Number(0), Acknowledgment Number(ISN + 1), Flags(SYN, ACK)
Data Segment: Source Port(client), Destination(7000), Payload Length(1024 Bytes) 

Then
verify the first data segment's checksum: show the one's-complement sum of the
eight 16-bit header words with CHECKSUM taken as zero, and combine it with the
payload's sum (your own code may compute that part; say so). 

The one's-complement sum of the eight 16-bit header words with the ETP-T set to 0 combined with the payload's one's-complement sum is 0xFFFF

Finally: UDP
already has a checksum, so why does ETP-T need its own? (Think about where the
relay sits.)_

ETP-T needs its own checksum because ETP-T relay sits between the sender and reciever which means the checksum provided by UDP by default wont gaurantee integrity. 

## Q2. The window and the bandwidth-delay product

_Describe your loss-0 curve. Compare it, window by window, with
min(W x stop-and-wait goodput, bottleneck capacity for file data). Where does it
stop growing, and how does that compare with w_fill_segments? 

Our growth stops growing at 2752.9 kbps with W=32. This is close to the theorhetical of 19.23 and the 3000 kbit/s maximum. 

Your plateau is
what fraction of the capacity line, and where does the rest go?_

Our plateau is 91.8% of the 3000kbit/s line. The 8.2% that is not used is used by the protocols overhead. 

## Q3. Stop-and-wait

_Compare sw_measured_kbps with sw_predicted_kbps. Account for the difference:
what does the formula leave out that your real system does?_

The sw_measured_kbps is 151.0 kbps which is higher than the sw_predicted_kbps which is 145.45 kbps. The formula doesnt account for kernel scheduling, immediate ACK generation, and minor variations in timer granularity in the virtual environment which all allow for higher throughput. 

## Q4. Loss, Go-Back-N and the queue

_How do 1% and 5% loss change goodput at small and large windows? 

At 1% loss does not have a major impact on goodput. At 5% Go-Back-N retransmits all unacknowledged packets in the window upon a single drop which has a much larger impact on goodput.  

Why does
Go-Back-N suffer more at large windows? Look at W = 128: what happened even at
loss 0? 

At loss 0 large windows still overflow the relay queue which triggers unnecessary retransmissions and queue congestion. 

Use the fwd_dropped_queue and retransmissions columns, and say what a
sender would need to do to avoid it._

To avoid queue drops and retransmissions the sender needs to implement congestion control to prevent flooding bootleneck queues. 

## Q5. The timer

_Using the srtt_ms and rto_ms columns, explain how your RTO relates to your round
trip at small windows and at W = 64, and why it changed. What does Karn's rule
protect against?

SRTT is 53.5ms RTO is 100ms. At W=64 SRTT increases to 177.3ms which is caused by queueing delays over the bottleneck which causes RTO to pull back to 181ms. Karns rule is used to prevent ambiguity in ACK matching. 

 What would happen in your profile with a fixed RTO of 20 ms,
and with a fixed RTO of 2 s?_

A fixed RTO of 20ms would cause unexpected retransmissions and timeouts. A fixed RTO of 2ms would cause a 2 second stall for any packet loss or queue delay. 
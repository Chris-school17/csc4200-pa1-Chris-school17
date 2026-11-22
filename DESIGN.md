# PA2 Design — ETP-T

_One to two pages. Short, specific answers beat long general ones. Every section
should be true of the code you submit. Delete these italic prompts when you write._

## 1. Architecture

_Which file holds the segment codec, which holds the transport, and what calls
what. Where is the one loop that waits for a datagram or a timer? Which state
does a connection keep for sending, and which for receiving?_

The segment codec is in etpt.py. The transport logic and socket management are in transport_etpt.py. etpt_send.py and etpt_recv.py import transport.py, which routes to transport_etpt.py. transport_etpt.py calls etpt.py functions (encode, decode, checksum) to process segments. The waiting pattern uses UDP socket timeouts along with conn.sock.recvfrom(65535) across connect, send_all, recv_exact, and close. The sending state is local_seq, expected_seq, _WINDOW, outstanding dictionary, and RTT/RTO estimators (srtt, rttvar, rto). The receiving state is recv_buffer (bytearray), expected_seq, peer_fin_received, and all protocol statistics counters.

## 2. Segments and the checksum

_How you build and check a segment. Where the checks of Specification §6.1
happen, and in what order. How you tested your checksum before you trusted it._

Building a segment is done by packing a 16 byte header with a zero checksum which computes the RFC 1071 Internet checksum over the header plus the payload and repacks the header with the valid checksum. Checking is done by using etpt.decode() to unpack and validate the incoming datagrams. Specification §6.1 is done in the decode() function where it checks the minimum length, protocol version, payload bonds, and checksum in that order. I tested the checksum with etpt.checksum() which implements the standard RFC 1071 one's complement sum with odd-byte padding.

## 3. The sender: window, timer, Go-Back-N

_How the window opens and slides. When the timer starts, restarts and stops.
What exactly happens on a timeout. What happens to an ACK that is old, repeated
or corrupted._

The window slides forward when a cumulative acknowledgment (ack) arrives, removing all acknowledged sequence numbers from the outstanding dictionary and updating base = ack. The timer starts on conn.sock.settimeout(conn.rto), restarts when a socket wait loop completes or when a valid acknowledgement advances a window, and when all outstanding bytes up to the end of the data stream have been acknowledged and the sending loop terminates. Old, repeated, or corrupted ACKs are ignored or caught by exception handlers. 

## 4. The retransmission timeout

_How you compute SRTT, RTTVAR and RTO. Which segments give RTT samples and which
do not (Karn), and how you know. How the RTO behaves after a timeout._

_update_rto() computes srtt and rttvar using the exponential weighted moving average formulas with $\alpha = 1/8$ and $\beta = 1/4$, and derives rto = max(MIN_RTO, min(MAX_RTO, srtt + K * rttvar)). Only segments that have never been retransmitted provide valid RTT samples while those that have been retransmitted don't. After a timeout, conn.rto is doubled (conn.rto = min(etpt.MAX_RTO, conn.rto * 2)), bounded by MAX_RTO.   

## 5. The receiver

_In-order delivery, cumulative ACKs, and what you do with duplicates and
out-of-order segments (discard or buffer — say which, and why)._

In-order payload bytes are appended to conn.recv_buffer, and cumulative acknowledgments are sent immediately via send_ack() for every valid incoming segment. Duplicates are handled by seq < conn.expected_seq which increments conn.duplicates and triggers an ACK retransmission immediately. Out of order segments are handled by seq > conn.expected_seq which increments conn.out_of_order and sends an ACK for the expected sequence number along with discarding the out-of-order payload.

## 6. Opening and closing

_SYN and its ACK; FIN in each direction; the linger. What goes wrong if a SYN,
a FIN or the last ACK is lost, and how your code copes. Name one weakness of
starting every connection at segment 0, and who could exploit it._

Connections open via a client SYN and server ACK. Termination uses FIN flags combined with a PEER_FIN_WAIT window and a final 2.0-second LINGER period. If a SYN, a FIN or the last ACK is lost it is handled by the transport's retry loops and timeouts (MAX_RETRIES). One weakness of starting every segment with zero is that it makes the inertial sequence number predictable which leaves the connection open to spoofing or blind injection attacks. 

## 7. Toward the project

_In the project your PA1 ETP/1 client and server run over this transport. What
already works in both directions, and what you would still have to change? Name
one thing your PA1 code assumed about TCP that ETP-T does differently._

In the final project, PA1 ETP/1 clients and servers will run directly over transport_etpt.py via the transport.py seam without modifying application code. Our PA1 code assumed that every TCP would provide a reliable ordered stream managed by the operating system socket stack while ETP-T runs over UDP and needs to have checks to handle the potential errors that using UDP might cause since UDP doesn't guarantee delivery like TCP does. 

## 8. Testing

_What did you test beyond `make check`? How? Name one bug your testing found,
how you found it, and the fix._

Aside from running 'make check' I conducted full parameter sweeps across varying window sizes between 1 and 64 under simulated network conditions to to evaluate end-to-end goodput, RTO estimator convergence, and performance stability. I did this by running automated bulk transfers using etpt-send and etpt-recv paired with test harnesses to capturing metrics such as goodput_kbps, retransmissions, timeouts, srtt_ms, and rto_ms into measurements.csv to verify that increasing the window scaled throughput correctly without causing congestion collapse. One bug I found in my testing was an ff-by-one window slide boundary error where ACKs acknowledging the upper edge of the window failed to clean up all expired outstanding segment keys, leading to redundant retransmissions under lossy conditions. I discovered it during high-window test sweeps where retransmission counters spiked unexpectedly even when packet loss was zero and I fixed it by updating the sliding window logic in send_all() to remove all dictionary keys where s < ack when base = ack is advanced.

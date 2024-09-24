import random
import socket
from packet import Packet

HOST = '127.0.0.1'
PORT = 12345
SSTHRESH = 8


def init_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return s


def send_window(sock, base, window_end, packets, loss_rate=0.1):
    for i in range(base, window_end):
        if random.random() > loss_rate:
            packet = Packet(i, packets[i]).pack()
            sock.sendto(packet, (HOST, PORT))
            print(f"Sent packet {i}")
        else:
            print(f"Packet {i} lost (simulated)")


def send_data(sock, packets):
    base = 0
    cwnd = 1  # Congestion window start at 1
    acked = base  # Highest acknowledged packet
    ack_counter = {}  # Counts occurrences of ACKs for fast retransmit

    while base < len(packets):
        window_end = min(base + cwnd, len(packets))
        send_window(sock, base, window_end, packets)

        while acked < window_end:
            ack = wait_for_ack(sock)
            if ack == -1:
                # Timeout occurred
                print("Timeout occurred, reducing cwnd and ssthresh")
                cwnd = max(cwnd // 2, 1)
                ssthresh = cwnd
                break  # Exit the inner loop and resend the window
            else:
                ack_counter[ack] = ack_counter.get(ack, 0) + 1
                if ack_counter[ack] == 3:
                    # Three duplicate ACKs received
                    print(f"Three duplicate ACKs for {ack}, triggering retransmission")
                    cwnd = max(cwnd // 2, 1)
                    ssthresh = cwnd
                    base = ack  # Go back to n
                    break  # Exit the inner loop for retransmission
                if ack > acked:
                    acked = ack
                    # print(f"Received new ACK: {ack}")

        if acked >= window_end:
            # All packets in the window were acknowledged
            base = acked
            # Adjust cwnd as per new rules
            if cwnd < SSTHRESH:
                cwnd *= 2
            else:
                cwnd += 1
            print(f"Window moved to {base}, cwnd set to {cwnd}")

    # Send an end mark packet that is empty or contains a specific end mark
    end_packet = Packet(len(packets), b'').pack()
    sock.sendto(end_packet, (HOST, PORT))
    print("Sent end-of-file packet")


def wait_for_ack(sock):
    try:
        sock.settimeout(1.0)
        data, _ = sock.recvfrom(1024)
        ack = int(data.decode())
        print(f"Received ACK: {ack}")
        return ack
    except socket.timeout:
        print("Timeout, no ACK received")
        return -1


def adjust_cwnd_ssthresh(cwnd):
    ssthresh = max(cwnd // 2, 1)
    cwnd = 1
    return ssthresh, cwnd


def adjust_cwnd_for_success(cwnd, ssthresh):
    if cwnd < ssthresh:
        cwnd *= 2  # SS - Exponential growth
    else:
        cwnd += 1  # CA - Linear growth
    return cwnd


def main(filepath='testfile.txt'):
    sock = init_socket()
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
            packets = [data[i:i + 512] for i in range(0, len(data), 512)]
        send_data(sock, packets)
    finally:
        sock.close()


if __name__ == "__main__":
    main()

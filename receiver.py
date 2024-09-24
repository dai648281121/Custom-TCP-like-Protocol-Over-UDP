import socket
from packet import Packet

HOST = '127.0.0.1'
PORT = 12345


def init_socket():
    """Initialize a UDP socket and bind it to a specified host and port."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, PORT))
    return s


def receive_data(sock):
    expected_seq_num = 0
    with open('received_file', 'wb') as f:
        while True:
            packet_bytes, addr = sock.recvfrom(1024)
            packet, valid = Packet.unpack(packet_bytes)
            if valid:
                if packet.seq_num == expected_seq_num:
                    # print(f"Received valid packet {packet.seq_num}")
                    if packet.data == b'':
                        print("End-of-file packet received. File transfer complete.")
                        break
                    else:
                        f.write(packet.data)
                        expected_seq_num += 1
                # else:
                    # print(f"Out-of-order packet {packet.seq_num} received, expected {expected_seq_num}")
                # Always send an ACK for the highest in-order packet
                send_ack(sock, addr, expected_seq_num)


def send_ack(sock, addr, ack):
    # print(f"Sending ACK {ack} to {addr}")
    sock.sendto(str(ack).encode(), addr)


def main():
    sock = init_socket()
    print("Receiver is ready and listening")
    try:
        receive_data(sock)
    finally:
        sock.close()


if __name__ == "__main__":
    main()

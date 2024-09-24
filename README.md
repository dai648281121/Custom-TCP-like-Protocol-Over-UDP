# Reliable Data Transfer Protocol over UDP

## Introduction

This project implements a custom TCP-like protocol over UDP to provide reliable data transfer. While UDP is inherently unreliable and does not guarantee packet delivery, ordering, or data integrity, this protocol handles these concerns through a combination of acknowledgments, retransmissions, sequence numbers, and a checksum. Additionally, the protocol incorporates basic congestion control based on TCP-Tahoe, using slow start and congestion avoidance to manage network congestion.

The project also includes a simple file transfer application (`myftp.py`) that uses this custom protocol to send and receive files over a network reliably and securely.

## Key Features

- **Reliable Data Transfer:** The protocol ensures reliable packet delivery despite network packet loss or reordering.
- **Data Integrity:** A checksum is used to detect corrupted packets, triggering retransmission when necessary.
- **Congestion Control:** Implements a simplified version of TCP-Tahoe with slow start and congestion avoidance to prevent overwhelming the network.
- **File Transfer Application:** A command-line based file transfer tool (`myftp.py`) that allows users to upload or download files using the protocol.

---

## Project Structure

The project consists of the following main components:

- **packet.py**: Defines the `Packet` class responsible for packing, unpacking, and verifying the integrity of transmitted data.
- **sender.py**: Handles sending of files using the custom protocol, including congestion control, retransmission, and timeout management.
- **receiver.py**: Receives data packets, verifies them, and assembles the transmitted file in the correct order.
- **myftp.py**: The main user interface that provides a simple command-line interface for file transfers using the protocol.

---

## Design Overview

This custom protocol over UDP implements core features inspired by TCP to ensure reliable and ordered file transfer across a network. The design includes:

1. **Packet Structure**:  
   Each packet is constructed with a 4-byte sequence number, a 1-byte checksum, and up to 512 bytes of data. The checksum is calculated by summing the sequence number and the byte values of the data, modulo 256, providing basic error detection.

2. **Reliability Features**:
   - **Checksums**: Ensure data integrity by comparing the calculated checksum of the received data with the transmitted value.
   - **Acknowledgments (ACKs)**: The receiver sends ACKs for successfully received packets, allowing the sender to confirm that the packet was received and move the transmission window forward.
   - **Retransmissions**: If a packet is lost or corrupted, the sender will detect this through timeouts or duplicate ACKs and retransmit the necessary packets.
   - **Sequence Numbers**: Track packet order, allowing the receiver to reorder out-of-sequence packets and identify missing packets.

3. **Congestion Control**:
   The sender controls the transmission rate using a congestion window (`cwnd`), which starts small and grows as more packets are successfully acknowledged. This simulates TCP-Tahoe:
   - **Slow Start**: The window size increases exponentially during the initial phase.
   - **Congestion Avoidance**: After reaching a threshold (`ssthresh`), the window grows linearly to prevent overwhelming the network.
   - **Fast Retransmit**: Three duplicate ACKs trigger immediate retransmission, assuming packet loss.
   - **Timeouts**: If no ACK is received within the timeout, the window is reduced, and the missing packet is retransmitted.

---

## How to Run the Project

### Prerequisites

- **Python 3** or higher is required to run this project.
- Ensure that you have `socket` and `struct` modules (included in Python’s standard library).

### Running the Application

1. **Start the Receiver**:
   - Open a terminal and run the following command:
     ```bash
     python myftp.py
     ```
   - This will start the receiver in a separate thread, waiting for incoming file transfers.

2. **Send a File**:
   - In the same terminal, type the following command to send a file:
     ```bash
     myftp> put <filename>
     ```

3. **Receive a File**:
   - The receiver will automatically receive files and save them to the current directory as `received_file`.

4. **Exit the Application**:
   - To exit, simply type:
     ```bash
     myftp> quit
     ```

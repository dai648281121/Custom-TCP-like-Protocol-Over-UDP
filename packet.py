import struct


class Packet:
    HEADER_FORMAT = 'B I'
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

    def __init__(self, seq_num, data):
        self.seq_num = seq_num
        self.data = data
        self.checksum = self.calculate_checksum()

    def calculate_checksum(self):
        checksum = (sum(self.data) + self.seq_num) % 256
        return checksum

    def pack(self):
        header = struct.pack(self.HEADER_FORMAT, self.checksum, self.seq_num)
        return header + self.data

    @classmethod
    def unpack(cls, packet_bytes):
        if len(packet_bytes) < cls.HEADER_SIZE:
            return None, False

        header = packet_bytes[:cls.HEADER_SIZE]
        data = packet_bytes[cls.HEADER_SIZE:]

        checksum, seq_num = struct.unpack(cls.HEADER_FORMAT, header)
        temp_packet = cls(seq_num, data)

        if temp_packet.calculate_checksum() == checksum:
            return temp_packet, True
        else:
            return temp_packet, False

import socket
import struct
import base64

server_ip '0.0.0.0'
server_port = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
sock.bind((server_ip, server_port))

def receive_file():
    data = {}
    packets_received = set()
    expected_packet_count = None

    while True:
        packet, address = sock.recvfrom(65536)
        icmp_header = packet[20:28]
        icmp_type, code, _, _, _ = struct.unpack('!BBHHH', icmp_header)
        if icmp_type == 8 and code == 0:
            sequence_number = struct.unpack('!H', packet[28:30])[0]
            data[sequence_number] = packet[30:]

            if expected_packet_count is None:
                expected_packet_count = struct.unpack('!H', packet[26:28])[0]
            packets_received.add(sequence_number)

            if len(packets_received) == expected_packet_count:
                break

    sorted_packets = [packet[1] for packet in sorted(data.items())]
    file_data = base64.b64decode(b''.join(sorted_packets))
    with open('received_file.bin', 'wb') as file:
        file.write(file_data)

    print("File received and saved.")
print("Waiting for file transfer...")
receive_file()

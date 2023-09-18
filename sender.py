import socket
import struct
import base64
print("input machine ip")
server_ip = input("ip: ")

server_ip = "192.168.1.235"
server_port = 0
print("dont send files past 75mb or problems will happen")
file_path = input('file: ')
chunk_size = 256

sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

def send_file():
    with open(file_path, 'rb') as file:
        file_data = file.read()

    encoded_data = base64.b64encode(file_data)
    chunks = [encoded_data[i:i + chunk_size] for i in range(0, len(encoded_data), chunk_size)]

    for i, chunk in enumerate(chunks):
        icmp_header = struct.pack('!BBHHH', 8, 0, 0, i, len(chunks))
        packet = icmp_header + struct.pack('!H', i) + chunk
        sock.sendto(packet, (server_ip, server_port))

    print("File sent successfully.")
send_file()


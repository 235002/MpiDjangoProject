import socket
import sys
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening
server_address = ('127.0.0.1', 10000)
print('Connecting to {0} port {1}'.format(server_address[0], server_address[1]))
sock.connect(server_address)
time.sleep(1)

messages = [
    'Part one of the message.',
    'Part two of the message.',
]
amount_excepted = len(''.join(messages))

try:
    # Send data
    for message in messages:
        print('Sending {0}'.format(message))
        sock.sendall(message.encode())
        time.sleep(1.5)
    # Look for the response
    amount_received = 0

    while amount_received < amount_excepted:
        data = sock.recv(16)
        amount_received += len(data)
        print('Received ', data.decode())
finally:
    print('Closing socket.')
    sock.close()

# messages = [
#     'This is the message. ',
#     'It will be sent ',
#     'in parts. '
# ]
#
# server_address = ('127.0.0.1', 10000)
#
# # Create a TCP/IP socket
# socks = [
#     socket.socket(socket.AF_INET, socket.SOCK_STREAM),
#     socket.socket(socket.AF_INET, socket.SOCK_STREAM),
# ]
#
# # Connect the socket to the port where the server is listening
# print('Connecting to {0} port {1}'.format(server_address[0], server_address[1]))
# for s in socks:
#     s.connect(server_address)
#
# try:
#     for message in messages:
#         print('message', message)
#         # Send messages on both sockets
#         for s in socks:
#             print('{0}: sending {1}'.format(s.getsockname(), message))
#             s.send(message.encode())
#
#         # Read responses on both sockets
#         for s in socks:
#             data = s.recv(1024)
#             print('{0} received {1}'.format(s.getsockname(), data.decode()))
# finally:
#     for s in socks:
#         s.close()
#         print('Closing socket', s.getsockname())
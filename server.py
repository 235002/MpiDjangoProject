import select
import socket
import sys
from multiprocessing import Queue

# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)

# Bind the socket to the port
server_address = ('127.0.0.1', 10000)
print('Starting server up {0} on {1} port'.format(server_address[0], server_address[1]))
server.bind(server_address)

# Listen for incoming connections
server.listen(5)

# Sockets from which we expect to read
inputs = [server]
# Sockets from which we expect to write
outputs = []
# Outgoing messages queues (socket:Queue)
message_queues = {}

while inputs:
    # Wait for at least one of the sockets to be ready for processing
    print('Waiting for the next event')

    # Set timeout for select
    timeout = 1
    readable, writeable, exceptional = select.select(inputs, outputs, inputs, timeout)

    if not (readable or writeable or exceptional):
        print('Timed out, do some other work here.')
        continue

    # Handle inputs
    for s in readable:
        if s is server:
            # A "readable" server socket is ready to accept a connections
            connection, client_address = s.accept()
            print('New connection from ', client_address)
            connection.setblocking(0)
            inputs.append(connection)

            # Give the connection a queue for data we want to send
            message_queues[connection] = Queue()
        else:
            data = s.recv(1024)
            if data:
                # A readable client socket has data
                print('Received data ', data, ' from ', s.getpeername())
                message_queues[s].put(data)
                # Add output channel for response
                if s not in outputs:
                    outputs.append(s)
            else:
                # Interprets empty results as closed connection
                print('Closing ', client_address, ' after reading no data.')
                # Stop listening for input on the connection
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()
                # Remove messages queue
                del message_queues[s]

    # Handle outputs
    for s in writeable:
        try:
            next_msg = message_queues[s].get_nowait()
        except Exception:
            # No messages waiting so stop checking for writability
            print('Output queue for ', s.getpeername(), ' is empty')
            outputs.remove(s)
        else:
            print('Sending {0} to {1}'.format(next_msg, s.getpeername()))
            s.send(next_msg)

    # Handle "exceptional conditions"
    for s in exceptional:
        print('Handling exceptional condition for ', s.getpeername())
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        # Remove message queue
        del message_queues[s]



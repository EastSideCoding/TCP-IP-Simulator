from socket import *
from random import *

server_port = 12000

# Establish server socket as TCP on IPv4 network.
server_socket = socket(AF_INET, SOCK_STREAM)

# Binds socket to current host IP with given server_port.
server_socket.bind(('', server_port))

# Sets server to maintain two TCP connections.
server_socket.listen(2)

print("The server is ready to receive")

receiver_socket, addr1 = server_socket.accept()
print("Receiver connection established")
sender_socket, addr2 = server_socket.accept()
print("Sender connection established")

while True:
    # Receives a packet from sender client.
    message = sender_socket.recv(1024)

    # Looks for the specific connection closing message.
    if message.decode() == "CLOSE":
        receiver_socket.send(message)
        break;

    odds = randint(1, 100)

    # If random integer falls outside range, then packet drop is simulated.
    if odds >= 35:
        # Otherwise packet is sent to receiver.
        receiver_socket.send(message)

        # Collects acknowledgement message from receiver and forwards to sender.
        reply = receiver_socket.recv(1024)
        sender_socket.send(reply)

receiver_socket.close()
sender_socket.close()
server_socket.close()
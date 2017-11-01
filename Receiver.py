from socket import *

server_name = 'localhost'
server_port = 12000

# Establish client socket as TCP on IPv4 network
client_socket = socket(AF_INET, SOCK_STREAM)

# Initial TCP connection to server
client_socket.connect((server_name, server_port))

print("Ready to receive.")

# Buffering window for the receiver. False indicates that the corresponding
# packet has not been received.
window = [False for x in range(5)]
base = 0

while True:
    # receives sender message and responses with acknowledgement
    packet, server_address = client_socket.recvfrom(1024)
    message = packet.decode()

    # Looks for the specific connection closing command.
    if message == "CLOSE":
        break

    print("Receiving: " + message)

    # Sets the corresponding window value to True to indicate that the packet has
    # been received.
    if (int(message) - base >= 0):
        if window[int(message) - base]:
            print("DUPLICATE PACKET: " + message)
        else:
            window[int(message) - base] = True

    # Status strings to be printed at the end of the loop to add clarity.
    sending_queue = "Sending packets: "
    waiting_queue = "Waiting on packets: "
    buffer_queue = "Buffering: "

    # Shifts the window and the base as long as the leading value of the window
    # is true.
    while window[0] or len(window) < 5:
        sending_queue += str(base) + " "
        del(window[0]) # Deletes the first value of the window.
        window.append(False) # Adds False to the end of the window.
        base += 1 # Increments the base packet number by one.


    for x in range(5):
        if not window[x]:
            waiting_queue += str(x + base) + " "
        else:
            buffer_queue += str(x + base) + " "

    print(sending_queue)
    print(buffer_queue)
    print(waiting_queue)
    print("\n")

    response = 'ACK: ' + message
    client_socket.send(response.encode())
    
client_socket.close()
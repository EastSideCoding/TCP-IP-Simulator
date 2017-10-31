from socket import *

server_name = 'localhost'
server_port = 12000

# Establish client socket as TCP on IPv4 network.
client_socket = socket(AF_INET, SOCK_STREAM)

# Initial TCP connection to server.
client_socket.connect((server_name, server_port))

# Set socket time out value to .1 second.
client_socket.settimeout(.1)

base = 0
total_packages = 20

# Buffering window for the sender. False values indicate that the corresponding
# packet hasn't been acknowledged.    
window = [False for x in range(5)]

while base < total_packages:
    print("\nBase = " + str(base) + "\n")
    for x in range(5):

        # Sends package depending on whether it has already been previously
        # acknowledged.
        if (not window[x]) and (x + base) < total_packages:
            client_socket.send(str(x + base).encode())
            try:
                # Waits .1 second for server to deliver acknowledgement message.
                response, server_address = client_socket.recvfrom(1024)
                print(response.decode())

                # Mark the packet in window as acknowledged.
                window[x] = True;

            except timeout:
                # Resends the message if time out occurs.
                print("Timeout for packet " + str(x + base))
                continue

    # Shifts the window and the base as long as the leading value of the window
    # is true.
    while window[0] or len(window) < 5:
        del window[0] # Deletes the first element of the window.
        window.append(False) # Adds False to the end of the window.
        base += 1 # Increments the base packet number.

# Sends a specific command to close all connections.
client_socket.send("CLOSE".encode())
client_socket.close()
import pickle
import socket

# Set up the server socket
host = '127.0.0.1'  # Replace with the server IP address
port = 5002  # Replace with the server port number
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
print('Bind successfully')
s.listen(1)

while True:
    print('Server is listening...')
    
    try:
        # Accept a client connection
        client_socket, addr = s.accept()
        print('Client connected:', addr)

        # Receive the array bytes from the client
        array_bytes = b''
        while True:
            try:
                data = client_socket.recv(4096)
                if not data:
                    break
                array_bytes += data
            except socket.error as e:
                print('Error receiving data:', str(e))
                break

        # Convert the array bytes back to a 2D array using pickle
        array_2D = pickle.loads(array_bytes)

        # Print the received array
        print('Received array:')
        print(array_2D)

        # Close the client socket
        client_socket.close()

    except socket.error as e:
        print('Error accepting client connection:', str(e))
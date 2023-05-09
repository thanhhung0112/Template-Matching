import socket
import pickle
import numpy as np

def send_data(points, ip_address, port):
    
    array_bytes = pickle.dumps(points)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connect to the server
        s.connect((ip_address, port))

        # Send the array bytes through the socket in chunks
        chunk_size = 4096
        bytes_sent = 0
        while bytes_sent < len(array_bytes):
            try:
                chunk = array_bytes[bytes_sent:bytes_sent + chunk_size]
                s.sendall(chunk)
                bytes_sent += len(chunk)
            except socket.error as e:
                print('Error sending data:', str(e))
                break
    except ConnectionRefusedError:
        print('Error: Connection refused. Please ensure the server is running.')
        
    finally:
        # Close the socket connection
        s.close()
    
if __name__ == "__main__":
    points = np.random.randint(0, 255, (4,))
    send_data(points, '127.0.0.1', 5002)
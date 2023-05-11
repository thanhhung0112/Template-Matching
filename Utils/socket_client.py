import socket
import numpy as np

def send_data(points, ip_address, port):
    # Convert the array to float32
    points = points.astype(np.float32)
    
    # Convert the float32 array to bytes
    array_bytes = points.tobytes()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connect to the server
        s.connect((ip_address, port))

        # Send the array bytes through the socket
        s.sendall(array_bytes)
        
    except ConnectionRefusedError:
        print('Error: Connection refused. Please ensure the server is running.')
        
    finally:
        # Close the socket connection
        s.close()
    
if __name__ == "__main__":
    points = np.array([[1.123, 5.0, 3.0, 4.0],
                       [1.123, 5.0, 3.0, 4.0]], dtype=np.float32)
    send_data(points, '127.0.0.1', 5003)

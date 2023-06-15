import socket
import numpy as np
import struct
import logging

logger = logging.getLogger(__name__)

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
        
    except Exception as e:
        logger.error(f'{e}\n')
        
    finally:
        # Close the socket connection
        s.close()
        
def send_float_array_data(data_array, ip_address, port):
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        server_address = (ip_address, port)
        client_socket.connect(server_address)
        
        num_data = len(data_array)
        byte_value = num_data.to_bytes(1, byteorder='big')
        client_socket.send(byte_value)

        # Send each float element separately
        for data in data_array:
            array_bytes = struct.pack('!4f', *data)
            # print(array_bytes)
            client_socket.sendall(array_bytes)

            logger.info(f"\nData: {data} sent successfully!\n")

    except Exception as e:
        logger.error(f'{e}\n')

    finally:
        # Close the socket connection
        client_socket.close()
    
if __name__ == "__main__":
    points = np.array([[1.123, 5.0, 3.0, 4.0],
                       [1.123, 5.0, 3.0, 4.0]], dtype=np.float32)
    send_data(points, '127.0.0.1', 5003)

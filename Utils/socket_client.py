import socket
import numpy as np
import struct
import logging
import time

logger = logging.getLogger(__name__)

def send_data(data_array, ip_address, port):
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to the server
        server_address = (ip_address, port)
        client_socket.connect(server_address)
        
        num_data = 5
        byte_value = num_data.to_bytes(1, byteorder='big')
        client_socket.send(byte_value)
        
        # Receive the data array
        data_bytes = client_socket.recv(16)
        data_array = struct.unpack('!4f', data_bytes)
        
        print(data_array)

    except Exception as e:
        logger.error(f'{e}\n')
        
    finally:
        client_socket.close()
        
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
            client_socket.sendall(array_bytes)
            
        response = client_socket.recv(1)
        
        if response[0] == 100:
            logger.info(f"sent successfully")
            client_socket.close()

    except Exception as e:
        logger.error(f'{e}\n')
        
    # finally:
    #     client_socket.close()
    
if __name__ == "__main__":
    points = np.random.randint(0, 255, (15, 4)).astype(np.float32)
    print(points)
    send_float_array_data(points, '192.168.176.1', 48952)
    send_data(np.array(points, dtype=np.float32), '192.168.176.1', 48953)

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <endian.h>

#define PORT 5003
#define ARRAY_SIZE 4

void printArray1D(float *array, int size)
{
    for (int i = 0; i < size; i++)
    {
        printf("%.4f ", array[i]);
    }
    printf("\n");
}

void reverseBytes(void *data, size_t size)
{
    size_t i;
    unsigned char *bytes = (unsigned char *)data;
    for (i = 0; i < size / 2; i++)
    {
        unsigned char temp = bytes[i];
        bytes[i] = bytes[size - i - 1];
        bytes[size - i - 1] = temp;
    }
}

int main(int argc, char *argv[])
{
    int socket_desc, client_sock, c, read_size;
    struct sockaddr_in server, client;
    float *array_bytes = NULL;
    float *message = NULL;
    int total_bytes = 0;
    int chunk_size = 4096;

    // Create socket
    socket_desc = socket(AF_INET, SOCK_STREAM, 0);
    if (socket_desc == -1)
    {
        printf("Could not create socket");
        return 1;
    }
    puts("Socket created");

    // Prepare the sockaddr_in structure
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = INADDR_ANY;
    server.sin_port = htons(PORT);

    // Bind the socket
    if (bind(socket_desc, (struct sockaddr *)&server, sizeof(server)) < 0)
    {
        perror("bind failed. Error");
        return 1;
    }
    puts("bind done");

    // Listen to the socket
    listen(socket_desc, 3);

    puts("Server started. Waiting for incoming connections...");

    while (1)
    {
        c = sizeof(struct sockaddr_in);

        // Accept connection from an incoming client
        client_sock = accept(socket_desc, (struct sockaddr *)&client, (socklen_t *)&c);

        if (client_sock < 0)
        {
            perror("accept failed");
            return 1;
        }
        puts("Connection accepted");

        // Receive the array bytes from the client
        char buffer[chunk_size];
        total_bytes = 0;

        while ((read_size = recv(client_sock, buffer, chunk_size, 0)) > 0)
        {
            total_bytes += read_size;
            array_bytes = (float *)realloc(array_bytes, total_bytes);
            memcpy(array_bytes + (total_bytes / sizeof(float) - read_size / sizeof(float)), buffer, read_size);
        }

        // Calculate the number of arrays received
        int num_arrays = total_bytes / (ARRAY_SIZE * sizeof(float));

        // Reverse the byte order if necessary
        #if __BYTE_ORDER == __BIG_ENDIAN
        for (int i = 0; i < total_bytes / sizeof(float); i++)
        {
            reverseBytes(&array_bytes[i], sizeof(float));
        }
        #endif

                // Print the received arrays
        printf("Received Arrays:\n");
        for (int i = 0; i < num_arrays; i++)
        {
            printf("Object %d: ", i + 1);
            printArray1D(&array_bytes[i * ARRAY_SIZE], ARRAY_SIZE);
        }

        // Free the dynamically allocated memory
        free(array_bytes);
        array_bytes = NULL;

        if (read_size == 0)
        {
            puts("Client disconnected");
        }
        else if (read_size == -1)
        {
            perror("recv failed");
        }

        // Close the client socket
        close(client_sock);
    }

    // Close the server socket
    close(socket_desc);

    return 0;
}

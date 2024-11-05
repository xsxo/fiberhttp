#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <windows.h>

#pragma comment(lib, "Ws2_32.lib") // Link with Ws2_32.lib

#define PORT 80
#define HOST "127.0.0.1"
#define BUFFER_SIZE 1024

DWORD WINAPI handle_client(LPVOID param) {
    SOCKET client_socket = (SOCKET)param;
    const char *data = "random=";
    char response[BUFFER_SIZE];

    snprintf(response, sizeof(response),
             "HTTP/1.1 200 OK\r\n"
             "Content-Type: text/html\r\n"
             "Content-Length: %lu\r\n"
             "\r\n"
             "%s",
             strlen(data), data);

    char buffer[BUFFER_SIZE];
    while (1) {
        int bytes_read = recv(client_socket, buffer, sizeof(buffer), 0);
        if (bytes_read <= 0) {
            break; // Connection closed or error
        }

        send(client_socket, response, strlen(response), 0);
    }

    closesocket(client_socket);
    return 0;
}

int main() {
    WSADATA wsaData;
    SOCKET server_socket, client_socket;
    struct sockaddr_in server_addr, client_addr;
    int client_len = sizeof(client_addr);

    // Initialize Winsock
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        printf("Error initializing Winsock: %d\n", WSAGetLastError());
        return 1;
    }

    server_socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (server_socket == INVALID_SOCKET) {
        printf("Error creating socket: %d\n", WSAGetLastError());
        WSACleanup();
        return 1;
    }

    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = inet_addr(HOST);
    server_addr.sin_port = htons(PORT);

    if (bind(server_socket, (struct sockaddr *)&server_addr, sizeof(server_addr)) == SOCKET_ERROR) {
        printf("Error binding socket: %d\n", WSAGetLastError());
        closesocket(server_socket);
        WSACleanup();
        return 1;
    }

    if (listen(server_socket, SOMAXCONN) == SOCKET_ERROR) {
        printf("Error listening on socket: %d\n", WSAGetLastError());
        closesocket(server_socket);
        WSACleanup();
        return 1;
    }

    printf("Server listening on http://%s:%d\n", HOST, PORT);

    while (1) {
        client_socket = accept(server_socket, (struct sockaddr *)&client_addr, &client_len);
        if (client_socket == INVALID_SOCKET) {
            printf("Error accepting connection: %d\n", WSAGetLastError());
            continue;
        }

        // Create a thread to handle the client
        HANDLE hThread = CreateThread(NULL, 0, handle_client, (LPVOID)client_socket, 0, NULL);
        if (hThread == NULL) {
            printf("Error creating thread: %d\n", GetLastError());
            closesocket(client_socket);
        } else {
            CloseHandle(hThread); // Close the thread handle, we don't need it
        }
    }

    closesocket(server_socket);
    WSACleanup();
    return 0;
}

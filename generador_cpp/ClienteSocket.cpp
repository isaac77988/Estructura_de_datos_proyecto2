#include "ClienteSocket.h"
#include <iostream>
#include <cstring>

ClienteSocket::ClienteSocket(const std::string& ip, int puerto)
    : ip_servidor(ip), puerto_servidor(puerto) {
#ifdef _WIN32
    WSADATA wsaData;
    WSAStartup(MAKEWORD(2, 2), &wsaData);
#endif
}

ClienteSocket::~ClienteSocket() {
#ifdef _WIN32
    WSACleanup();
#endif
}

void ClienteSocket::cerrarSocket(SocketType s) {
    if (s != SOCKET_INVALIDO) {
#ifdef _WIN32
        closesocket(s);
#else
        close(s);
#endif
    }
}

bool ClienteSocket::enviarTrama(const std::string& trama) {
    SocketType sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == SOCKET_INVALIDO) {
        return false;
    }

    struct sockaddr_in serv_addr;
    std::memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(puerto_servidor);
    serv_addr.sin_addr.s_addr = inet_addr(ip_servidor.c_str());

    if (connect(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0) {
        cerrarSocket(sock);
        return false;
    }

    send(sock, trama.c_str(), trama.length(), 0);

    char buffer[256] = {0};
    recv(sock, buffer, sizeof(buffer) - 1, 0);

    cerrarSocket(sock);
    return true;
}

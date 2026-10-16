#ifndef CLIENTE_SOCKET_H
#define CLIENTE_SOCKET_H

#ifdef _WIN32
    #include <winsock2.h>
    #include <ws2tcpip.h>
    typedef SOCKET SocketType;
    #define SOCKET_INVALIDO INVALID_SOCKET
#else
    #include <sys/socket.h>
    #include <netinet/in.h>
    #include <arpa/inet.h>
    #include <unistd.h>
    typedef int SocketType;
    #define SOCKET_INVALIDO -1
#endif

#include <string>

class ClienteSocket {
private:
    std::string ip_servidor;
    int puerto_servidor;

    void cerrarSocket(SocketType s);

public:
    ClienteSocket(const std::string& ip, int puerto);
    ~ClienteSocket();

    bool enviarTrama(const std::string& trama);
};

#endif

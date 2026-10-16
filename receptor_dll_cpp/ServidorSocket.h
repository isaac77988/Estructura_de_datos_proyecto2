#ifndef SERVIDOR_SOCKET_H
#define SERVIDOR_SOCKET_H

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

#include "ColaMensajes.h"
#include <string>
#include <thread>
#include <atomic>

class ServidorSocket {
private:
    int puerto;
    SocketType servidor_fd;
    std::atomic<bool> ejecutando;
    std::thread hilo_escucha;
    ColaMensajes cola_eventos;
    std::string buffer_ultimo_evento;

    void bucleEscucha();
    void cerrarSocket(SocketType s);

public:
    ServidorSocket(int puerto_escucha);
    ~ServidorSocket();

    bool iniciar();
    void detener();
    const char* extraerSiguienteEvento();
};

#endif

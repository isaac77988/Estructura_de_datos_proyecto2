#include "ServidorSocket.h"
#include <cstring>

ServidorSocket::ServidorSocket(int puerto_escucha)
    : puerto(puerto_escucha), servidor_fd(SOCKET_INVALIDO), ejecutando(false) {}

ServidorSocket::~ServidorSocket() {
    detener();
}

void ServidorSocket::cerrarSocket(SocketType s) {
    if (s != SOCKET_INVALIDO) {
#ifdef _WIN32
        closesocket(s);
#else
        close(s);
#endif
    }
}

bool ServidorSocket::iniciar() {
#ifdef _WIN32
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        return false;
    }
#endif

    servidor_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (servidor_fd == SOCKET_INVALIDO) {
#ifdef _WIN32
        WSACleanup();
#endif
        return false;
    }

    int opt = 1;
#ifdef _WIN32
    setsockopt(servidor_fd, SOL_SOCKET, SO_REUSEADDR, (const char*)&opt, sizeof(opt));
#else
    setsockopt(servidor_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
#endif

    struct sockaddr_in direccion;
    std::memset(&direccion, 0, sizeof(direccion));
    direccion.sin_family = AF_INET;
    direccion.sin_addr.s_addr = INADDR_ANY;
    direccion.sin_port = htons(puerto);

    if (bind(servidor_fd, (struct sockaddr*)&direccion, sizeof(direccion)) < 0) {
        cerrarSocket(servidor_fd);
#ifdef _WIN32
        WSACleanup();
#endif
        return false;
    }

    if (listen(servidor_fd, 5) < 0) {
        cerrarSocket(servidor_fd);
#ifdef _WIN32
        WSACleanup();
#endif
        return false;
    }

    ejecutando = true;
    hilo_escucha = std::thread(&ServidorSocket::bucleEscucha, this);
    return true;
}

void ServidorSocket::bucleEscucha() {
    struct sockaddr_in direccion_cliente;
#ifdef _WIN32
    int addrlen = sizeof(direccion_cliente);
#else
    socklen_t addrlen = sizeof(direccion_cliente);
#endif

    while (ejecutando) {
        SocketType cliente_socket = accept(servidor_fd, (struct sockaddr*)&direccion_cliente, &addrlen);
        if (cliente_socket == SOCKET_INVALIDO) {
            if (!ejecutando) break;
            continue;
        }

        char buffer[1024] = {0};
        int valread = recv(cliente_socket, buffer, sizeof(buffer) - 1, 0);
        if (valread > 0) {
            buffer[valread] = '\0';
            cola_eventos.encolar(std::string(buffer));

            const char* respuesta = "ACK_OK";
            send(cliente_socket, respuesta, std::strlen(respuesta), 0);
        }

        cerrarSocket(cliente_socket);
    }
}

const char* ServidorSocket::extraerSiguienteEvento() {
    buffer_ultimo_evento = cola_eventos.desencolar();
    return buffer_ultimo_evento.c_str();
}

void ServidorSocket::detener() {
    if (ejecutando) {
        ejecutando = false;
        if (servidor_fd != SOCKET_INVALIDO) {
#ifndef _WIN32
            shutdown(servidor_fd, SHUT_RDWR);
#endif
            cerrarSocket(servidor_fd);
            servidor_fd = SOCKET_INVALIDO;
        }
        if (hilo_escucha.joinable()) {
            hilo_escucha.join();
        }
#ifdef _WIN32
        WSACleanup();
#endif
    }
}

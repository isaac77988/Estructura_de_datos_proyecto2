#ifndef COLA_MENSAJES_H
#define COLA_MENSAJES_H

#include "NodoMensaje.h"
#include <string>
#include <mutex>

class ColaMensajes {
private:
    NodoMensaje* frente;
    NodoMensaje* final_cola;
    std::mutex mtx;

public:
    ColaMensajes();
    ~ColaMensajes();

    void encolar(const std::string& trama);
    std::string desencolar();
    bool estaVacia();
    void limpiar();
};

#endif

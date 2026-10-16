#ifndef NODO_MENSAJE_H
#define NODO_MENSAJE_H

#include <string>

class NodoMensaje {
private:
    std::string trama;
    NodoMensaje* siguiente;

public:
    NodoMensaje(const std::string& texto_trama);
    ~NodoMensaje();

    std::string getTrama() const;
    NodoMensaje* getSiguiente() const;
    void setSiguiente(NodoMensaje* nuevo_siguiente);
};

#endif

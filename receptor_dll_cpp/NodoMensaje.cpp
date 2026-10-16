#include "NodoMensaje.h"

NodoMensaje::NodoMensaje(const std::string& texto_trama)
    : trama(texto_trama), siguiente(nullptr) {}

NodoMensaje::~NodoMensaje() {}

std::string NodoMensaje::getTrama() const {
    return trama;
}

NodoMensaje* NodoMensaje::getSiguiente() const {
    return siguiente;
}

void NodoMensaje::setSiguiente(NodoMensaje* nuevo_siguiente) {
    siguiente = nuevo_siguiente;
}

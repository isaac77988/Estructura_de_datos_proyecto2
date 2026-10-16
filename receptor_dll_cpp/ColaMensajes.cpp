#include "ColaMensajes.h"

ColaMensajes::ColaMensajes() : frente(nullptr), final_cola(nullptr) {}

ColaMensajes::~ColaMensajes() {
    limpiar();
}

void ColaMensajes::encolar(const std::string& trama) {
    std::lock_guard<std::mutex> lock(mtx);
    NodoMensaje* nuevo = new NodoMensaje(trama);
    if (final_cola == nullptr) {
        frente = nuevo;
        final_cola = nuevo;
    } else {
        final_cola->setSiguiente(nuevo);
        final_cola = nuevo;
    }
}

std::string ColaMensajes::desencolar() {
    std::lock_guard<std::mutex> lock(mtx);
    if (frente == nullptr) {
        return "";
    }
    NodoMensaje* temp = frente;
    std::string valor = temp->getTrama();
    frente = frente->getSiguiente();
    if (frente == nullptr) {
        final_cola = nullptr;
    }
    delete temp;
    return valor;
}

bool ColaMensajes::estaVacia() {
    std::lock_guard<std::mutex> lock(mtx);
    return frente == nullptr;
}

void ColaMensajes::limpiar() {
    std::lock_guard<std::mutex> lock(mtx);
    while (frente != nullptr) {
        NodoMensaje* temp = frente;
        frente = frente->getSiguiente();
        delete temp;
    }
    final_cola = nullptr;
}

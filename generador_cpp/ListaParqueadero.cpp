#include "ListaParqueadero.h"
#include <cstdlib>

ListaParqueadero::ListaParqueadero(int capacidad)
    : cabeza(nullptr), capacidad_maxima(capacidad), cantidad_actual(0) {}

ListaParqueadero::~ListaParqueadero() {
    limpiar();
}

int ListaParqueadero::buscarCeldaPorPlaca(const std::string& placa) const {
    NodoVehiculo* actual = cabeza;
    while (actual != nullptr) {
        if (actual->getPlaca() == placa) {
            return actual->getNumeroCelda();
        }
        actual = actual->getSiguiente();
    }
    return -1;
}

bool ListaParqueadero::celdaEstaOcupada(int numero_celda) const {
    NodoVehiculo* actual = cabeza;
    while (actual != nullptr) {
        if (actual->getNumeroCelda() == numero_celda) {
            return true;
        }
        actual = actual->getSiguiente();
    }
    return false;
}

int ListaParqueadero::obtenerPrimeraCeldaLibre() const {
    if (cantidad_actual >= capacidad_maxima) {
        return -1;
    }
    for (int i = 1; i <= capacidad_maxima; ++i) {
        if (!celdaEstaOcupada(i)) {
            return i;
        }
    }
    return -1;
}

bool ListaParqueadero::insertarVehiculo(const std::string& placa, int celda, const std::string& hora) {
    if (cantidad_actual >= capacidad_maxima || celdaEstaOcupada(celda)) {
        return false;
    }
    NodoVehiculo* nuevo = new NodoVehiculo(placa, celda, hora);
    nuevo->setSiguiente(cabeza);
    cabeza = nuevo;
    cantidad_actual++;
    return true;
}

int ListaParqueadero::eliminarPorPlaca(const std::string& placa) {
    NodoVehiculo* actual = cabeza;
    NodoVehiculo* anterior = nullptr;

    while (actual != nullptr) {
        if (actual->getPlaca() == placa) {
            int celda_liberada = actual->getNumeroCelda();
            if (anterior == nullptr) {
                cabeza = actual->getSiguiente();
            } else {
                anterior->setSiguiente(actual->getSiguiente());
            }
            delete actual;
            cantidad_actual--;
            return celda_liberada;
        }
        anterior = actual;
        actual = actual->getSiguiente();
    }
    return -1;
}

std::string ListaParqueadero::obtenerPlacaAleatoriaActiva() const {
    if (cantidad_actual == 0 || cabeza == nullptr) {
        return "";
    }
    int indice = std::rand() % cantidad_actual;
    NodoVehiculo* actual = cabeza;
    for (int i = 0; i < indice && actual->getSiguiente() != nullptr; ++i) {
        actual = actual->getSiguiente();
    }
    return actual->getPlaca();
}

int ListaParqueadero::getCantidadActual() const {
    return cantidad_actual;
}

int ListaParqueadero::getCapacidadMaxima() const {
    return capacidad_maxima;
}

void ListaParqueadero::limpiar() {
    while (cabeza != nullptr) {
        NodoVehiculo* temp = cabeza;
        cabeza = cabeza->getSiguiente();
        delete temp;
    }
    cantidad_actual = 0;
}

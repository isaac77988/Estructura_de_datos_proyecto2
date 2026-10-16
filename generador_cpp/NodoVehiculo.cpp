#include "NodoVehiculo.h"

NodoVehiculo::NodoVehiculo(const std::string& placa_vehiculo, int celda, const std::string& hora)
    : placa(placa_vehiculo), numero_celda(celda), hora_ingreso(hora), siguiente(nullptr) {}

NodoVehiculo::~NodoVehiculo() {}

std::string NodoVehiculo::getPlaca() const {
    return placa;
}

int NodoVehiculo::getNumeroCelda() const {
    return numero_celda;
}

std::string NodoVehiculo::getHoraIngreso() const {
    return hora_ingreso;
}

NodoVehiculo* NodoVehiculo::getSiguiente() const {
    return siguiente;
}

void NodoVehiculo::setSiguiente(NodoVehiculo* nuevo_siguiente) {
    siguiente = nuevo_siguiente;
}

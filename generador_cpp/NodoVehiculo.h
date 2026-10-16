#ifndef NODO_VEHICULO_H
#define NODO_VEHICULO_H

#include <string>

class NodoVehiculo {
private:
    std::string placa;
    int numero_celda;
    std::string hora_ingreso;
    NodoVehiculo* siguiente;

public:
    NodoVehiculo(const std::string& placa_vehiculo, int celda, const std::string& hora);
    ~NodoVehiculo();

    std::string getPlaca() const;
    int getNumeroCelda() const;
    std::string getHoraIngreso() const;
    NodoVehiculo* getSiguiente() const;
    void setSiguiente(NodoVehiculo* nuevo_siguiente);
};

#endif

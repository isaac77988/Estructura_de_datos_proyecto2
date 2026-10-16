#ifndef LISTA_PARQUEADERO_H
#define LISTA_PARQUEADERO_H

#include "NodoVehiculo.h"
#include <string>

class ListaParqueadero {
private:
    NodoVehiculo* cabeza;
    int capacidad_maxima;
    int cantidad_actual;

public:
    ListaParqueadero(int capacidad = 12);
    ~ListaParqueadero();

    int buscarCeldaPorPlaca(const std::string& placa) const;
    bool celdaEstaOcupada(int numero_celda) const;
    int obtenerPrimeraCeldaLibre() const;
    bool insertarVehiculo(const std::string& placa, int celda, const std::string& hora);
    int eliminarPorPlaca(const std::string& placa);
    std::string obtenerPlacaAleatoriaActiva() const;
    int getCantidadActual() const;
    int getCapacidadMaxima() const;
    void limpiar();
};

#endif

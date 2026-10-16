#ifndef GENERADOR_PLACAS_H
#define GENERADOR_PLACAS_H

#include "ListaParqueadero.h"
#include "ClienteSocket.h"
#include <string>

class GeneradorPlacas {
private:
    ListaParqueadero parqueadero;
    ClienteSocket cliente_red;

    std::string construirPlacaAleatoria() const;
    std::string obtenerHoraActual() const;
    int calcularEsperaSegundos() const;

public:
    GeneradorPlacas(const std::string& ip_destino, int puerto_destino, int total_celdas = 12);
    ~GeneradorPlacas();

    void ejecutarCicloContinuo();
};

#endif

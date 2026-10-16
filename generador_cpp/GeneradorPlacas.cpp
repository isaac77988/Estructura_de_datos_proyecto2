#include "GeneradorPlacas.h"
#include <iostream>
#include <ctime>
#include <cstdlib>
#include <sstream>
#include <iomanip>
#include <thread>
#include <chrono>

GeneradorPlacas::GeneradorPlacas(const std::string& ip_destino, int puerto_destino, int total_celdas)
    : parqueadero(total_celdas), cliente_red(ip_destino, puerto_destino) {
    std::srand(static_cast<unsigned int>(std::time(nullptr)));
}

GeneradorPlacas::~GeneradorPlacas() {}

std::string GeneradorPlacas::construirPlacaAleatoria() const {
    std::string placa = "";
    for (int i = 0; i < 3; ++i) {
        placa += static_cast<char>('A' + (std::rand() % 26));
    }
    placa += "-";
    for (int i = 0; i < 3; ++i) {
        placa += static_cast<char>('0' + (std::rand() % 10));
    }
    return placa;
}

std::string GeneradorPlacas::obtenerHoraActual() const {
    std::time_t ahora = std::time(nullptr);
    std::tm* tiempo_local = std::localtime(&ahora);
    std::ostringstream oss;
    oss << std::put_time(tiempo_local, "%H:%M:%S");
    return oss.str();
}

int GeneradorPlacas::calcularEsperaSegundos() const {
    // Genera un intervalo aleatorio entre 2 y 5 segundos segun especificacion
    return 2 + (std::rand() % 4);
}

void GeneradorPlacas::ejecutarCicloContinuo() {
    std::cout << "=========================================================\n";
    std::cout << " GENERADOR DE PLACAS C++ INICIADO (Intervalo: 2 a 5 seg) \n";
    std::cout << "=========================================================\n";

    while (true) {
        std::string placa_seleccionada;
        bool forzar_repeticion = false;

        // Si el parqueadero esta lleno, obligatoriamente sale un vehiculo (placa repetida)
        // Si hay vehiculos adentro, 35% de probabilidad de repetir una placa para liberar celda
        if (parqueadero.getCantidadActual() >= parqueadero.getCapacidadMaxima()) {
            forzar_repeticion = true;
        } else if (parqueadero.getCantidadActual() > 0 && (std::rand() % 100) < 35) {
            forzar_repeticion = true;
        }

        if (forzar_repeticion) {
            placa_seleccionada = parqueadero.obtenerPlacaAleatoriaActiva();
        } else {
            placa_seleccionada = construirPlacaAleatoria();
        }

        std::string hora_actual = obtenerHoraActual();
        int celda_existente = parqueadero.buscarCeldaPorPlaca(placa_seleccionada);
        std::string trama_envio = "";

        if (celda_existente != -1) {
            // Placa repetida: se libera la celda que ocupaba
            int celda_liberada = parqueadero.eliminarPorPlaca(placa_seleccionada);
            trama_envio = placa_seleccionada + "|" + hora_actual + "|" + std::to_string(celda_liberada) + "|LIBERAR";
            std::cout << "[SALIDA  - PLACA REPETIDA] " << trama_envio << "\n";
        } else {
            // Placa nueva: busca primera celda disponible en la estructura de datos
            int celda_asignada = parqueadero.obtenerPrimeraCeldaLibre();
            if (celda_asignada != -1) {
                parqueadero.insertarVehiculo(placa_seleccionada, celda_asignada, hora_actual);
                trama_envio = placa_seleccionada + "|" + hora_actual + "|" + std::to_string(celda_asignada) + "|OCUPAR";
                std::cout << "[ENTRADA - NUEVO VEHICULO] " << trama_envio << "\n";
            }
        }

        if (!trama_envio.empty()) {
            cliente_red.enviarTrama(trama_envio);
        }

        int espera = calcularEsperaSegundos();
        std::this_thread::sleep_for(std::chrono::seconds(espera));
    }
}
